# TODO

Hanya yang masih rusak atau belum diputuskan. Rencana kerja masuk `architecture/PLAN.md`.

## Temuan review rilis (`architecture/REVIEW.md`)

- TUI remove/switch memakai nomor slot dari baris lama (`src/agyswap/tui.py:174`, `:190`). Kalau slot itu sempat dihapus lalu diisi akun lain dari terminal lain, `d` menghapus akun yang salah. Perbaikan: kirim `row["email"]`.
- `notify` dan label `Confirm` di TUI tidak di-escape (`src/agyswap/tui.py:165`, `:193`). Teks `[` dari luar (misalnya stderr `secret-tool`) bisa membuat app crash. Perbaikan: `escape()`.
- `agyswap list` mengembalikan exit 0 walaupun semua akun error (`src/agyswap/cli.py:234`).
- Mutasi yang lolos: guard merge `collect_usage`, token live untuk akun aktif, `flock`, `--slot 0`, `invalid_grant`, catch `KeyError`/`ValueError`.
- `hatchling` tidak di-pin (`pyproject.toml:36`).
- Environment `pypi` sudah dibatasi ke tag `v*`. Required reviewers dan ruleset proteksi tag `v*` tidak tersedia untuk repo private di GitHub Free; aktifkan setelah repo public.

## Temuan ship (tidak memblokir)

- `publish.yml`: action belum di-pin ke SHA. `id-token: write` dan `contents: write` ada di satu job bersama test. `ci.yml` belum punya `permissions: contents: read` dan `persist-credentials: false`.
- Switch, add, dan remove di TUI berjalan di thread UI (`src/agyswap/tui.py:157-193`), sehingga keyring yang terkunci membekukan dashboard.
- Refresh pertama bisa membaca binary agy (~210 MB) sampai 8 kali paralel (`usage.py:49`, `cli.py:170`).
- `save_store` (`cli.py:56`) tanpa `fsync`, dengan nama temp yang mudah ditebak dan tanpa `O_EXCL`/`O_NOFOLLOW`. `.lock` dibuka dengan `"w"`.
- `accounts.json` yang rusak menghasilkan traceback `JSONDecodeError`, bukan pesan error.
- Lookup `secret-tool` yang gagal dianggap "tidak login" (`cli.py:77`).
- Header `Authorization` ikut terkirim saat redirect (`usage.py:70`, teoretis).
- `collect_usage` menulis ulang store setiap refresh walaupun tidak ada perubahan (`cli.py:182`).

## Rilis

- Repo GitHub `rasvanjaya21/agyswap` masih **private**. User berencana menjadikannya public sebelum rilis. Selama private, link Homepage/Repository/Issues di PyPI dan instruksi `uv tool install git+https://github.com/rasvanjaya21/agyswap` di `README.md` tidak bisa dipakai orang lain.
- Nama paket PyPI `agyswap-cli` (command tetap `agyswap`): `agyswap` ditolak PyPI karena "too similar" dengan proyek `agy-swap` yang sudah ada. Pending publisher `agyswap-cli` sudah didaftarkan user (owner `rasvanjaya21`, repo `agyswap`, workflow `publish.yml`, environment `pypi`). Nama baru benar-benar terdaftar saat publish pertama berhasil. Environment `pypi` di GitHub sudah dibuat (2026-10-06).
- Banner di `README.md` memakai path relatif (`.github/assets/banner.webp`), sehingga tidak tampil di halaman PyPI. Ganti ke URL `raw.githubusercontent.com` setelah repo public. Badge `pip` dan `build` juga baru tampil setelah repo public dan rilis pertama terbit.

## Fitur yang belum ada

- **Usage tanpa cache dan backoff.** `collect_usage` (`src/agyswap/cli.py:147`) mengambil kuota semua akun setiap refresh, tanpa cache dan tanpa menangani 429/`Retry-After`.
- **`auto` belum ada**: auto-switch saat kuota mendekati batas, dengan threshold, cooldown, dan strategy. Kuota 5h + mingguan sudah tersedia lewat `usage.fetch_pools` (`retrieveUserQuotaSummary`), dan switch hanya efektif di antara sesi agy (agy membaca keyring sekali saat start). Respons saat bucket benar-benar habis belum terobservasi.
- **Alias, `disable`/`enable`, dan `switch --strategy best|next-available`** belum ada. Rotasi bare `switch` belum bisa melewati akun tertentu.
- **`--json`** untuk `list`, `status`, dan `switch` belum ada.
- **`export`/`import`** dan **layar watch** di TUI belum ada.
- **Error kuota tidak dibedakan**: 429 ditampilkan sebagai HTTP code biasa (`src/agyswap/usage.py:122`), dan akun dengan refresh token mati belum dikarantina.

## Platform

- Hanya Linux (`secret-tool`, `fcntl`, `pgrep`). Keychain macOS dan Credential Manager Windows belum ada.
- Fallback file token agy belum didukung (path belum terobservasi, lihat `architecture/OBSERVE.md`).
