# Ship

Ditulis lewat `/agyswap-ship` pada 2026-11-02 untuk rilis **0.3.2** (sebelumnya 0.3.1 dan 0.3.0 pada 2026-10-09).

## 0.3.2 (patch)

Rilis perbaikan kompatibilitas untuk Antigravity CLI (`agy`) versi 1.4.12:
- Mendukung format token baru agy 1.4.12 di keyring (`id_token_email` sebagai ganti JWT `id_token` yang dihilangkan).
- Menambahkan auto-discovery OAuth client ID dari binary agy saat token refresh bila claim `azp` tidak ada.
- Menangani fallback graceful saat binary agy tidak ada di runner headless.
- Validasi import menerima format token baru.
- Sinkronisasi enam core skills dengan upstream `agent-skills@301b02b`.

| Commit sejak `v0.3.1` | Kategori |
| --- | --- |
| `013de39 feat(skill): sync core skills with upstream agent-skills@301b02b` | patch |
| `d761828 feat(usage): scan and try client ids from binary during token refresh` | patch |
| `0d3706d feat(cli): support agy 1.4.12 id_token_email in email extraction and import validation` | patch |
| `23acd86 feat(test): add tests for agy 1.4.12 token format, client id fallback and import` | patch |
| `8593a33 docs(agents): update pinned agent-skills commit and document agy 1.4.12 auth` | patch |
| `2b17abe docs(architecture): add observation and validation records for agy 1.4.12` | patch |
| `6606294 chore(graph): generated code graph` | patch |
| `509ab5f docs(architecture): add prepare and commit records` | patch |
| `5911e92 fix(usage): handle missing agy binary during client id discovery` | patch |
| `d44771c docs(architecture): update commit record for usage discovery fix` | patch |

Kategori tertinggi adalah **patch**: tidak ada perintah, flag, atau tombol TUI baru. Semua perubahan bersifat backward-compatible dan memperbaiki interaksi dengan agy 1.4.12. Disetujui user sebagai rilis patch.

## Keputusan: GO

Tidak ada blocker.

- `architecture/OBSERVE.md` memuat observasi penuh dan validasi live agy 1.4.12.
- `TODO.md` tidak memuat temuan Critical, security Critical/High, atau bagian "Blocker rilis". Yang tersisa hanya Low dan Info.
- Seluruh 107 test unit lolos (termasuk 3 test regresi baru).
- CI GitHub Actions untuk commit master terakhir (`d44771c`) selesai dan berstatus sukses (`41384687990`).

## Cek

| Cek | Hasil |
| --- | --- |
| `git status` | bersih sebelum release commit |
| `uv sync --locked`, `ruff check`, `ruff format --check`, `pytest` (107 passed), `uv build` | lolos |
| CI untuk `d44771c` (sudah di-push user, `origin/master` sama) | `CI: completed success` (run `41384687990`) |
| Isi wheel | hanya `agyswap/` dan `agyswap_cli-*.dist-info/` |
| Isi sdist | `.gitignore`, `LICENSE`, `PKG-INFO`, `pyproject.toml`, `README.md`, `src`, `tests`, `uv.lock`; tanpa `.venv`, `docs/`, `skills/`, `architecture/`, `graphify-out/`, `.claude/`, `.agents/`, atau `accounts.json` |
| `git grep -n -E 'GOCSPX-[A-Za-z0-9_-]{20,}'` | kosong |
| Versi | hanya di `pyproject.toml`; `__init__.py` membacanya lewat `importlib.metadata` |
| agy | `1.4.12`, sama dengan `architecture/OBSERVE.md` |
| Audit dependency | `uvx pip-audit`: `No known vulnerabilities found` |
| Uji manual user | validasi live agy 1.4.12 terverifikasi sukses (`add`, `status`, `list` dengan keyring asli) |
| Kejelasan CLI/TUI | binding terlihat di footer, error message instruktif |
| Proteksi rilis GitHub | environment `pypi` trusted publishing, ruleset `release tags` untuk `refs/tags/v*` |

## Risiko yang diterima

- Temuan Low di `TODO.md`: celah symlink `_private_dir` hanya berlaku kalau `AGYSWAP_HOME` diletakkan di bawah induk yang bisa ditulis user lain; export gagal di filesystem tanpa hard link; `b`/`u` tanpa konfirmasi.
- Windows masih berstatus tidak didukung (issue `fcntl` pada `0.3.1`).

## Rollback

Versi yang sudah terbit di PyPI tidak bisa ditimpa atau diunggah ulang. Kalau 0.3.2 bermasalah:

1. Yank `0.3.2` di PyPI (Manage project → Releases → 0.3.2 → Yank). Pemakai yang mem-pin `==0.3.2` tetap bisa memasangnya, dan `pip install agyswap-cli` kembali ke `0.3.1`.
2. Perbaiki, lalu rilis `0.3.3` lewat siklus biasa.

Store tidak perlu dimigrasi: `0.3.1` membaca store dari `0.3.2` apa adanya.

## Perintah rilis

Commit rilis (`chore: release v0.3.2`) dibuat agent. Selanjutnya dijalankan user:

```bash
git push
# tunggu CI hijau
git tag v0.3.2
git push origin v0.3.2
# setujui job publish di tab Actions (environment pypi)
```

---

## Rilis Sebelumnya: 0.3.1 (patch)

Tag `v0.3.0` sudah di-push di `e66a5b6` sebelum commit README Discussions (`cf118af`) masuk, sehingga README di 0.3.0 tidak memuat badge dan link Discussions. Tag `v0.3.0` dilindungi ruleset (tidak bisa dihapus atau dipindah), jadi perubahan itu dirilis sebagai **0.3.1**.

| Versi | Tag | Workflow `Publish to PyPI` | GitHub release | PyPI |
| --- | --- | --- | --- | --- |
| 0.3.0 | `v0.3.0` → `e66a5b6` | `completed success` | `v0.3.0`, 2026-10-09T11:53:33Z | wheel dan sdist; deskripsi tanpa Discussions |
| 0.3.1 | `v0.3.1` → `8c27060` | `completed success` | `v0.3.1` (Latest), 2026-10-09T11:56:17Z | wheel dan sdist; deskripsi dengan Discussions |
