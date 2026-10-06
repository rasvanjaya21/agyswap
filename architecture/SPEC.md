# Spec: agyswap (state saat ini, v0.1.0)

Ditulis lewat `/agyswap-spec` (diisi dari state saat ini) pada 2026-10-06, dan diperbarui di siklus berikutnya setelah prepare dan observe: spec "as-built", disusun dari kode, `AGENTS.md`, `architecture/OBSERVE.md`, `architecture/REVIEW.md`, dan `TODO.md`, tanpa sesi tanya jawab. Spec ini jadi baseline; fitur berikutnya ditulis sebagai spec baru di atasnya.

## Objective

agyswap mengganti akun Google yang dipakai **Antigravity CLI (`agy`)** tanpa login ulang, dan menampilkan kuota setiap akun.

- **Pemakai:** orang yang memakai `agy` dengan lebih dari satu akun Google, dan ingin berpindah akun saat kuota satu akun menipis.
- **Di luar scope:** Antigravity IDE, Gemini CLI, Gemini Code Assist, dan produk Google AI lain.

User story yang sudah terpenuhi:

1. Sebagai pemakai agy, saya menyimpan akun yang sedang login (`agyswap add`), lalu `/logout` di agy, login akun lain, dan menyimpannya juga.
2. Saya berpindah akun dengan `agyswap switch` (rotasi), `agyswap switch 2`, atau `agyswap switch email`, lalu agy berikutnya masuk sebagai akun itu tanpa login ulang.
3. Saya melihat kuota setiap akun (`agyswap list`) atau lewat dashboard interaktif (`agyswap`).
4. Saya menghapus akun yang tidak dipakai (`agyswap remove`).

## Tech Stack

- Python 3.12+ (diuji 3.12, 3.13, 3.14), dikelola dengan uv.
- Runtime: `textual>=8.2.8,<9` (TUI) dan `rich>=15` (render bar). Sisanya stdlib: `urllib`, `fcntl`, `concurrent.futures`, `argparse`, `json`.
- Keyring: `secret-tool` (libsecret, Secret Service). Hanya Linux.
- Dev: `pytest`, `ruff`. Build: hatchling.

## Commands

```bash
uv sync                              # .venv + agyswap editable
uv run agyswap                       # TUI (bare, di TTY)
uv run agyswap add [--slot N]
uv run agyswap list | ls
uv run agyswap status
uv run agyswap switch [N|email] [--force] [--ignore-running]
uv run agyswap remove|rm N|email [--yes]
uv run ruff format . && uv run ruff check .
uv run pytest -q
uv build
uv run python scripts/docs.py        # mirror docs/
uv run python scripts/skills.py      # re-vendor skills dari upstream
```

## Project Structure

```
src/agyswap/cli.py     store, keyring, perintah, render kartu akun (dipakai list dan TUI)
src/agyswap/usage.py   refresh token dan pengambilan kuota
src/agyswap/tui.py     dashboard Textual
tests/test_swap.py     pytest dengan keyring palsu
architecture/          output setiap skill siklus proyek
skills/, scripts/, docs/, graphify-out/   tooling agent (lihat AGENTS.md)
```

## Perilaku saat ini

### Penyimpanan

- Token agy ada di keyring: `service=gemini`, `username=antigravity`, berupa JSON. Email diambil dari claim `email` di `id_token` (`architecture/OBSERVE.md`, "Penyimpanan login").
- agyswap menyimpan salinan token per akun di `~/.agyswap/accounts.json` (`{"accounts": {"<slot>": {"email", "token"}}}`), mode 0600, ditulis atomik. Lokasinya bisa diganti dengan `AGYSWAP_HOME`.
- Setiap perubahan store lewat `locked_store()` (flock `~/.agyswap/.lock`).

### Perintah

| Perintah | Perilaku |
| -------- | -------- |
| `add [--slot N]` | Menyimpan login agy yang aktif. Akun yang sudah ada diperbarui di tempat. `--slot` wajib angka ≥ 1, ditolak kalau slot berisi akun lain, dan memindahkan akun yang sama ke slot baru. Gagal dengan pesan jelas kalau agy belum login |
| `list` / `ls` | Kartu per akun: slot, email, `● active`, satu bar per bucket kuota (persen terpakai, hitung mundur reset). Token akun tidak aktif yang kedaluwarsa di-refresh di memori lalu digabung ke store |
| `status` | Email akun aktif dan slotnya, atau keterangan bahwa login itu belum disimpan |
| `switch [N\|email]` | Tanpa target: rotasi ke slot berikutnya. Ditolak kalau ada proses `agy` selain updater (`--ignore-running` untuk memaksa); `--force` melewati penyalinan token live ke slotnya. Sebelum menulis keyring: token live disalin ke slotnya, dan login yang belum disimpan otomatis disimpan ke slot baru |
| `remove` / `rm` | Menghapus akun dari store. Di TTY bertanya `[y/N]` (peringatan kalau akun aktif); tanpa TTY wajib `--yes`/`-y` |
| bare `agyswap` | TTY: membuka TUI. Bukan TTY: `no command given`, exit 2 |

### Kuota

- Sumber: `POST daily-cloudcode-pa.googleapis.com/v1internal:retrieveUserQuotaSummary`, satu `Pool` per bucket: grup (`Gemini`, `Claude/GPT`) × window (`5h`, `weekly`). Kartu menampilkan nama grup sekali, lalu baris `5h` dan `weekly`; bucket yang masih penuh tanpa hitung mundur reset.
- Refresh token lewat `oauth2.googleapis.com/token`, dengan client ID dari claim `azp` dan client secret yang dibaca dari binary `agy` saat runtime.
- Semua request memakai User-Agent `antigravity` dan timeout 20 detik.

### TUI

- Tema pitch black. Judul `agyswap - Antigravity CLI Accounts Swap` di tengah.
- Kartu akun: kartu terpilih berlatar biru `#0178d4`, `● active` oranye `#ffa62b`, bar hijau/kuning/merah sesuai pemakaian.
- Footer abu gelap `#141414` dengan badge key oranye, sejajar dengan baris status (jumlah akun, jam update, interval refresh 2 menit).
- Tombol: `enter`/`s` switch, `a` add, `d` remove (konfirmasi `y`/`n`), `r` refresh, `j`/`k`, `q`. Command palette dimatikan.
- Refresh kuota berjalan di worker thread, tidak memblokir UI.

### Distribusi dan dokumentasi

- Nama paket PyPI `agyswap-cli` (belum terdaftar; `agyswap` ditolak PyPI karena terlalu mirip proyek lain), command tetap `agyswap`, versi hanya di `pyproject.toml`. `uv build` menghasilkan wheel berisi `agyswap/` saja.
- Rilis lewat tag `v*`: `.github/workflows/publish.yml` menjalankan test, build, publish ke PyPI (trusted publishing), dan membuat GitHub release. CI (`ci.yml`) menjalankan ruff, pytest, dan build di Python 3.12–3.14.
- `README.md` mengikuti format README user: banner `.github/assets/banner.webp`, tagline, badge author, versi, pip, dan build, lalu Description, Status, Techstacks, Installation, Configuration, Usage, Development, Testing, Deployment, Architecture, Credit, dan Member.

## Code Style

Ikuti gaya `src/agyswap/cli.py`: fungsi kecil di level modul, `cmd_*` mengembalikan pesan (dicetak oleh `main`, ditampilkan sebagai notify oleh TUI), error untuk user lewat `SwapError`/`UsageError`, komentar hanya untuk alasan yang tidak terlihat dari kode.

```python
def cmd_remove(target: str) -> str:
    with locked_store() as store:
        slot = find_slot(store, target)
        email = store["accounts"].pop(slot)["email"]
        save_store(store)
    return f"Removed account {slot}: {email}"
```

Ruff: line-length 120, rule `E F W I UP B`, `docs/`, `skills/`, dan `graphify-out/` dikecualikan.

## Testing Strategy

- pytest di `tests/test_swap.py`, 7 test. Keyring dipalsukan (`read_token`/`write_token`/`agy_running` di-monkeypatch), store di `tmp_path` lewat `AGYSWAP_HOME`, jaringan dipalsukan lewat `usage._post` atau `cli.account_usage`.
- Yang dibuktikan: round-trip add/switch/remove dengan token hasil refresh tetap tersimpan; switch ditolak saat agy berjalan; email dari token rusak; pengelompokan bucket kuota; login yang belum disimpan diselamatkan sebelum switch; `--slot` tidak menimpa akun lain; refresh usage tidak membatalkan remove yang terjadi bersamaan.
- Cek manual oleh user (sudah dilakukan 2026-10-06): add dua akun sungguhan lewat `/logout` → login → `add`, lalu switch bolak-balik tanpa login ulang.
- Belum dites otomatis: TUI (hanya pilot headless manual), `fresh_token` terhadap server sungguhan, dan `secret-tool` sungguhan.

## Boundaries

- **Always:** jalankan ruff dan pytest sebelum commit; setiap perubahan store lewat `locked_store()`; salin token live ke slotnya sebelum switch; ikuti `architecture/OBSERVE.md` untuk semua fakta tentang agy.
- **Ask first:** menulis keyring sungguhan atau store `~/.agyswap/`; endpoint Google baru (selain refresh, `fetchAvailableModels`, `retrieveUserQuotaSummary`); dependency baru; mengubah workflow CI atau rilis; push dan tag rilis.
- **Never:** mencetak atau meng-commit token atau client secret; memanggil endpoint yang mengubah state akun; menulis keyring di luar `cmd_switch`; menyentuh Antigravity IDE; probing keyring dengan `busctl get-property` berulang.

## Success Criteria (baseline v0.1.0)

- [x] `add`, `list`, `status`, `switch`, `remove`, dan TUI berjalan seperti tabel di atas.
- [x] Switch dua akun sungguhan tanpa login ulang (diverifikasi user).
- [x] Tidak ada jalur yang menimpa login tanpa salinan, atau slot milik akun lain.
- [x] `ruff check`, `ruff format --check`, `pytest` (7), dan `uv build` lolos; wheel hanya berisi `agyswap/`, dan `twine check` lolos.
- [x] Validasi ulang dengan store sementara (agy 1.3.0): `add`, `status`, `list` berjalan tanpa error (`architecture/OBSERVE.md`, Validasi).
- [x] Kuota menampilkan window 5 jam **dan** mingguan.

## Open Questions

Diambil dari `TODO.md`; masing-masing butuh spec sendiri sebelum dikerjakan:

1. **Fitur yang belum ada:** cache dan backoff 429, auto-switch (hanya efektif di antara sesi agy), alias, disable/enable, `--strategy`, `--json`, konfirmasi `remove` di CLI, export/import, layar watch, arti `--force`, dan exit code bare non-TTY.
2. **Sesi paralel per akun (`run`).** Belum mungkin: `--gemini_dir` tidak mengisolasi token, dan path file token fallback belum terobservasi.
3. **Rilis.** Repo masih private, `agyswap-cli` belum terdaftar di PyPI, dan pending publisher belum terkonfirmasi. Banner README memakai path relatif sehingga tidak tampil di PyPI.
4. **Deskripsi proyek** menyebut rotasi otomatis dan sesi paralel sebagai target, padahal keduanya belum ada.

---

# Capability Map: semua butir `TODO.md` yang bisa dikerjakan

Ditulis lewat `/agyswap-spec kerjakan semua di TODO.md` pada 2026-10-06 (Phase 0). Butir-butir ini bisa dites dan dirilis terpisah, jadi map ini harus disetujui user dulu, sebelum spec per modul ditulis sebagai section "Spec modul: <module-id>" di file ini.

| Module id | Tanggung jawab | Bergantung pada | Butir `TODO.md` |
| --------- | -------------- | --------------- | --------------- |
| `render-polish` (selesai) | Test menjaga baris tanpa reset (tanpa spasi di ujung); lebar kolom grup dihitung dari nama grup terpanjang | — | Kualitas kode (2 butir) |
| `cli-safety` (selesai) | `remove` minta konfirmasi `y/N` di TTY (ditambah flag lewati untuk script); bare `agyswap` di luar TTY exit 2; arti `--force` diselaraskan | — | `remove` tanpa konfirmasi, bare non-TTY, arti `--force` |
| `account-flags` | Field `alias` dan `disabled` per akun di `accounts.json`; perintah `alias`, `disable`, `enable`; target switch/remove lewat alias; rotasi bare `switch` melewati akun disabled; penanda di `list` dan TUI | — | Alias, disable/enable |
| `usage-cache` | Cache kuota per akun di `~/.agyswap/` dengan umur maksimum; backoff saat 429 berdasarkan `Retry-After`; pembacaan terakhir yang valid tetap ditampilkan saat fetch gagal | — | Usage tanpa cache dan backoff |
| `switch-strategy` | `switch --strategy best\|next-available`: memilih akun dari sisa kuota (5h + mingguan), melewati akun disabled | `account-flags`, `usage-cache` | `--strategy` |
| `json-output` | `--json` untuk `list`, `status`, `switch` (envelope berversi, tanpa nilai token) | `account-flags`, `usage-cache` | `--json` |
| `export-import` | `export` / `import` akun ke file JSON 0600 (berisi refresh token; peringatan jelas), menolak menimpa akun lain tanpa `--force` | `account-flags` | export/import |
| `tui-watch` | Layar watch di TUI: kuota semua akun yang diperbarui otomatis, tanpa aksi switch | `usage-cache` | layar watch |

Build order: `render-polish`, `cli-safety` → `account-flags` → `usage-cache` → `switch-strategy`, `json-output` → `export-import` → `tui-watch`

**Di luar map** (terblokir, lihat `TODO.md`):

- Butuh observasi saat kuota benar-benar habis: `auto` dan pemisahan error kuota.
- Butuh login di sesi terisolasi: `run`.
- Butuh aksi user: rilis (repo public, PyPI, banner).
- Tidak bisa diuji di mesin ini: macOS/Windows.

**Keputusan user** (2026-10-06, "boleh, setujui"): map disetujui, dan ketiga usulan di bawah diterima seperti tertulis. Spec modul ditulis sebagai section di file ini (di bawah), mengikuti build order. Gelombang pertama: `render-polish` dan `cli-safety`.

**Keputusan yang diajukan:**

1. Arti `--force` di `switch`: berarti "lewati penyalinan token live", dengan flag baru untuk "abaikan agy yang berjalan", atau tetap seperti sekarang dan perbedaannya dicatat?
2. Nama flag untuk melewati konfirmasi `remove`: `--yes`/`-y`?
3. Format file export: JSON envelope tanpa enkripsi, dengan ekstensi `.agyswap`?

---

## Spec modul: render-polish

Module id `render-polish` dari Capability Map di atas. Tidak bergantung pada modul lain.

### Objective

Merapikan dua kekurangan render kartu akun yang ditemukan di `architecture/REVIEW.md` (Suggestion 2 dan 3):

1. **Guard `if p.reset:` belum dijaga test** (`src/agyswap/cli.py:219`). Mutasi `if True:` lolos karena test memakai `rstrip()`.
2. **Lebar kolom grup tetap 12** (`src/agyswap/cli.py:213`). Nama grup diambil dari respons `retrieveUserQuotaSummary` (`architecture/OBSERVE.md`, "Kuota per window"), dan nama yang lebih panjang dari 12 karakter akan menggeser kolom window.

Pemakai tidak melihat perubahan apa pun selama nama grup masih "Gemini" dan "Claude/GPT".

### Perilaku

- Baris bucket yang masih penuh (`reset=None`) berakhir tepat setelah persen, tanpa spasi di ujung.
- Lebar kolom grup = nama grup terpanjang di kartu itu + 2 spasi, dengan minimum 12, supaya tampilan sekarang tidak berubah. Kolom window tetap sejajar di semua baris kartu.
- `list` dan TUI berubah bersamaan, karena keduanya memakai `account_text`.

### Testing Strategy

- **Test 1:** baris bucket penuh dicek tanpa `rstrip()`, dengan `assert not line.endswith(" ")`. Mutasi `if p.reset:` → `if True:` harus membuatnya merah.
- **Test 2:** kartu dengan grup palsu bernama 20 karakter. Kolom window harus berada di posisi yang sama di semua baris, dan nama grup tidak terpotong.
- `test_account_text_groups_5h_and_weekly` yang sudah ada tetap hijau. Ini sekaligus membuktikan lebar minimum 12 tidak mengubah tampilan sekarang.

### Boundaries

- **Always:** tetap satu fungsi `account_text` untuk `list` dan TUI.
- **Never:** mengubah warna, bar, atau format reset (itu keputusan tampilan dari user, lihat `AGENTS.md`).

### Success Criteria

- [x] Test kolom lebar merah dulu, lalu hijau. Test spasi di ujung hijau sejak awal (guard sudah ada) dan dibuktikan lewat mutasi di bawah.
- [x] Mutasi `if p.reset:` → `if True:` tertangkap test.
- [x] Output `uv run agyswap list` (store sementara) tidak berubah untuk akun sungguhan.
- [x] `uv run ruff check .`, `uv run ruff format --check .`, dan `uv run pytest -q` lolos.

### Open Questions

Tidak ada.

---

## Spec modul: cli-safety

Module id `cli-safety` dari Capability Map di atas. Tidak bergantung pada modul lain.

### Objective

Mengubah tiga perilaku CLI supaya perintah yang merusak tidak jalan tanpa sengaja dan script bisa mengenali kesalahan:

1. `remove` minta konfirmasi.
2. Bare `agyswap` di luar TTY gagal dengan exit 2.
3. Arti baru `--force` di `switch`.

Keputusan user (2026-10-06, persetujuan Capability Map):

- `--force` berarti "lewati penyalinan token live", ditambah flag baru untuk "abaikan agy yang berjalan".
- Konfirmasi `remove` bisa dilewati dengan `--yes`/`-y`.

### Perilaku

| Perilaku | agyswap setelah modul ini |
| -------- | -------------------------- |
| Konfirmasi `remove` | Peringatan kalau akun itu aktif, lalu `Remove account N (email)? [y/N] `. Jawaban selain `y`/`yes` → `Cancelled`, exit 0, store tidak berubah |
| Melewati konfirmasi | `--yes`/`-y`. Tanpa TTY dan tanpa `--yes`, `remove` ditolak dengan exit 1, bukan menunggu input |
| Bare tanpa TTY | `agyswap: error: no command given — try 'agyswap --help'`, exit 2 |
| `switch --force` | **Tidak** menyalin token live ke slotnya sebelum switch. Login live yang belum disimpan **tetap** diselamatkan ke slot baru (invariant di `AGENTS.md`), jadi `--force` tidak pernah menghilangkan login |
| Mengabaikan agy yang berjalan | Flag `--ignore-running`. Tanpa flag ini, switch ditolak selama ada proses `agy` selain updater, karena agy membaca keyring sekali saat start dan menyimpan ulang token tiap jam (`architecture/OBSERVE.md`, "Proses") |

Pesan penolakan saat agy berjalan diperbarui supaya menyebut `--ignore-running`, bukan `--force`.

### Keamanan token

- `remove` hanya menghapus salinan di store. Keyring tidak disentuh, sama seperti sekarang.
- `--force` mengurangi sinkronisasi: token live yang lebih baru tidak disalin ke slotnya, sehingga slot itu memakai token lama. Karena Google tidak merotasi refresh token (`OBSERVE.md`, "Siklus token"), token lama itu tetap bisa di-refresh. Tidak ada token yang hilang.
- Login yang belum disimpan selalu diselamatkan, dengan atau tanpa `--force`.

### Dampak ke CLI dan TUI

- **CLI:**
  - `remove` mendapat `--yes`/`-y`.
  - `switch` mendapat `--ignore-running`, dan `--force` berganti arti.
  - Bare `agyswap` non-TTY sekarang exit 2.
- **TUI tidak berubah:** remove sudah memakai modal konfirmasi sendiri, dan switch di TUI tetap menolak saat agy berjalan.
- **Dokumentasi:** `README.md` (Usage) dan `AGENTS.md` (Invariants: "`--ignore-running` overrides") diperbarui.

### Testing Strategy

Semua dengan pytest, keyring palsu, dan `AGYSWAP_HOME=tmp_path`:

- `remove` tanpa `--yes`, input `n` (via `monkeypatch` pada `builtins.input` dan `sys.stdin.isatty`) → `Cancelled`, akun tetap ada.
- `remove` dengan input `y` → akun terhapus. Dengan `--yes` → terhapus tanpa prompt.
- `remove` tanpa TTY dan tanpa `--yes` → exit 1 dan akun tetap ada.
- `main([])` saat non-TTY → `SystemExit` dengan kode 2 dan pesan `no command given`.
- `switch --ignore-running` saat `agy_running()` bernilai `True` → switch berhasil. `switch --force` saat agy berjalan tetap ditolak.
- `switch --force`: token live yang lebih baru **tidak** disalin ke slotnya (slot memakai token lama), dan login yang belum disimpan tetap diselamatkan.

### Boundaries

- **Always:** prompt hanya di TTY; script memakai `--yes`.
- **Ask first:** mengubah arti flag lain di luar modul ini.
- **Never:** `--force` atau `--ignore-running` yang melewati penyelamatan login yang belum disimpan.

### Success Criteria

- [x] Test baru merah dulu, lalu hijau, kecuali `test_force_still_saves_an_unstored_login` yang hijau sejak awal karena menjaga perilaku yang dipertahankan.
- [x] `uv run agyswap remove 1` di TTY bertanya dulu (dicoba user 2026-10-06: prompt `Remove account 1 (<email>)? [y/N]`, Enter → `Cancelled`);
- [x] `echo | uv run agyswap remove 1` exit 1; `uv run agyswap remove 1 --yes` langsung menghapus (diuji dengan store sementara).
- [x] `uv run agyswap < /dev/null` exit 2.
- [x] `README.md` dan `AGENTS.md` menyebut `--yes`, `--ignore-running`, dan arti baru `--force`.
- [x] `uv run ruff check .`, `uv run ruff format --check .`, dan `uv run pytest -q` lolos.

### Open Questions

- Nama flag `--ignore-running`: setuju, atau mau nama lain (misalnya `--while-running`)?
