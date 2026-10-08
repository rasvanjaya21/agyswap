# TODO

Hanya yang masih rusak atau belum diputuskan. Rencana kerja masuk `architecture/PLAN.md`.

## Rilis

- **Repo GitHub `rasvanjaya21/agyswap` masih private** (dikerjakan user). Selama private, link di sidebar PyPI, badge `build`, banner (`raw.githubusercontent.com`), dan link `TODO.md`/`architecture/` di `README.md` memberi 404 untuk publik.
- Perbaikan halaman PyPI (banner absolut, link absolut, badge versi dihapus, license PEP 639, link Changelog) ada di working tree dan baru tampil di PyPI lewat rilis 0.2.0.
- Environment `pypi`: required reviewers dan ruleset proteksi tag `v*` tidak tersedia untuk repo private di GitHub Free; aktifkan setelah repo public.

## Temuan review rilis v0.2.0 (`architecture/REVIEW.md`)

- `~/.agyswap` (atau `AGYSWAP_HOME`) yang sudah ada tidak dikencangkan ke 0700: `mkdir(exist_ok=True)` tidak mengubah mode folder yang sudah ada (`src/agyswap/cli.py`, `_write_private` dan `locked_store`). Perbaikan: cek `st_mode & 0o077` dan pemiliknya, lalu tolak atau `chmod 0700`.
- `hatchling>=1.27,<2` tidak di-pin persis (`pyproject.toml`); uv.lock tidak mencakup build backend.
- HTTP 403 dari endpoint kuota hanya tampil sebagai `quota request failed (HTTP 403)` (`src/agyswap/usage.py`, `fetch_pools`). Untuk akun yang diblokir Google, body-nya berisi `reason: TOS_VIOLATION` (`architecture/OBSERVE.md`). Perbaikan: tampilkan `status`/`reason` dari body error (tanpa token), misalnya `disabled by Google (TOS_VIOLATION), appeal required`, dan pertimbangkan menandai akun itu `disabled`.
- Belum diputuskan: `auto` saat tidak ada yang login langsung switch ke akun terbaik. Spec belum menyebutnya.

## Fitur yang belum ada

- **Sesi paralel per akun (`run`)** belum ada: `--gemini_dir` tidak mengisolasi token, dan path file token fallback belum terobservasi (`architecture/OBSERVE.md`).
- **Ambang `auto` belum divalidasi dengan kuota yang benar-benar habis.** Isi `retrieveUserQuotaSummary` saat bucket habis, dan respons `invalid_grant` serta `Retry-After` sungguhan, belum terobservasi; kodenya mengikuti perilaku standar.

## Platform

- Hanya Linux (`secret-tool`, `fcntl`, `pgrep`). Keychain macOS dan Credential Manager Windows belum ada.
- Fallback file token agy belum didukung (path belum terobservasi, lihat `architecture/OBSERVE.md`).
