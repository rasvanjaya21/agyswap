# Commit

Ditulis lewat `/agyswap-commit` pada 2026-10-08, setelah `/agyswap-prepare` kedua. Belum di-push; push dijalankan user.

## Commit yang dibuat

| Hash | Pesan | File |
| ---- | ----- | ---- |
| `d87911b` | `feat(package): migrate license to pep 639, add changelog url and pin hatchling range` | `pyproject.toml` |
| `4ea06ba` | `feat(workflow): pin actions to commit sha, restrict permissions and split publish into build, publish and release jobs` | `.github/workflows/ci.yml`, `publish.yml`, `skills.yml` |
| `c686c90` | `feat(usage): add revoked and rate limited errors, clamp retry-after, refuse redirects and scan agy binary once` | `src/agyswap/usage.py` |
| `7ec04fc` | `feat(cli): add alias, disable, enable, auto, quota strategy, json output, export, import and usage cache, harden store writes` | `src/agyswap/cli.py` |
| `5c526b2` | `fix(tui): run actions in workers, target accounts by email and escape external text` | `src/agyswap/tui.py` (tanpa tombol `x`) |
| `2f27235` | `feat(tui): add disable and enable toggle on x` | `src/agyswap/tui.py` |
| `0784c9f` | `feat(test): add tests for review fixes, account flags, quota strategy, auto, json and export` | `tests/test_swap.py` |
| `ef62a24` | `docs(project): add v0.2.0 usage, use absolute links for pypi and remove version badge` | `README.md`, `CONTRIBUTING.md` |
| `94f08a1` | `feat(skill): update keyring writer rule and remove version badge step` | `skills/agyswap-{build,review,ship}/SKILL.md` |
| `7afd229` | `docs(agents): add v0.2.0 commands and invariants, update todo` | `AGENTS.md`, `TODO.md` |
| `a910b6a` | `chore(graph): generated code graph` | `graphify-out/GRAPH_REPORT.md`, `graph.html`, `graph.json` |
| `281c2f1` | `docs(architecture): add v0.1.0 publish result to ship record` | `architecture/SHIP.md` |
| (commit terakhir) | `docs(architecture): add observe, spec, plan, build, test, review, prepare and commit records for v0.2.0` | `architecture/{OBSERVE,SPEC,PLAN,BUILD,TEST,REVIEW,PREPARE,COMMIT}.md` |

## Alasan pengelompokan

- **Urutan:** config dulu (`package`, `workflow`), lalu kode dari bawah ke atas mengikuti dependensinya (`usage` → `cli` → `tui`), lalu test, docs, skill, graph, dan catatan `architecture/`.
- **`tui.py` dipecah per hunk:**
  - `5c526b2` memperbaiki perilaku yang memang rusak di v0.1.0: aksi memakai slot dari baris lama, notifikasi tanpa escape, dan aksi yang memblokir thread UI. Karena itu type-nya `fix`.
  - `2f27235` menambah tombol `x`.
  - File di `5c526b2` sudah dicek valid (`ast.parse`) dan tidak memuat `toggle`.
- **`cli.py` dan `usage.py` satu commit per modul.** Hardening dari review dan ship v0.1.0 (store atomik, lock `O_NOFOLLOW`, error keyring, exit code `list`, redirect, scan binary) bertaut di hunk yang sama dengan fitur v0.2.0. Misalnya `save_store` menjadi `_write_private`, dan pesan 429 menjadi `RateLimited`. Pemisahan per hunk tidak jelas, jadi keduanya masuk satu commit yang menyebut hardening di pesannya.
- **`SHIP.md` terpisah:** isinya hasil publish v0.1.0 dari sesi sebelumnya, bukan catatan siklus v0.2.0.
- **Test satu commit** setelah semua kode: satu file yang menguji semua modul.

## Tidak di-commit

Tidak ada. `git status` bersih setelah commit terakhir. `dist/`, `.venv/`, dan cache serta backup `graphify-out/` di-gitignore.
