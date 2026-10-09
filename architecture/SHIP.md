# Ship

Ditulis lewat `/agyswap-ship` pada 2026-10-09 untuk rilis **0.3.0**.

## Keputusan: GO

Tidak ada blocker.

- `architecture/REVIEW.md` adalah review rilis (cakupan `git diff v0.2.0`) dengan keputusan "siap rilis". Laporan itu dicatat di `306d570`, dan tidak ada commit kode sesudahnya.
- `TODO.md` tidak memuat temuan Critical, security Critical/High, atau bagian "Blocker rilis". Yang tersisa hanya Low dan Info.

## Cek

| Cek | Hasil |
| --- | --- |
| `git status` | bersih |
| `uv sync --locked`, `ruff check`, `ruff format --check`, `pytest` (104 passed), `uv build` | lolos |
| CI untuk `306d570` (sudah di-push user, `origin/master` sama) | `CI: completed success` (`gh run list`) |
| Isi wheel | hanya `agyswap/` dan `agyswap_cli-*.dist-info/` |
| Isi sdist | `.gitignore`, `LICENSE`, `PKG-INFO`, `pyproject.toml`, `README.md`, `src`, `tests`, `uv.lock`; tanpa `.venv`, `docs/`, `skills/`, `architecture/`, `graphify-out/`, `.claude/`, `.agents/`, atau `accounts.json` |
| `git grep -n -E 'GOCSPX-[A-Za-z0-9_-]{20,}'` | kosong |
| Versi | hanya di `pyproject.toml`; `__init__.py` membacanya lewat `importlib.metadata` |
| agy | `1.3.1`, sama dengan `architecture/OBSERVE.md` |
| Audit dependency | `uvx pip-audit`: `No known vulnerabilities found` (dijalankan saat review) |
| Uji manual user | dikonfirmasi 2026-10-09: butir 1.1–1.12 (TUI) dan 1.13 (`auto` dua akun sungguhan). Rilis ini tidak mengubah `add`, `switch`, atau format store; folder store `0700` dites otomatis. |
| Kejelasan CLI/TUI (pengganti accessibility web) | footer menampilkan `s a d x n r q m`, tombol lain ada di modal More; pesan error TUI menyebut tombol perbaikannya (`Press x on it first.`, `Press a first.`) |
| Proteksi rilis GitHub | environment `pypi` wajib disetujui `rasvanjaya21`, admin bypass mati; ruleset `release tags` aktif untuk `refs/tags/v*` (diverifikasi lewat `gh api`) |

## Versi: 0.3.0 (minor)

Kategori tertinggi adalah **minor**, karena ada tombol TUI baru yang terlihat pemakai. Tidak ada perubahan yang merusak: perintah, flag, format store, dan exit code tetap. Versi disetujui user (butir 2.1).

| Commit | Kategori |
| --- | --- |
| `7adb2c2 feat(package): pin hatchling build backend to 1.32.4` | patch |
| `2184616 feat(workflow): disable uv cache in release build` | patch |
| `46e0e7f feat(cli): tighten existing store folder to 0700 and refuse one owned by another user` | patch (hardening; folder milik user lain kini ditolak) |
| `16c84ea feat(cli): add tui wording to errors that name cli commands or flags` | patch |
| `0f8f931 feat(cli): reject control characters in imported alias and disabled reason` | patch |
| `4ce57ef feat(usage): remove cli command from revoked token message` | patch |
| `de30dd3 feat(tui): add alias, more menu with best, auto, export and import, keep cursor on its account and show loading state` | **minor** (tombol TUI baru) |
| `5f53fbd feat(test): …` | patch |
| `90a7800 docs(project): …`, `f8d3ead docs(agents): …`, `ad857aa chore(graph): …`, `306d570 docs(architecture): …` | patch |

## Risiko yang diterima

- Temuan Low di `TODO.md`: celah symlink `_private_dir` hanya berlaku kalau `AGYSWAP_HOME` diletakkan di bawah induk yang bisa ditulis user lain; export gagal di filesystem tanpa hard link; `b`/`u` tanpa konfirmasi.
- `AGYSWAP_HOME` yang sudah ada kini di-chmod `0700`. Kalau seseorang mengarahkannya ke folder bersama, izin folder itu berubah. Hal ini tercatat di README.

## Rollback

Versi yang sudah terbit di PyPI tidak bisa ditimpa atau diunggah ulang. Kalau 0.3.0 bermasalah:

1. Yank `0.3.0` di PyPI (Manage project → Releases → 0.3.0 → Yank). Pemakai yang mem-pin `==0.3.0` tetap bisa memasangnya, dan `pip install agyswap-cli` kembali ke `0.2.0`.
2. Perbaiki, lalu rilis `0.3.1` lewat siklus biasa.

Store tidak perlu dimigrasi: `0.2.0` membaca store dari `0.3.0` apa adanya.

## Perintah rilis

Commit rilis (`chore: release v0.3.0`, berisi `pyproject.toml` dan `uv.lock`) dibuat agent. Selanjutnya dijalankan user:

```bash
git push
# tunggu CI hijau
git tag v0.3.0
git push origin v0.3.0
# setujui job publish di tab Actions (environment pypi)
```

## Hasil publish

Belum. Diisi setelah tag di-push dan job `publish` disetujui.
