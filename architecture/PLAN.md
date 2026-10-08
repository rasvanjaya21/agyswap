# Implementation Plan: gelombang 2026-10-08 (v0.2.0)

## Overview

Membangun tujuh modul dari `architecture/SPEC.md` ("Gelombang 2026-10-08"): `account-flags`, `quarantine`, `usage-cache`, `switch-strategy`, `auto`, `json-output`, `export-import`. `tui-watch` dibatalkan. Hasilnya dirilis sebagai `0.2.0` bersama perbaikan temuan review/ship dan halaman PyPI yang sudah ada di working tree.

## Architecture Decisions

- **Field opsional, tanpa migrasi.** `alias`, `disabled`, `disabled_reason` dibaca dengan `acc.get(...)`; store v0.1.0 tetap valid.
- **Satu lock untuk dua file.** `usage.json` ditulis di bawah `locked_store()` yang sama dengan `accounts.json`. Penulisan atomik 0600 dipisah jadi helper `_write_private(path, data)` yang dipakai keduanya.
- **Fetch tetap di luar lock.** `switch --strategy` dan `auto` memanggil `collect_usage()` dulu (jaringan, tanpa lock), lalu memilih akun, lalu `cmd_switch(<email terpilih>)` yang mengambil lock dan menjalankan semua invariant switch yang sudah ada. Pilihan memakai email supaya tidak salah slot.
- **Pemilihan akun adalah fungsi murni** `pick_account(rows, strategy, threshold, current)` di `cli.py`, dites tanpa keyring dan jaringan.
- **Cache yang dianggap terbaca untuk strategy**: fetch berhasil, atau cache berumur ≤ 30 menit (baris `stale`). Lebih tua dari itu dianggap tidak terbaca.
- **Error bertipe.** `usage.TokenRevoked(UsageError)` untuk `invalid_grant`, `usage.RateLimited(UsageError)` dengan `retry_after` (detik) untuk 429 dari endpoint kuota. Pesan untuk pemakai tidak berubah, jadi baris error lama tetap sama.
- **Hasil switch terstruktur.** `cmd_switch` mengembalikan dict `{switched, slot, email, saved_slot}`; teks untuk CLI dan TUI dibentuk oleh `switch_message(result)`. Ini yang dipakai `--json`.
- **Baris `collect_usage`** mendapat key `alias`, `disabled`, `disabled_reason`, `stale` (umur detik atau `None`), `retry_at`. `account_text` dan `--json` membaca dari dict yang sama.

## Dependency Graph

```
usage.py  (TokenRevoked, RateLimited, Retry-After)
   │
cli.py    store fields ─ find_slot(alias) ─ disable/enable ─ rotation
   │          │
   │      collect_usage ─ quarantine merge ─ usage.json cache/backoff
   │          │
   │      pick_account ─ switch --strategy ─ auto
   │          │
   │      --json (list/status/switch/auto)     export / import
   │
tui.py    kartu (alias, disabled, stale) ─ tombol x
```

## Task List

### Phase 1: account-flags

## Task 1 (selesai): Alias dan target lewat alias

**Description:** `agyswap alias <target> [nama]` menyetel atau menghapus alias. `find_slot` mencocokkan slot → email → alias (tanpa membedakan huruf besar). `account_text` menampilkan `email (alias)`.

**Acceptance criteria:**
- [x] Alias ditolak (exit 1) kalau dipakai akun lain, angka saja, atau berisi `@`; tanpa nama → alias dihapus.
- [x] `switch <alias>` dan `remove <alias> --yes` mengenai akun yang benar.
- [x] Store v0.1.0 tanpa field baru tetap jalan di semua perintah.

**Verification:**
- [x] `uv run pytest -q`, `uv run ruff check .`, `uv run ruff format --check .`
- [x] `AGYSWAP_HOME=$(mktemp -d)`: `uv run agyswap add`, `uv run agyswap alias 1 main`, `uv run agyswap list` menampilkan `(main)`; shred store.

**Dependencies:** None · **Files:** `src/agyswap/cli.py`, `tests/test_swap.py` · **Scope:** S

## Task 2 (selesai): Disable/enable, rotasi melewati akun disabled

**Description:** `disable`/`enable <target>`. Bare `switch` melewati akun disabled; `switch <akun disabled>` ditolak. `collect_usage` tidak mem-fetch akun disabled dan mengembalikan barisnya dengan `disabled_reason`. `account_text` menampilkan akun disabled redup tanpa bar.

**Acceptance criteria:**
- [x] Rotasi melewati akun disabled; semua akun lain disabled → `No enabled account to switch to`, exit 1, keyring tidak ditulis.
- [x] `switch <disabled>` → exit 1 dengan pesan `enable` di spec.
- [x] `account_usage` tidak dipanggil untuk akun disabled.

**Verification:**
- [x] `uv run pytest -q`, ruff.

**Dependencies:** Task 1 · **Files:** `src/agyswap/cli.py`, `tests/test_swap.py` · **Scope:** S

## Task 3 (selesai): Tombol `x` di TUI

**Description:** `x` men-toggle disable/enable akun terpilih lewat email, di thread worker yang sama dengan aksi lain. Footer dan tabel tombol di `AGENTS.md`/`README.md` mendapat `x`.

**Acceptance criteria:**
- [x] Pilot headless: `x` memanggil disable untuk akun aktif-enabled dan enable untuk akun disabled, dengan email.
- [x] Error tetap tampil tanpa markup dan tanpa isi exception selain tipe.

**Verification:**
- [x] `uv run pytest -q`, ruff.

**Dependencies:** Task 2 · **Files:** `src/agyswap/tui.py`, `tests/test_swap.py` · **Scope:** S

### Checkpoint: Setelah Task 1–3
- [x] `uv run pytest -q`, `uv run ruff check .`, `uv run ruff format --check .` lolos
- [x] `uv run agyswap` (TUI) dengan store sementara menampilkan alias dan akun disabled

### Phase 2: quarantine dan usage-cache

## Task 4 (selesai): Karantina `invalid_grant`

**Description:** `fresh_token` melempar `TokenRevoked`. Merge `collect_usage` (di bawah lock) menandai akun `disabled: true`, `disabled_reason: token revoked` hanya kalau token di store masih sama dengan yang di-fetch. `cmd_add` menghapus tanda `token revoked` (bukan `manual`).

**Acceptance criteria:**
- [x] `_post` palsu dengan `invalid_grant` → akun disabled `token revoked`.
- [x] Token yang diganti `add` di tengah fetch → tanda tidak dipasang.
- [x] `add` ulang menghapus `token revoked`; `manual` tetap.

**Verification:**
- [x] `uv run pytest -q`, ruff.

**Dependencies:** Task 2 · **Files:** `src/agyswap/usage.py`, `src/agyswap/cli.py`, `tests/test_swap.py` · **Scope:** S

## Task 5 (selesai): Cache kuota `usage.json`

**Description:** Helper `_write_private`. Fetch sukses menyimpan `{fetched_at, pools}` per email ke `usage.json` (0600, di bawah lock, entri email yang hilang dibuang). Fetch gagal → baris memakai pools dari cache dengan `stale` = umur detik; `account_text` menambahkan `stale, <umur> ago` di samping error.

**Acceptance criteria:**
- [x] Sukses menulis cache; gagal menampilkan cache + `stale`; tanpa cache → baris error seperti sekarang.
- [x] `usage.json` mode 0600 dan tidak berisi substring token mana pun.
- [x] `accounts.json` tetap tidak ditulis ulang kalau token tidak berubah.

**Verification:**
- [x] `uv run pytest -q`, ruff.
- [x] Manual (agent): store sementara, `uv run agyswap list` sekali, lalu `HTTPS_PROXY=http://127.0.0.1:9 uv run agyswap list` menampilkan angka terakhir dengan `stale`; shred store dan `usage.json`.

**Dependencies:** Task 2 · **Files:** `src/agyswap/cli.py`, `tests/test_swap.py` · **Scope:** M

## Task 6 (selesai): Backoff 429

**Description:** `fetch_pools` melempar `RateLimited` dengan `retry_after` dari header `Retry-After` (detik atau tanggal HTTP; default 300). `collect_usage` menyimpan `retry_at` di cache dan melewati fetch akun itu sampai waktunya; barisnya menampilkan cache + `rate limited, retry in <m>m`.

**Acceptance criteria:**
- [x] `Retry-After: 120`, `Retry-After: <tanggal HTTP>`, dan tanpa header → `retry_at` benar.
- [x] Refresh berikutnya sebelum `retry_at` tidak memanggil `account_usage`; sesudahnya memanggil lagi.

**Verification:**
- [x] `uv run pytest -q`, ruff.

**Dependencies:** Task 5 · **Files:** `src/agyswap/usage.py`, `src/agyswap/cli.py`, `tests/test_swap.py` · **Scope:** S

### Checkpoint: Setelah Task 4–6
- [x] Test dan ruff lolos
- [x] `/agyswap-observe` bagian B: `list` dengan akun sungguhan dan store sementara tanpa error; keyring tidak ditulis (hash sama)

### Phase 3: switch-strategy, auto, json-output

## Task 7 (selesai): `switch --strategy` dan `--threshold`

**Description:** `pick_account(rows, strategy, threshold, current)` murni. `switch --strategy best|next-available [--threshold 90]`: `collect_usage()` tanpa lock → pilih → `cmd_switch(email)`. `--strategy` dengan `<target>` → exit 2. `cmd_switch` mengembalikan dict hasil; `switch_message()` membentuk teks untuk CLI dan TUI.

**Acceptance criteria:**
- [x] `best` memilih `max(used)` terendah, seri ke slot terkecil; `next-available` mengikuti urutan rotasi; keduanya melewati akun disabled, aktif, ≥ threshold, error tanpa cache, dan cache > 30 menit.
- [x] Tanpa kandidat → `No account below 90% usage`, exit 1, keyring palsu tidak ditulis.
- [x] `switch` tanpa `--strategy` dan TUI tetap berperilaku sama (test lama hijau).

**Verification:**
- [x] `uv run pytest -q`, ruff.

**Dependencies:** Task 5 · **Files:** `src/agyswap/cli.py`, `src/agyswap/tui.py`, `tests/test_swap.py` · **Scope:** M

## Task 8 (selesai): `agyswap auto`

**Description:** `auto [--threshold 90] [--strategy best] [--ignore-running]`. Akun aktif di bawah threshold → no-op exit 0. Di atas → switch lewat `pick_account`. Tanpa kandidat, atau kuota akun aktif tidak terbaca → exit 1 tanpa switch. agy berjalan → ditolak sebelum fetch.

**Acceptance criteria:**
- [x] Empat cabang di atas, masing-masing dengan pesan dari spec; keyring palsu hanya ditulis di cabang switch.
- [x] Akun aktif yang belum disimpan diselamatkan (lewat `cmd_switch`).

**Verification:**
- [x] `uv run pytest -q`, ruff.
- [ ] Manual (user, dua akun sungguhan): saat satu akun ≥ 90%, `agyswap auto` lalu `agy` masuk sebagai akun lain.

**Dependencies:** Task 7 · **Files:** `src/agyswap/cli.py`, `tests/test_swap.py` · **Scope:** S

## Task 9 (selesai): `--json`

**Description:** `--json` untuk `list`, `status`, `switch`, `auto` dengan bentuk di spec (`"version": 1`, `reset` ISO, `stale`, `max_used` untuk `auto`). `SwapError` dengan `--json` → `{"version": 1, "error": ...}` di stdout, exit code sama.

**Acceptance criteria:**
- [x] `json.loads` sukses untuk keempat perintah dan untuk error; key sesuai spec.
- [x] Output tidak berisi substring access/refresh/id token.

**Verification:**
- [x] `uv run pytest -q`, ruff.
- [x] `AGYSWAP_HOME=$(mktemp -d)`: `uv run agyswap list --json | python3 -m json.tool` dengan akun sungguhan; shred store.

**Dependencies:** Task 7, 8 · **Files:** `src/agyswap/cli.py`, `tests/test_swap.py` · **Scope:** M

### Checkpoint: Setelah Task 7–9
- [x] Test dan ruff lolos
- [ ] Review dengan user sebelum lanjut (perilaku `auto` dan bentuk JSON)

### Phase 4: export-import dan dokumen

## Task 10 (selesai): `export`

**Description:** `export <file> [--force]` menulis envelope `agyswap-export` v1 dengan `O_CREAT|O_EXCL|O_NOFOLLOW`, 0600 (`--force` menghapus file lama dulu). Akun aktif memakai token keyring tanpa mengubah store/keyring. Peringatan di stderr.

**Acceptance criteria:**
- [x] File 0600, berisi semua akun beserta field opsional; file yang ada ditolak tanpa `--force`.
- [x] Token akun aktif = token keyring; store dan keyring palsu tidak berubah.

**Verification:**
- [x] `uv run pytest -q`, ruff.

**Dependencies:** Task 1, 2 · **Files:** `src/agyswap/cli.py`, `tests/test_swap.py` · **Scope:** S

## Task 11 (selesai): `import`

**Description:** `import <file> [--force]`: validasi seluruh file dulu (format, versi, email = claim `email` token), lalu tulis di bawah lock. Email baru → slot berikutnya; email ada → skip, atau ganti token dan field dengan slot tetap kalau `--force`. Tidak menulis keyring.

**Acceptance criteria:**
- [x] Round-trip export → store kosong → import menghasilkan akun yang sama.
- [x] Satu entri tidak valid → seluruh import ditolak, store tidak berubah.
- [x] `Imported N, skipped M` benar untuk skip dan `--force`.

**Verification:**
- [x] `uv run pytest -q`, ruff.

**Dependencies:** Task 10 · **Files:** `src/agyswap/cli.py`, `tests/test_swap.py` · **Scope:** S

## Task 12 (selesai): Dokumen

**Description:** `README.md` (Usage: perintah dan flag baru, tombol `x`, Status), `AGENTS.md` (Layout: perintah dan `usage.json`; Invariants: quarantine hanya menandai, export 0600 `O_EXCL`, `auto` hanya sekali jalan), `TODO.md` (hapus butir fitur yang selesai), `architecture/SPEC.md` (centang Success Criteria).

**Acceptance criteria:**
- [x] Setiap perintah dan flag di `uv run agyswap --help` ada di README.
- [x] `TODO.md` hanya menyisakan yang belum dikerjakan.

**Verification:**
- [x] `uv run ruff check .`, `uv run ruff format --check .`

**Dependencies:** Task 1–11 · **Files:** `README.md`, `AGENTS.md`, `TODO.md`, `architecture/SPEC.md` · **Scope:** S

### Checkpoint: Selesai
- [x] Semua Success Criteria gelombang 2026-10-08 di `architecture/SPEC.md` terpenuhi (kecuali manual check `auto`, yang dicatat sebagai cek user)
- [x] `uv build` lolos; wheel hanya `agyswap/` dan `agyswap_cli-*.dist-info/`
- [ ] Siap untuk `/agyswap-test` → `/agyswap-review` → `/agyswap-prepare` → `/agyswap-commit` → `/agyswap-ship` (`0.2.0`)

## Risks and Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| `invalid_grant` dan `Retry-After` belum pernah terobservasi (`OBSERVE.md`) | Med | Ikuti respons OAuth/HTTP standar; quarantine hanya menandai (bisa `enable`); validasi ulang lewat `/agyswap-observe` B saat terjadi |
| Isi kuota saat bucket habis belum terobservasi | Med | Threshold 90% < 100%, dan fraction yang hilang sudah dihitung habis; `auto` tidak bergantung pada nilai tepat saat habis |
| Race antara fetch tanpa lock dan switch/quarantine | High | Pilihan dan tanda memakai email; quarantine hanya jika token sama; `cmd_switch` tetap memegang lock untuk seluruh mutasinya |
| `usage.json` atau output `--json` membocorkan token | High | `usage.json` hanya pools; test substring token untuk `usage.json`, `--json`, dan stdout/stderr export |
| `cmd_switch` berubah tipe kembalian | Low | `switch_message()` dipakai CLI dan TUI; test TUI yang ada menjaga notifikasi |
| `cli.py` makin besar (±370 → ±600 baris) | Low | Tetap satu modul sesuai Layout; pecah hanya kalau review memintanya |

## Open Questions

- Batas umur cache untuk strategy (30 menit) adalah default dari plan ini; ganti sebelum Task 7 kalau mau nilai lain.

