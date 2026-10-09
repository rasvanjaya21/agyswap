# Prepare

Ditulis lewat `/agyswap-prepare` pada 2026-10-09, setelah `/agyswap-review` rilis 0.3.0 dan sebelum `/agyswap-commit`. Belum di-commit.

## 1. TODO.md

- Dipulihkan: heading `## Fitur yang belum ada`, yang hilang saat bagian temuan review disisipkan.
- Dihapus pada sesi ini (sudah selesai atau sudah diputuskan):
  - semua temuan review v0.2.0: folder `0700` diperbaiki, `hatchling` di-pin, alasan 403 dan `auto` tanpa login diputuskan user tetap seperti sekarang;
  - catatan repo private dan pengaturan GitHub, keduanya sudah dikerjakan dan diverifikasi lewat `gh api`;
  - manual check `auto` dua akun, dikonfirmasi user.
- Ditambah: temuan review rilis 0.3.0 yang tidak diperbaiki (celah symlink `_private_dir`, export di filesystem tanpa hard link, `b`/`u` tanpa konfirmasi).
- Diperbarui: butir kuota habis kini menyebut bahwa ambang 90% sudah divalidasi user, sehingga yang tersisa hanya respons saat bucket benar-benar habis.

## 2. Memory Claude dan Antigravity

Dilewati (aturan 0). Sisi Antigravity kosong: `~/.gemini/antigravity-cli/knowledge/` hanya berisi `knowledge.lock`, dan `conversation_summaries.db` tidak punya sesi dengan workspace agyswap.

## 3. Yang usang

- `architecture/BUILD.md`, `PLAN.md`, `REVIEW.md`, dan `TEST.md` sudah ditulis ulang untuk gelombang ini. Catatan v0.2.0 tetap ada di git (`c5b6ce4`).
- `architecture/SPEC.md` bagian as-built "TUI" kini merujuk ke "Gelombang 2026-10-09".
- `architecture/SHIP.md` masih catatan v0.2.0 dan akan ditulis ulang oleh `/agyswap-ship`.

## 4. Sisa debug

Tidak ada:

- tidak ada file untracked, `breakpoint`, `pdb`, `# TODO`, `skip`, atau `xfail`;
- satu-satunya `print` baru di `src/` adalah output CLI (`alias … dropped`);
- `git grep` untuk `GOCSPX-…`, `ya29.…`, dan `1//0…` kosong.

## 5. Docs

- `CONTRIBUTING.md` ("Releasing"):
  - setup environment `pypi`: hanya tag `v*`, required reviewer, self-review diizinkan untuk maintainer tunggal, admin bypass mati;
  - ruleset tag `v*`: restrict updates, restrict deletions, block force pushes, tanpa restrict creations;
  - catatan bahwa job publish menunggu approval.
- `AGENTS.md`: tiga jebakan Textual yang terbukti di sesi ini (`clear`/`extend` harus di-await dan di bawah lock, TUI menelan stdout/stderr, `run_test` mematikan notifikasi). Tombol TUI dan invariant instruksi CLI/TUI serta folder `0700` sudah diperbarui sebelumnya.
- `README.md`: tombol baru, perilaku kursor, default export `~/agyswap-export.agyswap`, dan catatan bahwa `AGYSWAP_HOME` harus folder sendiri.
- `docs/`: versi textual 8.2.8, rich 15.0.0, dan pytest 9.1.1 sama dengan `uv.lock`, jadi tidak di-mirror ulang.

## 6. Skills

`uv run python scripts/skills.py` → `agent-skills@1401c8b: updated nothing`. Bagian agyswap tetap sesuai repo.

## 7. Pengetahuan

- Fakta repo (jebakan Textual) masuk ke `AGENTS.md`.
- Koreksi user di sesi ini masuk memory Claude `manual-checks`: daftar yang harus dijawab user dibuat satu daftar bernomor bertingkat (1.1, 2.1). Sisi Antigravity tidak punya memory untuk diselaraskan.

## 8. Formatter, linter, test, build

| Perintah | Hasil |
| --- | --- |
| `uv sync --locked` | lolos |
| `uv run ruff format .` | 22 file tidak berubah |
| `uv run ruff check .` | tanpa temuan |
| `uv run pytest -q` | 104 passed |
| `uv build` | wheel dan sdist `agyswap_cli-0.2.0` (versi dinaikkan di `/agyswap-ship`) |

## 9. Graphify

`graphify update .` lalu `graphify label . --backend=gemini`: **970 node, 1679 edge, 54 komunitas**. Semua komunitas punya label; tidak ada yang `Community N` atau sekadar nama file.
