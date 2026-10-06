# Prepare

Ditulis lewat `/agyswap-prepare` pada 2026-10-06, setelah review rilis v0.1.0 dan sebelum `/agyswap-commit`. Perubahan yang belum di-commit sejak `82927ef`:

- **Perbaikan blocker ship dan Important review rilis:** `src/agyswap/{cli,usage,tui}.py`, 8 test baru.
- **Deskripsi paket baru:** `pyproject.toml`, `README.md`.
- **Fan-out reviewer dipindah dari ship ke review:** `skills/agyswap-{ship,review}/SKILL.md`, `AGENTS.md`.
- **Catatan:** `architecture/SHIP.md` (baru), `REVIEW.md`, `TODO.md`.

## 1. TODO.md

- **Dihapus:**
  - butir "TEST.md usang" (diperbarui di langkah 3);
  - sebelumnya di sesi ini: blocker ship 1–3, temuan review diff, dua Important review rilis, dan butir cek `GOCSPX`.
- **Diperbarui:** referensi `file:line` di "Temuan review rilis" dan "Temuan ship" sesuai kode saat ini. Butir slot/email dan escape markup diberi penjelasan dan perbaikannya. Butir environment `pypi` menjadi: tag `v*` sudah dibatasi, required reviewers dan ruleset tersedia setelah repo public.
- **Tetap:** semua Suggestion review rilis dan temuan ship, atas keputusan user ("taruh di TODO.md saja dulu").

## 2. Memory Claude dan Antigravity

Dilewati sesuai aturan 0, karena sisi Antigravity kosong: tidak ada knowledge item dan tidak ada sesi agyswap di `conversation_summaries.db`. Memory Claude baru di sesi ini: `reply-language` (balas user dalam bahasa Indonesia).

## 3. Yang usang

- **`architecture/TEST.md`:**
  - 20 test / 61% menjadi 28 test / 82%;
  - tabel baru untuk 8 test jalur error dan TUI;
  - daftar jalur yang belum dites disusun ulang, karena TUI sudah tidak 0% dan `_post` sudah dites.
- **`skills/agyswap-prepare/SKILL.md`:** scan secret `git grep -n -E "GOCSPX|ya29\.|1//0"` tidak pernah bisa kosong, karena regex di `usage.py` ikut cocok. Diganti pola secret lengkap.
- **Catatan historis yang dibiarkan:** `SHIP.md` mencatat pass NO-GO pertama, dan `BUILD.md` mencatat build lama.

## 4. Sisa debug

- Tidak ada `breakpoint()`, `pdb`, `skip`, `xfail`, atau file coba-coba.
- Harness verifikasi di `/tmp` sudah dihapus.
- Scan secret pola lengkap: kosong.

## 5. Docs

- **`AGENTS.md`, invariant baru:** tidak ada exception yang boleh lolos dari TUI (crash report Textual mencetak locals). Handler hanya menampilkan teks `SwapError` atau jenis exception, dan memanggil UI di luar `except`. `_post` dan `_secret_tool` memetakan error jaringan dan timeout keyring.
- **`AGENTS.md`, asal fan-out:** fan-out reviewer berasal dari `commands/ship.md` upstream yang tidak di-vendor, dan sekarang dijalankan di `/agyswap-review`.
- **`README.md`:** tagline baru tanpa fitur yang belum ada. Bagian Status tidak berubah dan tetap benar.
- **`docs/`:** textual 8.2.8, rich 15.0.0, pytest 9.1.1, sama dengan `uv.lock`. `.mcp.json` tetap 1:1.

## 6. Skills

- `uv run python scripts/skills.py`: `agent-skills@1401c8b: updated nothing`.
- **Bagian agyswap yang diubah:**
  - `agyswap-ship`: hanya cek rilis, semver, GO/NO-GO, dan rollback. NO-GO otomatis tanpa review rilis yang Approve. Scan secret memakai pola lengkap.
  - `agyswap-review`: cakupan biasa atau rilis, fan-out tiga reviewer, dan verifikasi Critical/Important oleh agent utama.
  - `agyswap-prepare`: pola scan secret.

## 7. Pengetahuan

- **Repo:** invariant TUI dan perpindahan fan-out dicatat di `AGENTS.md` dan skill.
- **User:**
  - memory `reply-language`;
  - aturan "agent tidak push atau tag" sudah ada di memory dan `AGENTS.md`.
- **Keputusan user di sesi ini (tercatat di repo):**
  - deskripsi paket diganti;
  - semua Suggestion masuk `TODO.md`;
  - `auto` menarik untuk siklus berikutnya, dimulai dengan `/agyswap-observe` (file token dengan `--gemini_dir` saat keyring tidak terjangkau, dan respons saat kuota habis).

## 8. Formatter, linter, test, build

| Perintah | Hasil |
| -------- | ----- |
| `uv sync --locked` | Audited 15 packages |
| `uv run ruff format .` | 22 files left unchanged |
| `uv run ruff check .` | All checks passed |
| `uv run pytest -q` | 28 passed |
| `uv build` | `agyswap_cli-0.1.0` wheel dan sdist |

## 9. Graphify

- `graphify update .` lalu `graphify label . --backend=gemini`: beberapa komunitas masih bernama file (`cli.py`, `docs.py`, `README.md`).
- `graphify label . --backend=claude-cli`: semua komunitas bernama.
- Hasil: 745 node, 1072 edge, 27 komunitas.

## Uji manual oleh user

Tidak ada yang wajib. Perbaikan sesi ini hanya menyentuh jalur error (jaringan, timeout keyring, TUI), tidak menyentuh `add`, `switch`, atau format store, dan semuanya dites otomatis.

## Langkah berikutnya

`/agyswap-commit` → user `git push` dan menunggu CI hijau → `/agyswap-ship`.
