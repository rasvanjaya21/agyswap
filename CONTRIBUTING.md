# Contributing

## Setup

```bash
git clone https://github.com/rasvanjaya21/agyswap && cd agyswap
uv sync                 # creates .venv with agyswap installed in editable mode
uv run pytest -q
uv run agyswap          # TUI
```

Requirements: Linux, Python 3.12+, [uv](https://docs.astral.sh/uv/), and `secret-tool` (libsecret).

Tests never touch the real keyring, the network, or `~/.agyswap/`. For a manual run against your real agy login, use a throwaway store and shred it afterwards:

```bash
export AGYSWAP_HOME=$(mktemp -d)
uv run agyswap add && uv run agyswap list
shred -u "$AGYSWAP_HOME/accounts.json"
```

### Agent Tooling

This repository is set up for Claude Code and Antigravity (`agy`). Skills live in `skills/` and MCP servers in `.mcp.json`; each agent reads them through symlinks that are not committed. Create them once after cloning:

```bash
mkdir -p .claude .agents
ln -s ../skills .claude/skills
ln -s ../skills .agents/skills
ln -s ../.mcp.json .agents/mcp_config.json
```

Antigravity does not load project MCP servers yet ([antigravity-cli#60](https://github.com/google-antigravity/antigravity-cli/issues/60)), so register the ones from `.mcp.json` globally as well:

```bash
agy mcp add textual bunx -- --bun mcp-remote@0.14.3 https://gitmcp.io/Textualize/textual
agy mcp add rich bunx -- --bun mcp-remote@0.14.3 https://gitmcp.io/Textualize/rich
agy mcp add pytest bunx -- --bun mcp-remote@0.14.3 https://gitmcp.io/pytest-dev/pytest
```

The six core skills vendor their method from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). Pull the latest upstream with `uv run python scripts/skills.py` (`--check` only reports); the weekly `Skills upstream` workflow fails when they fall behind.

`docs/` holds offline copies of the official Textual, Rich, and pytest docs, pinned to the versions in `uv.lock`. Regenerate them after a version bump with `uv run python scripts/docs.py`.

The code graph lives in `graphify-out/`. Refresh it with `graphify update .` and then `graphify label . --backend=gemini`.

See [AGENTS.md](./AGENTS.md) for how skills, `docs/`, and MCP servers fit together.

## Development Workflow

1. Create a branch: `git checkout -b feature/your-feature-name`
2. Make your changes, with a failing test first (`tests/`, pytest)
3. Format and lint: `uv run ruff format .` and `uv run ruff check .` (config in `[tool.ruff]`, CI runs both)
4. Run tests: `uv run pytest -q`
5. Build when packaging changed: `uv build`
6. Commit using the conventions below

## Commit Conventions

`type(scope): description`, in lowercase and imperative mood, with no trailing period and on one line. Scopes in use: `cli`, `usage`, `tui`, `src`, `test`, `package`, `lock`, `vcs`, `workflow`, `project`, `docs`, `architecture`, `agents`, `skill`, `mcp`, `graph`. A whole-repo release is `chore: release vX.Y.Z`.

## Releasing

Releases are published to PyPI by `.github/workflows/publish.yml` when a `v*` tag is pushed. The version lives only in `pyproject.toml`.

One-time setup:

1. On PyPI, go to Account → Publishing → "Add a new pending publisher". Set the project name to the name in `pyproject.toml`, owner `rasvanjaya21`, repository `agyswap`, workflow `publish.yml`, and environment `pypi`.
2. On GitHub, create the `pypi` environment under Settings → Environments.

Pick the bump from the commits since the last tag: **major** for anything that breaks existing use (a removed or renamed command or flag, an incompatible store format, changed exit codes), **minor** for new user-visible capability, and **patch** for everything else. While the version is `0.x`, a breaking change only bumps minor. The first release ships `0.1.0` as is. `/agyswap-ship` does this categorisation and proposes the version.

Each release:

```bash
uv version --bump patch        # or minor / major
uv lock
git add pyproject.toml uv.lock README.md   # README carries the version badge
git commit -m "chore: release v$(uv version --short)"
git push                       # wait for CI to pass
git tag "v$(uv version --short)"
git push origin "v$(uv version --short)"
```

A published version cannot be replaced. To roll back, yank the bad version on PyPI and release a patch.
