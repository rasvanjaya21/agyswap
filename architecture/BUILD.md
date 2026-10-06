# Build log: kuota 5 jam + mingguan

Ditulis lewat `/agyswap-build` pada 2026-10-06. Serah terima untuk Phase 2 di `architecture/PLAN.md`. Belum di-commit; commit lewat `/agyswap-commit`.

## Task 1: Ambil kuota dari `retrieveUserQuotaSummary` — selesai

- **Diimplementasikan:**
  - `src/agyswap/usage.py`: `fetch_pools` sekarang memanggil `POST https://daily-cloudcode-pa.googleapis.com/v1internal:retrieveUserQuotaSummary` (`QUOTA_URL`) dengan body `{}`. Hasilnya satu `Pool` per bucket, berurutan per grup sesuai respons, lalu `5h` sebelum `weekly` (`WINDOW_ORDER`).
  - `Pool` sekarang punya field `group`, `window`, `used`, `reset`, plus properti `label` (`"<group> <window>"`) supaya render yang ada tetap jalan.
  - Nama grup diambil dari `displayName`: akhiran "Models" dibuang dan " and " diganti "/", jadi "Gemini" dan "Claude/GPT".
  - Bucket penuh (`remainingFraction` ≥ 1) diberi `reset=None`.
  - `remainingFraction` yang hilang dianggap habis (terpakai 100%), karena respons saat bucket habis belum terobservasi.
  - Konstanta `MODELS_URL` dan pengelompokan model dari `fetchAvailableModels` dihapus.
- **Dibuktikan oleh:**
  - `tests/test_swap.py::test_fetch_pools_reads_5h_and_weekly_windows`, menggantikan `test_fetch_pools_groups_shared_buckets`. Fixture-nya memakai bentuk respons dari `architecture/OBSERVE.md`. Test ini merah dulu (URL masih `fetchAvailableModels`), lalu hijau.
  - `test_fetch_pools_maps_http_errors`, yang memastikan HTTP 403 tetap menjadi `UsageError` dengan pesan yang sama.
  - Cek manual read-only: `usage.account_usage(cli.read_token())` untuk akun aktif cocok dengan `agy -p /quota --output-format json` (terpakai dan reset sama untuk keempat bucket; bucket penuh tanpa reset, sesuai desain).
- **Hasil:** `uv run ruff format .` tanpa perubahan, `uv run ruff check .` lolos, `uv run pytest -q` 8 passed.
- **Ditunda ke Task 2:**
  - Render kartu masih memakai `label` satu baris per bucket dengan kolom 16 karakter, sehingga `Claude/GPT weekly` (17 karakter) sedikit bergeser.
  - Pengelompokan per grup dan format hari untuk reset mingguan.

## Task 2: Tampilkan 5 jam dan mingguan di `list` dan TUI — selesai

- **Diimplementasikan:** `src/agyswap/cli.py`, fungsi `account_text`:
  - Setiap grup tampil dengan nama grup tebal di baris pertamanya saja (kolom 12), lalu kolom window (`5h`/`weekly`, lebar 8), bar, persen, dan hitung mundur reset.
  - Bucket dengan `reset=None` (masih penuh) tidak menampilkan hitung mundur.
  - Reset mingguan memakai format hari (`4d 19h`) dari `_countdown` yang sudah ada.
  - TUI ikut berubah karena memakai render yang sama.
- **Dibuktikan oleh:**
  - `tests/test_swap.py::test_account_text_groups_5h_and_weekly`. Test ini merah dulu, lalu hijau. Isinya: baris header, nama grup sekali saja, kolom window sejajar antar grup, format hari dan jam, dan tanpa hitung mundur untuk bucket penuh.
  - Manual: `agyswap list` dengan store sementara untuk akun aktif menampilkan kedua grup × kedua window (reset mingguan `6d 22h`), lalu store di-`shred`.
  - Screenshot TUI headless (Textual pilot, data contoh) rapi di latar hitam dan saat kartu terpilih biru.
- **Hasil:** ruff lolos, `pytest` 9 passed.

## Task 3: Perbarui dokumen ke perilaku baru — selesai

- **Diimplementasikan:**
  - `README.md`:
    - Status: kalimat "only covers the 5-hour window" dihapus.
    - Usage: TUI menampilkan kedua grup dengan window 5 jam dan mingguan.
  - `AGENTS.md`: ringkasan auth menyatakan `usage.fetch_pools` membaca `retrieveUserQuotaSummary`, dan `fetchAvailableModels` tidak dipakai lagi.
  - `architecture/SPEC.md`:
    - Bagian Kuota memakai sumber baru.
    - Kriteria kuota mingguan dicentang.
    - Open question kuota mingguan dihapus, dan sisanya dinomori ulang.
  - `TODO.md`:
    - Butir "Kuota" dihapus.
    - Referensi error kuota pindah ke `usage.py:126`.
  - `architecture/OBSERVE.md`:
    - Baris `fetchAvailableModels` ditandai "diganti".
    - Hasil cek manual ditambahkan ke Validasi.
- **Dibuktikan oleh:** `grep -rn fetchAvailableModels README.md AGENTS.md src/` hanya menyisakan kalimat di `AGENTS.md` yang menyatakan endpoint itu tidak dipakai lagi.

## Setelah review

`Pool.label` dihapus saat `/agyswap-prepare` setelah review, karena tidak dipakai lagi sejak Task 2 (Suggestion 1 di `architecture/REVIEW.md`). Suite tetap 9 passed.

## Verifikasi akhir

`uv run ruff format --check .` dan `uv run ruff check .` lolos. `uv run pytest -q` menghasilkan 9 passed. `uv build` lolos.

## Commit

Tidak ada commit per task. Seluruh baseline repo belum pernah di-commit, jadi commit per task akan ikut membawa isi `cli.py` dan `usage.py` secara utuh. Commit dikerjakan lewat `/agyswap-commit` sesuai siklus.

## Menunggu user

Checkpoint dua akun sudah dicentang (user, 2026-10-06; lihat `architecture/OBSERVE.md`, Validasi).

---

# Build log: render-polish + cli-safety

Ditulis lewat `/agyswap-build auto` pada 2026-10-06. Serah terima untuk "Implementation Plan: render-polish + cli-safety" di `architecture/PLAN.md`, dengan spec di `architecture/SPEC.md` ("Spec modul: render-polish") dan `architecture/SPEC.md` ("Spec modul: cli-safety"). Tidak ada commit per task, dengan alasan yang sama seperti build kuota: baseline belum pernah di-commit.

## Task 1: Render tanpa spasi di ujung, kolom grup dinamis — selesai

- **Diimplementasikan:** di `cli.account_text`, `width = max(12, panjang nama grup terpanjang + 2)` dipakai untuk kolom grup.
- **Dibuktikan oleh:**
  - `test_account_text_widens_group_column_for_long_names`: merah dulu, lalu hijau.
  - `test_account_text_full_bucket_row_has_no_trailing_space`: hijau sejak awal karena guard `if p.reset:` sudah ada. Test ini dibuktikan lewat mutasi: `if True:` sekarang membuatnya merah. Sebelumnya mutasi itu lolos di `REVIEW.md`.
  - Manual: `list` dengan store sementara tidak berubah.

## Task 2: Konfirmasi `remove` dengan `--yes`/`-y` — selesai

- **Diimplementasikan:**
  - `cli.confirm_remove(target)`:
    - Tanpa TTY → `SwapError("Refusing to remove without confirmation. Pass --yes …")`, exit 1.
    - Akun aktif → `warning: account N (email) is currently active` ke stderr.
    - Prompt `Remove account N (email)? [y/N] `; hanya `y`/`yes` yang menghapus.
  - `main` menampilkan `Cancelled` (exit 0) kalau ditolak.
  - Flag `-y`/`--yes` di parser `remove`.
  - `cmd_remove` dan modal TUI tidak berubah.
- **Dibuktikan oleh:**
  - `test_remove_asks_and_cancels_on_no`, `test_remove_warns_for_active_account_and_removes_on_yes`, dan `test_remove_without_tty_needs_yes`, ketiganya merah dulu.
  - `test_switch_roundtrip` disesuaikan memakai `remove 1 --yes`, karena pytest tidak punya TTY. Ini perubahan perilaku yang disengaja, dan tidak ada assertion yang dilonggarkan.
  - Manual: `echo | agyswap remove 1` exit 1 dengan pesan penolakan, dan `agyswap remove 1 --yes` menghapus (store sementara).
- **Cek manual user (2026-10-06):** `uv run agyswap remove 1` menampilkan `Remove account 1 (<email>)? [y/N]`, dan Enter menghasilkan `Cancelled`.

## Task 3: Bare `agyswap` di luar TTY exit 2 — selesai

- **Diimplementasikan:** `parser.error("no command given — try 'agyswap --help'")`.
- **Dibuktikan oleh:** `test_bare_agyswap_without_tty_exits_2` (merah dulu), dan manual `uv run agyswap < /dev/null` exit 2.

## Task 4: arti baru `--force`, `--ignore-running` baru — selesai

- **Diimplementasikan:**
  - `cmd_switch(target, force=False, ignore_running=False)`. Penolakan saat agy berjalan sekarang hanya dilewati oleh `ignore_running`, dan pesannya menyebut `--ignore-running`.
  - `force` hanya melewati penyalinan token live ke slot akun live yang sudah tersimpan. Login yang belum disimpan tetap diselamatkan.
  - Flag `--force` (help baru) dan `--ignore-running` di parser `switch`.
- **Bug yang ditemukan saat build (Prove-It):** implementasi pertama memakai `if current and not force: … elif live_email:`. Dengan `--force`, alur jatuh ke `elif`, sehingga login live yang **sudah tersimpan** disimpan lagi ke slot baru (duplikat). Assertion `sorted(accounts) == ["1", "2"]` ditambahkan ke `test_force_skips_syncing_the_live_token` dan terbukti merah. Setelah diperbaiki dengan `if current: if not force: …`, test itu hijau.
- **Dibuktikan oleh:**
  - `test_ignore_running_overrides_running_agy_but_force_does_not` (merah dulu).
  - `test_force_skips_syncing_the_live_token` (merah dulu, termasuk regresi duplikat).
  - `test_force_still_saves_an_unstored_login`: hijau sejak awal; ini menjaga invariant.
  - Pilot TUI: `s` memanggil `cmd_switch('2', False)`, dan `d` lalu `y` memanggil `cmd_remove('2')`.

## Task 5: Dokumen — selesai

- `README.md`: `remove` bertanya (pakai `--yes` di script); `--ignore-running` dan arti `--force`.
- `AGENTS.md`, bagian Invariants: `--ignore-running`, batasan `--force`, dan konfirmasi `remove` beserta modal TUI.
- `TODO.md`: konfirmasi `remove`, arti `--force`, bare non-TTY, dan bagian "Kualitas kode" dihapus.
- `architecture/SPEC.md`: tabel perintah dan baris Commands diperbarui.

## Verifikasi akhir

`uv run ruff format --check .` (22 file) dan `uv run ruff check .` lolos. `uv run pytest -q` menghasilkan 18 passed. `uv build` lolos.

## Menunggu user


## Setelah review (render-polish + cli-safety)

Atas persetujuan user, temuan `architecture/REVIEW.md` ditindaklanjuti:

- `test_remove_enter_defaults_to_no`: menjaga default `N` (Important 1).
- `test_account_text_widens_group_column_for_long_names`: sekarang juga meng-assert jarak dua spasi setelah nama grup panjang (Suggestion 1).
- `confirm_remove` menangkap `EOFError` dan `KeyboardInterrupt` sebagai "tidak" dan mencetak baris baru (Suggestion 2). `test_remove_ctrl_d_or_ctrl_c_cancels` merah dulu, lalu hijau.
- Peringatan akun aktif tetap membaca keyring (Suggestion 3, keputusan user).

Ketiga mutasi (jawaban kosong = ya, `+2` → `+0`, dan Ctrl-D = ya) sekarang tertangkap. ruff lolos, `pytest` 20 passed.
