---
name: agyswap-prepare
description: Rapikan repo agyswap sebelum commit atau sesi berikutnya — perbarui TODO.md, selaraskan memory Claude dan Antigravity, hapus yang usang dan sisa debug, perbarui docs dan skills, jalankan formatter, linter, test, dan build, lalu graphify update dan label. Gunakan saat user meminta prepare atau bersih-bersih repo.
version: 1.0.0
---

# /agyswap-prepare

Tahap **PREPARE** dalam siklus agyswap (`/agyswap-prepare` → `/agyswap-observe` → `/agyswap-spec` → `/agyswap-plan` → `/agyswap-build` → `/agyswap-test` → `/agyswap-review` → `/agyswap-prepare` → `/agyswap-commit` → `/agyswap-ship`). Dijalankan di awal siklus sebelum merancang spec, dan setelah review untuk merapikan repo sebelum commit dan ship.

Instruksi dari user:

- Update temuan dan hapus yang sudah selesai di `TODO.md`.
- Selaraskan memory hasil Antigravity (agy/Gemini) dengan memory hasil Claude, karena user memakai dua agent.
- Hapus yang sudah usang dan sudah tidak relevan.
- Hapus sisa debug.
- Update docs, untuk developer dan untuk AI agent.
- Update skills.
- Update pengetahuan kamu.
- Jalankan linter, formatter, test, dan build, dan pastikan tidak ada error. **Special case: langsung jalankan tanpa minta izin.**
- `graphify update` dan label.

Kerjakan berurutan seperti di bawah. Mulai dengan membaca `AGENTS.md`, lalu `git status`, `git diff`, dan `git log --oneline -20` untuk tahu apa yang berubah sejak commit terakhir. Pakai `graphify query` untuk orientasi sebelum grep.

## 1. TODO.md

- Cek setiap temuan terhadap kode saat ini, jangan terhadap ingatan. Temuan yang sudah diperbaiki **dihapus**, bukan dicentang.
- Perbarui referensi `file:line` yang bergeser dan deskripsi yang tidak akurat lagi.
- Tambahkan temuan baru dari pekerjaan sejak prepare terakhir, pada tingkat keparahan yang sesuai.
- `TODO.md` hanya berisi yang masih rusak atau belum diputuskan. Rencana kerja masuk `architecture/PLAN.md`.

## 2. Selaraskan memory Claude dan Antigravity

Kedua agent tidak bisa membaca percakapan satu sama lain. Satu-satunya jalur serah terima yang dibaca keduanya adalah repo ini.

| Agent       | Lokasi memory |
| ----------- | ------------- |
| Claude Code | `~/.claude/projects/<proyek>/memory/` (folder proyek Claude Code untuk repo ini), dengan indeks di `MEMORY.md` dan satu fakta per file |
| Antigravity | Knowledge Items di `~/.gemini/antigravity-cli/knowledge/` (`index.md`, `archive/`), plus artefak per percakapan di `~/.gemini/antigravity-cli/brain/<conversation-id>/` untuk sesi terbaru di workspace ini |

Isi `brain/<conversation-id>/` sebagian besar ada di `.system_generated/logs/transcript.jsonl` (satu step per baris, `type` `USER_INPUT` atau `PLANNER_RESPONSE`). Jangan lewati folder `.system_generated/`. Cari sesi agyswap sejak prepare terakhir lewat `sqlite3 ~/.gemini/antigravity-cli/conversation_summaries.db "select conversation_id, last_modified_time, title from conversation_summaries where workspace_uris like '%agyswap%' order by last_modified_time desc"`. Lalu baca pesan user (koreksi, preferensi) dan kesimpulan akhir model (fakta repo) dengan `jq`.

Aturannya:

0. Kalau salah satu sisi kosong, atau isi keduanya tidak ada yang berbeda, **lewati langkah ini**. Jangan membuat memory, rule, atau file konfigurasi baru di sisi mana pun hanya untuk "menyamakan".
1. Baca keduanya. Kumpulkan fakta yang hanya ada di salah satu sisi.
2. **Fakta tentang repo** (konvensi, keputusan, jebakan, perintah, perilaku agy) dipindah ke `AGENTS.md`, `architecture/OBSERVE.md`, atau skill yang relevan, lalu dihapus dari memory privat. Yang ditulis di repo terbaca oleh kedua agent.
3. **Preferensi user** (gaya kerja, koreksi, hal yang disukai atau tidak) yang ada di satu memory tapi bertentangan atau hilang di memory lain yang sudah berisi, disamakan isinya.
4. Kalau kedua sisi bertentangan, cek ke kode atau ke riwayat. Yang terverifikasi dan lebih baru yang menang. Kalau tidak bisa diverifikasi, tanya user.
5. Hapus memory yang sudah salah atau tidak relevan di kedua sisi. Jangan menyalin isi percakapan mentah, dan jangan pernah menyalin nilai token.

## 3. Hapus yang usang

- Kode, file, script, dependency, atau konfigurasi yang tidak dipakai lagi. Pastikan dulu tidak ada yang mereferensikannya (`graphify query`, lalu grep) dan tidak ada di `architecture/PLAN.md`. Kalau ragu apakah sesuatu masih direncanakan, tanya dulu sebelum menghapus.
- Klaim di `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, skill, atau `architecture/*.md` yang sudah tidak benar.
- File di `architecture/` yang menggambarkan pekerjaan yang sudah lama selesai dan tidak lagi jadi serah terima.

## 4. Hapus sisa debug

- `print()` yang mencetak variabel untuk debugging. **Jangan** menghapus `print()` yang merupakan output CLI untuk user (hasil `cmd_*`, pesan `error:`).
- `breakpoint()`, `pdb`, kode yang di-comment-out, `# TODO` sementara yang sudah selesai.
- `pytest.mark.skip` atau `xfail` sementara di `tests/`.
- File coba-coba di root, `src/`, atau `tests/` yang tidak dimaksudkan untuk di-commit, termasuk harness `/tmp` yang terlanjur disalin ke repo.
- Token, refresh token, atau client secret yang tercetak ke log atau tertinggal di file. Jalankan `git grep -n -E "GOCSPX|ya29\.|1//0"` dan pastikan kosong.

## 5. Update docs

- **Untuk developer:** `README.md` (instalasi dan pemakaian untuk pemakai paket, karena ikut dipublikasikan ke PyPI) dan `CONTRIBUTING.md` (setup developer, bagian "Agent Tooling", cara rilis).
- **Untuk AI agent:** `AGENTS.md`, supaya struktur, perintah, perilaku agy, invariants, dan tooling agent sesuai kenyataan.
- **`docs/` (mirror dokumentasi resmi):** bandingkan versi di header tiap file dengan `uv.lock`. Kalau ada yang berbeda, jalankan `uv run python scripts/docs.py`. Jangan edit file di `docs/` dengan tangan.
- Jaga pasangan server gitmcp di `.mcp.json` dan file di `docs/` tetap 1:1. Kalau server ditambah atau dihapus, perbarui juga `scripts/docs.py` dan instruksi `agy mcp add` di `CONTRIBUTING.md`.

## 6. Update skills

- Periksa bagian khusus agyswap di setiap `skills/agyswap-*/SKILL.md`: perintah, path, file output, dan aturan harus sesuai repo saat ini.
- Selaraskan enam skill inti dengan upstream terbaru: jalankan `uv run python scripts/skills.py`. Script itu mengambil HEAD `addyosmani/agent-skills`, menyusun ulang `# Method` dan `# Reference`, dan memperbarui hash commit di skill dan di `AGENTS.md`. Bagian agyswap di atas `# Method` tidak disentuh. Lalu baca `git diff skills/`: kalau perubahan upstream bertentangan dengan bagian agyswap, perbarui bagian agyswap-nya, bukan bagian yang di-vendor.
- Jangan edit `# Method` atau `# Reference` dengan tangan; perubahan itu akan hilang di `scripts/skills.py` berikutnya.
- Setiap folder skill hanya berisi `SKILL.md`. Skill baru harus dicatat di `AGENTS.md`.

## 7. Update pengetahuan kamu

- Hal baru yang dipelajari di sesi ini tentang repo masuk ke `AGENTS.md` atau skill. Perilaku agy yang baru terbukti masuk ke `architecture/OBSERVE.md`. Hal tentang user masuk ke memory kedua agent (langkah 2).
- Kalau ada koreksi dari user di sesi ini, simpan sebagai memory feedback beserta alasannya.

## 8. Formatter, linter, test, build

Jalankan langsung, tanpa bertanya:

```bash
uv sync --locked
uv run ruff format .
uv run ruff check .
uv run pytest -q
uv build
```

- Perbaiki setiap error sampai semuanya hijau. Jangan pernah membungkam error dengan `# noqa`, mengubah `[tool.ruff]` supaya lebih longgar, atau menghapus dan men-skip test.
- Kalau ada error yang tidak bisa diperbaiki tanpa keputusan user, hentikan dan laporkan output persisnya.
- `dist/` hasil build di-gitignore; tidak perlu dihapus.

## 9. Graphify update dan label

1. Jalankan `graphify update .` untuk mengekstrak ulang kode ke `graphify-out/graph.json`. Perintah ini mengembalikan nama komunitas ke nama default.
2. Beri label komunitas dengan `graphify label . --backend=gemini` (atau `--backend=claude-cli` sebagai alternatif), yang memakai LLM untuk menamai setiap komunitas dan menulis ulang `GRAPH_REPORT.md` serta `graph.json`. Jangan menulis label dengan tangan.
3. Pastikan nama komunitas di `GRAPH_REPORT.md` bukan lagi `Community N` atau sekadar nama file. Kalau masih ada `Community N`, jalankan lagi dengan `--missing-only`. Kalau yang tersisa nama file, `--missing-only` tidak mengubahnya; jalankan ulang seluruhnya dengan `--backend=claude-cli`.

## 10. Ringkasan

Tutup dengan laporan singkat per langkah: temuan yang dihapus atau ditambah di `TODO.md`, memory yang dipindah atau diselaraskan, apa yang dihapus sebagai usang atau sisa debug, docs dan skills yang diubah, hasil setiap perintah di langkah 8, dan jumlah node, edge, dan komunitas dari graphify.

Tulis ringkasan yang sama ke `architecture/PREPARE.md`, menggantikan isi sebelumnya.

**Jangan commit.** Sarankan `/agyswap-commit` kalau user ingin commit.
