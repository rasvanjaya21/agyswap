# Spec: agyswap (as-built, v0.2.0)

Ditulis lewat `/agyswap-spec` (diisi dari state saat ini) pada 2026-10-06, dan diperbarui di siklus berikutnya setelah prepare dan observe: spec "as-built", disusun dari kode, `AGENTS.md`, `architecture/OBSERVE.md`, `architecture/REVIEW.md`, dan `TODO.md`, tanpa sesi tanya jawab. Spec ini jadi baseline; fitur berikutnya ditulis sebagai spec baru di atasnya. Diselaraskan dengan v0.2.0 pada 2026-10-08; detail fitur v0.2.0 ada di "Gelombang 2026-10-08" di bawah.

## Objective

agyswap mengganti akun Google yang dipakai **Antigravity CLI (`agy`)** tanpa login ulang, dan menampilkan kuota setiap akun.

- **Pemakai:** orang yang memakai `agy` dengan lebih dari satu akun Google, dan ingin berpindah akun saat kuota satu akun menipis.
- **Di luar scope:** Antigravity IDE, Gemini CLI, Gemini Code Assist, dan produk Google AI lain.

User story yang sudah terpenuhi:

1. Sebagai pemakai agy, saya menyimpan akun yang sedang login (`agyswap add`), lalu `/logout` di agy, login akun lain, dan menyimpannya juga.
2. Saya berpindah akun dengan `agyswap switch` (rotasi), `agyswap switch 2`, atau `agyswap switch email`, lalu agy berikutnya masuk sebagai akun itu tanpa login ulang.
3. Saya melihat kuota setiap akun (`agyswap list`) atau lewat dashboard interaktif (`agyswap`).
4. Saya menghapus akun yang tidak dipakai (`agyswap remove`).
5. Saya menamai akun (`alias`), mengeluarkannya dari rotasi (`disable`/`enable`), memilih akun dari sisa kuota (`switch --strategy`, `auto`), membaca keadaan dari script (`--json`), dan memindahkan akun ke mesin lain (`export`/`import`).

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
- agyswap menyimpan salinan token per akun di `~/.agyswap/accounts.json` (`{"accounts": {"<slot>": {"email", "token", "alias"?, "disabled"?, "disabled_reason"?}}}`), mode 0600, ditulis atomik. Kuota terakhir per email ada di `usage.json` (tanpa token). Lokasinya bisa diganti dengan `AGYSWAP_HOME`.
- Setiap perubahan store lewat `locked_store()` (flock `~/.agyswap/.lock`).

### Perintah

| Perintah | Perilaku |
| -------- | -------- |
| `add [--slot N]` | Menyimpan login agy yang aktif. Akun yang sudah ada diperbarui di tempat. `--slot` wajib angka ≥ 1, ditolak kalau slot berisi akun lain, dan memindahkan akun yang sama ke slot baru. Gagal dengan pesan jelas kalau agy belum login |
| `list` / `ls` | Kartu per akun: slot, email, `● active`, satu bar per bucket kuota (persen terpakai, hitung mundur reset). Token akun tidak aktif yang kedaluwarsa di-refresh di memori lalu digabung ke store |
| `status` | Email akun aktif dan slotnya, atau keterangan bahwa login itu belum disimpan |
| `switch [N\|email\|alias]` | Tanpa target: rotasi ke slot berikutnya yang tidak disabled; `--strategy best\|next-available [--threshold N]` memilih dari kuota. Ditolak kalau ada proses `agy` selain updater (`--ignore-running` untuk memaksa); `--force` melewati penyalinan token live ke slotnya. Sebelum menulis keyring: token live disalin ke slotnya, dan login yang belum disimpan otomatis disimpan ke slot baru |
| `remove` / `rm` | Menghapus akun dari store. Di TTY bertanya `[y/N]` (peringatan kalau akun aktif); tanpa TTY wajib `--yes`/`-y` |
| `alias`, `disable`, `enable` | Nama pendek unik; akun disabled dilewati rotasi, strategy, dan `auto`, dan kuotanya tidak di-fetch |
| `auto [--threshold N] [--strategy …]` | Sekali jalan: pindah dari akun aktif kalau ≥ threshold (default 90%) atau disabled |
| `export <file>` / `import <file>` | File 0600 berisi refresh token; import memvalidasi seluruh file dan tidak menulis keyring |
| `--json` | `list`, `status`, `switch`, `auto`: satu objek JSON `"version": 1`, tanpa token |
| bare `agyswap` | TTY: membuka TUI. Bukan TTY: `no command given`, exit 2 |

### Kuota

- Sumber: `POST daily-cloudcode-pa.googleapis.com/v1internal:retrieveUserQuotaSummary`, satu `Pool` per bucket: grup (`Gemini`, `Claude/GPT`) × window (`5h`, `weekly`). Kartu menampilkan nama grup sekali, lalu baris `5h` dan `weekly`; bucket yang masih penuh tanpa hitung mundur reset.
- Refresh token lewat `oauth2.googleapis.com/token`, dengan client ID dari claim `azp` dan client secret yang dibaca dari binary `agy` saat runtime.
- Semua request memakai User-Agent `antigravity` dan timeout 20 detik.

### TUI

- Tema pitch black. Judul `agyswap - Antigravity CLI Accounts Swap` di tengah.
- Kartu akun: kartu terpilih berlatar biru `#0178d4`, `● active` oranye `#ffa62b`, bar hijau/kuning/merah sesuai pemakaian.
- Footer abu gelap `#141414` dengan badge key oranye, sejajar dengan baris status (jumlah akun, jam update, interval refresh 2 menit).
- Tombol: `enter`/`s` switch, `a` add, `d` remove (konfirmasi `y`/`n`), `x` disable/enable, `r` refresh, `j`/`k`, `q`. Command palette dimatikan.
- Refresh kuota dan semua aksi berjalan di worker thread, tidak memblokir UI; aksi menargetkan akun lewat email.

### Distribusi dan dokumentasi

- Nama paket PyPI `agyswap-cli` (0.1.0 sudah terbit; `agyswap` ditolak PyPI karena terlalu mirip proyek lain), command tetap `agyswap`, versi hanya di `pyproject.toml`. `uv build` menghasilkan wheel berisi `agyswap/` saja.
- Rilis lewat tag `v*`: `.github/workflows/publish.yml` menjalankan test, build, publish ke PyPI (trusted publishing), dan membuat GitHub release. CI (`ci.yml`) menjalankan ruff, pytest, dan build di Python 3.12–3.14.
- `README.md` mengikuti format README user: banner (URL absolut ke `.github/assets/banner.webp` supaya tampil di PyPI), tagline, badge author, pip, dan build, lalu Description, Status, Techstacks, Installation, Configuration, Usage, Development, Testing, Deployment, Architecture, Credit, dan Member.

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

Yang tersisa ada di `TODO.md`:

1. **Sesi paralel per akun (`run`).** Belum mungkin: `--gemini_dir` tidak mengisolasi token, dan path file token fallback belum terobservasi.
2. **Rilis 0.2.0.** Repo masih private; required reviewers untuk environment `pypi` baru bisa diaktifkan setelah public.
3. **`auto` saat tidak ada yang login** langsung switch ke akun terbaik; belum diputuskan apakah itu yang diinginkan.

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
| `quarantine` (2026-10-08) | Akun yang refresh token-nya ditolak `invalid_grant` otomatis ditandai `disabled` dengan alasan `token revoked`; `add` ulang menghapus tanda itu | `account-flags` | Akun refresh token mati belum dikarantina |
| `auto` (2026-10-08) | `agyswap auto` sekali jalan: kalau akun aktif terpakai ≥ threshold di window mana pun, switch ke akun lain lewat strategy | `switch-strategy`, `quarantine` | `auto` |

Build order: `render-polish`, `cli-safety` → `account-flags` → `usage-cache`, `quarantine` → `switch-strategy`, `json-output` → `auto`, `export-import` (`tui-watch` dibatalkan 2026-10-08)

**Di luar map** (terblokir, lihat `TODO.md`):

- Isi `retrieveUserQuotaSummary` saat bucket habis belum terobservasi (`OBSERVE.md`). `auto` tidak bergantung padanya: threshold di bawah 100% dan fraction yang hilang sudah dihitung habis.
- Butuh login di sesi terisolasi: `run`.
- Butuh aksi user: rilis (repo public, PyPI, banner).
- Tidak bisa diuji di mesin ini: macOS/Windows.

**Keputusan user** (2026-10-06, "boleh, setujui"): map disetujui, dan ketiga usulan di bawah diterima seperti tertulis. Spec modul ditulis sebagai section di file ini (di bawah), mengikuti build order. Gelombang pertama: `render-polish` dan `cli-safety`.

**Keputusan yang diajukan:**

1. Arti `--force` di `switch`: berarti "lewati penyalinan token live", dengan flag baru untuk "abaikan agy yang berjalan", atau tetap seperti sekarang dan perbedaannya dicatat?
2. Nama flag untuk melewati konfirmasi `remove`: `--yes`/`-y`?
3. Format file export: JSON envelope tanpa enkripsi, dengan ekstensi `.agyswap`?

---

# Gelombang 2026-10-08: modul tersisa

Ditulis lewat `/agyswap-spec` setelah `/agyswap-observe` agy 1.3.1. Keputusan user (2026-10-08):

- `auto` adalah perintah sekali jalan (`agyswap auto`), bukan wrapper atau daemon.
- Akun dianggap hampir habis kalau terpakai **≥ 90%** di window mana pun (5h atau mingguan, grup mana pun); bisa diubah dengan `--threshold`.
- Akun dengan `invalid_grant` otomatis ditandai `disabled`.
- Semua modul tersisa masuk gelombang ini, dengan build order dari map di atas.

Format export mengikuti usulan yang disetujui 2026-10-06: JSON envelope tanpa enkripsi, ekstensi `.agyswap`.

Fakta agy yang dipakai (semua dari `architecture/OBSERVE.md`, agy 1.3.1): agy membaca keyring sekali saat start, jadi switch hanya efektif di antara sesi ("Proses"); kuota dari `retrieveUserQuotaSummary` per akun dengan window `5h` dan `weekly` ("Kuota per window"); fraction yang hilang dihitung habis; kuota habis berarti agy berhenti dengan `RESOURCE_EXHAUSTED (code 429)` ("Host dan rate limit"); refresh token tidak dirotasi ("Siklus token").

## Bentuk store

`accounts.json` mendapat field opsional per akun. Store lama tetap terbaca tanpa migrasi; field yang tidak ada berarti nilai default.

```json
{"accounts": {"1": {"email": "a@x.com", "token": "<blob keyring>", "alias": "work", "disabled": true, "disabled_reason": "token revoked"}}}
```

| Field | Default | Arti |
| ----- | ------- | ---- |
| `alias` | tidak ada | Nama pendek unik (tanpa membedakan huruf besar), bukan angka saja, tanpa `@` |
| `disabled` | `false` | Akun dilewati rotasi, strategy, dan `auto`; kuotanya tidak di-fetch |
| `disabled_reason` | tidak ada | `manual` (dari `disable`) atau `token revoked` (dari `quarantine`) |

Cache kuota disimpan terpisah di `~/.agyswap/usage.json` (tanpa token, mode 0600, lewat `locked_store()` yang sama).

## Spec modul: account-flags

### Objective

Pemakai dengan banyak akun bisa menamai akun dan mengeluarkan akun dari rotasi tanpa menghapusnya.

### Perilaku

| Perintah | Hasil |
| -------- | ----- |
| `agyswap alias <target> <nama>` | Set alias. Ditolak (exit 1) kalau nama sudah dipakai akun lain, berupa angka saja, atau berisi `@` |
| `agyswap alias <target>` | Hapus alias |
| `agyswap disable <target>` | `disabled: true`, `disabled_reason: manual` |
| `agyswap enable <target>` | Hapus `disabled` dan `disabled_reason` |
| Target di semua perintah | slot, email, atau alias (urutan pencocokan itu) |
| Bare `switch` | Rotasi melewati akun disabled. Kalau semua akun lain disabled: `No enabled account to switch to`, exit 1 |
| `switch <akun disabled>` | Ditolak: `Account N is disabled (<alasan>). Run agyswap enable N first.`, exit 1 |
| `list` / TUI | Alias tampil setelah email (`a@x.com (work)`). Akun disabled tampil redup dengan `disabled: <alasan>`, tanpa bar kuota |
| TUI | Tombol `x` men-toggle disable/enable akun terpilih (target lewat email) |

Akun aktif boleh di-disable; itu hanya mengeluarkannya dari rotasi berikutnya.

### Keamanan token

Tidak ada token yang dibuat, dihapus, atau ditulis ke keyring. Semua mutasi lewat `locked_store()`.

### Testing Strategy

pytest dengan keyring palsu: alias set/clear/bentrok/angka/`@`; target lewat alias di `switch` dan `remove`; rotasi melewati akun disabled; switch eksplisit ke akun disabled ditolak; store lama tanpa field baru tetap jalan; `account_text` menampilkan alias dan `disabled`; tombol `x` di TUI memanggil disable/enable dengan email.

### Success Criteria

- [x] Perintah dan perilaku di tabel di atas lolos test.
- [x] Store v0.1.0 terbaca tanpa perubahan.

## Spec modul: usage-cache

### Objective

Kuota tetap terlihat saat fetch gagal, dan agyswap berhenti memanggil Google sementara setelah 429.

### Perilaku

- Setiap fetch yang berhasil menyimpan `{fetched_at, pools}` per email ke `usage.json`.
- Kalau fetch gagal, baris menampilkan pembacaan terakhir dengan penanda `stale, <umur> ago` di samping error.
- 429 dari `retrieveUserQuotaSummary` menyimpan `retry_at`: header `Retry-After` (detik atau tanggal HTTP) kalau ada, kalau tidak sekarang + 5 menit. Sampai `retry_at`, akun itu tidak di-fetch; barisnya menampilkan cache dan `rate limited, retry in <m>m`.
- Akun disabled tidak di-fetch.
- Entri untuk email yang sudah tidak ada di store dibuang saat ditulis.
- Tidak ada umur maksimum untuk dipakai sebelum fetch: `list` dan TUI tetap fetch setiap kali (kecuali backoff). Cache hanya pengganti saat gagal dan sumber data untuk strategy.

### Keamanan token

`usage.json` tidak berisi token. Ditulis atomik 0600 seperti `accounts.json`.

### Testing Strategy

`account_usage` palsu: fetch sukses menulis cache; fetch gagal menampilkan cache + `stale`; 429 dengan dan tanpa `Retry-After` menyetel `retry_at` dan melewati fetch berikutnya; akun disabled tidak memanggil fetch; `usage.json` tanpa substring token.

### Success Criteria

- [x] Perilaku di atas lolos test, dan `list` dengan jaringan mati menampilkan angka terakhir.

## Spec modul: quarantine

### Objective

Akun yang refresh token-nya sudah dicabut berhenti dipilih secara otomatis.

### Perilaku

- `usage.fresh_token` melempar `TokenRevoked` (subclass `UsageError`) untuk `invalid_grant`; pesannya tetap `token revoked, sign in with agy again and agyswap add`.
- Di merge `collect_usage` (di bawah lock), akun yang mendapat `TokenRevoked` ditandai `disabled: true`, `disabled_reason: token revoked`, **hanya kalau** token di store masih sama dengan yang di-fetch (kalau user sudah `add` ulang di tengah jalan, tanda tidak dipasang).
- `add` untuk akun yang `disabled_reason: token revoked` menghapus tanda itu, karena tokennya baru. `disabled_reason: manual` tetap.

Kode `invalid_grant` untuk token yang dicabut belum pernah terobservasi (`OBSERVE.md`, "Belum terobservasi"); spec ini mengikuti respons OAuth standar dan dicek ulang di B (Validasi) saat terjadi.

### Testing Strategy

`_post` palsu mengembalikan `invalid_grant`: akun jadi disabled; token yang diganti di tengah fetch tidak ditandai; `add` ulang menghapus tanda `token revoked` tapi tidak `manual`.

### Success Criteria

- [x] Perilaku di atas lolos test.

## Spec modul: switch-strategy

### Objective

Switch memilih akun yang masih punya kuota, bukan sekadar akun berikutnya.

### Perilaku

- `agyswap switch --strategy next-available` → akun berikutnya dalam urutan rotasi yang **memenuhi syarat**.
- `agyswap switch --strategy best` → akun yang memenuhi syarat dengan pemakaian tertinggi paling rendah (`max(used)` di keempat bucket); seri diputus dengan nomor slot terkecil.
- Memenuhi syarat: tidak disabled, bukan akun aktif, kuota terbaca (fetch atau cache yang masih valid), dan semua bucket `used < threshold`.
- `--threshold <persen>` (default `90`, 1–100) berlaku untuk keduanya.
- Tidak ada yang memenuhi syarat: `No account below 90% usage`, exit 1, keyring tidak disentuh.
- `--strategy` tidak boleh dipakai bersama `<target>` (argparse error, exit 2).
- Tanpa `--strategy`, perilaku `switch` tidak berubah (selain melewati akun disabled).
- Semua invariant `switch` tetap: tolak saat agy berjalan, simpan login yang belum disimpan, salin token live.

### Testing Strategy

Kuota palsu untuk tiga akun: `best` memilih pemakaian terendah, `next-available` melewati akun ≥ threshold dan akun disabled, seri ke slot terkecil, tidak ada kandidat → exit 1 tanpa menulis keyring, `--strategy` + target → exit 2.

### Success Criteria

- [x] Perilaku di atas lolos test.

## Spec modul: auto

### Objective

Satu perintah yang bisa dijalankan sebelum `agy` (`agyswap auto && agy`) supaya sesi berikutnya tidak mulai di akun yang hampir habis.

### Perilaku

- `agyswap auto [--threshold N] [--strategy best|next-available]` (default `best`, `90`).
- Akun aktif `used < threshold` di semua bucket → `Account N (email) is fine (max X% used)`, exit 0, tidak ada switch.
- Akun aktif ≥ threshold di bucket mana pun → switch lewat strategy, cetak `Switched to account M: email (max Y% used)`, exit 0.
- Tidak ada kandidat → `No account below N% usage; staying on account N`, exit 1.
- Kuota akun aktif tidak terbaca (error dan tidak ada cache) → tidak switch, exit 1.
- agy sedang berjalan → ditolak seperti `switch` (exit 1); `--ignore-running` tersedia.
- Akun aktif yang belum disimpan → diselamatkan ke slot baru, sama seperti `switch`.
- Tidak ada cooldown terpisah: setiap `auto` membaca kuota baru, dan akun yang baru ditinggalkan tidak dipilih lagi selama masih ≥ threshold.

### Testing Strategy

Kuota palsu: aktif di bawah threshold → no-op tanpa menulis keyring; aktif di atas → switch ke akun yang dipilih strategy; tanpa kandidat → exit 1; error fetch akun aktif → exit 1 tanpa switch; agy berjalan → exit 1.

### Manual check oleh user

Dengan dua akun sungguhan, saat satu akun ≥ 90%: `agyswap auto` lalu `agy` masuk sebagai akun lain.

### Success Criteria

- [x] Perilaku di atas lolos test.
- [ ] Manual check di atas dilakukan user.

## Spec modul: json-output

### Objective

Script dan status bar bisa membaca keadaan agyswap tanpa mem-parse teks.

### Perilaku

`--json` pada `list`, `status`, `switch`, dan `auto`. Output satu objek JSON di stdout dengan `"version": 1`. Error (`SwapError`) dengan `--json` dicetak sebagai `{"version": 1, "error": "<pesan>"}` di stdout, exit code tetap.

```json
{"version": 1, "accounts": [{"slot": "1", "email": "a@x.com", "alias": "work", "active": true, "disabled": false, "disabled_reason": null, "error": null, "stale": false, "pools": [{"group": "Gemini", "window": "5h", "used": 0.12, "reset": "2026-10-08T18:54:30+00:00"}]}]}
{"version": 1, "email": "a@x.com", "slot": "1"}
{"version": 1, "switched": true, "slot": "2", "email": "b@x.com", "saved_slot": null}
```

`status` saat tidak login: `{"version": 1, "email": null, "slot": null}`. `auto` memakai bentuk `switch` ditambah `"max_used"`.

### Keamanan token

Tidak ada field token di output mana pun; test memeriksa substring refresh token tidak muncul.

### Testing Strategy

`json.loads` untuk setiap perintah; bentuk key; error sebagai JSON; tidak ada substring token.

### Success Criteria

- [x] Perilaku di atas lolos test.

## Spec modul: export-import

### Objective

Memindahkan akun ke mesin lain atau mencadangkannya tanpa login ulang.

### Perilaku

- `agyswap export <file>` menulis `{"format": "agyswap-export", "version": 1, "accounts": [{"email", "alias", "disabled", "disabled_reason", "token"}]}` dengan mode 0600 dan `O_EXCL`; file yang sudah ada ditolak kecuali `--force`. Ekstensi `.agyswap` disarankan, tidak diwajibkan.
- Untuk akun aktif, token yang diekspor adalah salinan keyring (yang terbaru), tanpa mengubah store atau keyring.
- Peringatan di stderr: `<file> holds refresh tokens: anyone with it can use these accounts.`
- `agyswap import <file>`: email baru masuk ke slot berikutnya; email yang sudah ada dilewati (`skipped a@x.com (already stored)`) kecuali `--force`, yang mengganti token dan field-nya tetapi mempertahankan nomor slot. Akhirnya `Imported N, skipped M`.
- Entri yang `email`-nya tidak sama dengan claim `email` di token-nya, atau formatnya salah, ditolak seluruhnya sebelum ada yang ditulis (exit 1).
- `import` tidak pernah menulis keyring.

### Keamanan token

File export berisi refresh token tanpa enkripsi (keputusan 2026-10-06). Ditulis 0600 dengan `O_EXCL`/`O_NOFOLLOW`. Tidak ada token di stdout atau stderr.

### Testing Strategy

Round-trip export → store kosong → import; mode 0600; tolak menimpa tanpa `--force`; akun aktif memakai token keyring; skip dan `--force` saat import; email tidak cocok → seluruh import ditolak; keyring palsu tidak ditulis.

### Success Criteria

- [x] Perilaku di atas lolos test.

## Spec modul: tui-watch

### Objective

Disetujui di map 2026-10-06 sebagai "kuota semua akun yang diperbarui otomatis, tanpa aksi switch". Dashboard sekarang sudah melakukan itu setiap 2 menit, jadi yang tersisa hanyalah mode yang tidak bisa mengubah apa pun.

### Perilaku

- `agyswap tui --watch` (dan bare `agyswap --watch` di TTY) membuka dashboard yang sama tanpa binding `s`/`enter`, `a`, `d`, `x`; footer hanya `r` dan `q`.
- Interval refresh `--interval <detik>` (default 120, minimum 30) berlaku untuk dashboard biasa dan watch.

### Testing Strategy

`run_test` dengan `--watch`: menekan `s`, `a`, `d`, `x` tidak memanggil `cmd_*`; footer hanya `r` dan `q`; interval diteruskan ke `set_interval`.

### Success Criteria

- [ ] Dibatalkan 2026-10-08 (tidak dibangun).

## Dampak gabungan ke CLI dan TUI

- **Perintah baru:** `alias`, `disable`, `enable`, `auto`, `export`, `import`.
- **Flag baru:** `switch --strategy/--threshold`, `--json` (list, status, switch, auto), `export/import --force`, `tui --watch/--interval`.
- **TUI:** tombol `x`; alias dan status disabled di kartu; penanda `stale` dan `rate limited`.
- **Docs:** `README.md` (Usage, tabel tombol), `AGENTS.md` (Layout, Invariants untuk quarantine dan export), `TODO.md` (hapus butir yang selesai).

## Boundaries (gelombang ini)

- **Always:** semua mutasi store lewat `locked_store()`; keyring hanya ditulis oleh `switch` dan `auto`; tidak ada token di output, log, atau `usage.json`.
- **Ask first:** dependency baru; mengubah format `accounts.json` di luar field opsional di atas; mengubah default threshold.
- **Never:** `auto` yang berjalan di latar atau mengubah sesi agy yang sedang berjalan; menghapus akun secara otomatis (quarantine hanya menandai).

## Success Criteria (gelombang ini)

- [x] Semua modul lolos test masing-masing; `uv run ruff check .`, `uv run ruff format --check .`, `uv run pytest -q`, dan `uv build` lolos.
- [x] Store v0.1.0 tetap terbaca.
- [ ] Manual check `auto` oleh user (lihat modul `auto`).

## Open Questions (gelombang ini)

Dijawab user 2026-10-08 ("oke, setujui, langsung ke 0.2.0"): spec disetujui beserta rekomendasinya.

1. **`tui-watch` dihapus dari gelombang ini** (rekomendasi diterima): dashboard sudah refresh sendiri, dan `--interval` tidak dibutuhkan. Section modulnya tetap sebagai catatan, tidak dibangun.
2. **Error JSON di stdout** untuk `--json`: disetujui.
3. **Rilis:** langsung `0.2.0` (minor: perintah dan flag baru, kompatibel ke belakang). Perbaikan halaman PyPI ikut di rilis ini; tidak ada `0.1.1`.

