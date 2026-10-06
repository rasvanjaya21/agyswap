# Ship: v0.1.0 (rilis pertama)

Ditulis lewat `/agyswap-ship` pada 2026-10-06. Tiga spesialis berjalan paralel (`code-reviewer`, `security-auditor`, `test-engineer`) terhadap seluruh paket, karena belum ada tag rilis.

## Keputusan: **NO-GO**

Satu crash Critical di TUI dan satu crash jaringan yang bisa mencetak secret ke terminal. Keduanya kecil untuk diperbaiki, tapi langsung terlihat pemakai baru. Tidak ada jalur yang menghilangkan token.

## Blocker

1. **TUI crash saat refresh dengan store kosong** (`src/agyswap/tui.py:125`, `:137`). `lv.clear()` tidak menunggu item lama terhapus, lalu `ListItem(..., id="empty")` ditambahkan lagi dengan id yang sama, sehingga muncul `DuplicateIds` dan worker refresh menutup app. Ini terjadi pada pemakai tanpa akun yang menekan `r`, setelah refresh otomatis 2 menit, atau setelah akun terakhir dihapus. Ditemukan `code-reviewer` dan direproduksi dengan Textual pilot; penyebabnya juga dicek di kode. **Perbaikan:** hapus `id="empty"` (tidak ada yang meng-query id itu), lalu tambah test pilot yang me-refresh dua kali pada store kosong.
2. **Error jaringan saat membaca respons lolos dari penanganan error** (`src/agyswap/usage.py:70`, `cli.py:160`). `urlopen` hanya membungkus error saat request dikirim ke dalam `URLError`. `TimeoutError`, `ConnectionResetError`, dan `RemoteDisconnected` saat membaca respons keluar mentah. Akibatnya `agyswap list` mencetak traceback dan TUI tertutup. Ketiga spesialis menemukannya secara terpisah, dan semuanya membuktikannya dengan test sementara. Menurut `security-auditor` (Medium), traceback Textual (`show_locals=True`) mencetak client secret lengkap dan 80 karakter refresh token ke terminal. Karena itu temuan ini diperlakukan sebagai blocker. **Perbaikan:** di `_post`, tangkap `OSError` di luar `URLError` dan ubah menjadi `UsageError(f"network error: {type(e).__name__}")`. `action_refresh` juga harus menangkap `SwapError`/`UsageError` dan menampilkannya di status line. Tambah test `_post` yang melempar `TimeoutError`.
3. **Deskripsi paket mengklaim fitur yang belum ada** (`pyproject.toml:4`, `README.md:6`). Teks "automatic rate-limit rotation" dan "parallel sessions" masuk ke halaman PyPI, padahal bagian Status di README sendiri bilang keduanya belum ada. Teks ini dipertahankan atas permintaan user dengan catatan "dicek ulang sebelum rilis". **Keputusan user:** ubah deskripsinya sekarang, atau terima sebagai risiko.

## Perbaikan yang disarankan (tidak memblokir)

| Sumber | Temuan | Lokasi |
| ------ | ------ | ------ |
| security (Medium) | Action di `publish.yml` di-pin ke tag, bukan SHA. `id-token: write` dan `contents: write` ada di satu job yang juga menjalankan test. Pin ke SHA, lalu pisahkan job `build` / `publish` / `release`. | `.github/workflows/publish.yml` |
| code | Switch, add, dan remove berjalan di thread UI, sehingga keyring yang terkunci membekukan TUI. Pindahkan ke `@work(thread=True)`. | `src/agyswap/tui.py:148-177` |
| code | Refresh pertama bisa membaca binary agy (~210 MB) sampai 8 kali bersamaan, karena `lru_cache` tidak mencegah pemanggilan paralel. Panggil `_agy_client_secrets()` sekali sebelum thread pool dimulai. | `usage.py:47-56`, `cli.py:165` |
| security, code (Low) | `save_store` tanpa `fsync`. Nama temp `accounts.tmp` mudah ditebak dan dibuka tanpa `O_EXCL`/`O_NOFOLLOW`. `.lock` dibuka dengan `"w"`. Pakai `tempfile.mkstemp` dan `fsync`, lalu buka lock dengan `O_NOFOLLOW`. | `cli.py:50-64` |
| test | `accounts.json` yang rusak menghasilkan traceback `JSONDecodeError`. | `cli.py` `load_store` |
| code | Lookup `secret-tool` yang gagal dianggap "tidak login". Belum terbukti bisa terjadi bersamaan dengan store yang berhasil. | `cli.py:77` |
| security (Low) | `ci.yml` tanpa `permissions: contents: read`, dan checkout tanpa `persist-credentials: false`. | `.github/workflows/ci.yml` |
| security (Low) | Header `Authorization` ikut terkirim saat redirect (teoretis). | `usage.py:69` |
| code | `collect_usage` menulis ulang store setiap refresh walaupun tidak ada yang berubah. | `cli.py:176` |
| test | `fresh_token` (`usage.py:79-110`) dan `tui.py` (0%) belum punya test. Cabang `fresh_token` sudah dicek benar dengan test sementara. | |
| code | Cek "`git grep -n GOCSPX` kosong" di skill ship tidak pernah bisa lolos, karena regex di `usage.py:56` dan dokumentasi ikut cocok. Ganti dengan pola secret lengkap (`GOCSPX-[A-Za-z0-9_-]{20,}`). | `skills/agyswap-ship/SKILL.md` |

## Cek sebelum GO

| Cek | Hasil |
| --- | ----- |
| `uv sync --locked` | lolos |
| `uv run ruff check .`, `ruff format --check .` | lolos (21 file) |
| `uv run pytest -q` | 20 passed |
| `uv build` | `agyswap_cli-0.1.0` wheel dan sdist |
| Isi wheel | hanya `agyswap/` dan `agyswap_cli-0.1.0.dist-info/` |
| Isi sdist | tidak ada `.venv`, `docs/`, `skills/`, `architecture/`, `graphify-out/`, `.claude/`, `.agents/`, `accounts.json` |
| Secret di repo | tidak ada nilai secret. Kecocokan `GOCSPX` hanya regex dan teks dokumentasi. |
| `pip-audit` (lock) | No known vulnerabilities |
| Versi | `pyproject.toml` 0.1.0, badge README `version-0.1.0`, `__init__` lewat `importlib.metadata` |
| agy | 1.3.0, sama dengan `architecture/OBSERVE.md` |
| Uji manual dua akun | sudah (`architecture/TEST.md`) |
| Push dan CI | **belum**: remote `master` = `5e2f7b7` (CI hijau), HEAD lokal `82927ef` masih 3 commit di depan |

## CLI dan TUI (pengganti accessibility)

Binding terlihat di footer. Pesan error `SwapError` menyebut langkah perbaikan. Pengecualian: crash pada blocker 1 dan 2 tidak menampilkan pesan, hanya traceback.

## Versi

Belum ada tag, jadi ini rilis pertama: **0.1.0** tanpa bump dan tanpa commit rilis. Semua 28 commit sejak `Initial commit` membentuk kemampuan awal:

- **Kemampuan (feat):**
  - `vcs`, `package`, `lock`, `src`, `usage`, `cli`, `tui`, `test`, `workflow`, `docs`, `mcp`, `skill`,
  - rename distribusi `agyswap-cli`: `package`, `lock`, `src`, `workflow`, `skill`.
- **Dokumentasi (docs):** `project`, `agents`, `architecture`.
- **Artefak (chore):** `graph`.

Versi akhir tetap keputusan user.

## Risiko yang diterima (setelah blocker diperbaiki)

- Repo masih private. Link di PyPI dan banner relatif README tidak tampil sampai repo public (`TODO.md`, bagian Rilis).
- Hanya Linux. `auto` dan `run` belum ada; README menyebutnya di bagian Status.

## Rencana rollback

- **Pemicu:** crash pada perintah umum, kehilangan token atau store, atau secret tercetak.
- **Langkah:**
  1. Yank `agyswap-cli==0.1.0` di PyPI (Manage project → Releases → Yank). Versi yang sudah terbit tidak bisa ditimpa atau diunggah ulang, jadi tidak dihapus.
  2. Perbaiki lewat siklus normal.
  3. Rilis `0.1.1`.
- Pemakai yang sudah memasang: `uv tool install --reinstall agyswap-cli==<versi sehat>`. `~/.agyswap/accounts.json` tidak berubah format, jadi tidak perlu migrasi.
- GitHub release `v0.1.0`: tandai sebagai bermasalah di catatan rilis. Tag tidak dihapus agent; itu keputusan user.

## Tindak lanjut (2026-10-06)

Blocker 1 dan 2 diperbaiki atas perintah user, dengan pola Prove-It (ketiga test merah dulu, lalu hijau):

- `tui.py`: `id="empty"` dihapus. `action_refresh` menangkap `SwapError` dan menampilkannya di status line, jadi app tidak tertutup.
- `usage._post`: `OSError` dan `http.client.HTTPException` selain `URLError` menjadi `UsageError("network error: <Jenis>")` dengan `from None`, sehingga tidak ada traceback dan tidak ada locals yang tercetak.
- Test baru:
  - `test_dropped_connection_becomes_a_row_error` (`TimeoutError`, `ConnectionResetError`, `RemoteDisconnected`),
  - `test_tui_survives_refresh_on_empty_store`,
  - `test_tui_shows_refresh_error_instead_of_exiting`.
- Hasil: ruff lolos, `pytest` 23 passed. Setelah tindak lanjut `/agyswap-review` (`architecture/REVIEW.md`): 25 passed.

Blocker 3 (deskripsi paket) masih menunggu keputusan user. Keputusan GO/NO-GO baru diambil di `/agyswap-ship` berikutnya.

## Hasil publish

Belum dipublikasikan (NO-GO).

## Langkah berikutnya

Fan-out reviewer dipindah dari `/agyswap-ship` ke `/agyswap-review` (keputusan user, 2026-10-06). Review rilis sekarang wajib sebelum ship.

1. ~~Blocker 3~~: diputuskan user, deskripsi diganti menjadi "Switch between multiple Antigravity CLI accounts, with a quota dashboard for every account" di `pyproject.toml` dan `README.md`.
2. Jalankan `/agyswap-review` dengan cakupan rilis (seluruh paket, karena belum ada tag). `REVIEW.md` yang sekarang hanya mereview diff perbaikan.
3. `/agyswap-prepare` → `/agyswap-commit`.
4. User menjalankan `git push` dan menunggu CI hijau.
5. Jalankan `/agyswap-ship`. Kalau GO, user menjalankan `git tag v0.1.0 && git push origin v0.1.0`.
