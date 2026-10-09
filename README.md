<p align="center">
    <a href="#"><img src="https://raw.githubusercontent.com/rasvanjaya21/agyswap/master/.github/assets/banner.webp" width="250"></a>
</p>

<p align="center">
    <strong>Switch between multiple Antigravity CLI accounts, with a quota dashboard for every account.</strong>
</p>

<p align="center">
    <a href="#"><img src="https://img.shields.io/badge/author-rasvanjaya21-white" alt="author-name"></a>
    <a href="https://pypi.org/project/agyswap-cli/"><img src="https://img.shields.io/pypi/v/agyswap-cli?label=pip" alt="pypi-version"></a>
    <a href="https://github.com/rasvanjaya21/agyswap/actions/workflows/ci.yml"><img src="https://github.com/rasvanjaya21/agyswap/actions/workflows/ci.yml/badge.svg" alt="build-status"></a>
    <a href="https://github.com/rasvanjaya21/agyswap/discussions"><img src="https://img.shields.io/github/discussions/rasvanjaya21/agyswap?label=discussions" alt="discussions"></a>
</p>

## Description

agyswap switches the Google account used by the Antigravity CLI (`agy`) without signing in again, and shows the quota left on every account. It does not work with the Antigravity IDE, Gemini CLI, or other Google AI products.

agy keeps its login in the OS keyring as a single OAuth token. agyswap stores a copy of each account's token, and switching writes another account's copy back to the keyring. The next `agy` you start runs as that account.

Inspired by [claude-swap](https://github.com/realiti4/claude-swap).

## Status

**Usable on Linux.** Adding accounts, switching between them (by hand, by quota, or with `auto` when the active account runs low), aliases, enable/disable, export/import, JSON output, the quota list, and the interactive dashboard all work. Switching between two real accounts without signing in again has been verified.

Not built yet: parallel sessions with different accounts, and macOS/Windows keyrings. [`TODO.md`](https://github.com/rasvanjaya21/agyswap/blob/master/TODO.md) lists every open item. Questions, ideas, and feedback are welcome in [Discussions](https://github.com/rasvanjaya21/agyswap/discussions).

## Techstacks

Python 3.12+ managed with uv. The dashboard uses Textual and Rich; everything else is the standard library, plus `secret-tool` (libsecret) for the keyring.

## Installation

```bash
$ uv tool install agyswap-cli    # or: pipx install agyswap-cli / pip install agyswap-cli
$ agyswap --help                 # the command is still agyswap
```

agyswap needs Linux with a Secret Service keyring (GNOME Keyring or KWallet) and `secret-tool` (`dnf install libsecret` or `apt install libsecret-tools`).

## Configuration

| Variable | What it does |
| --- | --- |
| `AGYSWAP_HOME` | Where agyswap keeps its account store. Defaults to `~/.agyswap`. The store, `accounts.json`, holds refresh tokens and is written with mode `0600`; the quota cache `usage.json` sits next to it. The folder is kept at `0700` (an existing one is tightened, and one owned by another user is refused), so point it at a folder of its own, never at `~` or a shared folder. |

## Usage

Unlike Claude Code, agy has no account picker. To add an account, sign out of agy, sign in with that account, then store it:

```bash
$ agy             # /logout, then sign in with account A, then exit
$ agyswap add
$ agy             # /logout, then sign in with account B, then exit
$ agyswap add
```

Signing out of agy does not revoke the token agyswap already stored.

`agyswap add --slot 3` stores the account in slot 3 (moving it if it is already stored elsewhere); it refuses a slot that holds another account.

Run `agyswap` on its own (or `agyswap tui`) for the dashboard. It shows every account's quota for both model groups (Gemini, and Claude/GPT), each with its 5-hour and weekly window and reset times, and marks the active account. Usage refreshes every 2 minutes. The cursor starts on the active account and stays on the same account across refreshes.

| Key | Action |
| --- | --- |
| `enter` / `s` | Switch to the highlighted account |
| `a` | Add the account agy is signed in with |
| `d` | Remove the highlighted account |
| `x` | Disable or enable the highlighted account |
| `n` | Set or clear the highlighted account's alias |
| `m` | Show the shortcuts below that are not in the footer |
| `b` | Switch to the account with the most quota left (`switch --strategy best`) |
| `u` | Switch away only if the active account is at 90% or more (`auto`) |
| `e` | Export all accounts, refresh tokens included, to a file (default `~/agyswap-export.agyswap`) |
| `i` | Import accounts from an export file |
| `r` | Refresh usage of all accounts |
| `j` / `k` | Move |
| `q` | Quit |

The same actions are available as commands:

```bash
$ agyswap switch                  # rotate to the next enabled account
$ agyswap switch 2                # by slot
$ agyswap switch user@gmail.com   # by email
$ agyswap switch work             # by alias
$ agyswap list                    # quota of every account
$ agyswap status
$ agyswap remove 2                # asks first; add --yes (-y) in scripts
```

Name accounts and leave some out of rotation:

```bash
$ agyswap alias 2 work            # omit the name to clear it
$ agyswap disable 3               # skipped by switch, --strategy, and auto
$ agyswap enable 3
```

Pick an account by quota. An account qualifies when every bucket (5-hour and weekly, both model groups) is below the threshold, 90% by default:

```bash
$ agyswap switch --strategy best             # the account with the most quota left
$ agyswap switch --strategy next-available   # the next account in order that qualifies
$ agyswap auto                               # switch only if the active account reached 90%
$ agyswap auto && agy                        # check before every session
```

`auto` runs once and exits; it never runs in the background. It exits 1 without switching when no account qualifies or the active account's quota cannot be read. Add `--threshold 80` to either command to change the limit.

`list`, `status`, `switch`, and `auto` accept `--json` and print one JSON object (`"version": 1`) without any token. Errors become `{"version": 1, "error": "..."}` with the same exit code.

The last good quota reading is cached in `usage.json` next to the store. When a fetch fails, `list` and the dashboard show that reading marked `stale`. After an HTTP 429, agyswap waits for `Retry-After` (5 minutes if absent) before asking Google again. An account whose refresh token is rejected (`invalid_grant`) is disabled with the reason `token revoked`; sign in with it again and run `agyswap add` to bring it back.

Move accounts to another machine:

```bash
$ agyswap export accounts.agyswap   # 0600, refuses to overwrite without --force
$ agyswap import accounts.agyswap   # skips stored accounts unless --force
```

The export file holds refresh tokens without encryption. Anyone who has it can use those accounts, so keep it private and delete it after the import. Only import files you exported yourself: agyswap checks that each token's email claim matches its entry, but cannot verify the signature, so a crafted file could label someone else's login with your email.

Exit agy before you switch. A running agy reads the keyring only when it starts and saves its own token back every hour, which would undo the switch. `agyswap switch` refuses while agy is running; `--ignore-running` overrides that. `--force` switches without first copying the live login's token back into its slot.

## Development

```bash
$ git clone https://github.com/rasvanjaya21/agyswap && cd agyswap
$ uv sync          # creates .venv with agyswap installed in editable mode
$ uv run agyswap
```

For a manual run against your real agy login, use a throwaway store and shred it afterwards:

```bash
$ export AGYSWAP_HOME=$(mktemp -d)
$ uv run agyswap add && uv run agyswap list
$ shred -u "$AGYSWAP_HOME/accounts.json"
```

## Testing

```bash
$ uv run ruff format .    # formatter
$ uv run ruff check .     # linter
$ uv run pytest -q        # tests
$ uv build                # wheel and sdist into dist/
```

Tests never touch the real keyring, the network, or `~/.agyswap/`. The keyring, the store, and every Google request are faked.

## Deployment

Releases are published to PyPI by [`publish.yml`](https://github.com/rasvanjaya21/agyswap/blob/master/.github/workflows/publish.yml) when a `v*` tag is pushed. The version lives only in `pyproject.toml`.

```bash
$ uv version --bump patch
$ uv lock
$ git commit -am "chore: release v$(uv version --short)"
$ git push                                  # wait for CI to pass
$ git tag "v$(uv version --short)" && git push origin "v$(uv version --short)"
```

A published version cannot be replaced. To roll back, yank it on PyPI and release a patch. The one-time PyPI and GitHub setup is in [`CONTRIBUTING.md`](https://github.com/rasvanjaya21/agyswap/blob/master/CONTRIBUTING.md).

## Architecture

Design decisions and the reasoning behind them live in [`architecture/`](https://github.com/rasvanjaya21/agyswap/tree/master/architecture), one file per workflow that produced it. [`OBSERVE.md`](https://github.com/rasvanjaya21/agyswap/blob/master/architecture/OBSERVE.md) maps how agy stores its login and reports quota, with the evidence for each fact; [`SPEC.md`](https://github.com/rasvanjaya21/agyswap/blob/master/architecture/SPEC.md) specifies the current version; [`PLAN.md`](https://github.com/rasvanjaya21/agyswap/blob/master/architecture/PLAN.md) lays out the next tasks; [`REVIEW.md`](https://github.com/rasvanjaya21/agyswap/blob/master/architecture/REVIEW.md) holds the latest code review.

[`AGENTS.md`](https://github.com/rasvanjaya21/agyswap/blob/master/AGENTS.md) holds the conventions and the development cycle, and is the single channel shared by every agent working here. [`TODO.md`](https://github.com/rasvanjaya21/agyswap/blob/master/TODO.md) holds open findings and is deleted entry by entry as they are resolved.

## Credit

- id: agyswap
- displayName: agyswap - Antigravity CLI Accounts Swap
- authorName: rasvanjaya21
- authorEmail: rasvanjaya21@gmail.com
- authorURL: https://github.com/rasvanjaya21

## Member

- @rasvanjaya21 [assigned]
