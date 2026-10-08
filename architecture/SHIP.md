# Ship

Ditulis lewat `/agyswap-ship` pada 2026-10-08 untuk rilis **v0.2.0**. Rilis v0.1.0 (2026-10-06, tag `v0.1.0` di `f563362`) tercatat di riwayat git file ini.

## Keputusan: GO

Semua cek otomatis lolos, dan uji manual dua akun sungguhan dilakukan user pada 2026-10-08 (lihat "Uji manual oleh user"). Tidak ada commit kode setelah `REVIEW.md`; commit setelahnya hanya catatan (`OBSERVE.md`, `TODO.md`, `SHIP.md`) dan commit rilis.

## Cek

| Cek | Hasil |
| --- | ----- |
| `git status` bersih, `master` = `origin/master` (`6d440b7`) | lolos |
| `architecture/REVIEW.md` adalah review rilis sejak `v0.1.0`, verdict Approve setelah perbaikan | lolos |
| Tidak ada commit kode setelah commit yang mencatat `REVIEW.md` (`6d440b7` = HEAD) | lolos |
| `TODO.md` tanpa temuan Critical, security Critical/High, atau "Blocker rilis" (sisa: tiga Low/pertanyaan) | lolos |
| `uv sync --locked`, `ruff check`, `ruff format --check`, `pytest` (94 passed), `uv build` | lolos |
| CI `6d440b7` (`ci.yml`, workflow yang baru di-pin) | success |
| Wheel: hanya `agyswap/` dan `agyswap_cli-*.dist-info/` | lolos |
| Sdist: `src/`, `tests/`, `README.md`, `LICENSE`, `pyproject.toml`, `uv.lock`, `.gitignore`, `PKG-INFO`; tanpa `.venv`, `docs/`, `skills/`, `architecture/`, `graphify-out/`, `accounts.json` | lolos |
| `git grep -n -E 'GOCSPX-[A-Za-z0-9_-]{20,}'` | kosong |
| Versi hanya di `pyproject.toml` (masih `0.1.0`, di-bump di commit rilis) | lolos |
| README sesuai fitur; yang belum ada (`run`, macOS/Windows) di bagian Status | lolos |
| `agy --version` = 1.3.1 = versi di `architecture/OBSERVE.md` | lolos |
| Uji manual dua akun sungguhan | lolos (user, 2026-10-08) |
| Kejelasan CLI/TUI: tombol `x` di footer; error menyebut langkah perbaikan (`agyswap enable N`, `--ignore-running`, `--force`) | lolos |

## Versi: 0.2.0 (minor)

Disetujui user 2026-10-08 ("langsung ke 0.2.0"). Commit sejak `v0.1.0`:

| Commit | Kategori |
| ------ | -------- |
| `7ec04fc feat(cli): add alias, disable, enable, auto, quota strategy, json output, export, import and usage cache, harden store writes` | **minor**: perintah dan flag baru |
| `2f27235 feat(tui): add disable and enable toggle on x` | **minor**: tombol TUI baru |
| `c686c90 feat(usage): add revoked and rate limited errors, clamp retry-after, refuse redirects and scan agy binary once` | minor (bagian dari karantina dan backoff) |
| `5c526b2 fix(tui): run actions in workers, target accounts by email and escape external text` | patch |
| `d87911b feat(package): …`, `4ea06ba feat(workflow): …` | patch: metadata, CI |
| `0784c9f feat(test): …`, `94f08a1 feat(skill): …`, `ef62a24`, `7afd229`, `a910b6a`, `281c2f1`, `6d440b7`, `b5b5111`, `01c5bfe` (docs, graph) | patch |

Perubahan perilaku yang bisa dirasakan script, sehingga minor dan bukan patch:
- `list` keluar dengan exit 1 kalau semua akun aktif error (sebelumnya selalu 0).
- Teks "Saved unstored login …" berubah.

Di 0.x, ini cukup dengan minor. Store v0.1.0 tetap terbaca tanpa migrasi.

## Uji manual oleh user

Dilakukan user 2026-10-08 dengan store asli (empat akun):

- `list`: tiga akun dengan kuota 5h/weekly. Akun 4 gagal `quota request failed (HTTP 403)`, karena Google menonaktifkan layanan untuk akun itu (`TOS_VIOLATION`, dicatat di `OBSERVE.md` dan `TODO.md`), bukan bug agyswap.
- `alias 1 satu` lalu `switch satu`, lalu rotasi `switch` (1 → 2), `add` (update di tempat), `disable 1`, dan `auto` (`is fine (max 0% used)`): semua sesuai.
- Setelah switch, `agy` `/quota` menampilkan `Account: rasvanjaya21@gmail.com` tanpa login ulang.
- `enable 1`, lalu TUI: `x` men-toggle disable/enable, `s` switch ke akun 1, dan agy masuk sebagai akun itu.
- Tidak teruji manual, tetapi dicakup unit test: pesan `No enabled account…` (masih ada akun lain yang aktif) dan alias yang bertahan setelah `add` (`add` dijalankan di akun tanpa alias).

Langkah yang direncanakan:

Pakai dua akun yang sudah ada di `~/.agyswap`. Pastikan tidak ada `agy` yang berjalan. Cadangkan dulu: `uv run agyswap export ~/agyswap-backup.agyswap`, lalu `shred -u` setelah selesai.

1. `uv run agyswap list`: kedua akun tampil dengan kuota 5h dan weekly, tanpa error.
2. `uv run agyswap alias 1 satu`, lalu `uv run agyswap switch satu`, lalu `agy` dan `/quota`: agy masuk sebagai akun 1 tanpa login ulang.
3. `uv run agyswap switch` (rotasi), lalu `agy`: agy masuk sebagai akun 2.
4. `uv run agyswap add` untuk akun yang aktif: alias tetap ada di `list`.
5. `uv run agyswap disable 1`, lalu `uv run agyswap switch`: ditolak dengan `No enabled account to switch to.`. Lalu `uv run agyswap enable 1`.
6. `uv run agyswap auto`: `is fine (max N% used)`, atau switch kalau akun aktif ≥ 90%.
7. `uv run agyswap` (TUI): `x` men-toggle disable di akun terpilih, `s` switch, lalu `agy` masuk sebagai akun yang dipilih.

## Rencana rollback

- **Pemicu:**
  - `switch` atau `auto` menulis token yang salah ke keyring.
  - `accounts.json` atau `usage.json` rusak.
  - Traceback berisi data sensitif.
  - `agy` gagal masuk setelah switch.
- **Langkah:**
  1. Yank `agyswap-cli` 0.2.0 di PyPI (versi tidak bisa dihapus atau diunggah ulang).
  2. Pemakai kembali ke versi lama: `uv tool install agyswap-cli==0.1.0`. Store v0.2.0 tetap terbaca oleh 0.1.0, yang mengabaikan field `alias`/`disabled`/`disabled_reason` dan `usage.json`.
  3. Perbaiki, lalu rilis `0.2.1`.
- **Data pemakai:** `accounts.json` tidak dimigrasi, jadi tidak ada langkah balik data. Login yang rusak dipulihkan dengan `agyswap import` dari file export, atau dengan login ulang di agy lalu `agyswap add`.
- **Waktu:** yank kurang dari 5 menit; patch mengikuti siklus normal.

## Risiko yang diterima

- `TODO.md` (Low): folder `AGYSWAP_HOME` yang sudah ada tidak dikencangkan ke 0700; `hatchling` belum di-pin persis.
- Environment `pypi` belum punya required reviewers, karena repo masih private.
- Ambang `auto` belum divalidasi dengan kuota yang benar-benar habis (`OBSERVE.md`). Threshold 90% berada di bawah titik habis.
- Repo masih private. Link GitHub, badge, dan banner di halaman PyPI memberi 404 sampai repo dijadikan public.

## Cara rilis (setelah GO)

Agent hanya membuat commit rilis. Push dan tag dijalankan user:

```bash
uv version --bump minor        # 0.1.0 -> 0.2.0
uv lock
git add pyproject.toml uv.lock
git commit -m "chore: release v$(uv version --short)"
git push
# tunggu CI hijau
git tag "v$(uv version --short)"
git push origin "v$(uv version --short)"
```

Tag `v0.2.0` memicu `publish.yml`: job `build` (cek tag sama dengan versi, test, build), lalu `publish` (trusted publishing, satu-satunya job dengan `id-token: write`), lalu `release` (GitHub release). Ini rilis pertama dengan workflow yang dipecah tiga job, jadi pantau ketiganya.

## Hasil publish

Belum. Commit rilis sudah dibuat agent; menunggu user push branch, CI hijau, lalu push tag `v0.2.0`.
