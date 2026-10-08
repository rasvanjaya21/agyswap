# Test

Ditulis lewat `/agyswap-test` pada 2026-10-06, diperbarui 2026-10-08 setelah build dan review rilis v0.2.0. Suite: `uv run pytest -q` → **94 passed**.

Coverage diukur ad hoc dengan `uv run --with coverage coverage run -m pytest`, tanpa menambah dependency ke `pyproject.toml`:

| File | Statement | Tercakup | Sebelumnya (v0.1.0) |
| ---- | --------- | -------- | ------------------- |
| `src/agyswap/cli.py` | 587 | 97% | 88% |
| `src/agyswap/usage.py` | 132 | 89% | 76% |
| `src/agyswap/tui.py` | 109 | 96% (Textual pilot) | 79% |
| `src/agyswap/__init__.py` | 5 | 60% | sebagian |
| **Total** | 833 | **95%** | 82% |

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

### Perbaikan temuan review dan ship (2026-10-08)

| Test | Membuktikan |
| ---- | ----------- |
| `test_list_exits_1_when_every_account_fails` | `list` exit 1 kalau semua akun error, 0 kalau ada yang terbaca |
| `test_corrupt_store_is_a_swap_error` | `accounts.json` rusak → pesan error, bukan traceback |
| `test_keyring_read_failure_is_not_signed_out` | `secret-tool lookup` dengan stderr → `SwapError`; exit 1 tanpa stderr → tidak login |
| `test_save_store_leaves_no_temp_file` | tulis atomik tidak meninggalkan file temp, mode 0600 |
| `test_locked_store_is_exclusive` | `flock` membuat pemegang kedua menunggu |
| `test_add_slot_zero_is_rejected` | `--slot 0` ditolak |
| `test_usage_uses_live_token_for_active_account` | baris akun aktif memakai token keyring |
| `test_usage_merge_skips_older_or_foreign_tokens` | merge menolak token yang lebih lama atau milik akun lain, dan store tidak ditulis ulang tanpa perubahan |
| `test_usage_catches_malformed_token_errors` | `KeyError`/`ValueError` menjadi error baris biasa |
| `test_invalid_grant_says_token_revoked` | `invalid_grant` → "token revoked" |
| `test_quota_429_is_named` | 429 dari endpoint kuota punya pesan sendiri |
| `test_requests_never_follow_redirects` | redirect ditolak, `Authorization` tidak ikut ke host lain |
| `test_tui_targets_accounts_by_email_and_escapes_markup` | aksi TUI memakai email; teks `[` tidak membuat app crash |

### Gelombang v0.2.0

| Test | Membuktikan |
| ---- | ----------- |
| `test_alias_set_clear_and_target` | alias set/clear; tolak bentrok, angka, `@`; target lewat alias di `switch` dan `remove` |
| `test_account_text_shows_alias` | kartu menampilkan `email (alias)` |
| `test_rotation_skips_disabled_accounts` | rotasi melewati akun disabled, switch eksplisit ke akun disabled ditolak, semua disabled → exit 1, `enable` |
| `test_usage_skips_disabled_accounts` | akun disabled tidak di-fetch; kartu `disabled: manual` tanpa bar |
| `test_tui_x_toggles_disable_by_email` | tombol `x` memanggil disable/enable dengan email (dibuktikan dengan mutasi) |
| `test_revoked_token_quarantines_account` | `invalid_grant` → `disabled_reason: token revoked` |
| `test_quarantine_skips_token_replaced_during_fetch` | token yang di-`add` ulang di tengah fetch tidak dikarantina |
| `test_add_clears_revoked_mark_but_keeps_alias_and_manual` | `add` ulang menghapus `token revoked`, mempertahankan alias dan `manual` |
| `test_usage_cache_fills_failed_fetch` | cache 0600 tanpa token; fetch gagal memakai cache + `stale`; email yang dihapus dibuang |
| `test_corrupt_usage_cache_is_ignored`, `test_malformed_cache_entry_is_not_shown` | cache rusak tidak membuat refresh gagal |
| `test_rate_limited_reads_retry_after` | `Retry-After` detik, tanggal HTTP, tidak ada, dan tidak valid |
| `test_rate_limited_account_is_not_fetched_until_retry_at` | tidak ada request sebelum `retry_at`, ada lagi sesudahnya |
| `test_pick_account_strategies` | `best`/`next-available`: threshold, disabled, aktif, cache ≤ 30 menit, seri ke slot terkecil, wrap-around |
| `test_switch_strategy_switches_to_picked_account`, `test_switch_strategy_rejects_target`, `test_switch_strategy_refuses_while_agy_runs` | `switch --strategy` end-to-end, `<target>` + `--strategy` → exit 2, tolak sebelum fetch saat agy berjalan |
| `test_auto_*` (6 test) | no-op di bawah threshold, switch di atasnya, tanpa kandidat, kuota tidak terbaca, agy berjalan, login belum tersimpan (diselamatkan, dan tidak ditinggalkan kalau kuotanya masih cukup) |
| `test_json_output_for_list_status_switch_auto`, `test_list_json_on_empty_store` | bentuk JSON, error sebagai JSON, tidak ada substring token |
| `test_export_import_roundtrip`, `test_import_rejects_whole_file_on_bad_entry`, `test_import_rejects_unreadable_or_foreign_files`, `test_import_drops_alias_taken_by_another_account` | export 0600 tanpa menimpa, token keyring untuk akun aktif, skip/`--force`, validasi seluruh file, alias bentrok dibuang, keyring tidak ditulis |
| `test_fresh_token_refreshes_and_skips_rejected_client`, `test_fresh_token_fails_when_no_client_is_accepted` | refresh sukses (access/id token baru, refresh token tetap), `invalid_client` mencoba secret berikutnya, token yang masih valid tidak di-refresh |
| `test_switch_to_active_account_is_a_no_op` | switch ke akun aktif tidak menulis keyring |
| `test_tui_remove_confirms_and_targets_email` | modal remove: `n` batal, `y` menghapus lewat email |
| `test_threshold_must_be_a_percentage` | `--threshold` hanya 0 < x ≤ 100 |

Mutasi yang diperiksa (mutan harus membuat test merah): token pengganti di karantina, guard `retry_at`, prune cache, threshold di `pick_account`, `O_EXCL`/0600 di export, cek agy berjalan di strategy, fallback `invalid_client`, `cmd_add` di `auto`. Semuanya mati. `test_switch_strategy_refuses_while_agy_runs` awalnya lolos walau cek dihapus (error fetch ditelan jadi baris), dan `test_auto_saves_unstored_live_login_first` awalnya tidak menyentuh jalur "belum tersimpan"; keduanya diperbaiki.

### Review rilis v0.2.0

Test reproduksi untuk temuan review (merah dulu) dan test yang mematikan mutan yang hidup. Rinciannya per temuan ada di `architecture/REVIEW.md`: `test_auto_skips_account_revoked_in_the_same_run`, `test_auto_leaves_a_disabled_active_account`, `test_retry_after_is_clamped`, `test_import_rejects_malformed_entries`, `test_import_drops_invalid_alias_and_keeps_own_alias_on_force`, `test_list_exit_code_ignores_disabled_accounts`, `test_export_file_errors_are_swap_errors`, `test_switch_rejects_flags_that_would_be_ignored`, `test_old_cache_is_not_used_to_pick`, `test_agy_running_ignores_only_the_bg_updater`, `test_add_slot_move_keeps_alias_and_disable`, `test_threshold_is_strict`, `test_auto_refuses_before_saving_or_fetching_while_agy_runs`, `test_auto_json_reports_saved_slot_after_switch`, `test_list_json_marks_stale_and_disabled_reason`, `test_cache_survives_while_account_is_disabled`, `test_switch_to_disabled_current_account_is_already_on`, `test_alias_can_change_case_on_same_account`, `test_usage_refresh_never_writes_the_keyring`.

## Jalur yang belum dites otomatis

Diurutkan dari risiko tertinggi:

- **`usage._scan_client_secrets`**: binary agy tidak ditemukan atau tidak berisi secret (dipalsukan di semua test). Dicek manual: dua secret terbaca dari agy 1.3.1.
- **`fresh_token` error lain:** HTTP selain `invalid_client`/`invalid_grant` dan `URLError` saat refresh.
- **Pembungkus `secret-tool` (`write_token` gagal)**: hanya timeout dan lookup yang dites.
- **`cmd_status` teks**, pesan `No accounts stored` di `switch`, dan `tui` lewat `main` (dispatch).
- **TUI:** `enter` (on_list_view_selected) dan `a` hanya lewat jalur `_run` yang sama dengan `s`.

## Cek manual

Sudah dilakukan (agent, store sementara, akun sungguhan, hash keyring tidak berubah): `add`, `alias`, `list`, `list` dengan jaringan diputus (penanda `stale`), `list --json`, `auto --json` (satu akun, 58% → no-op).

Menunggu user:

- `agyswap auto` dengan dua akun sungguhan saat satu akun ≥ 90%, lalu `agy` masuk sebagai akun lain.
- Saat kuota 5h sebuah akun benar-benar habis: kabari agent untuk probe read-only `retrieveUserQuotaSummary` (`architecture/OBSERVE.md`).
