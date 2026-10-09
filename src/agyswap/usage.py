"""Quota for an agy account, read the same way agy's /quota does (Cloud Code retrieveUserQuotaSummary)."""

from __future__ import annotations

import base64
import email.utils
import http.client
import json
import re
import shutil
import threading
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from functools import lru_cache
from pathlib import Path

QUOTA_URL = "https://daily-cloudcode-pa.googleapis.com/v1internal:retrieveUserQuotaSummary"
WINDOW_ORDER = {"5h": 0, "weekly": 1}
TOKEN_URL = "https://oauth2.googleapis.com/token"
_secrets_lock = threading.Lock()


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    # urllib copies Authorization onto the redirect target; neither endpoint redirects, so refuse.
    def redirect_request(self, *args, **kwargs):
        return None


_opener = urllib.request.build_opener(_NoRedirect)


class UsageError(Exception):
    pass


class TokenRevoked(UsageError):
    pass


class RateLimited(UsageError):
    def __init__(self, msg: str, retry_after: int):
        super().__init__(msg)
        self.retry_after = retry_after


MAX_RETRY_AFTER = 3600


def _retry_after(value: str | None, default: int = 300) -> int:
    # Retry-After is either delay-seconds or an HTTP date (RFC 9110). Clamped: a
    # hostile or huge value must not stop quota fetching for days.
    try:
        if value and value.strip().isascii() and value.strip().isdigit():
            secs = int(value)
        else:
            when = email.utils.parsedate_to_datetime(value)
            if when.tzinfo is None:
                when = when.replace(tzinfo=UTC)
            secs = int((when - datetime.now(UTC)).total_seconds())
    except (TypeError, ValueError, OverflowError):
        return default
    return min(max(0, secs), MAX_RETRY_AFTER)


@dataclass
class Pool:
    group: str  # model group sharing the quota, e.g. "Gemini", "Claude/GPT"
    window: str  # "5h" or "weekly"
    used: float  # 0..1
    reset: datetime | None  # None while the bucket is full: its reset keeps sliding


def _group_name(display: str) -> str:
    # "Gemini Models" -> "Gemini", "Claude and GPT models" -> "Claude/GPT"
    return re.sub(r"\s+models$", "", display, flags=re.I).replace(" and ", "/")


def claims(token: str | None) -> dict:
    try:
        payload = json.loads(token)["id_token"].split(".")[1]
        return json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
    except (TypeError, KeyError, IndexError, ValueError):
        return {}


def _agy_client_secrets() -> tuple[str, ...]:
    # Refresh runs one thread per account; scan the ~200 MB binary once, not once per thread.
    with _secrets_lock:
        return _scan_client_secrets()


@lru_cache(maxsize=1)
def _scan_client_secrets() -> tuple[str, ...]:
    # agy is an installed-app OAuth client and ships its client secret inside the
    # binary. Read it from there rather than copying Google's credential into this repo.
    path = Path(shutil.which("agy") or Path.home() / ".local/bin/agy")
    try:
        data = path.read_bytes()
    except OSError:
        raise UsageError(f"agy binary not found at {path}; needed to refresh tokens") from None
    return tuple(sorted({m.decode() for m in re.findall(rb"GOCSPX-[A-Za-z0-9_-]{28}", data)}))


def parse_time(s: str) -> datetime | None:
    # Go writes nanoseconds; fromisoformat takes at most microseconds.
    try:
        return datetime.fromisoformat(re.sub(r"(\.\d{6})\d+", r"\1", s).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def _post(url: str, data: bytes, headers: dict | None = None) -> dict:
    # Cloud Code rejects the default Python-urllib agent with 403.
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "antigravity", **(headers or {})})
    try:
        with _opener.open(req, timeout=20) as r:
            return json.load(r)
    except urllib.error.URLError:
        raise  # callers map HTTP and connect errors
    except (OSError, http.client.HTTPException) as e:
        # urlopen only wraps connect errors; a timeout or reset while reading comes through raw.
        raise UsageError(f"network error: {type(e).__name__}") from None


def fresh_token(token: str) -> str:
    """Return the token JSON with a usable access token, refreshing it if expired.

    Google does not rotate the refresh token here, so the stored copy stays valid.
    """
    tok = json.loads(token)
    now = datetime.now(UTC)
    expiry = parse_time(tok["token"].get("expiry", ""))
    if expiry and expiry > now + timedelta(minutes=2):
        return token
    client_id = claims(token).get("azp")
    for secret in _agy_client_secrets():
        form = urllib.parse.urlencode(
            {
                "client_id": client_id,
                "client_secret": secret,
                "refresh_token": tok["token"]["refresh_token"],
                "grant_type": "refresh_token",
            }
        ).encode()
        try:
            r = _post(TOKEN_URL, form)
        except urllib.error.HTTPError as e:
            body = e.read()
            if b"invalid_client" in body:
                continue  # the binary carries more than one client; try the next
            if b"invalid_grant" in body:
                raise TokenRevoked("token revoked, sign in with agy again and add the account") from e
            raise UsageError(f"token refresh failed (HTTP {e.code})") from e
        except urllib.error.URLError as e:
            raise UsageError(f"network error: {e.reason}") from e
        tok["token"]["access_token"] = r["access_token"]
        tok["token"]["expiry"] = (now + timedelta(seconds=r["expires_in"])).isoformat()
        if "id_token" in r:
            tok["id_token"] = r["id_token"]
        return json.dumps(tok)
    raise UsageError("no agy OAuth client secret accepted this token")


def fetch_pools(token: str) -> list[Pool]:
    access = json.loads(token)["token"]["access_token"]
    try:
        data = _post(
            QUOTA_URL,
            b"{}",
            {"Authorization": f"Bearer {access}", "Content-Type": "application/json"},
        )
    except urllib.error.HTTPError as e:
        if e.code == 429:
            retry = _retry_after(e.headers.get("Retry-After") if e.headers else None)
            raise RateLimited("rate limited (HTTP 429), try again later", retry) from e
        raise UsageError(f"quota request failed (HTTP {e.code})") from e
    except urllib.error.URLError as e:
        raise UsageError(f"network error: {e.reason}") from e
    pools = []
    for group in data.get("groups", []):
        name = _group_name(group.get("displayName", "?"))
        buckets = sorted(group.get("buckets", []), key=lambda b: WINDOW_ORDER.get(b.get("window"), 9))
        for b in buckets:
            frac = b.get("remainingFraction")
            # An exhausted bucket has not been observed yet; treat a missing fraction as empty.
            frac = frac if isinstance(frac, int | float) else 0.0
            reset = None if frac >= 1 else parse_time(b.get("resetTime", ""))
            pools.append(Pool(name, b.get("window", "?"), 1 - frac, reset))
    return pools


def account_usage(token: str) -> tuple[list[Pool], str]:
    """Pools for one account, plus the (possibly refreshed) token to store back."""
    token = fresh_token(token)
    return fetch_pools(token), token
