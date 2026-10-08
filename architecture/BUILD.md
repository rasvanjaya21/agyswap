# Build log: gelombang 2026-10-08 (v0.2.0)

Ditulis lewat `/agyswap-build auto` pada 2026-10-08, mengikuti "Implementation Plan: gelombang 2026-10-08" di `architecture/PLAN.md`. Tidak di-commit per task: working tree sudah berisi perbaikan temuan review/ship yang belum di-commit di file yang sama, jadi semuanya di-commit lewat `/agyswap-commit` per kategori.

## Task 1: Alias — selesai

- **Diimplementasikan:** `cmd_alias` (set/clear, tolak bentrok tanpa membedakan huruf besar, angka saja, dan `@` lewat `_valid_alias`); `find_slot` mencocokkan slot → email → alias; `account_text` menampilkan `email (alias)`; baris `collect_usage` membawa `alias`.
- **Dibuktikan oleh:** `test_alias_set_clear_and_target`, `test_account_text_shows_alias` (merah dulu, lalu hijau).

## Task 2: Disable/enable — selesai

- **Diimplementasikan:** `cmd_disable(target, reason="manual")`, `cmd_enable`; rotasi bare `switch` melewati akun disabled (`No enabled account to switch to.`); switch eksplisit ke akun disabled ditolak; `collect_usage` tidak mem-fetch akun disabled; `account_text` menampilkan `disabled: <alasan>` tanpa bar.
- **Dibuktikan oleh:** `test_rotation_skips_disabled_accounts`, `test_usage_skips_disabled_accounts`.

## Task 3: Tombol `x` — selesai

- **Diimplementasikan:** `Binding("x", "toggle", "Disable/Enable")` dan `action_toggle` di `tui.py`, lewat `_run` (thread worker, target email).
- **Dibuktikan oleh:** `test_tui_x_toggles_disable_by_email`. Test ini ditulis bersama kodenya, jadi dibuktikan dengan mutasi (target slot + selalu disable → test merah).

## Task 4: Karantina — selesai

- **Diimplementasikan:** `usage.TokenRevoked(UsageError)` untuk `invalid_grant`; merge `collect_usage` menandai `disabled_reason: token revoked` hanya kalau token di store sama dengan yang di-fetch. `cmd_add` sekarang **memperbarui** entri (dulu menimpa seluruhnya, sehingga alias dan tanda disable hilang setiap `add` ulang) dan menghapus tanda `token revoked`, tidak `manual`.
- **Dibuktikan oleh:** `test_revoked_token_quarantines_account`, `test_quarantine_skips_token_replaced_during_fetch`, `test_add_clears_revoked_mark_but_keeps_alias_and_manual`.

## Task 5: Cache `usage.json` — selesai

- **Diimplementasikan:** `_write_private` (dipakai `save_store` dan cache), `usage_path`, `load_usage` (cache rusak = kosong), `_update_usage_cache` di bawah lock (simpan pembacaan sukses, buang email yang tidak ada, isi baris gagal dengan cache + `stale` detik), `_ago`, penanda `(stale, <umur> ago)` di `account_text`.
- **Dibuktikan oleh:** `test_usage_cache_fills_failed_fetch`, `test_corrupt_usage_cache_is_ignored`.
- **Cek manual (agent):** store sementara dengan akun sungguhan, `list` lalu `HTTPS_PROXY=http://127.0.0.1:9 list` menampilkan angka terakhir dengan `(stale, 0m ago)`; `usage.json` mode 600; hash keyring tidak berubah.

## Task 6: Backoff 429 — selesai

- **Diimplementasikan:** `usage.RateLimited(UsageError)` dengan `retry_after` dari `Retry-After` (detik atau tanggal HTTP, default 300); `collect_usage` melewati fetch sampai `retry_at` di cache dan menampilkan `rate limited, retry in <m>`.
- **Dibuktikan oleh:** `test_rate_limited_reads_retry_after`, `test_rate_limited_account_is_not_fetched_until_retry_at`.

## Task 7: `switch --strategy` — selesai

- **Diimplementasikan:** `pick_account` murni (`best`: `max(used)` terendah, seri ke slot terkecil; `next-available`: urutan rotasi setelah akun aktif), `MAX_STALE = 30 menit`, `_readable`, `_max_used`; `switch_account` mengembalikan dict, `cmd_switch` dan `switch_message` membentuk teks (TUI tidak berubah); `cmd_switch_strategy`; `--threshold` lewat `_percent` (0–100); `<target>` + `--strategy` → exit 2.
- **Dibuktikan oleh:** `test_pick_account_strategies`, `test_switch_strategy_switches_to_picked_account`, `test_switch_strategy_rejects_target`.
- **Perubahan teks:** catatan login yang diselamatkan kini `Saved the unstored live login as account N.` (tanpa email).

## Task 8: `auto` — selesai

- **Diimplementasikan:** `cmd_auto` dan `auto_message`. Login live yang belum disimpan disimpan dulu lewat `cmd_add` (supaya kuotanya terbaca), lalu `collect_usage`, lalu no-op / switch / exit 1 sesuai spec.
- **Dibuktikan oleh:** `test_auto_stays_below_threshold`, `test_auto_switches_when_active_is_over_threshold`, `test_auto_without_candidate_or_quota_stays`, `test_auto_refuses_while_agy_runs`, `test_auto_saves_unstored_live_login_first`.
- **Ditunda ke user:** manual check dua akun sungguhan (akun ≥ 90%).

## Task 9: `--json` — selesai

- **Diimplementasikan:** `--json` di `list`, `status`, `switch`, `auto`; `row_json`, `_emit`; error sebagai `{"version": 1, "error": ...}` di stdout; `used` dibulatkan 6 desimal.
- **Dibuktikan oleh:** `test_json_output_for_list_status_switch_auto` (juga memastikan tidak ada substring token).
- **Cek manual (agent):** `list --json` dan `auto --json` dengan akun sungguhan dan store sementara; `auto` tidak switch (satu akun, di bawah threshold).

## Task 10–11: `export` / `import` — selesai

- **Diimplementasikan:** `cmd_export` (`O_CREAT|O_EXCL|O_NOFOLLOW` 0600, `--force` menghapus file lama dulu, token keyring untuk akun aktif, peringatan di stderr); `_read_export` memvalidasi seluruh file sebelum menulis; `cmd_import` (slot berikutnya, skip atau `--force` dengan slot tetap; alias yang bentrok atau tidak valid dibuang dengan pesan).
- **Dibuktikan oleh:** `test_export_import_roundtrip`, `test_import_rejects_whole_file_on_bad_entry`, `test_import_drops_alias_taken_by_another_account`.

## Task 12: Dokumen — selesai

- `README.md` (Status, Configuration, Usage: alias, disable/enable, strategy, `auto`, `--json`, cache/backoff, karantina, export/import, `add --slot`, tombol `x`), `AGENTS.md` (Layout, tombol, Invariants), `TODO.md` (sisa: `run`, validasi kuota habis), centang `SPEC.md` dan `PLAN.md`.

## Verifikasi akhir

- `uv run ruff format --check .`, `uv run ruff check .`, `uv run pytest -q` (65 passed), `uv build` lolos; wheel hanya `agyswap/` dan `agyswap_cli-*.dist-info/`.

## Menunggu user

- Review checkpoint Task 7–9 (perilaku `auto`, bentuk JSON) dilewati oleh mode `auto`; ditinjau di `/agyswap-review`.
- Manual check `auto` dengan dua akun sungguhan.
