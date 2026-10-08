# Prepare

Ditulis lewat `/agyswap-prepare` pada 2026-10-08, setelah `/agyswap-review` rilis v0.2.0 dan sebelum `/agyswap-commit`. Belum di-commit.

## 1. TODO.md

- Diperbaiki: butir rilis yang menyebut perbaikan halaman PyPI "sudah ada di `master`". Perbaikan itu masih ada di working tree, belum di-commit.
- Sudah ditambahkan saat review (dicek ulang terhadap kode, masih berlaku):
  - `AGYSWAP_HOME` yang sudah ada tidak dikencangkan ke 0700.
  - `hatchling` belum di-pin persis.
  - Belum diputuskan: perilaku `auto` saat tidak ada yang login.
- Butir lain (repo private, environment `pypi`, `run`, validasi kuota habis, platform) masih berlaku.

## 2. Memory Claude dan Antigravity

Dilewati sesuai aturan 0: sisi Antigravity kosong. `~/.gemini/antigravity-cli/knowledge/` hanya berisi `knowledge.lock`, dan `conversation_summaries.db` tidak punya percakapan dengan workspace agyswap. Tidak ada memory baru yang dibuat.

## 3. Yang usang

- `architecture/PLAN.md` dan `architecture/BUILD.md`: rencana dan log v0.1.0 (baseline, kuota 5 jam + mingguan, render-polish + cli-safety) dihapus. Semuanya sudah dirilis dan tetap ada di git history. Yang tersisa hanya gelombang v0.2.0.
- `architecture/SPEC.md`:
  - Spec modul `render-polish` dan `cli-safety` (sudah selesai di v0.1.0) dihapus.
  - Baseline diselaraskan ke v0.2.0: bentuk store, `usage.json`, tabel perintah (`alias`, `disable`/`enable`, `auto`, `export`/`import`, `--json`, `--strategy`), tombol `x`, aksi TUI di worker thread, dan status PyPI (0.1.0 sudah terbit, bukan "belum terdaftar").
  - Open Questions lama, yang mendaftar fitur yang kini sudah dibangun, diganti dengan sisa yang benar-benar terbuka.
- `CONTRIBUTING.md`: kalimat "The first release ships `0.1.0` as is" dihapus.
- `architecture/TEST.md`: jumlah test 75 → 94, coverage (cli 97%, tui 96%, usage 89%, total 95%), dan daftar test review rilis.

## 4. Sisa debug

- `git grep` untuk `GOCSPX-…`, `ya29.…`, dan `1//0…`: kosong.
- Tidak ada `breakpoint()`, `pdb`, `skip`/`xfail`, atau `# TODO` di `src/` dan `tests/`.
- Tidak ada file untracked.
- Helper test `pytest_fail` diganti nama menjadi `_fail` (awalan `pytest_` dipakai untuk hook pytest).
- Sisa eksperimen reviewer di `/tmp` (`/tmp/mut`, checksum, store sementara) sudah dihapus. Store dengan token palsu di-shred.

## 5. Docs

- `docs/` cocok dengan `uv.lock` (textual 8.2.8, rich 15.0.0, pytest 9.1.1); tidak perlu di-mirror ulang.
- `README.md` dan `AGENTS.md` sudah diperbarui di build dan review, termasuk peringatan import, yang dicek ulang di sini.

## 6. Skills

- `uv run python scripts/skills.py`: `agent-skills@1401c8b: updated nothing`. Upstream tidak berubah.
- `agyswap-review` dan `agyswap-build`: aturan "hanya `cmd_switch` yang menulis keyring" diganti `switch_account` (dipakai `switch`, `switch --strategy`, `auto`). Di `agyswap-build` ditambahkan bahwa `import`/`export` juga tidak pernah menulis keyring.
- `agyswap-ship` dan `CONTRIBUTING.md` (sejak awal siklus): langkah "perbarui badge versi" dihapus.

## 7. Pengetahuan

- Tidak ada koreksi user di sesi ini yang perlu disimpan sebagai memory feedback.
- Fakta baru tentang agy 1.3.1 (`RESOURCE_EXHAUSTED (code 429) … Resets in …`, key snake_case di `agy -p /quota`, updater yang di-spawn per sesi, baris "not logged in" palsu saat start) sudah ada di `architecture/OBSERVE.md`. `AGENTS.md` sudah menyebut 1.3.1.

## 8. Formatter, linter, test, build

| Perintah | Hasil |
| -------- | ----- |
| `uv sync --locked` | Audited 15 packages |
| `uv run ruff format .` | 22 files left unchanged |
| `uv run ruff check .` | No issues found |
| `uv run pytest -q` | 94 passed |
| `uv build` | `agyswap_cli-0.1.0.tar.gz` dan `.whl` (versi dinaikkan di `/agyswap-ship`) |

## 9. Graphify

- `graphify update .`: **915 node, 1593 edge, 49 komunitas**.
- `graphify label . --backend=gemini`: semua komunitas berlabel, tanpa `Community N` dan tanpa label nama file.

## Berikutnya

`/agyswap-commit`, lalu `/agyswap-ship` (bump ke `0.2.0`).
