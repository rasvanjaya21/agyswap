# Prepare

Ditulis lewat `/agyswap-prepare` pada 2026-10-26, setelah perbaikan sinkronisasi upstream skills dan pembersihan repo. Belum di-commit.

## 1. TODO.md

- Semua butir tetap valid dan sesuai dengan status kode saat ini (temuan review 0.3.0, fitur belum ada, dan platform Linux only / Windows rusak di 0.3.1).
- Tidak ada temuan yang dihapus atau ditambahkan di sesi ini.

## 2. Memory Claude dan Antigravity

Dilewati (aturan 0). Sisi Antigravity kosong: `~/.gemini/antigravity-cli/knowledge/` hanya berisi `knowledge.lock`. Tidak ada divergensi memory yang perlu diselaraskan.

## 3. Yang usang

Tidak ada file usang di root atau `architecture/`. Sembilan file `architecture/` sesuai siklus yang ditetapkan di `AGENTS.md`.

## 4. Sisa debug

Tidak ada sisa debug:
- tidak ada `breakpoint()`, `pdb`, `# TODO`, `skip`, atau `xfail`;
- tidak ada file coba-coba atau file sementara di root, `src/`, atau `tests/`;
- `git grep` untuk `GOCSPX-…`, `ya29.…`, dan `1//0…` kosong (tidak ada token atau secret yang bocor).

## 5. Docs

- `README.md`, `CONTRIBUTING.md`, dan `AGENTS.md` sudah mutakhir.
- `docs/`: versi `textual` (8.2.8), `rich` (15.0.0), dan `pytest` (9.1.1) identik dengan `uv.lock`.
- Pasangan gitmcp di `.mcp.json` dan file di `docs/` tetap 1:1 (`textual`, `rich`, `pytest`).

## 6. Skills

- `uv run python scripts/skills.py --check` → `up to date with agent-skills@aeac41d`.
- 6 file core skills di `skills/` sudah tersinkron dengan upstream `addyosmani/agent-skills@aeac41d`.

## 7. Pengetahuan

- Pola kegagalan mingguan CI `Skills upstream` terverifikasi bersumber dari pemeriksaan `scripts/skills.py --check`.
- Catatan observasi statis Windows agy 1.3.3 sudah tercatat di `architecture/OBSERVE.md` dan `TODO.md`.

## 8. Formatter, linter, test, build

| Perintah | Hasil |
| --- | --- |
| `uv sync --locked` | lolos (15 packages audited) |
| `uv run ruff format .` | 22 file tidak berubah |
| `uv run ruff check .` | tanpa temuan (bersih) |
| `uv run pytest -q` | 104 passed in 11.70s |
| `uv build` | berhasil build wheel dan sdist `agyswap_cli-0.3.1` |

## 9. Graphify

`graphify update .` lalu `graphify label . --backend=gemini`: **971 node, 1679 edge, 56 komunitas**. Semua komunitas memiliki label deskriptif; tidak ada `Community N` mentah.
