"""Multi-account switcher for the Antigravity CLI (agy).

agy keeps its OAuth token in the OS keyring via go-keyring
(service "gemini", user "antigravity") as a JSON blob. An account is
a stored copy of that blob; switching writes another copy back.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path

from rich.console import Console
from rich.text import Text

from agyswap import __version__
from agyswap.usage import Pool, RateLimited, TokenRevoked, UsageError, account_usage, claims, parse_time

SERVICE = "gemini"
USERNAME = "antigravity"


class SwapError(Exception):
    """`str()` is the CLI wording; `tui` is the same message with TUI keys instead of commands."""

    def __init__(self, msg: str, tui: str | None = None) -> None:
        super().__init__(msg)
        self.tui = tui or msg


def store_path() -> Path:
    return Path(os.environ.get("AGYSWAP_HOME", Path.home() / ".agyswap")) / "accounts.json"


def load_store() -> dict:
    p = store_path()
    if not p.exists():
        return {"accounts": {}}
    try:
        return json.loads(p.read_text())
    except ValueError:
        raise SwapError(
            f"{p} is not valid JSON. Fix or move it, then run `agyswap add` again.",
            tui=f"{p} is not valid JSON. Fix or move it, then press r.",
        ) from None


@contextmanager
def locked_store():
    """Load the store under an exclusive lock; hold it for the whole read-modify-write."""
    lock = store_path().with_name(".lock")
    _private_dir(lock.parent)
    fd = os.open(lock, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield load_store()
    finally:
        os.close(fd)


def save_store(store: dict) -> None:
    _write_private(store_path(), store)


def usage_path() -> Path:
    return store_path().with_name("usage.json")


def load_usage() -> dict:
    """Last good quota per email. A missing or broken cache is just empty."""
    try:
        data = json.loads(usage_path().read_text())
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _private_dir(d: Path) -> None:
    """Create the store folder 0700; tighten an existing one, and refuse one owned by someone else."""
    d.mkdir(mode=0o700, parents=True, exist_ok=True)
    st = d.stat()
    if st.st_uid != os.getuid():
        raise SwapError(f"{d} is not owned by you; refusing to keep refresh tokens there.")
    if st.st_mode & 0o077:
        d.chmod(0o700)


def _write_private(p: Path, data: dict) -> None:
    _private_dir(p.parent)
    # Refresh tokens live in the store: mkstemp creates an unguessable 0600 file with O_EXCL.
    fd, tmp = tempfile.mkstemp(dir=p.parent, prefix=f".{p.stem}-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, p)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise
    dir_fd = os.open(p.parent, os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)


def _secret_tool(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
    # ponytail: Linux Secret Service only; macOS Keychain / Windows Credential Manager when needed.
    try:
        return subprocess.run(["secret-tool", *args], input=stdin, capture_output=True, text=True, timeout=30)
    except FileNotFoundError:
        raise SwapError("secret-tool not found. Install libsecret (e.g. `dnf install libsecret`).") from None
    except subprocess.TimeoutExpired:
        raise SwapError("keyring did not answer within 30s (locked?). Unlock it and try again.") from None


def read_token() -> str | None:
    r = _secret_tool("lookup", "service", SERVICE, "username", USERNAME)
    if r.returncode != 0 and r.stderr.strip():
        # A missing item exits 1 silently; anything on stderr is a keyring failure, not "signed out".
        raise SwapError(f"Failed to read keyring: {r.stderr.strip()}")
    return r.stdout if r.returncode == 0 and r.stdout else None


def write_token(token: str) -> None:
    r = _secret_tool(
        "store",
        f"--label=Password for '{USERNAME}' on '{SERVICE}'",
        "service",
        SERVICE,
        "username",
        USERNAME,
        stdin=token,
    )
    if r.returncode != 0:
        raise SwapError(f"Failed to write keyring: {r.stderr.strip()}")


def email_of(token: str | None) -> str | None:
    return claims(token).get("email") or None


def agy_running() -> bool:
    # The background updater never touches the token; any other agy process may refresh it.
    r = subprocess.run(["pgrep", "-a", "-x", "agy"], capture_output=True, text=True)
    return any("--bg-updater" not in line for line in r.stdout.splitlines())


def find_slot(store: dict, target: str) -> str:
    accounts = store["accounts"]
    if target in accounts:
        return target
    for key in ("email", "alias"):
        for slot, acc in accounts.items():
            if (acc.get(key) or "").lower() == target.lower():
                return slot
    raise SwapError(
        f"No account matches '{target}'. Run `agyswap list`.", tui=f"No account matches '{target}'. Press r."
    )


def slot_for_email(store: dict, email: str | None) -> str | None:
    if not email:
        return None
    return next((s for s, a in store["accounts"].items() if a["email"].lower() == email.lower()), None)


def next_slot(store: dict) -> str:
    return str(max(map(int, store["accounts"]), default=0) + 1)


def cmd_add(slot: int | None = None) -> str:
    token = read_token()
    email = email_of(token)
    if not email:
        raise SwapError(
            "agy is not signed in. Run `agy`, sign in, exit, then `agyswap add`.",
            tui="agy is not signed in. Run `agy`, sign in, exit, then press a.",
        )
    with locked_store() as store:
        existing = slot_for_email(store, email)
        if slot is None:
            slot = existing or next_slot(store)
        else:
            if slot < 1:
                raise SwapError("--slot must be 1 or higher.")
            slot = str(slot)
            other = store["accounts"].get(slot)
            if other and other["email"].lower() != email.lower():
                raise SwapError(f"Slot {slot} holds {other['email']}. Remove it first or pick another slot.")
            if existing and existing != slot:
                store["accounts"][slot] = store["accounts"].pop(existing)  # move the account to the requested slot
        # Keep alias and a manual disable; a fresh sign-in lifts a revoked-token quarantine.
        acc = store["accounts"].setdefault(slot, {})
        if acc.get("disabled_reason") == "token revoked":
            acc.pop("disabled", None)
            acc.pop("disabled_reason", None)
        acc.update(email=email, token=token)
        save_store(store)
    return f"{'Updated' if existing == slot else 'Moved' if existing else 'Added'} account {slot}: {email}"


def collect_usage() -> list[dict]:
    """Quota for every stored account. Refreshed tokens are saved back to the store."""
    store = load_store()
    live = read_token()
    active = email_of(live)
    now = datetime.now(UTC)
    retry_at = {e: parse_time(v.get("retry_at")) for e, v in load_usage().items() if isinstance(v, dict)}

    def one(slot: str) -> dict:
        acc = store["accounts"][slot]
        # The keyring copy is the newest for the active account; never write the keyring here.
        token = live if acc["email"] == active else acc["token"]
        row = {
            "slot": slot,
            "email": acc["email"],
            "alias": acc.get("alias"),
            "active": acc["email"] == active,
            "disabled": bool(acc.get("disabled")),
            "disabled_reason": acc.get("disabled_reason"),
            "pools": [],
            "error": None,
            "stale": None,
        }
        if row["disabled"]:
            return row
        if (until := retry_at.get(acc["email"])) and until > now:
            # Backing off after a 429; the cached reading fills the row.
            row["error"] = f"rate limited, retry in {_ago(int((until - now).total_seconds()) + 59)}"
            row["backoff"] = until
            return row
        try:
            row["pools"], acc["token"] = account_usage(token)
        except TokenRevoked as e:
            row["error"], row["revoked"] = str(e), True
        except RateLimited as e:
            row["error"], row["backoff"] = str(e), now + timedelta(seconds=e.retry_after)
        except (UsageError, KeyError, ValueError) as e:
            row["error"] = str(e)
        except Exception as e:
            # The message or traceback of an unexpected error may carry token text; keep the type only.
            row["error"] = f"unexpected error: {type(e).__name__}"
        return row

    slots = sorted(store["accounts"], key=int)
    fetched = {acc["email"]: acc["token"] for acc in store["accounts"].values()}
    with ThreadPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one, slots))
    # The fetch ran unlocked for seconds; merge tokens into a fresh read so a
    # concurrent add/remove/switch is never undone.
    refreshed = {store["accounts"][r["slot"]]["email"]: store["accounts"][r["slot"]]["token"] for r in rows}
    revoked = {r["email"] for r in rows if r.pop("revoked", False)}
    quarantined = set()
    with locked_store() as current:
        changed = False
        for acc in current["accounts"].values():
            # Quarantine only the token that was rejected, not one re-added meanwhile. For the active
            # account the rejected token is the keyring copy; it shares the stored copy's refresh
            # token (Google does not rotate it), so comparing the stored copy is equivalent.
            if acc["email"] in revoked and acc["token"] == fetched[acc["email"]]:
                acc["disabled"], acc["disabled_reason"] = True, "token revoked"
                quarantined.add(acc["email"])
                changed = True
                continue
            # Only take a token that is still for this account and actually newer.
            new = refreshed.get(acc["email"])
            if new and new != acc["token"] and email_of(new) == acc["email"] and _expiry(new) > _expiry(acc["token"]):
                acc["token"] = new
                changed = True
        if changed:
            save_store(current)
        for row in rows:
            # Callers pick accounts from these rows; never offer one that was just quarantined.
            if row["email"] in quarantined:
                row["disabled"], row["disabled_reason"] = True, "token revoked"
        _update_usage_cache(rows, {a["email"] for a in current["accounts"].values()})
    return rows


def _pool_json(p: Pool) -> dict:
    return {
        "group": p.group,
        "window": p.window,
        "used": round(p.used, 6),
        "reset": p.reset.isoformat() if p.reset else None,
    }


def _update_usage_cache(rows: list[dict], emails: set[str]) -> None:
    """Under the store lock: save good readings, and show the last one on rows whose fetch failed."""
    now = datetime.now(UTC)
    cache = {e: v for e, v in load_usage().items() if e in emails}
    for row in rows:
        if row["disabled"]:
            continue
        if row["error"] is None:
            cache[row["email"]] = {"fetched_at": now.isoformat(), "pools": [_pool_json(p) for p in row["pools"]]}
            continue
        if until := row.pop("backoff", None):
            cache.setdefault(row["email"], {})["retry_at"] = until.isoformat()
        if (entry := cache.get(row["email"])) and "pools" in entry:
            try:
                row["pools"] = [
                    Pool(p["group"], p["window"], p["used"], parse_time(p["reset"])) for p in entry["pools"]
                ]
                row["stale"] = int((now - parse_time(entry["fetched_at"])).total_seconds())
            except (KeyError, TypeError, ValueError):
                pass  # a malformed entry is simply not shown
    _write_private(usage_path(), cache)


def _expiry(token: str) -> datetime:
    try:
        return parse_time(json.loads(token)["token"]["expiry"]) or datetime.min.replace(tzinfo=UTC)
    except (KeyError, ValueError, TypeError):
        return datetime.min.replace(tzinfo=UTC)


BAR = 30


def _countdown(reset: datetime | None) -> str:
    if not reset:
        return ""
    secs = max(0, int((reset - datetime.now(UTC)).total_seconds()))
    d, h, m = secs // 86400, secs % 86400 // 3600, secs % 3600 // 60
    return "resets " + (f"{d}d {h}h" if d else f"{h}h {m}m")


def _ago(secs: int) -> str:
    d, h, m = secs // 86400, secs % 86400 // 3600, secs % 3600 // 60
    return f"{d}d {h}h" if d else f"{h}h {m}m" if h else f"{m}m"


def _color(used: float) -> str:
    return "#22c55e" if used < 0.5 else "#eab308" if used < 0.8 else "#ef4444"


def account_text(row: dict) -> Text:
    t = Text()
    t.append(f"{row['slot']:>2}  ", "bold")
    t.append(row["email"], "bold")
    if row.get("alias"):
        t.append(f" ({row['alias']})", "dim")
    if row["active"]:
        t.append("  ● active", "bold #ffa62b")
    if row.get("disabled"):
        t.append(f"\n    disabled: {row.get('disabled_reason') or 'manual'}", "dim")
        return t
    prev_group = None
    width = max([12] + [len(p.group) + 2 for p in row["pools"]])
    for p in row["pools"]:
        filled = round(p.used * BAR)
        # Group name only on its first row; the window column stays aligned.
        t.append(
            f"\n    {p.group if p.group != prev_group else '':<{width}}", "bold" if p.group != prev_group else "dim"
        )
        prev_group = p.group
        t.append(f"{p.window:<8}", "dim")
        t.append("━" * filled, _color(p.used))
        t.append("━" * (BAR - filled), "grey35")
        t.append(f" {p.used:>4.0%}", f"bold {_color(p.used)}")
        if p.reset:
            t.append(f"  {_countdown(p.reset)}", "dim")
    if row["error"]:
        t.append(f"\n    ✕ {row['error']}", "#ef4444")
        if row.get("stale") is not None:
            t.append(f"  (stale, {_ago(row['stale'])} ago)", "dim")
    return t


def row_json(r: dict) -> dict:
    keys = ("slot", "email", "alias", "active", "disabled", "disabled_reason", "error")
    return {
        **{k: r.get(k) for k in keys},
        "disabled": bool(r.get("disabled")),
        "stale": r.get("stale") is not None,
        "pools": [_pool_json(p) for p in r["pools"]],
    }


def _emit(data: dict) -> None:
    print(json.dumps({"version": 1, **data}))


def cmd_list(as_json: bool = False) -> int:
    """Print every account; exit 1 when no account could be read."""
    if not load_store()["accounts"]:
        if as_json:
            _emit({"accounts": []})
        else:
            print("No accounts stored. Sign in to agy, then run `agyswap add`.")
        return 0
    rows = collect_usage()
    enabled = [r for r in rows if not r["disabled"]]
    code = 1 if enabled and all(r["error"] for r in enabled) else 0
    if as_json:
        _emit({"accounts": [row_json(r) for r in rows]})
        return code
    console = Console()
    for row in rows:
        console.print(account_text(row))
        console.print()
    return code


def cmd_status(as_json: bool = False) -> None:
    email = email_of(read_token())
    slot = slot_for_email(load_store(), email) if email else None
    if as_json:
        _emit({"email": email, "slot": slot})
    elif not email:
        print("Not signed in.")
    else:
        print(f"{email} (account {slot})" if slot else f"{email} (not stored, run `agyswap add`)")


def cmd_switch(target: str | None = None, force: bool = False, ignore_running: bool = False) -> str:
    return switch_message(switch_account(target, force, ignore_running))


def switch_message(r: dict) -> str:
    note = f"Saved the unstored live login as account {r['saved_slot']}. " if r["saved_slot"] else ""
    return note + f"{'Switched to' if r['switched'] else 'Already on'} account {r['slot']}: {r['email']}"


MAX_STALE = 30 * 60  # older cached quota is too old to pick an account by


def pick_account(rows: list[dict], strategy: str, threshold: float) -> dict | None:
    """The account to move to: enabled, not active, quota known, every bucket below threshold (percent)."""

    def ok(r: dict) -> bool:
        return _readable(r) and not r["active"] and not r["disabled"] and _max_used(r) * 100 < threshold

    if strategy == "best":
        return min(filter(ok, rows), key=lambda r: (_max_used(r), int(r["slot"])), default=None)
    rows = sorted(rows, key=lambda r: int(r["slot"]))
    start = next((i + 1 for i, r in enumerate(rows) if r["active"]), 0)
    return next(filter(ok, rows[start:] + rows[:start]), None)


def cmd_switch_strategy(strategy: str, threshold: float, ignore_running: bool = False) -> dict:
    if agy_running() and not ignore_running:
        raise SwapError(f"{AGY_RUNNING} (--ignore-running to override)", tui=AGY_RUNNING)
    # Quota is fetched unlocked; switch_account re-checks everything under the lock.
    row = pick_account(collect_usage(), strategy, threshold)
    if row is None:
        raise SwapError(f"No account below {threshold:g}% usage.")
    return switch_account(row["email"], ignore_running=ignore_running)


def _readable(r: dict) -> bool:
    return bool(r["pools"]) and (r["error"] is None or (r["stale"] is not None and r["stale"] <= MAX_STALE))


def _max_used(r: dict) -> float:
    return max(p.used for p in r["pools"])


def cmd_auto(threshold: float = 90, strategy: str = "best", ignore_running: bool = False) -> dict:
    """Move off the active account once any of its buckets reaches `threshold` percent."""
    if agy_running() and not ignore_running:
        raise SwapError(f"{AGY_RUNNING} (--ignore-running to override)", tui=AGY_RUNNING)
    saved = None
    live_email = email_of(read_token())
    if live_email and not slot_for_email(load_store(), live_email):
        # Never leave a login without a stored copy; this also lets its quota be read.
        cmd_add()
        saved = slot_for_email(load_store(), live_email)
    rows = collect_usage()
    active = next((r for r in rows if r["active"]), None)
    # A disabled active account (e.g. quarantined) is left whatever its quota.
    if active and not active["disabled"]:
        if not _readable(active):
            raise SwapError(f"Cannot read the quota of account {active['slot']}; not switching.")
        if _max_used(active) * 100 < threshold:
            return {
                "switched": False,
                "slot": active["slot"],
                "email": active["email"],
                "saved_slot": saved,
                "max_used": _max_used(active),
            }
    row = pick_account(rows, strategy, threshold)
    if row is None:
        staying = f"; staying on account {active['slot']}" if active else ""
        raise SwapError(f"No account below {threshold:g}% usage{staying}.")
    result = switch_account(row["email"], ignore_running=ignore_running)
    return {**result, "saved_slot": saved or result["saved_slot"], "max_used": _max_used(row)}


def auto_message(r: dict) -> str:
    if not r["switched"]:
        return f"Account {r['slot']} ({r['email']}) is fine (max {r['max_used']:.0%} used)"
    return switch_message(r) + f" (max {r['max_used']:.0%} used)"


AGY_RUNNING = "agy is running. Exit it first: a running agy refreshes and re-saves its own token, undoing the switch."


def switch_account(target: str | None = None, force: bool = False, ignore_running: bool = False) -> dict:
    """Switch the keyring login. `force` skips copying the live token back into its slot,
    an unstored live login is still saved first."""
    if agy_running() and not ignore_running:
        raise SwapError(f"{AGY_RUNNING} (--ignore-running to override)", tui=AGY_RUNNING)
    with locked_store() as store:
        if not store["accounts"]:
            raise SwapError("No accounts stored. Run `agyswap add` first.", tui="No accounts stored. Press a first.")
        saved = None
        live = read_token()
        live_email = email_of(live)
        current = slot_for_email(store, live_email)
        if current:
            if not force:
                # Capture the live token so refreshes made by agy are not lost.
                store["accounts"][current]["token"] = live
        elif live_email:
            # Never overwrite a login we have no copy of: store it first.
            current = next_slot(store)
            store["accounts"][current] = {"email": live_email, "token": live}
            saved = current
        if target is None:
            slots = sorted(store["accounts"], key=int)
            start = slots.index(current) + 1 if current else 0
            rotation = slots[start:] + slots[:start]
            target = next((s for s in rotation if s != current and not store["accounts"][s].get("disabled")), None)
            if target is None:
                raise SwapError("No enabled account to switch to.")
        slot = find_slot(store, target)
        acc = store["accounts"][slot]
        if acc.get("disabled") and slot != current:
            disabled = f"Account {slot} is disabled ({acc.get('disabled_reason', 'manual')})."
            raise SwapError(f"{disabled} Run `agyswap enable {slot}` first.", tui=f"{disabled} Press x on it first.")
        if slot == current:
            save_store(store)
            return {"switched": False, "slot": slot, "email": acc["email"], "saved_slot": saved}
        save_store(store)  # persist synced token before overwriting the keyring
        write_token(store["accounts"][slot]["token"])
        return {"switched": True, "slot": slot, "email": acc["email"], "saved_slot": saved}


def _printable(text: str) -> bool:
    """No control characters: text from a file must never reach the terminal as escape codes."""
    return not any(ord(c) < 0x20 or ord(c) == 0x7F for c in text)


def _valid_alias(name: object) -> bool:
    # Slots are digits and emails hold '@'; an alias must never shadow either.
    return isinstance(name, str) and bool(name) and not name.isdigit() and "@" not in name and _printable(name)


def cmd_alias(target: str, name: str | None) -> str:
    with locked_store() as store:
        slot = find_slot(store, target)
        acc = store["accounts"][slot]
        if not name:
            acc.pop("alias", None)
            save_store(store)
            return f"Cleared alias of account {slot}: {acc['email']}"
        if not _valid_alias(name):
            raise SwapError("An alias cannot be all digits or contain '@'.")
        owner = next((s for s, a in store["accounts"].items() if (a.get("alias") or "").lower() == name.lower()), None)
        if owner and owner != slot:
            raise SwapError(f"Alias '{name}' is already used by account {owner}.")
        acc["alias"] = name
        save_store(store)
    return f"Account {slot} ({acc['email']}) is now '{name}'"


def cmd_disable(target: str, reason: str = "manual") -> str:
    with locked_store() as store:
        slot = find_slot(store, target)
        acc = store["accounts"][slot]
        acc["disabled"], acc["disabled_reason"] = True, reason
        save_store(store)
    return f"Disabled account {slot}: {acc['email']}"


def cmd_enable(target: str) -> str:
    with locked_store() as store:
        slot = find_slot(store, target)
        acc = store["accounts"][slot]
        acc.pop("disabled", None)
        acc.pop("disabled_reason", None)
        save_store(store)
    return f"Enabled account {slot}: {acc['email']}"


EXPORT_FORMAT = "agyswap-export"
ACCOUNT_FIELDS = ("email", "alias", "disabled", "disabled_reason", "token")


def cmd_export(path: str, force: bool = False) -> str:
    """Write every account, refresh tokens included, to a new 0600 file."""
    store = load_store()
    live = read_token()
    live_email = email_of(live)
    accounts = []
    for slot in sorted(store["accounts"], key=int):
        acc = {k: v for k, v in store["accounts"][slot].items() if k in ACCOUNT_FIELDS}
        if live_email and acc["email"].lower() == live_email.lower():
            acc["token"] = live  # the keyring copy is the newest one
        accounts.append(acc)
    data = json.dumps({"format": EXPORT_FORMAT, "version": 1, "accounts": accounts}, indent=2)
    target = Path(path)
    if not force and (target.exists() or target.is_symlink()):
        raise SwapError(
            f"{path} already exists. Pass --force to replace it.", tui=f"{path} already exists. Choose another file."
        )
    tmp = None
    try:
        # Complete 0600 file first, then put it in place: the old export survives a failed write,
        # and os.link refuses an existing name (or symlink) without --force.
        fd, tmp = tempfile.mkstemp(dir=target.parent, prefix=".agyswap-export-", suffix=".tmp")
        with os.fdopen(fd, "w") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        if force:
            os.replace(tmp, target)
        else:
            os.link(tmp, target)
    except FileExistsError:
        raise SwapError(
            f"{path} already exists. Pass --force to replace it.", tui=f"{path} already exists. Choose another file."
        ) from None
    except OSError as e:
        raise SwapError(f"Cannot write {path}: {type(e).__name__}") from None
    finally:
        if tmp:
            Path(tmp).unlink(missing_ok=True)
    print(f"warning: {path} holds refresh tokens: anyone with it can use these accounts.", file=sys.stderr)
    return f"Exported {len(accounts)} account{'s' if len(accounts) != 1 else ''} to {path}"


def _valid_entry(acc: object) -> bool:
    """An export entry agy could use: a full token blob whose email claim matches, sane fields.

    The id_token signature is not verified, so only import files you exported yourself."""
    if not isinstance(acc, dict) or not isinstance(email := acc.get("email"), str) or not email:
        return False
    if not _printable(email):
        return False
    try:
        tok = json.loads(acc["token"])
        shape = isinstance(tok["token"]["refresh_token"], str) and isinstance(tok["id_token"], str)
    except (KeyError, TypeError, ValueError):
        return False
    reason = acc.get("disabled_reason", "")
    fields = isinstance(acc.get("disabled", False), bool) and isinstance(reason, str) and _printable(reason)
    return shape and fields and email_of(acc["token"]) == email


def _read_export(path: str) -> list[dict]:
    """Validate the whole file before anything is written."""
    try:
        data = json.loads(Path(path).read_text())
    except (OSError, ValueError) as e:
        raise SwapError(f"Cannot read {path}: {type(e).__name__}") from None
    if not isinstance(data, dict) or data.get("format") != EXPORT_FORMAT or data.get("version") != 1:
        raise SwapError(f"{path} is not an agyswap export (version 1).")
    accounts = data.get("accounts")
    if not isinstance(accounts, list):
        raise SwapError(f"{path} has no account list.")
    for i, acc in enumerate(accounts, 1):
        if not _valid_entry(acc):
            raise SwapError(
                f"Entry {i} in {path} is invalid or its token belongs to another account. Nothing imported."
            )
    return [{k: v for k, v in acc.items() if k in ACCOUNT_FIELDS} for acc in accounts]


def cmd_import(path: str, force: bool = False) -> str:
    """Add exported accounts to the store. Never touches the keyring."""
    incoming = _read_export(path)
    added = skipped = 0
    with locked_store() as store:
        for acc in incoming:
            slot = slot_for_email(store, acc["email"])
            if slot and not force:
                print(f"skipped {acc['email']} (already stored)")
                skipped += 1
                continue
            slot = slot or next_slot(store)  # --force keeps the slot number
            alias = acc.get("alias")
            taken = any(
                (a.get("alias") or "").lower() == str(alias).lower() for s, a in store["accounts"].items() if s != slot
            )
            if alias is not None and (taken or not _valid_alias(alias)):
                print(f"alias {alias!r} dropped for {acc['email']} (taken or invalid)")
                del acc["alias"]
            store["accounts"][slot] = acc
            added += 1
        save_store(store)
    return f"Imported {added}, skipped {skipped}"


def cmd_remove(target: str) -> str:
    with locked_store() as store:
        slot = find_slot(store, target)
        email = store["accounts"].pop(slot)["email"]
        save_store(store)
    return f"Removed account {slot}: {email}"


def confirm_remove(target: str) -> bool:
    """Ask before forgetting an account. Only prompts on a TTY."""
    store = load_store()
    slot = find_slot(store, target)
    email = store["accounts"][slot]["email"]
    if not sys.stdin.isatty():
        raise SwapError("Refusing to remove without confirmation. Pass --yes to remove from a script.")
    if email == email_of(read_token()):
        print(f"warning: account {slot} ({email}) is currently active", file=sys.stderr)
    try:
        answer = input(f"Remove account {slot} ({email})? [y/N] ")
    except (EOFError, KeyboardInterrupt):
        print()  # Ctrl-D / Ctrl-C mean "no"; keep the prompt line tidy
        return False
    return answer.strip().lower() in ("y", "yes")


def _percent(value: str) -> float:
    v = float(value)
    if not 0 < v <= 100:
        raise argparse.ArgumentTypeError("must be between 0 and 100")
    return v


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="agyswap", description="Multi-account switcher for the Antigravity CLI (agy)")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("tui", help="interactive dashboard (also: bare agyswap)")
    add = sub.add_parser("add", help="store the account agy is signed in with")
    add.add_argument("--slot", type=int, help="store into this slot number")
    ls = sub.add_parser("list", aliases=["ls"], help="list stored accounts with quota usage")
    st = sub.add_parser("status", help="show the active account")
    sw = sub.add_parser("switch", help="switch to next account, or to <num|email|alias>")
    sw.add_argument("target", nargs="?")
    sw.add_argument(
        "--force", action="store_true", help="switch without copying the live login's token back into its slot first"
    )
    sw.add_argument("--ignore-running", action="store_true", help="switch even if agy is running")
    sw.add_argument("--strategy", choices=["best", "next-available"], help="pick the account by quota left")
    sw.add_argument("--threshold", type=_percent, help="usage %% an account must stay below (default 90)")
    al = sub.add_parser("alias", help="name an account; omit the name to clear it")
    al.add_argument("target")
    al.add_argument("name", nargs="?")
    for name, desc in (("disable", "leave an account out of switching"), ("enable", "put a disabled account back")):
        sub.add_parser(name, help=desc).add_argument("target")
    au = sub.add_parser("auto", help="switch away from the active account once it is nearly out of quota")
    au.add_argument("--threshold", type=_percent, default=90, help="usage %% that triggers a switch (default 90)")
    au.add_argument(
        "--strategy", choices=["best", "next-available"], default="best", help="how to pick the next account"
    )
    au.add_argument("--ignore-running", action="store_true", help="switch even if agy is running")
    for sp in (ls, st, sw, au):
        sp.add_argument("--json", action="store_true", help="print one JSON object (no tokens)")
    ex = sub.add_parser("export", help="write all accounts (with refresh tokens) to a file")
    ex.add_argument("file")
    ex.add_argument("--force", action="store_true", help="replace the file if it exists")
    im = sub.add_parser("import", help="add accounts from an export file (only files you exported yourself)")
    im.add_argument("file")
    im.add_argument("--force", action="store_true", help="replace accounts that are already stored")
    rm = sub.add_parser("remove", aliases=["rm"], help="forget a stored account (num|email|alias)")
    rm.add_argument("target")
    rm.add_argument("-y", "--yes", action="store_true", help="remove without asking")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd is None:
        if not (sys.stdin.isatty() and sys.stdout.isatty()):
            parser.error("no command given — try 'agyswap --help'")
        args.cmd = "tui"
    try:
        match args.cmd:
            case "tui":
                from agyswap.tui import AgySwapApp

                AgySwapApp().run()
            case "add":
                print(cmd_add(args.slot))
            case "list" | "ls":
                return cmd_list(args.json)
            case "status":
                cmd_status(args.json)
            case "switch":
                if args.strategy and args.target:
                    parser.error("switch takes either <target> or --strategy, not both")
                if args.strategy and args.force:
                    parser.error("--force only applies to a switch without --strategy")
                if args.threshold is not None and not args.strategy:
                    parser.error("--threshold only applies with --strategy")
                if args.strategy:
                    r = cmd_switch_strategy(args.strategy, args.threshold or 90, args.ignore_running)
                else:
                    r = switch_account(args.target, args.force, args.ignore_running)
                print(json.dumps({"version": 1, **r}) if args.json else switch_message(r))
            case "alias":
                print(cmd_alias(args.target, args.name))
            case "auto":
                r = cmd_auto(args.threshold, args.strategy, args.ignore_running)
                print(json.dumps({"version": 1, **r}) if args.json else auto_message(r))
            case "export":
                print(cmd_export(args.file, args.force))
            case "import":
                print(cmd_import(args.file, args.force))
            case "disable":
                print(cmd_disable(args.target))
            case "enable":
                print(cmd_enable(args.target))
            case "remove" | "rm":
                if not args.yes and not confirm_remove(args.target):
                    print("Cancelled")
                    return 0
                print(cmd_remove(args.target))
    except SwapError as e:
        if getattr(args, "json", False):
            _emit({"error": str(e)})
        else:
            print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
