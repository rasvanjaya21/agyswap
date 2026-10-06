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
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console
from rich.text import Text

from agyswap import __version__
from agyswap.usage import UsageError, account_usage, claims, parse_time

SERVICE = "gemini"
USERNAME = "antigravity"


class SwapError(Exception):
    pass


def store_path() -> Path:
    return Path(os.environ.get("AGYSWAP_HOME", Path.home() / ".agyswap")) / "accounts.json"


def load_store() -> dict:
    p = store_path()
    if not p.exists():
        return {"accounts": {}}
    return json.loads(p.read_text())


@contextmanager
def locked_store():
    """Load the store under an exclusive lock; hold it for the whole read-modify-write."""
    lock = store_path().with_name(".lock")
    lock.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    with open(lock, "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield load_store()


def save_store(store: dict) -> None:
    p = store_path()
    p.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    # Refresh tokens live here: owner-only from the first byte.
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(store, f, indent=2)
    os.replace(tmp, p)


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
    for slot, acc in accounts.items():
        if acc["email"].lower() == target.lower():
            return slot
    raise SwapError(f"No account matches '{target}'. Run `agyswap list`.")


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
        raise SwapError("agy is not signed in. Run `agy`, sign in, exit, then `agyswap add`.")
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
                del store["accounts"][existing]  # move the account to the requested slot
        store["accounts"][slot] = {"email": email, "token": token}
        save_store(store)
    return f"{'Updated' if existing == slot else 'Moved' if existing else 'Added'} account {slot}: {email}"


def collect_usage() -> list[dict]:
    """Quota for every stored account. Refreshed tokens are saved back to the store."""
    store = load_store()
    live = read_token()
    active = email_of(live)

    def one(slot: str) -> dict:
        acc = store["accounts"][slot]
        # The keyring copy is the newest for the active account; never write the keyring here.
        token = live if acc["email"] == active else acc["token"]
        row = {"slot": slot, "email": acc["email"], "active": acc["email"] == active, "pools": [], "error": None}
        try:
            row["pools"], acc["token"] = account_usage(token)
        except (UsageError, KeyError, ValueError) as e:
            row["error"] = str(e)
        except Exception as e:
            # The message or traceback of an unexpected error may carry token text; keep the type only.
            row["error"] = f"unexpected error: {type(e).__name__}"
        return row

    slots = sorted(store["accounts"], key=int)
    with ThreadPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one, slots))
    # The fetch ran unlocked for seconds; merge tokens into a fresh read so a
    # concurrent add/remove/switch is never undone.
    refreshed = {store["accounts"][r["slot"]]["email"]: store["accounts"][r["slot"]]["token"] for r in rows}
    with locked_store() as current:
        for acc in current["accounts"].values():
            # Only take a token that is still for this account and actually newer.
            new = refreshed.get(acc["email"])
            if new and new != acc["token"] and email_of(new) == acc["email"] and _expiry(new) > _expiry(acc["token"]):
                acc["token"] = new
        if current["accounts"]:
            save_store(current)
    return rows


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


def _color(used: float) -> str:
    return "#22c55e" if used < 0.5 else "#eab308" if used < 0.8 else "#ef4444"


def account_text(row: dict) -> Text:
    t = Text()
    t.append(f"{row['slot']:>2}  ", "bold")
    t.append(row["email"], "bold")
    if row["active"]:
        t.append("  ● active", "bold #ffa62b")
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
    return t


def cmd_list() -> None:
    if not load_store()["accounts"]:
        print("No accounts stored. Sign in to agy, then run `agyswap add`.")
        return
    console = Console()
    for row in collect_usage():
        console.print(account_text(row))
        console.print()


def cmd_status() -> None:
    email = email_of(read_token())
    if not email:
        print("Not signed in.")
        return
    slot = slot_for_email(load_store(), email)
    print(f"{email} (account {slot})" if slot else f"{email} (not stored, run `agyswap add`)")


def cmd_switch(target: str | None = None, force: bool = False, ignore_running: bool = False) -> str:
    """Switch the keyring login. `force` skips copying the live token back into its slot,
    an unstored live login is still saved first."""
    if agy_running() and not ignore_running:
        raise SwapError(
            "agy is running. Exit it first: a running agy refreshes and re-saves "
            "its own token, undoing the switch. (--ignore-running to override)"
        )
    with locked_store() as store:
        if not store["accounts"]:
            raise SwapError("No accounts stored. Run `agyswap add` first.")
        note = ""
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
            note = f"Saved unstored login {live_email} as account {current}. "
        slots = sorted(store["accounts"], key=int)
        if target is None:
            target = slots[(slots.index(current) + 1) % len(slots)] if current else slots[0]
        slot = find_slot(store, target)
        if slot == current:
            save_store(store)
            return note + f"Already on account {slot}: {store['accounts'][slot]['email']}"
        save_store(store)  # persist synced token before overwriting the keyring
        write_token(store["accounts"][slot]["token"])
        return note + f"Switched to account {slot}: {store['accounts'][slot]['email']}"


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


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="agyswap", description="Multi-account switcher for the Antigravity CLI (agy)")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("tui", help="interactive dashboard (also: bare agyswap)")
    add = sub.add_parser("add", help="store the account agy is signed in with")
    add.add_argument("--slot", type=int, help="store into this slot number")
    sub.add_parser("list", aliases=["ls"], help="list stored accounts with quota usage")
    sub.add_parser("status", help="show the active account")
    sw = sub.add_parser("switch", help="switch to next account, or to <num|email>")
    sw.add_argument("target", nargs="?")
    sw.add_argument(
        "--force", action="store_true", help="switch without copying the live login's token back into its slot first"
    )
    sw.add_argument("--ignore-running", action="store_true", help="switch even if agy is running")
    rm = sub.add_parser("remove", aliases=["rm"], help="forget a stored account")
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
                cmd_list()
            case "status":
                cmd_status()
            case "switch":
                print(cmd_switch(args.target, args.force, args.ignore_running))
            case "remove" | "rm":
                if not args.yes and not confirm_remove(args.target):
                    print("Cancelled")
                    return 0
                print(cmd_remove(args.target))
    except SwapError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
