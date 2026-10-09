# Build log: gelombang 2026-10-09 (paritas CLI–TUI dan rapikan TUI)

Mengikuti "Implementation Plan: gelombang 2026-10-09" di `architecture/PLAN.md`. Task 1–3, 5, dan 6 dibangun bertahap lewat `/agyswap-observe` atas permintaan user sebelum spec dan plan ditulis; Task 4 lewat `/agyswap-build`. Belum di-commit; semuanya masuk lewat `/agyswap-commit` per kategori. Log gelombang v0.2.0 ada di git (`c5b6ce4`).

## Task 1: Kursor selalu terlihat — selesai

- **Diimplementasikan:** `_show` menjadi async, menunggu `lv.clear()` dan `lv.extend(...)` sebelum mengisi `lv.index`, lalu menaruh kursor di email yang sama atau di akun active. Akar masalahnya: index diisi saat item lama belum terhapus, jadi sorotan jatuh ke item yang sedang dihapus.
- **Dibuktikan oleh:** `test_tui_cursor_starts_on_active_and_stays_visible_on_its_email` (merah dulu, lalu hijau).

## Task 2: Instruksi CLI dan TUI terpisah — selesai

- **Diimplementasikan:** `SwapError(msg, tui=None)` dengan atribut `tui`; `tui=` di tujuh pesan yang menyebut perintah/flag CLI; `AGY_RUNNING` tanpa catatan override, CLI menambahkannya; TUI memakai `e.tui` di `_run` dan `action_refresh`; teks `TokenRevoked` netral.
- **Dibuktikan oleh:** `test_errors_give_cli_and_tui_their_own_instructions`; test CLI lama (`No account matches 'nope'. Run \`agyswap list\`.`) tetap lulus.

## Task 3: `n`, `m` More, `b`/`u`/`e`/`i` — selesai

- **Diimplementasikan:** modal `Prompt` (Input, `enter`/`esc`), modal `More` yang meneruskan tombolnya ke `action_*`, `_switch_best` dan `_auto` sebagai pembungkus pesan, binding `b`/`u`/`e`/`i` dengan `show=False`, `m` di akhir footer, label `Add` dan `Toggle`.
- **Dibuktikan oleh:** `test_tui_alias_best_auto_export_import_reach_their_commands`; lebar footer 89 kolom dari pilot headless.

## Task 4: Default nama file export — selesai

- **Diimplementasikan:** modal `e` terisi `agyswap-export.agyswap`.
- **Dibuktikan oleh:** langkah `e` + `enter` di `test_tui_alias_best_auto_export_import_reach_their_commands` (merah dulu dengan `agyswap-export.json`, lalu hijau).

## Task 5: Loading, toast, scrollbar — selesai

- **Diimplementasikan:** `Static#loading` di tengah dan `ListView { display: none }` sampai `_show` pertama, `lv.focus()` setelah tampil, `_fail` mengganti teks loading menjadi `Could not load accounts.`; `ToastRack { margin-bottom: 3 }`; `ListView { scrollbar-size: 0 0 }`.
- **Dibuktikan oleh:** `test_tui_shows_loading_in_the_middle_until_the_first_refresh`; posisi toast dan scroll dari pilot headless (bagian "Validasi" di `architecture/OBSERVE.md`).

## Task 6: Dokumen — selesai

- **Diimplementasikan:** tabel tombol dan perilaku kursor di `README.md`; daftar tombol dan invariant instruksi CLI/TUI di `AGENTS.md`; entri "Validasi" di `architecture/OBSERVE.md`.

## Temuan review v0.2.0 (persiapan rilis 0.3.0) — selesai

- **Diimplementasikan:** `_private_dir` di `cli.py`, dipakai `locked_store` dan `_write_private`: membuat folder `0700`, `chmod 0700` folder yang sudah ada kalau grup/lainnya punya akses, dan `SwapError` kalau pemiliknya bukan user. `pyproject.toml`: `hatchling==1.32.4` (versi yang dipilih `uv build`).
- **Dibuktikan oleh:** `test_existing_store_dir_is_tightened_and_must_be_ours` (merah dulu, lalu hijau); `uv build` lulus dengan pin.
- **Diputuskan user, tanpa perubahan kode:** error 403 tetap `quota request failed (HTTP 403)`; `auto` saat tidak ada yang login tetap switch ke akun terbaik.

## Perbaikan review rilis 0.3.0 — selesai

- **Diimplementasikan:** `asyncio.Lock` di `_show`; export TUI ke `~/agyswap-export.agyswap` dengan path absolut dan pesan refresh token (`_export`, `_abspath`); `_printable` untuk email, `disabled_reason`, dan alias import, laporan alias `!r`; `enable-cache: false` di job build `publish.yml`.
- **Dibuktikan oleh:** test di `architecture/REVIEW.md` ("Diperbaiki"), masing-masing merah dulu; mutasi 18/18 mati.

## Ditunda

- Rincian import (`skipped …`, `alias … dropped`) tidak tampil di TUI; hanya ringkasan (keputusan default, `architecture/SPEC.md`).
