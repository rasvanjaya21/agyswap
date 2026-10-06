# Commit

Ditulis lewat `/agyswap-commit` pada 2026-10-06. Ini commit pertama setelah `Initial commit`: seluruh pekerjaan baseline v0.1.0 dipecah per kategori, pesan dalam bahasa Inggris dengan gaya commit user, dan tanpa trailer co-author atau atribusi. Belum di-push.

## Commit yang dibuat

| Hash | Pesan | File |
| ---- | ----- | ---- |
| `133591f` | `feat(vcs): add gitignore and python version` | `.gitignore`, `.python-version` |
| `8d68987` | `feat(package): init agyswap package metadata and entry points` | `pyproject.toml` |
| `255c1c8` | `feat(lock): add uv lockfile` | `uv.lock` |
| `6d0df1c` | `feat(src): init agyswap package` | `src/agyswap/__init__.py`, `src/agyswap/__main__.py` |
| `3a72d19` | `feat(usage): implement token refresh and 5h and weekly quota fetch` | `src/agyswap/usage.py` |
| `b675383` | `feat(cli): implement account store, keyring switch and commands` | `src/agyswap/cli.py` |
| `32300d2` | `feat(tui): add pitch black accounts dashboard` | `src/agyswap/tui.py` |
| `52bf33d` | `feat(test): add store, switch, remove, quota and render tests` | `tests/test_swap.py` |
| `3e4d0f9` | `feat(workflow): add ci, publish and weekly skills check` | `.github/workflows/…` |
| `189a549` | `docs(project): update readme, add license, contributing and banner` | `CONTRIBUTING.md`, `.github/assets/…`, `LICENSE`, `README.md` |
| `00b0f98` | `feat(docs): add offline docs mirror for textual, rich and pytest` | `docs/pytest.md`, `docs/rich.md`, `docs/textual.md`, `scripts/docs.py` |
| `98b2de2` | `feat(mcp): add gitmcp servers for textual, rich and pytest` | `.mcp.json` |
| `022d9b5` | `feat(skill): add agyswap project cycle skills` | `scripts/skills.py`, `skills/agyswap-build/…`, `skills/agyswap-commit/…`, `skills/agyswap-observe/…`, `skills/agyswap-plan/…`, `skills/agyswap-prepare/…`, `skills/agyswap-review/…`, `skills/agyswap-ship/…`, `skills/agyswap-spec/…`, `skills/agyswap-test/…` |
| `79dc594` | `docs(agents): add agents guide, claude entry and todo` | `AGENTS.md`, `CLAUDE.md`, `TODO.md` |
| `e7ca51f` | `chore(graph): generated code graph` | `.graphifyignore`, `graphify-out/graph.html`, `graphify-out/graph.json`, `graphify-out/GRAPH_REPORT.md` |
| (commit ini) | `docs(architecture): add observe, spec, plan, build, test, review, prepare and commit records` | `architecture/*.md` (termasuk file ini) |

## Alasan pengelompokan

- **Urutan:** konfigurasi dulu (`vcs`, `package`, `lock`), lalu kode per modul sesuai arah dependensi (`src` → `usage` → `cli` → `tui`), lalu test, workflow, dokumen proyek, mirror docs, MCP, skill, instruksi agent, artefak graph, dan terakhir catatan `architecture/`.
- **Satu file utuh per niat.** Setiap file kode hanya punya satu riwayat (semuanya file baru), jadi tidak perlu stage per hunk.
- **`scripts/` dipecah sesuai pasangannya:** `scripts/docs.py` ikut commit `docs`, dan `scripts/skills.py` ikut commit `skill`, sesuai tabel scope di skill commit.
- **`.github/assets/banner.webp`** ikut commit `project`, karena hanya dipakai `README.md`.
- **`.graphifyignore`** ikut commit `graph`.

## File yang sengaja tidak di-commit

- `.venv/`, `dist/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`: hasil build, cache, dan environment lokal (di-gitignore).
- `.claude/`, `.agents/`: hanya symlink lokal ke `skills/` dan `.mcp.json` (di-gitignore; cara membuatnya ada di `CONTRIBUTING.md`).
- `graphify-out/` selain `GRAPH_REPORT.md`, `graph.html`, `graph.json`: cache dan backup graphify (di-gitignore).
- Tidak ada `accounts.json`, token, client secret, atau `.env` di working tree.

## Hook

Tidak ada git hook di repo ini. Semua commit dibuat tanpa `--no-verify`.
