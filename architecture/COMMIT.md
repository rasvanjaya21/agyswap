# Commit

Ditulis lewat `/agyswap-commit` pada 2026-10-06, setelah `/agyswap-prepare`. Ini commit dari pass ship pertama (NO-GO), perbaikan blocker, review rilis, dan pemindahan fan-out reviewer.

| Hash | Pesan | File |
| ---- | ----- | ---- |
| `d282307` | `fix(usage): map read-time network errors to usage errors` | `src/agyswap/usage.py` |
| `8583b6a` | `fix(cli): report keyring timeouts and unexpected usage errors without traceback` | `src/agyswap/cli.py` |
| `85be519` | `fix(tui): keep dashboard running on empty store, refresh and action errors` | `src/agyswap/tui.py` |
| `9ff4cd1` | `feat(test): add network, keyring timeout and dashboard error tests` | `tests/test_swap.py` |
| `c0f318c` | `feat(package): update description to shipped features` | `pyproject.toml` |
| `8ba1a96` | `docs(project): update readme tagline to shipped features` | `README.md` |
| `2c8663b` | `feat(skill): move reviewer fan-out from ship to review, update secret scan pattern` | `skills/agyswap-ship/SKILL.md`, `skills/agyswap-review/SKILL.md`, `skills/agyswap-prepare/SKILL.md` |
| `0085b7a` | `docs(agents): add tui error invariant and release review findings` | `AGENTS.md`, `TODO.md` |
| `77a8c7b` | `chore(graph): generated code graph` | `graphify-out/GRAPH_REPORT.md`, `graph.html`, `graph.json` |
| (commit ini) | `docs(architecture): add ship record and update review, test, prepare and commit records` | `architecture/SHIP.md`, `REVIEW.md`, `TEST.md`, `PREPARE.md`, `COMMIT.md` |

## Alasan pengelompokan

- **Kode per modul, dipisah dari test.** Jenisnya `fix`, karena ketiganya memperbaiki crash pada kode yang sudah di-commit: TUI `DuplicateIds`, error jaringan dan timeout keyring yang keluar sebagai traceback, dan crash report yang mencetak token.
- **Deskripsi paket (`package`) dan tagline README (`project`)** dipisah sesuai scope, walaupun berasal dari satu keputusan.
- **Ketiga skill dalam satu commit**, karena satu alasan: tanggung jawab ship dan review dipisah. Perubahan pola scan secret di `agyswap-prepare` berasal dari temuan yang sama (cek `GOCSPX` di ship).
- **`AGENTS.md` dan `TODO.md`** masuk scope `agents`.

## Tidak di-commit

Tidak ada. `dist/`, `.venv/`, dan cache `graphify-out/` di-gitignore.

## Push

Push dijalankan user sendiri:

```bash
git push
```

Setelah CI hijau, jalankan `/agyswap-ship`.
