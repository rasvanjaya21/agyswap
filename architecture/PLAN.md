# Implementation Plan: gelombang 2026-10-09 (paritas CLI–TUI dan rapikan TUI)

## Overview

Memverifikasi dan menuntaskan `architecture/SPEC.md` bagian "Gelombang 2026-10-09". Kode untuk hampir semua task sudah ada di working tree (dibangun bertahap lewat `/agyswap-observe` atas permintaan user); task yang sudah lulus verifikasinya dicentang. Satu task tersisa: default nama file export. Plan v0.2.0 sebelumnya selesai lewat rilis `c5b6ce4`; manual check `auto` dua akun yang belum dijalankan dipindah ke `TODO.md`.

## Architecture Decisions

- **Dua teks dalam satu error.** `SwapError(msg, tui=...)`: `str(e)` tetap pesan CLI (output CLI dan test lama tidak berubah), `e.tui` untuk TUI. Tidak ada tabel terjemahan terpisah; teks TUI ditulis di tempat error dibuat.
- **TUI hanya memanggil `cmd_*` yang sudah ada.** `b`, `u`, `e`, `i`, `n` tidak menambah logika di `cli.py`; semua invariant (lock, penolakan saat agy berjalan, export `0600`) tetap di satu tempat.
- **Kursor berdasarkan email.** `_show` menunggu `clear()`/`extend()` selesai lalu menaruh index ke email yang sama atau ke akun active; ini sekaligus memperbaiki sorotan yang hilang.
- **Satu modal input** (`Prompt`) untuk alias, export, dan import; satu modal daftar (`More`) yang meneruskan tombolnya ke action app.
- **Tampilan lewat CSS saja**: toast (`ToastRack { margin-bottom: 3 }`), scrollbar (`scrollbar-size: 0 0`), loading (`#loading`, `ListView` `display: none` sampai muat pertama).

Dependensi: `tui.py` → `cli.py` (`SwapError.tui`, `cmd_*`) → `usage.py` (teks `TokenRevoked`). Tidak ada perubahan perilaku agy; tidak ada kondisi `architecture/OBSERVE.md` baru yang perlu ditangani.

## Task List

### Phase 1: Kursor dan pesan

## Task 1 (selesai): Kursor selalu terlihat, mulai di akun active

**Acceptance criteria:**
- [x] Muat pertama: kursor di akun active.
- [x] Setelah refresh dengan urutan berubah: kursor di email yang sama, tepat satu item `highlighted`.

**Verification:**
- [x] `uv run pytest -q -k cursor_starts` (gagal sebelum perbaikan, lulus sesudahnya)

**Dependencies:** None. **Files:** `src/agyswap/tui.py`, `tests/test_swap.py`. **Scope:** S

## Task 2 (selesai): Instruksi CLI dan TUI terpisah

**Acceptance criteria:**
- [x] Setiap `SwapError` yang menyebut perintah/flag CLI dan bisa muncul dari TUI punya `tui=` (disabled, agy berjalan, belum login, belum ada akun, target tidak ada, JSON rusak, export sudah ada).
- [x] TUI menampilkan `e.tui` di toast dan baris status; teks `TokenRevoked` netral.

**Verification:**
- [x] `uv run pytest -q -k own_instructions`
- [x] `grep -n -E "SwapError\(.*(agyswap |--[a-z])" src/agyswap/cli.py | grep -v "tui="` hanya menyisakan pesan khusus CLI (`--slot`, `remove` tanpa `--yes`, format export).

**Dependencies:** None. **Files:** `src/agyswap/cli.py`, `src/agyswap/usage.py`, `src/agyswap/tui.py`, `tests/test_swap.py`. **Scope:** M

### Checkpoint: Setelah Task 1–2
- [x] `uv run ruff check .` dan `uv run pytest -q` lulus

### Phase 2: Fitur CLI di TUI

## Task 3 (selesai): `n` alias, `m` More dengan `b`/`u`/`e`/`i`

**Acceptance criteria:**
- [x] `n` membuka modal terisi alias lama; isi → `cmd_alias(email, name)`, kosong → `None`, `esc` → tidak ada panggilan.
- [x] `b` → `cmd_switch_strategy("best", 90)`, `u` → `cmd_auto()`, `e`/`i` → modal path dengan `~` diekspansi.
- [x] `m` membuka More; `esc` tidak menjalankan apa pun, `b` di dalamnya menjalankan switch terbaik. Footer: Switch, Add, Remove, Toggle, Alias, Refresh, Quit, More.

**Verification:**
- [x] `uv run pytest -q -k reach_their_commands`
- [x] Pilot headless: lebar footer 89 kolom.

**Dependencies:** Task 2 (error dari `b`/`u`/`e` memakai `e.tui`). **Files:** `src/agyswap/tui.py`, `tests/test_swap.py`. **Scope:** S

## Task 4 (selesai): Default nama file export `agyswap-export.agyswap`

**Description:** Modal `e` terisi `agyswap-export.agyswap`, mengikuti ekstensi di spec export-import.

**Acceptance criteria:**
- [x] Modal export terisi `agyswap-export.agyswap`; menekan `enter` tanpa mengubah memanggil `cmd_export` dengan path itu.

**Verification:**
- [x] `uv run pytest -q -k reach_their_commands` (tambah langkah `e` + `enter` tanpa isi baru)
- [x] `uv run ruff check .` dan `uv run ruff format --check .`

**Dependencies:** Task 3. **Files:** `src/agyswap/tui.py`, `tests/test_swap.py`. **Scope:** XS

### Checkpoint: Setelah Task 3–4
- [x] `uv run pytest -q` lulus

### Phase 3: Tampilan dan dokumen

## Task 5 (selesai): Loading di tengah, toast, scrollbar

**Acceptance criteria:**
- [x] `Loading accounts…` di tengah sampai muat pertama; daftar lalu tampil dan mendapat fokus; gagal → `Could not load accounts.`
- [x] Toast di kanan bawah di atas baris status.
- [x] Scrollbar daftar tidak tampil; arrow keys tetap menggulir.

**Verification:**
- [x] `uv run pytest -q -k loading_in_the_middle`
- [x] Pilot headless (dicatat di "Validasi" `architecture/OBSERVE.md`): toast `y=14..16`, status `y=18`; lebar scrollbar `0`, `scroll_y` 0 → 24.

**Dependencies:** Task 1. **Files:** `src/agyswap/tui.py`, `tests/test_swap.py`. **Scope:** S

## Task 6 (selesai): Dokumen

**Acceptance criteria:**
- [x] `README.md`: tabel tombol (`n`, `m`, `b`, `u`, `e`, `i`, `r` semua akun) dan perilaku kursor.
- [x] `AGENTS.md`: daftar tombol TUI dan invariant "CLI dan TUI masing-masing memberi instruksinya sendiri".
- [x] `architecture/OBSERVE.md` bagian Validasi mencatat setiap langkah.

**Verification:**
- [x] `uv run ruff format --check .`

**Dependencies:** Task 1–5. **Files:** `README.md`, `AGENTS.md`, `architecture/OBSERVE.md`. **Scope:** S

### Checkpoint: Selesai
- [x] `uv run ruff format --check .`, `uv run ruff check .`, `uv run pytest -q` lulus
- [x] Manual check oleh user di TUI sungguhan (dikonfirmasi user 2026-10-09, butir 1.1–1.12; `auto` dua akun 1.13): sorotan tetap terlihat setelah `r`; modal `m`, `n`, `e`; toast di atas baris status; `s` pada akun disabled memberi `Press x on it first.`
- [ ] Lanjut `/agyswap-test` → `/agyswap-review` → `/agyswap-prepare` → `/agyswap-commit`

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Pesan baru di `cli.py` menyebut perintah CLI tanpa `tui=` | Med | Invariant di `AGENTS.md`; grep di Task 2 dijalankan ulang di `/agyswap-review`. |
| `e` menulis refresh token ke file di cwd TUI | Med | Sama dengan CLI (`0600`, tidak menimpa); judul modal menyebut "with refresh tokens". |
| `b`/`u` mengganti akun dengan satu tombol | Low | Tetap ditolak saat agy berjalan; hasil tampil di toast. |
| Footer terpotong di < 89 kolom | Low | Diputuskan user: dibiarkan. |

## Open Questions

- Tidak ada. Keputusan 2026-10-09 tercatat di `architecture/SPEC.md`.
