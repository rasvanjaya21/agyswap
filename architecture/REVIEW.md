# Review: render-polish + cli-safety

Ditulis lewat `/agyswap-review` pada 2026-10-06. Yang direview adalah perubahan siklus ini (Task 1–5 di "Implementation Plan: render-polish + cli-safety", `architecture/PLAN.md`). Belum ada yang di-stage, karena baseline repo belum pernah di-commit:

- `src/agyswap/cli.py`: `account_text` (lebar kolom), `confirm_remove`, `cmd_switch(force, ignore_running)`, parser, dan `main`
- `tests/test_swap.py`: 9 test baru
- `README.md`, `AGENTS.md`, `architecture/*`, `TODO.md`

**Verdict: Approve.** Important 1 serta Suggestion 1 dan 2 sudah diperbaiki setelah review (lihat "Tindak lanjut"). Suggestion 3 dipertahankan atas keputusan user. Tidak ada temuan Critical. Tidak ada jalur yang menghilangkan token: `--force` tetap menyelamatkan login yang belum disimpan, `remove` tidak menyentuh keyring, dan semua perubahan store tetap lewat `locked_store()`.

## Verifikasi

- `uv run ruff format --check .` dan `uv run ruff check .` lolos. `uv run pytest -q`: 18 passed. `uv build` lolos.
- **Uji mutasi** (setiap mutasi dibalik, suite dijalankan, lalu file dipulihkan):

| Mutasi | Hasil |
| ------ | ----- |
| `--yes` diabaikan (`if not confirm_remove`) | tertangkap |
| cek TTY di `confirm_remove` dimatikan | tertangkap |
| peringatan akun aktif dimatikan | tertangkap |
| `--force` selalu menyalin token live | tertangkap |
| penolakan saat agy berjalan memakai `force`, bukan `ignore_running` | tertangkap |
| jawaban kosong (Enter) dianggap ya | **lolos** (Important 1) |
| `len(p.group) + 2` → `len(p.group)` di lebar kolom | **lolos** (Suggestion 1) |

- **Manual (user):** prompt `remove` di terminal, dan Enter menghasilkan `Cancelled`. Kuota dua akun di TUI cocok dengan `/quota`.
- **Pilot TUI:** `s` memanggil `cmd_switch('2', False)`, dan `d` lalu `y` memanggil `cmd_remove('2')`.

## Lima sumbu

- **Correctness:** sesuai `SPEC.md` ("Spec modul: cli-safety") dan `SPEC.md` ("Spec modul: render-polish"). Bug duplikat slot `--force` sudah tertangkap dan diperbaiki saat build. Ctrl-D di prompt tidak tertangani (Suggestion 2).
- **Readability:** `confirm_remove` pendek, satu tanggung jawab, dengan docstring yang menjelaskan alasannya. `cmd_switch` punya docstring yang menyebut batasan `--force`.
- **Architecture:** konfirmasi tetap di lapisan CLI (`main`), sementara `cmd_remove` dan modal TUI tidak berubah. Arah `tui.py` → `cli.py` → `usage.py` tetap.
- **Security:** tidak ada token yang tercetak. Scan secret bersih, kecuali teks pola di skill prepare dan `PREPARE.md`. Tidak ada `busctl`.
- **Performance:** `confirm_remove` membaca keyring satu kali hanya untuk peringatan akun aktif (Suggestion 3). Tidak ada request jaringan baru.

## Important

1. **Default `N` pada prompt `remove` tidak dijaga test** (`src/agyswap/cli.py:301`). Mutasi yang menerima jawaban kosong sebagai "ya" lolos. Akibatnya, kalau kode berubah sampai Enter menghapus akun, tidak ada test yang menangkapnya, padahal default `N` adalah pengaman utama prompt ini. **Perbaikan:** tambah test dengan `input` mengembalikan `""`, lalu assert `Cancelled` dan akun tetap ada.

## Suggestion

1. **Jarak antara nama grup panjang dan kolom window tidak dites** (`src/agyswap/cli.py:210`). Mutasi `+2` → `+0` lolos karena test hanya mengecek kolom sejajar. **Perbaikan:** di `test_account_text_widens_group_column_for_long_names`, assert `long_name + "  "` ada di baris pertama.
2. **Ctrl-D atau Ctrl-C di prompt `remove` memunculkan traceback** (`src/agyswap/cli.py:301`). `EOFError`/`KeyboardInterrupt` dari `input()` tidak ditangkap. Terverifikasi: `EOFError` uncaught, dan akun tetap ada (tidak ada data hilang). **Perbaikan:** tangkap keduanya di `confirm_remove`, perlakukan sebagai "tidak" (`Cancelled`), dan tambah test-nya.
3. **`confirm_remove` membaca keyring hanya untuk peringatan** (`src/agyswap/cli.py:299`). Kalau keyring terkunci, `remove` bisa memicu dialog unlock, padahal remove sendiri tidak butuh keyring. **Perbaikan:** biarkan seperti sekarang, atau lewati peringatan saat `read_token` gagal. Keputusan user; dicatat di `TODO.md`.

## Tindak lanjut (2026-10-06, atas persetujuan user)

- **Important 1:** `test_remove_enter_defaults_to_no`. Mutasi "jawaban kosong = ya" sekarang tertangkap.
- **Suggestion 1:** `test_account_text_widens_group_column_for_long_names` sekarang meng-assert `long_name + "  "`. Mutasi `+2` → `+0` sekarang tertangkap.
- **Suggestion 2:** `confirm_remove` menangkap `EOFError` dan `KeyboardInterrupt` sebagai "tidak" (`Cancelled`). `test_remove_ctrl_d_or_ctrl_c_cancels` merah dulu (`EOFError`), lalu hijau. Mutasi `return False` → `return True` tertangkap.
- **Suggestion 3:** dipertahankan atas keputusan user. `remove` tetap membaca keyring untuk memperingatkan akun aktif.
- Hasil: ruff lolos, `pytest` 20 passed.

## FYI

- `--force` sekarang berarti "lewati penyalinan token live", dan `--ignore-running` mengambil alih arti lama. Ini perubahan perilaku, tapi belum ada rilis (catatan rilis di `PLAN.md`).
- `test_switch_roundtrip` disesuaikan dengan `remove --yes`, karena pytest tidak punya TTY. Ini perubahan perilaku yang disengaja; tidak ada assertion yang dilonggarkan.

