# Commit

Ditulis lewat `/agyswap-commit` pada 2026-10-06. Isinya penggantian nama distribusi PyPI menjadi `agyswap-cli` (PyPI menolak `agyswap` karena terlalu mirip proyek lain yang sudah ada; command dan package import tetap `agyswap`), plus catatan persiapan rilis: pending publisher PyPI dan environment `pypi` di GitHub. Commit dipecah per scope, tanpa trailer co-author atau atribusi, dan belum di-push.

## Commit yang dibuat

| Hash | Pesan | File |
| ---- | ----- | ---- |
| `59f0d5a` | `feat(package): rename distribution to agyswap-cli` | `pyproject.toml` |
| `2552843` | `feat(lock): sync lockfile with agyswap-cli` | `uv.lock` |
| `c84ccbc` | `feat(src): read version from agyswap-cli distribution` | `src/agyswap/__init__.py` |
| `d2eaa37` | `feat(workflow): update wheel check for agyswap-cli dist-info` | `.github/workflows/ci.yml` |
| `e2bedf4` | `docs(project): update pip badge and install command for agyswap-cli` | `README.md` |
| `825b8ae` | `feat(skill): update ship wheel check for agyswap-cli` | `skills/agyswap-ship/SKILL.md` |
| `f05efdc` | `docs(agents): note agyswap-cli distribution and release setup` | `AGENTS.md`, `TODO.md` |
| (commit ini) | `docs(architecture): update spec and commit record for agyswap-cli` | `architecture/SPEC.md`, `architecture/COMMIT.md` |

## Alasan pengelompokan

- Urutan konfigurasi → kode → workflow → dokumen, sama dengan commit baseline: `package` dulu (nama distribusi), lalu `lock` yang mengikutinya, `src` yang membaca versi dari nama baru, dan `workflow` yang pengecekan wheel-nya bergantung pada nama `agyswap_cli-*.dist-info`.
- `AGENTS.md` dan `TODO.md` digabung dalam satu commit `agents`, karena keduanya mencatat hal yang sama: nama distribusi dan status persiapan rilis.
- Setiap file hanya berisi satu niat, jadi tidak perlu stage per hunk.

## File yang sengaja tidak di-commit

Tidak ada. Working tree bersih setelah commit ini. `graphify-out/` tidak dibuat ulang, karena perubahannya hanya nama distribusi dan teks.

## Hook

Tidak ada git hook. Semua commit dibuat tanpa `--no-verify`.
