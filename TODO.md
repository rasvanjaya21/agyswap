# TODO

Hanya yang masih rusak atau belum diputuskan. Rencana kerja masuk `architecture/PLAN.md`.

## Temuan review rilis 0.3.0 (`architecture/REVIEW.md`)

- [Low] `_private_dir` memakai `stat`/`chmod` pada path, bukan fd: kalau `AGYSWAP_HOME` berada di bawah folder induk yang bisa ditulis user lain (tanpa sticky bit), folder bisa ditukar dengan symlink di antara cek dan tulis (`src/agyswap/cli.py`, `_private_dir`). Tidak berlaku untuk `~/.agyswap` default. Perbaikan: `os.open(d, O_RDONLY | O_DIRECTORY | O_NOFOLLOW)` lalu `fstat`/`fchmod`, dan tolak induk yang bisa ditulis grup/lainnya.
- [Low] Export ke filesystem tanpa hard link (vfat/exFAT, sebagian FUSE) gagal dengan `Cannot write …` karena langkah terakhir `os.link` (`cmd_export`). Tidak bocor, tapi export ke flashdisk tidak bisa.
- [Info] `b` dan `u` di TUI mengganti akun dengan satu tombol tanpa konfirmasi; semua invariant `switch_account` tetap berlaku.

## Fitur yang belum ada

- **Sesi paralel per akun (`run`)** belum ada: `--gemini_dir` tidak mengisolasi token, dan path file token fallback belum terobservasi (`architecture/OBSERVE.md`).
- **Respons kuota yang benar-benar habis belum terobservasi.** Ambang `auto` 90% sudah divalidasi user dengan dua akun sungguhan (2026-10-09), tapi isi `retrieveUserQuotaSummary` saat bucket habis, dan respons `invalid_grant` serta `Retry-After` sungguhan, belum terobservasi; kodenya mengikuti perilaku standar.

## Platform

- Hanya Linux (`secret-tool`, `fcntl`, `pgrep`). Keychain macOS dan Credential Manager Windows belum ada.
- Fallback file token agy belum didukung (path belum terobservasi, lihat `architecture/OBSERVE.md`).
