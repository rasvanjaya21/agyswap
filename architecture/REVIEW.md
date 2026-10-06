Cakupan: **review rilis v0.1.0**. Belum ada tag, jadi yang direview seluruh paket di working tree (`src/`, `tests/`, `pyproject.toml`, `README.md`, `.github/workflows/`), termasuk perbaikan blocker ship yang belum di-commit.

# Review rilis v0.1.0

Ditulis lewat `/agyswap-review` pada 2026-10-06. Tiga reviewer berjalan paralel (`code-reviewer`, `security-auditor`, `test-engineer`). Temuan Important diverifikasi ulang oleh agent utama.

**Verdict: Approve** setelah tindak lanjut di bawah. Awalnya Request changes karena dua Important, keduanya kecil. Tidak ada temuan Critical, dan tidak ada temuan security Critical/High. Tidak ada jalur yang menghilangkan token: store selalu disimpan sebelum keyring ditulis.

## Verifikasi

- `uv run ruff check .` dan `ruff format --check .` lolos. `uv run pytest -q`: 25 passed. `uv build` bersih.
- **Wheel:** hanya `agyswap/*.py` dan dist-info. **Sdist:** tanpa store, tanpa secret, dan token di test hanya placeholder.
- `git grep -n -E 'GOCSPX-[A-Za-z0-9_-]{20,}|ya29\.|1//0'`: hanya teks pola di `skills/agyswap-prepare/SKILL.md`. Riwayat git (`git log -p --all`): 0 kecocokan.
- `pip-audit` (`uv export --all-groups`): tidak ada kerentanan yang diketahui.
- **Coverage:** `cli.py` 86%, `usage.py` 76%, `tui.py` 67%, total 79% (sebelumnya 61%).
- **Mutasi** (21 mutasi oleh `test-engineer`): 13 tertangkap, 8 lolos (Important 3 dan Suggestion 5).
- **Reproduksi Important 1 oleh agent utama:** dengan Textual pilot, `write_token` dibuat melempar `subprocess.TimeoutExpired`, lalu tombol `s` ditekan. Hasilnya `TimeoutExpired` keluar mentah dan app tertutup.

## Lima sumbu

- **Correctness:** semua invariant di `AGENTS.md` dipenuhi kode. Fallback di jalur error TUI belum lengkap (Important 1 dan 2).
- **Readability:** perbaikan blocker kecil dan berkomentar.
- **Architecture:** arah `tui.py` → `cli.py` → `usage.py` tetap.
- **Security:** CLI tidak pernah mencetak locals, karena traceback default Python tidak menampilkannya, dan semua pesan error bebas token. TUI memakai crash report Textual (`show_locals=True`), sehingga setiap exception yang lolos dari handler adalah jalur bocor (Important 1 dan 2).
- **Performance:** temuan lama sudah ada di `TODO.md` (aksi TUI di thread UI, binary agy dibaca paralel).

## Important

1. **Aksi switch, add, dan remove di TUI crash pada error selain `SwapError`, dan crash report mencetak awal access token serta semua email** (`src/agyswap/tui.py:155-161`, akar masalah di `src/agyswap/cli.py:67-72`).
   - **Penyebab:** `_secret_tool` hanya menangkap `FileNotFoundError`. Keyring yang terkunci dan dibiarkan 30 detik memunculkan `subprocess.TimeoutExpired`, yang lolos dari `_run`.
   - **Jalur lain dengan akibat sama:** `OSError` dari `save_store`, dan `accounts.json` yang rusak.
   - **Di CLI:** traceback biasa tanpa locals, tidak rapi tapi tidak bocor.
   - Ditemukan ketiga reviewer, lalu direproduksi agent utama.
   - **Perbaikan:**
     - `_secret_tool` menangkap `TimeoutExpired` dan melempar `SwapError("keyring did not answer within 30s (locked?)") from None`.
     - `_run` menambah `except Exception` yang hanya menampilkan nama jenis exception, sama dengan `action_refresh`.
     - Tambah test pilot untuk `s` dengan `TimeoutExpired`.
2. **Handler error refresh memanggil `call_from_thread` di dalam blok `except`** (`src/agyswap/tui.py:121-127`, `security-auditor` L1).
   - **Akibat:** kalau pemanggilan itu gagal (app sedang ditutup), exception asal ikut terbawa sebagai `__context__`. Crash report lalu mencetak frame `fresh_token`, termasuk **client secret lengkap** (35 karakter, di bawah batas potong 80 karakter).
   - **Kemungkinan:** rendah, karena butuh exception tak terduga dari `collect_usage` sekaligus `q` saat refresh berjalan. Dampaknya tinggi dan perbaikannya tiga baris.
   - Diverifikasi dengan membaca kode: kedua pemanggilan `call_from_thread` memang berada di dalam `except`.
   - **Perbaikan:**
     - Susun pesan di dalam `except`, panggil `call_from_thread` di luarnya.
     - Di `collect_usage.one` (`cli.py:160`), tangkap `Exception` dan simpan hanya nama jenisnya di `row["error"]`. Satu respons aneh tidak lagi menjatuhkan seluruh `list`, dan jalur ini tertutup dari sumbernya.

## Suggestion

1. **`architecture/TEST.md` sudah usang:** masih 20 test, coverage 61%, dan `tui.py` 0%. Perbarui saat `/agyswap-prepare`.
2. **TUI memakai nomor slot dari baris yang bisa berumur sampai 120 detik** (`src/agyswap/tui.py:167`, `:183`). Kalau terminal lain menghapus slot N lalu menambah akun baru ke slot N, tombol `d` menghapus akun baru, padahal dialog menampilkan email lama. Akibatnya salinan refresh token satu-satunya bisa hilang. Kemungkinannya kecil. **Perbaikan:** kirim `row["email"]`, bukan `row["slot"]` (`find_slot` sudah mencocokkan email).
3. **Pesan `notify` dan label `Confirm` tidak di-escape** (`src/agyswap/tui.py:157`, `:160`, `:186`). Teks `[` dari stderr `secret-tool` bisa membuat app crash saat dirender (tanpa token). **Perbaikan:** pakai `escape()`.
4. **`agyswap list` mengembalikan exit 0 walaupun semua akun error** (`src/agyswap/cli.py:229-236`).
5. **Mutasi yang lolos:**
   - guard merge `collect_usage`: cek email, cek expiry lebih baru, dan seluruh blok (M3–M5);
   - token live untuk baris akun aktif (M12);
   - `flock` di `locked_store` (M14);
   - `--slot 0` (M16);
   - `invalid_grant` menjadi "token revoked" (M19);
   - catch `KeyError`/`ValueError` di `collect_usage` (M21).

   `test-engineer` sudah menulis sketsa test untuk setiap mutasi dan semuanya lolos di kode saat ini.
6. **`hatchling` tidak di-pin** (`pyproject.toml:36`). Artefak PyPI dibangun dengan versi apa pun yang tersedia saat tag.
7. **Environment `pypi` di GitHub:** deployment sudah dibatasi ke tag `v*` (dicek lewat `gh api`). Required reviewers dan ruleset proteksi tag belum tersedia untuk repo private di GitHub Free (API: `Upgrade to GitHub Pro or make this repository public`), jadi diaktifkan setelah repo public.
8. **Badge `version-0.1.0` di `README.md:11` di-hardcode**, padahal versi seharusnya hanya ada di `pyproject.toml`. Ini sudah jadi langkah di `/agyswap-ship` (badge diperbarui di commit rilis), jadi cukup dicatat.

## Tindak lanjut (2026-10-06, atas perintah user)

- **Important 1:**
  - `_secret_tool` mengubah `TimeoutExpired` menjadi `SwapError("keyring did not answer within 30s (locked?) …")`.
  - `_run` di TUI menangkap `Exception` dan hanya menampilkan `failed: <Jenis>`.
  - Test: `test_secret_tool_timeout_is_a_swap_error` dan `test_tui_action_error_does_not_close_the_app`. Yang kedua juga meng-assert isi pesan exception tidak tampil di notifikasi.
- **Important 2:**
  - `action_refresh` dan `_run` menyusun pesan di dalam `except`, lalu memanggil UI di luarnya. Exception asal tidak lagi terbawa sebagai `__context__`; ini diverifikasi dengan membaca kode, karena tidak ada test yang memicu `call_from_thread` gagal.
  - `collect_usage.one` menangkap `Exception` sebagai `unexpected error: <Jenis>`. Test: `test_unexpected_usage_error_stays_on_its_row`.
- Ketiga test merah dulu, lalu hijau. Ruff lolos, `pytest` 28 passed.
- Suggestion tetap terbuka di `TODO.md`.

## FYI

- Email author `rasvanjaya21@gmail.com` akan tampil di metadata PyPI. Ini sudah diputuskan sebagai identitas publik.
- Temuan lama yang tetap berlaku ada di `TODO.md`, bagian "Temuan ship".
