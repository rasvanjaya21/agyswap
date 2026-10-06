<p align="center">
    <a href="#"><img src=".github/assets/banner.webp" width="250"></a>
</p>

<p align="center">
    <strong>Switch between multiple Antigravity CLI accounts, with a quota dashboard for every account.</strong>
</p>

<p align="center">
    <a href="#"><img src="https://img.shields.io/badge/author-rasvanjaya21-white" alt="author-name"></a>
    <a href="#"><img src="https://img.shields.io/badge/version-0.1.0-blue" alt="project-version"></a>
    <a href="https://pypi.org/project/agyswap-cli/"><img src="https://img.shields.io/pypi/v/agyswap-cli?label=pip" alt="pypi-version"></a>
    <a href="https://github.com/rasvanjaya21/agyswap/actions/workflows/ci.yml"><img src="https://github.com/rasvanjaya21/agyswap/actions/workflows/ci.yml/badge.svg" alt="build-status"></a>
</p>

## Description

agyswap switches the Google account used by the Antigravity CLI (`agy`) without signing in again, and shows the quota left on every account. It does not work with the Antigravity IDE, Gemini CLI, or other Google AI products.

agy keeps its login in the OS keyring as a single OAuth token. agyswap stores a copy of each account's token, and switching writes another account's copy back to the keyring. The next `agy` you start runs as that account.

## Status

**Usable on Linux.** Adding accounts, switching between them, the quota list, and the interactive dashboard all work, and switching between two real accounts without signing in again has been verified.

Not built yet: automatic switching when an account runs low, parallel sessions with different accounts, aliases, enable/disable, export/import, and macOS/Windows keyrings. `TODO.md` lists every open item.

## Techstacks

Python 3.12+ managed with uv. The dashboard uses Textual and Rich; everything else is the standard library, plus `secret-tool` (libsecret) for the keyring.

## Installation

```bash
$ uv tool install agyswap-cli    # or: pipx install agyswap-cli / pip install agyswap-cli
$ agyswap --help                 # the command is still agyswap
```

Until the first release is on PyPI, install from GitHub instead:

```bash
$ uv tool install git+https://github.com/rasvanjaya21/agyswap
```

agyswap needs Linux with a Secret Service keyring (GNOME Keyring or KWallet) and `secret-tool` (`dnf install libsecret` or `apt install libsecret-tools`).

## Configuration

| Variable | What it does |
| --- | --- |
| `AGYSWAP_HOME` | Where agyswap keeps its account store. Defaults to `~/.agyswap`. The store, `accounts.json`, holds refresh tokens and is written with mode `0600`. |

## Usage

Unlike Claude Code, agy has no account picker. To add an account, sign out of agy, sign in with that account, then store it:

```bash
$ agy             # /logout, then sign in with account A, then exit
$ agyswap add
$ agy             # /logout, then sign in with account B, then exit
$ agyswap add
```

Signing out of agy does not revoke the token agyswap already stored.

Run `agyswap` on its own (or `agyswap tui`) for the dashboard. It shows every account's quota for both model groups (Gemini, and Claude/GPT), each with its 5-hour and weekly window and reset times, and marks the active account. Usage refreshes every 2 minutes.

| Key | Action |
| --- | --- |
| `enter` / `s` | Switch to the highlighted account |
| `a` | Add the account agy is signed in with |
| `d` | Remove the highlighted account |
| `r` | Refresh usage |
| `j` / `k` | Move |
| `q` | Quit |

The same actions are available as commands:

```bash
$ agyswap switch                  # rotate to the next account
$ agyswap switch 2                # by slot
$ agyswap switch user@gmail.com   # by email
$ agyswap list                    # quota of every account
$ agyswap status
$ agyswap remove 2                 # asks first; add --yes (-y) in scripts
```

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

Releases are published to PyPI by `.github/workflows/publish.yml` when a `v*` tag is pushed. The version lives only in `pyproject.toml`.

```bash
$ uv version --bump patch
$ uv lock
$ git commit -am "chore: release v$(uv version --short)"
$ git push                                  # wait for CI to pass
$ git tag "v$(uv version --short)" && git push origin "v$(uv version --short)"
```

A published version cannot be replaced. To roll back, yank it on PyPI and release a patch. The one-time PyPI and GitHub setup is in `CONTRIBUTING.md`.

## Architecture

Design decisions and the reasoning behind them live in `architecture/`, one file per workflow that produced it. `OBSERVE.md` maps how agy stores its login and reports quota, with the evidence for each fact; `SPEC.md` specifies the current version; `PLAN.md` lays out the next tasks; `REVIEW.md` holds the latest code review.

`AGENTS.md` holds the conventions and the development cycle, and is the single channel shared by every agent working here. `TODO.md` holds open findings and is deleted entry by entry as they are resolved.

## Credit

- id: agyswap
- displayName: agyswap - Antigravity CLI Accounts Swap
- authorName: rasvanjaya21
- authorEmail: rasvanjaya21@gmail.com
- authorURL: https://github.com/rasvanjaya21

## Member

- @rasvanjaya21 [assigned]
