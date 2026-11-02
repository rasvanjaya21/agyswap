# Prepare

Ditulis lewat `/agyswap-prepare` pada 2026-11-02, setelah observasi dan perbaikan kompatibilitas agy 1.4.12 (`id_token_email` dan client ID discovery). Belum di-commit.

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

- `AGENTS.md` diperbarui dengan catatan format auth agy 1.4.12 (`id_token_email` dan client ID scanning).
- `architecture/OBSERVE.md` diperbarui dengan hasil observasi dan validasi live agy 1.4.12.
- `README.md` dan `CONTRIBUTING.md` sudah mutakhir.
- `docs/`: versi `textual` (8.2.8), `rich` (15.0.0), dan `pytest` (9.1.1) identik dengan `uv.lock`.
- Pasangan gitmcp di `.mcp.json` dan file di `docs/` tetap 1:1 (`textual`, `rich`, `pytest`).

## 6. Skills

- `uv run python scripts/skills.py` diverifikasi; semua core skills sinkron dengan upstream `addyosmani/agent-skills@301b02b`.
- Bagian agyswap di tiap skill tetap utuh dan tidak bertentangan.

## 7. Pengetahuan

- Format token agy 1.4.12 yang meniadakan `id_token` dan menyimpan `id_token_email` dicatat ke `architecture/OBSERVE.md` dan `AGENTS.md`.
- Penemuan 3 client IDs di binary agy untuk token refresh dicatat ke `architecture/OBSERVE.md`.

## 8. Formatter, linter, test, build

| Perintah | Hasil |
| --- | --- |
| `uv sync --locked` | lolos (15 packages audited) |
| `uv run ruff format .` | 22 file tidak berubah |
| `uv run ruff check .` | tanpa temuan (bersih) |
| `uv run pytest -q` | 107 passed in 15.29s (3 test baru untuk agy 1.4.x) |
| `uv build` | berhasil build wheel dan sdist `agyswap_cli-0.3.1` |

## 9. Graphify

`graphify update .` lalu `graphify label . --backend=gemini`: **978 node, 1698 edge, 57 komunitas**. Semua komunitas memiliki label deskriptif; tidak ada `Community N` mentah.
