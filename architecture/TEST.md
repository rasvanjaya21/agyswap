# Test

Ditulis lewat `/agyswap-test` pada 2026-10-06 dan diperbarui di `/agyswap-prepare` setelah review rilis v0.1.0. Suite: `uv run pytest -q` → **28 passed**.

Coverage diukur ad hoc dengan `uv run --with coverage coverage run --source=src/agyswap -m pytest`, tanpa menambah dependency ke `pyproject.toml`:

| File | Statement | Tercakup | Sebelumnya |
| ---- | --------- | -------- | ---------- |
| `src/agyswap/cli.py` | 266 | 88% | 85% |
| `src/agyswap/usage.py` | 101 | 76% | 58% |
| `src/agyswap/tui.py` | 105 | 79% (Textual pilot) | 0% |
| `src/agyswap/__init__.py`, `__main__.py` | 8 | sebagian | sebagian |
| **Total** | 480 | **82%** | 61% |

## Apa yang dibuktikan setiap test

Semua test memakai keyring palsu, store di `tmp_path` (`AGYSWAP_HOME`), dan jaringan palsu. Tidak ada yang menyentuh keyring asli, jaringan, atau `~/.agyswap/`.

### Store, switch, remove

| Test | Membuktikan |
| ---- | ----------- |
| `test_switch_roundtrip` | add dua akun, `switch` rotasi dan per email (case-insensitive), token hasil refresh agy disalin ke slot sebelum switch, target tidak dikenal ditolak, `remove --yes`, mode file store `0600` |
| `test_switch_refuses_while_running` | switch ditolak selama ada proses agy selain updater |
| `test_switch_saves_unstored_live_login_first` | login live yang belum disimpan diselamatkan ke slot baru sebelum keyring ditimpa |
| `test_add_slot_never_overwrites_other_account` | `--slot` tidak menimpa akun lain; akun yang sama dipindah |
| `test_usage_refresh_does_not_undo_concurrent_remove` | refresh usage tidak membatalkan `remove` yang terjadi bersamaan, dan token yang lebih baru tetap digabung |
| `test_ignore_running_overrides_running_agy_but_force_does_not` | saat agy berjalan: tanpa flag dan `--force` ditolak, `--ignore-running` berhasil |
| `test_force_skips_syncing_the_live_token` | `--force` tidak menyalin token live ke slotnya, dan tidak menyimpan login live sebagai slot duplikat (regresi bug yang ditemukan saat build) |
| `test_force_still_saves_an_unstored_login` | `--force` tetap menyelamatkan login yang belum disimpan (invariant) |

### CLI

| Test | Membuktikan |
| ---- | ----------- |
| `test_remove_asks_and_cancels_on_no` | prompt `Remove account 1 (a@x.com)? [y/N] `; `n` → `Cancelled`, akun tetap ada |
| `test_remove_warns_for_active_account_and_removes_on_yes` | peringatan "currently active" di stderr; `y` menghapus |
| `test_remove_without_tty_needs_yes` | tanpa TTY: tidak pernah prompt, exit 1 tanpa `--yes`; `--yes` menghapus |
| `test_remove_enter_defaults_to_no` | Enter (jawaban kosong) berarti "tidak": `Cancelled`, akun tetap ada |
| `test_remove_ctrl_d_or_ctrl_c_cancels` | Ctrl-D dan Ctrl-C di prompt berarti "tidak", tanpa traceback |
| `test_bare_agyswap_without_tty_exits_2` | bare `agyswap` non-TTY → exit 2, `no command given` |
| `test_email_of_garbage` | token rusak atau kosong tidak membuat crash |

### Kuota dan render

| Test | Membuktikan |
| ---- | ----------- |
| `test_fetch_pools_reads_5h_and_weekly_windows` | `retrieveUserQuotaSummary` di host `daily-cloudcode-pa`: urutan grup dan window, nama grup, `used`, bucket penuh tanpa reset, `remainingFraction` hilang dianggap habis |
| `test_fetch_pools_maps_http_errors` | HTTP error menjadi `UsageError` dengan pesan `HTTP <code>` |
| `test_account_text_groups_5h_and_weekly` | nama grup sekali, kolom window sejajar, reset dalam jam dan hari, bucket penuh tanpa hitung mundur |
| `test_account_text_full_bucket_row_has_no_trailing_space` | baris bucket penuh tanpa spasi di ujung (menangkap mutasi `if p.reset:` → `if True:`) |
| `test_account_text_widens_group_column_for_long_names` | nama grup 20 karakter tidak menggeser kolom window, dan tetap berjarak dua spasi darinya |

Test regresi untuk tiga temuan Critical lama, kuota per window, dan bug duplikat slot `--force` terbukti merah terhadap kode lama sebelum diperbaiki (`architecture/BUILD.md`). Dua test hijau sejak awal karena menjaga perilaku yang sudah ada: spasi di ujung, yang dibuktikan lewat mutasi, dan `--force` yang tetap menyelamatkan login.

### Jalur error dan TUI (dari ship dan review rilis v0.1.0)

| Test | Membuktikan |
| ---- | ----------- |
| `test_dropped_connection_becomes_a_row_error` | `TimeoutError`, `ConnectionResetError`, `RemoteDisconnected`, dan `IncompleteRead` saat membaca respons menjadi `network error: <Jenis>` di baris akun, bukan traceback |
| `test_post_keeps_http_errors_for_callers` | `HTTPError` dari `urlopen` tetap sampai ke pemanggil, sehingga `HTTP <code>` (dan cabang `invalid_client`/`invalid_grant`) tetap bekerja |
| `test_unexpected_usage_error_stays_on_its_row` | error tak terduga di satu akun hanya menjadi `unexpected error: <Jenis>` di barisnya |
| `test_secret_tool_timeout_is_a_swap_error` | keyring yang tidak menjawab 30 detik menjadi `SwapError` dengan langkah perbaikan |
| `test_tui_survives_refresh_on_empty_store` | refresh berulang pada store kosong tidak memicu `DuplicateIds` |
| `test_tui_shows_refresh_error_instead_of_exiting` | `SwapError` saat refresh tampil di status line, app tetap jalan |
| `test_tui_unexpected_refresh_error_shows_only_its_type` | error lain saat refresh hanya menampilkan jenisnya, tanpa isi pesan |
| `test_tui_action_error_does_not_close_the_app` | error di aksi `s` hanya menampilkan jenisnya di notifikasi, app tetap jalan |

## Jalur yang belum dites otomatis

Ini celah coverage, diurutkan dari risiko tertinggi. Mutasi yang lolos tercatat di `TODO.md`.

- **Guard merge di `collect_usage`** (cek email, cek expiry lebih baru) dan pemakaian token live untuk baris akun aktif.
- **`usage.fresh_token`**: `invalid_client` lalu mencoba secret berikutnya, `invalid_grant` menjadi "token revoked", dan refresh sukses yang dilanjutkan ke `fetch_pools`.
- **`flock` di `locked_store`**.
- **`usage._agy_client_secrets`**: binary agy tidak ditemukan, atau tidak berisi secret.
- **`cmd_add --slot 0`**, `cmd_switch` tanpa akun, switch ke akun yang sedang aktif, `cmd_list` dan `cmd_status`, serta dispatch `main`.
- **TUI:** modal `Confirm`, aksi `a` dan `d`, dan render baris akun.
- **Pembungkus `secret-tool` dan `pgrep`:** hanya jalur timeout yang dites. Sisanya bisa dites dengan `subprocess.run` palsu.

## Cek manual

Semua cek manual yang direncanakan sudah dilakukan user pada 2026-10-06:

- switch dua akun tanpa login ulang,
- kuota 5 jam dan mingguan di TUI cocok dengan `/quota` di agy (termasuk akun yang tidak aktif),
- prompt `remove` di terminal sungguhan.

Tidak ada cek manual yang menunggu.
