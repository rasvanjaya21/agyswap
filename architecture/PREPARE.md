# Prepare

Ditulis lewat `/agyswap-prepare` pada 2026-10-06, sebelum commit dan rilis pertama. Permintaan user:

- hapus semua referensi ke proyek referensi dan pembahasan port-nya,
- pastikan tidak ada informasi pribadi atau spesifik perangkat,
- siapkan semua yang dibutuhkan untuk commit dan rilis.

## 1. TODO.md

- **Diubah:** bagian "Paritas dengan …" menjadi "Fitur yang belum ada". Rujukan ke file proyek referensi dihapus.
- **Masih berlaku:**
  - Rilis: repo private, PyPI 404, dan banner.
  - Fitur yang belum ada: cache/backoff, `auto`, alias/disable/enable/`--strategy`, `--json`, export/import, watch, dan error kuota.
  - Platform.
- Referensi `file:line` masih tepat.

## 2. Memory Claude dan Antigravity

Dilewati sesuai aturan 0, karena knowledge Antigravity kosong. Memory Claude baru: `repo-hygiene`, berisi aturan "tanpa referensi proyek referensi dan tanpa data pribadi di repo" beserta alasannya.

## 3. Yang usang, referensi proyek referensi, dan data pribadi

- **Referensi proyek referensi dan port dihapus dari:**
  - `README.md`, `AGENTS.md`, `TODO.md`
  - komentar dan docstring di `src/agyswap/cli.py`
  - bagian agyswap di skill `build`, `review`, dan `spec`
  - `architecture/OBSERVE.md`, `SPEC.md`, `PLAN.md`, `BUILD.md`, `REVIEW.md`
- **Perubahan isi:**
  - Tabel "paritas" di spec `cli-safety` menjadi tabel "Perilaku" agyswap saja.
  - Ringkasan review paritas lama di `REVIEW.md` dihapus.
- **Data pribadi atau perangkat yang dihapus:**
  - path absolut home (rujukan clone lokal, proyek saudara, folder memory Claude di skill prepare),
  - email akun Google uji (diganti `akun 1`/`akun 2` atau `<email>`),
  - versi OS, kernel, dan paket (diganti "Linux dengan GNOME Keyring 48"),
  - nama file log bertanggal, jam dengan zona waktu, dan prefix client ID agy.
- **Yang tetap**, karena identitas publik untuk rilis: handle GitHub `rasvanjaya21`, email author di `pyproject.toml` dan section Credit di README, URL repo, dan `LICENSE`.
- **Scan akhir** di luar `docs/` (dan `graphify-out/` setelah dibuat ulang) untuk nama proyek referensi, path home absolut, email akun uji, username perangkat, versi OS, zona waktu, nama log bertanggal, dan client ID: kosong.
- **Riwayat git:** commit baru memakai email noreply GitHub. Nama author di `Initial commit` yang sudah ada di remote tidak diubah, karena butuh menulis ulang riwayat.

## 4. Sisa debug

Tidak ada `breakpoint()`, `pdb`, `# TODO`, `skip`/`xfail`, atau file coba-coba. Scan secret hanya mengenai teks pola di skill prepare.

## 5. Docs

- `docs/` (textual 8.2.8, rich 15.0.0, pytest 9.1.1) sama dengan `uv.lock`, dan `.mcp.json` tetap 1:1.
- `README.md`, `AGENTS.md`, dan `CONTRIBUTING.md` sudah bebas dari referensi proyek referensi dan sesuai perilaku sekarang.

## 6. Skills

- `uv run python scripts/skills.py`: `agent-skills@1401c8b: updated nothing`. Bagian yang di-vendor tidak berubah.
- Bagian agyswap:
  - `agyswap-spec`: butir "paritas" dihapus.
  - `agyswap-build`: rujukan ke implementasi proyek referensi dihapus.
  - `agyswap-review`: butir "perbedaan perilaku dengan …" dihapus.
  - `agyswap-prepare`: path memory Claude dibuat generik.

## 7. Pengetahuan

Koreksi user dicatat sebagai memory `repo-hygiene`. Aturan "satu file per tahap" sudah ada di `AGENTS.md` sejak prepare sebelumnya.

## 8. Formatter, linter, test, build, dan persiapan rilis

| Perintah | Hasil |
| -------- | ----- |
| `uv sync --locked` | Audited 15 packages |
| `uv run ruff format .` | 20 files left unchanged |
| `uv run ruff check .` | All checks passed |
| `uv run pytest -q` | 20 passed |
| `uv build` | `agyswap-0.1.0` wheel dan sdist |
| `twine check dist/*` | PASSED (wheel dan sdist) |

- **Isi sdist:** `src/agyswap/*`, `tests/test_swap.py`, `README.md`, `LICENSE`, `pyproject.toml`, `uv.lock`, `PKG-INFO`, `.gitignore`.
- **Isi wheel:** hanya `agyswap/` dan dist-info.
- **Yang di-ignore dan tidak akan ter-commit:** `.venv`, `.claude`, `.agents`, `dist`, `__pycache__`, `.pytest_cache`, `.ruff_cache`, cache `graphify-out/`.

## 9. Graphify

- `graphify update .` lalu `graphify label . --backend=gemini`: 6 komunitas masih bernama file.
- `graphify label . --backend=claude-cli`: semua komunitas bernama.
- Hasil akhir: 701 node, 975 edge, 27 komunitas. `GRAPH_REPORT.md`, `graph.json`, dan `graph.html` bebas dari referensi proyek referensi dan path pribadi.

## Uji manual oleh user

Tidak ada.

## Blocker rilis (bukan blocker commit)

- Repo masih private.
- Pending publisher PyPI dan environment `pypi` di GitHub belum terkonfirmasi.
- Banner README memakai path relatif.

Lihat `TODO.md`, bagian Rilis.
