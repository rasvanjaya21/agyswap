# Commit

Ditulis lewat `/agyswap-commit` pada 2026-10-09, setelah `/agyswap-prepare` kedua dan sebelum `/agyswap-ship` (0.3.0). Tanpa trailer co-author atau atribusi, sesuai instruksi user. Belum di-push.

## Commit

| Hash | Pesan | File |
| --- | --- | --- |
| `7adb2c2` | `feat(package): pin hatchling build backend to 1.32.4` | `pyproject.toml` |
| `2184616` | `feat(workflow): disable uv cache in release build` | `.github/workflows/publish.yml` |
| `46e0e7f` | `feat(cli): tighten existing store folder to 0700 and refuse one owned by another user` | `src/agyswap/cli.py` (bagian `_private_dir`) |
| `16c84ea` | `feat(cli): add tui wording to errors that name cli commands or flags` | `src/agyswap/cli.py` (bagian `SwapError.tui`) |
| `0f8f931` | `feat(cli): reject control characters in imported alias and disabled reason` | `src/agyswap/cli.py` (bagian `_printable`) |
| `4ce57ef` | `feat(usage): remove cli command from revoked token message` | `src/agyswap/usage.py` |
| `de30dd3` | `feat(tui): add alias, more menu with best, auto, export and import, keep cursor on its account and show loading state` | `src/agyswap/tui.py` |
| `5f53fbd` | `feat(test): add tests for tui parity, cursor, error wording, store folder and import validation` | `tests/test_swap.py` |
| `90a7800` | `docs(project): add new tui keys and export default, document release environment and tag ruleset` | `README.md`, `CONTRIBUTING.md` |
| `f8d3ead` | `docs(agents): add tui keys, cli and tui wording invariant and textual pitfalls, update todo` | `AGENTS.md`, `TODO.md` |
| `ad857aa` | `chore(graph): generated code graph` | `graphify-out/GRAPH_REPORT.md`, `graph.html`, `graph.json` |
| (commit ini) | `docs(architecture): add observe, spec, plan, build, test, review, prepare and commit records for 0.3.0` | `architecture/{OBSERVE,SPEC,PLAN,BUILD,TEST,REVIEW,PREPARE,COMMIT}.md` |

## Alasan pengelompokan

- Urutannya config (package, workflow), lalu kode per modul, lalu test, lalu docs dan artefak.
- `src/agyswap/cli.py` berisi tiga niat yang terpisah jelas, jadi dibagi menjadi tiga commit: folder store `0700`, teks TUI untuk error, dan karakter kontrol pada import. Versi antara disusun dengan menerapkan ulang editan ke `HEAD` lalu di-stage sebagai blob. Versi ketiga identik dengan working tree, dan setiap versi antara lolos `ast.parse`.
- `src/agyswap/tui.py` tetap satu commit. Kursor, tombol baru, tampilan, `e.tui`, lock `_show`, dan lokasi export saling terkait dalam fungsi yang sama (`_show`, `_run`, `action_*`), sehingga pemisahan per hunk tidak jelas.
- `usage.py` dipisah dari `cli.py` karena modulnya berbeda, walaupun niatnya sama dengan teks error CLI/TUI.
- Semua test masuk satu commit setelah kode, karena satu file test mencakup semua perubahan di atas.

## Tidak di-commit

Tidak ada. Working tree bersih setelah commit ini. `dist/` dan cache `graphify-out/` (backup per tanggal, `cache/`, `manifest.json`) di-gitignore.
