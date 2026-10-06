# Ship: v0.1.0 (rilis pertama)

Ditulis lewat `/agyswap-ship` pada 2026-10-06. Cek dijalankan pada commit `f6ebb3f` (`origin/master`); tag mengenai commit README sesudahnya (lihat "Cara rilis").

## Keputusan: **GO**

Semua cek lolos, review rilis Approve, dan tidak ada temuan Critical atau security Critical/High yang terbuka.

## Riwayat

1. **Pass ship pertama (NO-GO), di HEAD `82927ef`.** Saat itu skill ship masih menjalankan fan-out tiga reviewer, dan ditemukan tiga blocker:
   - TUI crash `DuplicateIds` pada store kosong;
   - error jaringan saat membaca respons keluar sebagai traceback, dan di TUI ikut mencetak client secret;
   - deskripsi paket mengklaim fitur yang belum ada.
2. **Ketiganya diperbaiki atau diputuskan user:**
   - `d282307`, `8583b6a`, `85be519`, `9ff4cd1`;
   - deskripsi diganti di `c0f318c` dan `8ba1a96`.
3. **Fan-out reviewer dipindah ke `/agyswap-review`** atas keputusan user (`2c8663b`). Ship sekarang hanya mengurus rilis.
4. **Review rilis seluruh paket:** dua Important (crash aksi TUI saat keyring timeout, dan exception chaining di handler refresh) diperbaiki sebelum commit. Verdict akhir **Approve** (`architecture/REVIEW.md`). Semua Suggestion masuk `TODO.md` atas keputusan user.

## Cek sebelum GO

| Cek | Hasil |
| --- | ----- |
| `git status` | bersih |
| Push dan CI | HEAD `f6ebb3f` = `origin/master`, dipush user. CI `f6ebb3f`: success |
| Review rilis | `REVIEW.md` bercakupan rilis (seluruh paket), verdict Approve, dicatat di `f6ebb3f` |
| Commit kode setelah review | 0 |
| `TODO.md` | tidak ada Critical, security Critical/High, atau "Blocker rilis" |
| `uv sync --locked` | lolos |
| `uv run ruff check .`, `ruff format --check .` | lolos (22 file) |
| `uv run pytest -q` | 28 passed |
| `uv build` | `agyswap_cli-0.1.0` wheel dan sdist |
| Isi wheel | hanya `agyswap/` dan `agyswap_cli-0.1.0.dist-info/` |
| Isi sdist | tanpa `.venv`, `docs/`, `skills/`, `architecture/`, `graphify-out/`, `.claude/`, `.agents/`, `accounts.json` |
| `git grep -n -E 'GOCSPX-[A-Za-z0-9_-]{20,}'` | kosong |
| `pip-audit` (`uv export --all-groups --no-emit-project`) | No known vulnerabilities found |
| Versi | `pyproject.toml` 0.1.0, badge README `version-0.1.0`, belum ada tag |
| agy | 1.3.0, sama dengan `architecture/OBSERVE.md` |
| Uji manual dua akun | sudah (`architecture/TEST.md`). Perubahan sejak itu hanya jalur error, tanpa perubahan `add`, `switch`, atau format store |
| Environment `pypi` | dibatasi ke tag `v*`. Required reviewers menunggu repo public |

**CLI dan TUI (pengganti accessibility):**
- Binding terlihat di footer.
- Pesan error menyebut langkah perbaikan, misalnya `secret-tool not found. Install libsecret …` dan `keyring did not answer within 30s (locked?). Unlock it and try again.`
- Error tak terduga hanya menampilkan jenisnya, tanpa traceback.

## Versi

Belum ada tag, jadi ini rilis pertama: **0.1.0**, tanpa bump dan tanpa commit rilis. Seluruh 38 commit sejak `Initial commit` membentuk kemampuan awal:

| Kategori | Commit |
| -------- | ------ |
| Kemampuan awal (minor, diserap rilis pertama) | `feat` untuk `vcs`, `package`, `lock`, `src`, `usage`, `cli`, `tui`, `test`, `workflow`, `docs`, `mcp`, `skill`; rename distribusi `agyswap-cli` |
| Perbaikan (patch) | `fix(usage)`, `fix(cli)`, `fix(tui)` |
| Docs, skill, artefak (patch) | `docs(project)`, `docs(agents)`, `docs(architecture)`, `feat(skill)`, `chore(graph)` |

Versi akhir tetap keputusan user.

## Risiko yang diterima

- Suggestion review rilis dan temuan ship lama di `TODO.md`, antara lain:
  - slot dari baris lama di TUI;
  - escape markup;
  - exit code `list`;
  - mutasi yang lolos;
  - `hatchling` belum di-pin;
  - action workflow belum di-pin ke SHA;
  - `save_store` tanpa `fsync`;
  - aksi TUI di thread UI.
- Repo masih private. Link di PyPI dan banner relatif README belum tampil sampai repo public.
- Hanya Linux. `auto` dan `run` belum ada; disebut di bagian Status README.
- Email author `rasvanjaya21@gmail.com` tampil di metadata PyPI (identitas publik, keputusan user).

## Rencana rollback

- **Pemicu:** crash pada perintah umum, kehilangan token atau store, secret tercetak, atau publish berisi file yang salah.
- **Langkah:**
  1. Yank `agyswap-cli==0.1.0` di PyPI (Manage project → Releases → Options → Yank). Versi yang sudah terbit tidak bisa ditimpa atau diunggah ulang, jadi jangan dihapus.
  2. Perbaiki lewat siklus normal, lalu rilis `0.1.1`.
  3. Di GitHub release `v0.1.0`, tambahkan catatan bahwa versi ini bermasalah. Tag tidak dihapus agent; itu keputusan user.
- **Pemakai yang sudah memasang:** `uv tool install --reinstall agyswap-cli==<versi sehat>`. Format `~/.agyswap/accounts.json` tidak berubah, jadi tidak perlu migrasi.

## Cara rilis (dijalankan user)

Tidak ada commit rilis (tanpa bump). Setelah keputusan GO, user menambahkan baris "Inspired by claude-swap" di bagian Description `README.md`. README menjadi deskripsi panjang di PyPI, jadi tag harus mengenai commit yang memuatnya, bukan `f6ebb3f`. Perubahan itu hanya docs (bukan `src/`, `tests/`, `pyproject.toml`, `uv.lock`, atau workflow), sehingga review rilis tetap berlaku.

```bash
git push
# tunggu CI hijau untuk HEAD
git tag v0.1.0
git push origin v0.1.0
```

Tag `v0.1.0` memicu `publish.yml`: cek tag sama dengan versi, test, build, publish ke PyPI lewat trusted publishing (environment `pypi`), lalu GitHub release. Pending publisher `agyswap-cli` menjadi proyek sungguhan saat publish pertama berhasil.

## Verifikasi setelah publish

- `gh run list --workflow publish.yml` → success.
- Halaman `https://pypi.org/project/agyswap-cli/0.1.0/` ada.
- Di direktori sementara: `uv tool run --from agyswap-cli==0.1.0 agyswap --help`, lalu `agyswap list` dengan akun sungguhan.

## Hasil publish

Belum. Menunggu user mendorong tag `v0.1.0`.
