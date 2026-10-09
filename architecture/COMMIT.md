# Commit

Ditulis lewat `/agyswap-commit` pada 2026-10-09, setelah commit rilis `e66a5b6 chore: release v0.3.0` dan sebelum tag `v0.3.0`. Tanpa trailer co-author atau atribusi. Belum di-push.

## Commit

| Hash | Pesan | File |
| --- | --- | --- |
| `cf118af` | `docs(project): add discussions badge and link to readme` | `README.md` |
| (commit ini) | `docs(architecture): update commit record for discussions readme change` | `architecture/COMMIT.md` |

## Alasan pengelompokan

- `README.md` berisi badge `discussions` dan satu kalimat di bagian Status yang menunjuk ke GitHub Discussions (sudah aktif di repo public, `has_discussions: true`). Keduanya punya satu niat, jadi satu commit.
- Catatan commit dipisah karena scope-nya `architecture`.
- Kedua commit hanya mengubah dokumen, bukan kode (`src/`, `tests/`, `pyproject.toml`, `uv.lock`, `.github/workflows/`), sehingga review rilis dan keputusan GO di `architecture/SHIP.md` tetap berlaku. `pyproject.toml` tetap `0.3.0`, jadi `git tag v0.3.0` di commit terakhir lolos cek versi `publish.yml`. README menjadi deskripsi paket di PyPI, sehingga perubahan ini ikut tampil di 0.3.0.

Commit gelombang 0.3.0 sebelumnya (`7adb2c2`…`306d570`, `79314f4`, `e66a5b6`) tercatat di riwayat git dan di `architecture/SHIP.md`.

## Tidak di-commit

Tidak ada. Working tree bersih setelah commit ini.
