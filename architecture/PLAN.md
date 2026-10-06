# Implementation Plan: agyswap baseline v0.1.0

Ditulis lewat `/agyswap-plan` pada 2026-10-06, diisi dari state saat ini (`architecture/SPEC.md`, `architecture/OBSERVE.md`, kode), dan diperbarui di siklus berikutnya untuk pekerjaan yang sama. Fase 1 mencatat pekerjaan yang sudah selesai. Fase 2 adalah satu-satunya kriteria sukses baseline yang belum terpenuhi: kuota mingguan.

## Overview

Baseline agyswap sudah berjalan: add, list, status, switch, remove, dan TUI, dengan token yang aman dari kehilangan. Yang tersisa untuk menutup baseline adalah sumber kuota. `fetchAvailableModels` hanya memuat window 5 jam, sehingga akun bisa tampil 0% terpakai padahal kuota mingguannya sudah terpakai 44–58%. Rencana ini memindahkan sumber kuota ke `retrieveUserQuotaSummary`, yang memuat window 5 jam dan mingguan per grup, lalu menampilkannya di `list` dan TUI.

## Architecture Decisions

- **Sumber kuota diganti, bukan ditambah.** `retrieveUserQuotaSummary` sudah memuat window 5 jam yang sama dengan `fetchAvailableModels`, plus window mingguan. Jalur `fetchAvailableModels` dihapus supaya tidak ada dua sumber yang bisa berbeda (`OBSERVE.md`, "Kuota per window").
- **Host mengikuti agy:** `daily-cloudcode-pa.googleapis.com`, dengan body `{}`, `Authorization: Bearer`, dan UA `antigravity` (`OBSERVE.md`, "Host dan rate limit").
- **Label grup dari respons, tidak di-hardcode.** Nama grup diambil dari `groups[].displayName` ("Gemini Models", "Claude and GPT models"), dan nama window dari `buckets[].window` (`5h`, `weekly`).
- **Reset bucket yang masih penuh diabaikan.** Bucket 5 jam dengan `remainingFraction: 1` melaporkan reset yang terus bergeser, jadi hitung mundurnya tidak ditampilkan (`OBSERVE.md`, baris bucket 5 jam yang belum dipakai).
- **`Pool` diganti menjadi `group`, `window`, `used`, `reset`.** `collect_usage`, merge token, dan TUI tidak berubah, dan hanya render yang menyesuaikan. Properti `label` sementara dihapus saat prepare setelah review, karena sudah tidak dipakai.

## Dependency Graph

```
usage.fetch_pools (sumber kuota)
    └── cli.account_text (render kartu)
            ├── cli.cmd_list
            └── tui.AgySwapApp (kartu di ListView)
```

## Task List

### Phase 1: Baseline (selesai)

- [x] Store akun di `~/.agyswap/accounts.json` (0600, atomik, `locked_store()`), keyring lewat `secret-tool`.
- [x] `add [--slot N]`, `status`, `switch [N|email] [--force]`, `remove`, termasuk tiga perbaikan Critical dari `REVIEW.md` (login tanpa salinan, slot milik akun lain, race di store).
- [x] Refresh token akun tidak aktif dengan client secret dari binary agy, User-Agent `antigravity`.
- [x] `list` dan TUI (tema pitch black, kartu, footer badge), refresh di worker thread.
- [x] 7 test pytest, ruff, CI, publish workflow, dan uji manual dua akun sungguhan oleh user.
- [x] `README.md` mengikuti format README user (banner, badge pip dan build); validasi ulang `add`/`status`/`list` dengan store sementara di agy 1.3.0.
- [x] Siklus proyek: SHIP terakhir setelah COMMIT, dan `/agyswap-ship` menentukan bump semver dari commit sejak tag terakhir.

### Phase 2: Kuota 5 jam + mingguan

## Task 1: Ambil kuota dari `retrieveUserQuotaSummary` — selesai

**Description:** `usage.fetch_pools` memanggil `POST https://daily-cloudcode-pa.googleapis.com/v1internal:retrieveUserQuotaSummary` dengan body `{}`, lalu menghasilkan satu `Pool` per bucket, berisi `group` (dari `groups[].displayName`), `window` (`5h`/`weekly`), `used = 1 - remainingFraction`, dan `reset`. `reset` bernilai `None` kalau bucket masih penuh. Konstanta dan kode `fetchAvailableModels` dihapus.

**Acceptance criteria:**
- [x] Respons dengan bentuk dari `OBSERVE.md` (dua grup, masing-masing bucket `5h` dan `weekly`) menghasilkan empat `Pool` dengan group, window, used, dan reset yang benar.
- [x] Bucket dengan `remainingFraction` 1 punya `reset=None`. `description` yang tidak ada tidak membuat error.
- [x] HTTP error dan network error tetap menjadi `UsageError` dengan pesan yang sama seperti sekarang.

**Verification:**
- [x] `uv run pytest -q`: test baru dengan `usage._post` palsu menggantikan `test_fetch_pools_groups_shared_buckets`.
- [x] `uv run ruff check .` dan `uv run ruff format --check .`
- [x] Manual (read-only): `uv run python -c "from agyswap import cli, usage; print([(p.group, p.window, round(p.used,3)) for p in usage.account_usage(cli.read_token())[0]])"` cocok dengan `agy -p /quota --output-format json`.

**Dependencies:** None

**Files likely touched:** `src/agyswap/usage.py`, `tests/test_swap.py`

**Estimated scope:** S

## Task 2: Tampilkan 5 jam dan mingguan di `list` dan TUI — selesai

**Description:** `cli.account_text` mengelompokkan pool per grup. Setiap grup tampil sebagai satu judul (misalnya `Gemini`, `Claude/GPT`), diikuti baris `5h` dan `weekly`, masing-masing dengan bar, persen, dan hitung mundur reset (`resets 4h 12m` atau `resets 2d 5h`). Bucket penuh tidak menampilkan hitung mundur. TUI ikut berubah karena memakai render yang sama.

**Acceptance criteria:**
- [x] Kartu akun memuat kedua window untuk kedua grup, berurutan sama di `list` dan TUI.
- [x] Hitung mundur mingguan memakai format hari (`2d 5h`). Bucket penuh tanpa hitung mundur.
- [x] Warna bar tetap hijau, kuning, atau merah sesuai pemakaian, dan kartu tetap terbaca di latar biru saat terpilih.

**Verification:**
- [x] `uv run pytest -q`: test render (`account_text` dengan pool palsu) memeriksa teks grup, `5h`, `weekly`, dan persen.
- [x] `uv run ruff check .` dan `uv run ruff format --check .`
- [x] Manual: `AGYSWAP_HOME=$(mktemp -d) uv run agyswap add && AGYSWAP_HOME=… uv run agyswap list` menunjukkan angka mingguan yang sama dengan `agy -p /quota`; screenshot headless TUI (Textual pilot) terlihat rapi. Hapus store sementara dengan `shred -u`.

**Dependencies:** Task 1

**Files likely touched:** `src/agyswap/cli.py`, `tests/test_swap.py`

**Estimated scope:** S

### Checkpoint: Setelah Task 1–2
- [x] `uv run pytest -q`, `uv run ruff check .`, `uv run ruff format --check .` lolos
- [x] `uv build` lolos
- [x] User melihat sendiri `uv run agyswap` dengan dua akun sungguhan: angka 5 jam dan mingguan cocok dengan `/quota` di agy

## Task 3: Perbarui dokumen ke perilaku baru — selesai

**Description:** Ganti semua klaim bahwa kuota berasal dari `fetchAvailableModels` atau hanya 5 jam.

**Acceptance criteria:**
- [x] `README.md` (Description dan Status: hapus kalimat "The quota shown today only covers the 5-hour window; the weekly window is next.") dan `AGENTS.md` (ringkasan auth: `fetchAvailableModels` tidak lagi dipakai) sesuai perilaku baru.
- [x] `architecture/OBSERVE.md`, bagian Validasi, mencatat hasil cek manual Task 2.
- [x] Butir "Kuota" di `TODO.md` dihapus, dan kriteria kuota di `architecture/SPEC.md` dicentang.

**Verification:**
- [x] `grep -rn fetchAvailableModels README.md AGENTS.md src/` hanya menyisakan penyebutan historis yang disengaja (di `OBSERVE.md`).
- [x] `uv run ruff check .`

**Dependencies:** Task 2

**Files likely touched:** `README.md`, `AGENTS.md`, `TODO.md`, `architecture/OBSERVE.md`, `architecture/SPEC.md`

**Estimated scope:** M

### Checkpoint: Selesai
- [x] Semua kriteria sukses baseline di `architecture/SPEC.md` terpenuhi
- [ ] Siap untuk `/agyswap-review`, lalu `/agyswap-prepare` → `/agyswap-commit` → `/agyswap-ship`

### Catatan rilis

Task 1–3 menambah kemampuan yang terlihat pemakai (kuota mingguan di `list` dan TUI), jadi termasuk **minor** menurut kategori di `/agyswap-ship`. Karena belum ada tag rilis, semuanya masuk rilis pertama `0.1.0` tanpa bump.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| `retrieveUserQuotaSummary` tidak terdokumentasi dan bisa berubah di versi agy berikutnya | High | Parser toleran terhadap field opsional dan grup tambahan; `/agyswap-observe` dijalankan ulang setiap `agy --version` berubah |
| Respons saat bucket benar-benar habis belum terobservasi | Med | Perlakukan `remainingFraction` yang hilang atau 0 sebagai 100% terpakai; dicatat di "Belum terobservasi" |
| Host `daily-cloudcode-pa` berbeda perilaku dengan `cloudcode-pa` | Low | Keduanya terobservasi menjawab sama; host dijadikan satu konstanta |
| Request tambahan per akun memicu rate limit | Low | Jumlah request per refresh tetap satu per akun (menggantikan `fetchAvailableModels`); cache dan backoff tetap ada di `TODO.md` |

## Di luar rencana ini

Semua butir lain di `TODO.md` (fitur yang belum ada, `run`/sesi paralel, rilis) butuh spec sendiri sebelum direncanakan.

## Open Questions

- Tidak ada untuk Task 1–3. Urutan grup di kartu mengikuti urutan respons (Gemini dulu, lalu Claude/GPT); bilang kalau mau dibalik.

---

# Implementation Plan: render-polish + cli-safety

Ditulis lewat `/agyswap-plan` pada 2026-10-06. Gelombang pertama Capability Map di `architecture/SPEC.md`, dengan spec di `architecture/SPEC.md` ("Spec modul: render-polish") dan `architecture/SPEC.md` ("Spec modul: cli-safety"). Rencana kuota di atas tetap dipertahankan: semua task-nya selesai, dan yang tersisa hanya cek manual oleh user.

## Overview

Dua modul kecil yang tidak saling bergantung:

- `render-polish` menutup Suggestion 2 dan 3 dari `REVIEW.md`.
- `cli-safety` menambah konfirmasi `remove` (`--yes`/`-y`), exit 2 untuk bare non-TTY, arti baru `--force`, dan flag baru `--ignore-running`. Nama flag ini dipakai karena open question di spec tidak dijawab; mudah diganti sebelum rilis.

## Architecture Decisions

- **Konfirmasi `remove` ada di `main`, bukan di `cmd_remove`.** TUI sudah punya modal konfirmasi sendiri dan memanggil `cmd_remove` langsung, jadi fungsi itu tetap tanpa prompt.
- **`cmd_switch(target, force=False, ignore_running=False)`.** TUI memanggil `cmd_switch(slot, False)` secara positional, jadi arti argumen kedua sekarang menjadi `force` (lewati sinkronisasi token live) dan TUI tetap aman: tidak memaksa, dan tetap menolak saat agy berjalan.
- **`--force` hanya melewati baris "capture the live token" untuk login yang sudah tersimpan.** Cabang "Never overwrite a login we have no copy of" tidak disentuh (invariant `AGENTS.md`).

## Dependency Graph

```
cli.account_text  ← cli.cmd_list, tui        (Task 1)
cli.main / build_parser                       (Task 2, 3, 4)
    └── cli.cmd_switch, cli.cmd_remove        (Task 4)
```

## Task List

## Task 1: Render tanpa spasi di ujung, kolom grup dinamis — selesai

**Description:** `account_text` menghitung lebar kolom grup sebagai `max(12, len(grup terpanjang) + 2)`, dan baris bucket penuh tidak diakhiri spasi.

**Acceptance criteria:**
- [x] Test baru: baris bucket penuh tanpa spasi di ujung (cek tanpa `rstrip()`), dan mutasi `if p.reset:` → `if True:` membuatnya merah.
- [x] Test baru: grup palsu dengan nama 20 karakter; kolom window sejajar di semua baris.
- [x] `test_account_text_groups_5h_and_weekly` tetap hijau (lebar minimum 12, tampilan sekarang tidak berubah).

**Verification:**
- [x] `uv run pytest -q`, `uv run ruff check .`, `uv run ruff format --check .`
- [x] Manual: `AGYSWAP_HOME=$(mktemp -d) uv run agyswap add && … list` sama seperti sebelumnya, lalu store di-`shred`.

**Dependencies:** None · **Files:** `src/agyswap/cli.py`, `tests/test_swap.py` · **Scope:** S

## Task 2: Konfirmasi `remove` dengan `--yes`/`-y` — selesai

**Description:** `main` menangani `remove`: cari slot dan email, beri peringatan kalau akun aktif, lalu tanya `Remove account N (email)? [y/N] ` (hanya di TTY). Jawaban selain `y`/`yes` → `Cancelled`, exit 0. Tanpa TTY dan tanpa `--yes` → `error: …` dengan exit 1. `--yes`/`-y` melewati prompt.

**Acceptance criteria:**
- [x] Input `n` → `Cancelled`, akun tetap ada; input `y` → akun terhapus.
- [x] Non-TTY tanpa `--yes` → exit 1, akun tetap ada; `--yes` → terhapus tanpa prompt.
- [x] Akun aktif → peringatan tercetak sebelum prompt.

**Verification:**
- [x] `uv run pytest -q` (monkeypatch `builtins.input` dan `sys.stdin.isatty`), ruff lolos.
- [x] Manual dengan store sementara: `uv run agyswap remove 1` bertanya; `echo | uv run agyswap remove 1` exit 1; `uv run agyswap remove 1 --yes` menghapus.

**Dependencies:** None · **Files:** `src/agyswap/cli.py`, `tests/test_swap.py` · **Scope:** S

## Task 3: Bare `agyswap` di luar TTY exit 2 — selesai

**Description:** Saat tidak ada subcommand dan stdin/stdout bukan TTY: `parser.error("no command given — try 'agyswap --help'")`, sehingga exit 2.

**Acceptance criteria:**
- [x] `main([])` non-TTY → `SystemExit(2)` dengan pesan `no command given`.
- [x] Di TTY, bare `agyswap` tetap membuka TUI (tidak berubah).

**Verification:**
- [x] `uv run pytest -q`; manual `uv run agyswap < /dev/null; echo $?` → `2`.

**Dependencies:** None · **Files:** `src/agyswap/cli.py`, `tests/test_swap.py` · **Scope:** XS

### Checkpoint: Setelah Task 1–3
- [x] `uv run pytest -q`, `uv run ruff check .`, `uv run ruff format --check .` lolos

## Task 4: arti baru `--force`, `--ignore-running` baru — selesai

**Description:** `switch --ignore-running` melewati penolakan saat agy berjalan. `switch --force` tidak menyalin token live ke slot akun live yang sudah tersimpan. Login live yang belum disimpan tetap diselamatkan, dengan atau tanpa `--force`. Pesan penolakan menyebut `--ignore-running`.

**Acceptance criteria:**
- [x] `agy_running()` bernilai `True`: tanpa flag → ditolak; `--force` → tetap ditolak; `--ignore-running` → berhasil.
- [x] `--force`: slot akun live tetap memakai token lama (token live yang lebih baru tidak disalin); tanpa `--force` token live disalin (test lama).
- [x] `--force` dengan login live yang belum disimpan → tetap disimpan ke slot baru sebelum keyring ditimpa.

**Verification:**
- [x] `uv run pytest -q` dengan keyring palsu; ruff lolos.
- [x] TUI tetap jalan (pilot headless: switch dan remove via modal).

**Dependencies:** None · **Files:** `src/agyswap/cli.py`, `tests/test_swap.py` · **Scope:** S

## Task 5: Dokumen — selesai

**Description:** `README.md` (Usage: `remove --yes`, `switch --force` dan `--ignore-running`), `AGENTS.md` (Invariants: "`--ignore-running` overrides"), dan `TODO.md` (hapus butir konfirmasi `remove`, bare non-TTY, arti `--force`, dan dua butir Kualitas kode).

**Acceptance criteria:**
- [x] Tidak ada lagi dokumen yang menyebut `--force` sebagai "abaikan agy yang berjalan".
- [x] `TODO.md` hanya menyisakan butir yang belum dikerjakan.

**Verification:**
- [x] `grep -rn -- "--force" README.md AGENTS.md CONTRIBUTING.md` sesuai arti baru; `uv run ruff check .`

**Dependencies:** Task 2–4 · **Files:** `README.md`, `AGENTS.md`, `TODO.md` · **Scope:** S

### Checkpoint: Selesai
- [x] Semua Success Criteria di kedua spec modul terpenuhi
- [x] `uv build` lolos
- [ ] Siap untuk `/agyswap-test` → `/agyswap-review` → `/agyswap-prepare` → `/agyswap-commit` → `/agyswap-ship`

## Risks and Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| TUI memanggil `cmd_switch(slot, False)` positional; arti argumen kedua berubah | Med | Argumen kedua tetap `False` (tidak memaksa); Task 4 menambah cek pilot TUI |
| Script lama yang memakai `switch --force` untuk melewati agy berjalan berubah perilaku | Low | Belum ada rilis (0.1.0 belum terbit); dicatat di README |
| Prompt `remove` menggantung di lingkungan non-interaktif | Med | Prompt hanya saat `sys.stdin.isatty()`; selain itu wajib `--yes` |

## Catatan rilis

`cli-safety` mengubah arti `--force`. Dalam kategori `/agyswap-ship` itu termasuk major, tapi karena masih `0.x` dan belum ada tag rilis, perubahan ini ikut rilis pertama `0.1.0`.

## Open Questions

- Nama `--ignore-running` dipakai sebagai default; ganti sebelum build kalau mau nama lain.
