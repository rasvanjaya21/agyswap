Cakupan: **review rilis**, semua perubahan sejak tag `v0.1.0` (commit `b5b5111`, `01c5bfe`, ditambah working tree yang belum di-commit): `src/agyswap/{cli,usage,tui}.py`, `tests/test_swap.py`, `pyproject.toml`, `README.md`, `.github/workflows/`.

# Review rilis v0.2.0

Ditulis lewat `/agyswap-review` pada 2026-10-08. Tiga reviewer berjalan paralel (`code-reviewer`, `security-auditor`, `test-engineer`). Agent utama memverifikasi setiap temuan Critical, Important, dan Medium dengan test reproduksi yang merah dulu, lalu memperbaikinya.

**Verdict: Approve setelah perbaikan.**
- Tidak ada temuan Critical.
- Tidak ada jalur yang menghilangkan token, menimpa slot akun lain, atau menulis keyring di luar `switch_account`.
- `git grep -n -E 'GOCSPX-[A-Za-z0-9_-]{20,}'` kosong.
- Wheel hanya berisi `agyswap/` dan dist-info. Sdist tanpa `accounts.json`, `.venv`, `docs/`, atau `skills/`.

Suite: 75 → **94 passed**. `ruff check`, `ruff format --check`, dan `uv build` lolos.

## Critical

Tidak ada.

## Important (diperbaiki)

1. **`auto` dan `switch --strategy` gagal, bukan melewati, akun yang token-nya dicabut di putaran yang sama** (`src/agyswap/cli.py`, `collect_usage`).
   - **Penyebab:** baris itu tetap `disabled: false` dan diisi pools dari cache, sehingga `pick_account` memilihnya. Setelah itu `switch_account` menolak karena store sudah menandainya `token revoked`.
   - **Perbaikan:** baris yang dikarantina di merge ikut ditandai `disabled`.
   - **Test:** `test_auto_skips_account_revoked_in_the_same_run` (merah dengan `Account 2 is disabled (token revoked)`).
2. **`auto` tidak pernah meninggalkan akun aktif yang disabled**, termasuk yang dikarantina (`cmd_auto`).
   - **Penyebab:** akun disabled tidak di-fetch, sehingga `_readable` false dan `auto` keluar dengan "Cannot read the quota". Akibatnya `auto` selalu menolak setelah token akun aktif dicabut.
   - **Perbaikan:** akun aktif yang disabled langsung diganti lewat strategy.
   - **Test:** `test_auto_leaves_a_disabled_active_account`.

## Medium / Suggestion dari security dan code review (diperbaiki)

3. **`Retry-After` yang ekstrem atau tidak valid** (`src/agyswap/usage.py`, `_retry_after`).
   - **Masalah:**
     - `99999999999999999999` membuat `OverflowError` di `timedelta`.
     - `²` membuat `ValueError`.
     - Tanggal tanpa zona waktu membuat `TypeError`.
     - Tanggal tahun 9999 memblokir fetch selama ribuan tahun.
   - **Perbaikan:** nilai dibatasi ke 0–`MAX_RETRY_AFTER` (3600 detik), tanggal naive dianggap UTC, dan nilai tidak valid jatuh ke 300.
   - **Test:** `test_retry_after_is_clamped`.
4. **Validasi `import`** (`_valid_entry`).
   - **Masalah:**
     - Token tanpa `token.refresh_token` atau `id_token` lolos validasi, lalu ditulis ke keyring saat switch.
     - `"disabled": "no"` dihitung sebagai disabled.
     - Email yang berisi escape terminal (OSC) dicetak apa adanya.
     - File `version: 2` diterima.
   - **Perbaikan:** keempatnya ditolak sebelum ada yang ditulis.
   - **Batas yang tersisa:** tanda tangan `id_token` tetap tidak bisa diverifikasi. README dan help `import` sekarang menyebut "hanya impor file yang kamu ekspor sendiri".
   - **Test:** `test_import_rejects_malformed_entries`, `test_import_drops_invalid_alias_and_keeps_own_alias_on_force`.
5. **`export`.**
   - **Masalah:** `--force` menghapus file lama sebelum menulis yang baru. Path berupa folder, atau folder induk yang tidak ada, menghasilkan traceback. Tulis yang gagal meninggalkan file token setengah jadi.
   - **Perbaikan:** file 0600 lengkap ditulis lewat `mkstemp` dan `fsync`, lalu dipindah dengan `os.replace` (`--force`) atau `os.link` (yang menolak nama yang sudah ada, termasuk symlink). `OSError` menjadi `Cannot write <path>: <tipe>`, dan file temp selalu dihapus.
   - **Test:** `test_export_file_errors_are_swap_errors`.
6. **Exit code `list` menghitung akun disabled sebagai terbaca.** Sekarang exit 1 kalau semua akun yang enabled error.
   - **Test:** `test_list_exit_code_ignores_disabled_accounts`.
7. **Flag yang diam-diam diabaikan.** `switch --strategy … --force` dan `switch <target> --threshold N` sekarang exit 2.
   - **Test:** `test_switch_rejects_flags_that_would_be_ignored`.
8. **Karantina akun aktif membandingkan token store, bukan token keyring yang ditolak.** Perilakunya setara karena refresh token tidak dirotasi (`OBSERVE.md`). Alasannya sekarang tertulis di komentar.

## Celah test dari test-engineer (ditutup)

52 mutan dijalankan, dan 22 hidup. Mutan yang menyangkut perilaku sekarang dimatikan oleh test baru (dicek ulang satu per satu: semuanya membuat test merah):

| Mutan | Test |
| ----- | ---- |
| umur cache dipaksa `0` | `test_old_cache_is_not_used_to_pick` |
| `<` jadi `<=` di `pick_account` dan `auto` | `test_threshold_is_strict` |
| `agy_running` menghitung `--bg-updater` atau selalu `False` | `test_agy_running_ignores_only_the_bg_updater` |
| `add --slot` membuang alias dan disable saat memindah akun | `test_add_slot_move_keeps_alias_and_disable` |
| guard agy di `auto` dihapus (sebelumnya hanya tertangkap belakangan oleh `switch_account`) | `test_auto_refuses_before_saving_or_fetching_while_agy_runs` |
| `saved_slot` hilang setelah switch | `test_auto_json_reports_saved_slot_after_switch` |
| `stale` selalu `false` atau `disabled_reason` hilang di JSON | `test_list_json_marks_stale_and_disabled_reason` |
| cache akun disabled ditimpa kosong | `test_cache_survives_while_account_is_disabled` |
| `markup=True` di notifikasi TUI | `test_tui_targets_accounts_by_email_and_escapes_markup` (sekarang memeriksa `Notification.markup`; versi lama hanya membaca `message`, jadi lolos untuk alasan yang salah) |
| invariant "refresh tidak menulis keyring" | `test_usage_refresh_never_writes_the_keyring` |
| switch ke akun aktif yang disabled, alias ganti huruf besar | `test_switch_to_disabled_current_account_is_already_on`, `test_alias_can_change_case_on_same_account` |

Mutan yang tetap hidup tetapi tidak mengubah perilaku saat ini:
- `find-alias-first` dan `export-no-filter`: tidak berefek selama alias valid dan store hanya berisi field yang dikenal.
- `backoff-ago-59`: hanya kosmetik pembulatan menit.

## Tidak diperbaiki (masuk `TODO.md`)

- **[Low] `~/.agyswap` yang sudah ada tidak dikencangkan ke 0700** (`mkdir(exist_ok=True)`). File di dalamnya 0600, tetapi folder bersama (`AGYSWAP_HOME`) bisa di-list atau diganti isinya oleh user lain.
- **[Low] `hatchling>=1.27,<2` tidak di-pin persis**; uv.lock tidak mencakup build backend.
- **[Low] Environment `pypi` tanpa required reviewers.** Baru bisa diaktifkan setelah repo public (sudah ada di `TODO.md`).
- **Pertanyaan:** perilaku `auto` saat tidak ada yang login. Sekarang `auto` langsung switch ke akun terbaik. Spec belum menyebutnya.

## Pengecekan yang bersih

- **Keyring:** hanya `switch_account` yang menulis, dan semua mutasi store lewat `locked_store()`.
- **Fetch dan merge:** fetch berjalan tanpa lock, lalu di-merge ke pembacaan baru (email sama, expiry lebih baru, karantina hanya untuk token yang sama).
- **TUI:** semua aksi lewat thread worker, target lewat email, error tampil tanpa markup atau hanya tipenya, dan tidak ada panggilan UI di dalam `except`.
- **Jaringan:** timeout 20 detik, User-Agent `antigravity`, redirect ditolak, dan `HTTPError`/`URLError` dipetakan.
- **File:** `usage.json` tanpa token. `--json` tanpa field token.
- **Workflow:** action di-pin ke SHA, `id-token: write` hanya di job publish yang tidak menjalankan kode proyek, dan `persist-credentials: false`.
- **Dependency** (rich 15.0.0, textual 8.2.8, pygments 2.21.0, markdown-it-py 4.2.0): tidak ada CVE yang diketahui. Dicek tanpa jaringan.
- **Dokumen:** tidak ada klaim README atau AGENTS.md yang bertentangan dengan kode.

## Untuk rilis

`pyproject.toml` masih `0.1.0`. `/agyswap-ship` harus menaikkannya ke `0.2.0` sebelum tag dibuat (`publish.yml` menolak tag yang tidak cocok, dan PyPI menolak versi yang sudah ada).
