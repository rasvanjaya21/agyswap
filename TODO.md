# TODO

Hanya yang masih rusak atau belum diputuskan. Rencana kerja masuk `architecture/PLAN.md`.

## Rilis

- Repo GitHub `rasvanjaya21/agyswap` masih **private**. User berencana menjadikannya public sebelum rilis. Selama private, link Homepage/Repository/Issues di PyPI dan instruksi `uv tool install git+https://github.com/rasvanjaya21/agyswap` di `README.md` tidak bisa dipakai orang lain.
- Proyek `agyswap` belum ada di PyPI (`https://pypi.org/pypi/agyswap/json` masih 404 per 2026-10-06). Akun PyPI user sudah ada, tapi pending publisher (owner `rasvanjaya21`, repo `agyswap`, workflow `publish.yml`, environment `pypi`) dan environment `pypi` di GitHub belum terkonfirmasi dibuat (lihat `CONTRIBUTING.md`, bagian Releasing).
- Banner di `README.md` memakai path relatif (`.github/assets/banner.webp`), sehingga tidak tampil di halaman PyPI. Ganti ke URL `raw.githubusercontent.com` setelah repo public. Badge `pip` dan `build` juga baru tampil setelah repo public dan rilis pertama terbit.
- Deskripsi di `pyproject.toml` dan `README.md` menyebut auto rate-limit rotation dan parallel sessions, padahal keduanya belum ada. Dipertahankan atas permintaan user sebagai target; perlu dicek ulang sebelum rilis.

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
