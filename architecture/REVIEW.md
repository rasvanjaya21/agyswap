Cakupan: review rilis 0.3.0, semua perubahan sejak tag `v0.2.0` (`git diff v0.2.0`; 0 commit sejak tag, semuanya di working tree: `src/agyswap/{cli,tui,usage}.py`, `tests/test_swap.py`, `pyproject.toml`, `.github/workflows/publish.yml`, `README.md`, `AGENTS.md`, `TODO.md`, `architecture/`), ditambah isi wheel dan sdist, workflow rilis, dan audit dependency.

# Review rilis 0.3.0 (2026-10-09)

Lewat `/agyswap-review`: tiga reviewer paralel (`code-reviewer`, `security-auditor`, `test-engineer`). Agent utama memverifikasi setiap temuan Important ke atas dengan menjalankannya, lalu memperbaikinya dengan test yang merah dulu.

**Keputusan: siap rilis.** Tidak ada temuan Critical. Satu Important dan satu Medium security sudah diperbaiki. Temuan Low yang tidak diperbaiki masuk `TODO.md`.

## Diperbaiki

### Important: dua refresh yang selesai bersamaan menggandakan kartu (`src/agyswap/tui.py`, `_show`)

`_show` kini async dan menunggu `lv.clear()`/`lv.extend()`, sehingga `_show` kedua bisa masuk di antara await tersebut. `exclusive=True` tidak menghentikan thread worker yang sudah berjalan. Pemicunya: `r` ditekan dua kali, atau refresh setelah aksi bertabrakan dengan refresh 2 menit. Hasilnya `ListView` berisi 2n kartu untuk n akun sampai refresh berikutnya.

- Diverifikasi: `asyncio.gather(app._show(rows), app._show(rows))` dengan 3 akun menghasilkan `items 6 rows 3`.
- Perbaikan: isi `_show` dijalankan di bawah `asyncio.Lock` (`self._show_lock`). Placeholder toko kosong kini juga di-`await`.
- Test: `test_tui_overlapping_refreshes_never_duplicate_cards` (merah `6 == 3`, lalu hijau).

### Medium (security): export dari TUI menaruh refresh token di cwd (`tui.py`, `action_export`)

Default `agyswap-export.agyswap` relatif terhadap folder tempat TUI dijalankan. TUI yang dibuka di dalam checkout git akan menulis token ke repo itu, dan `git add -A` bisa meng-commit-nya. Toast juga menampilkan path relatif, dan peringatan stderr `cmd_export` ditelan Textual.

- Perbaikan:
  - Default `~/agyswap-export.agyswap`.
  - Path dikirim absolut (`_abspath`), jadi toast menunjukkan lokasi sebenarnya.
  - Pesan sukses TUI menambahkan `It holds refresh tokens; keep it private.` (`_export`).
- Nama file tetap keputusan user; hanya lokasinya yang berubah.
- Test: `test_tui_alias_best_auto_export_import_reach_their_commands` (default dan `~` diekspansi), `test_tui_best_and_auto_use_the_cli_defaults_and_messages` (pesan `_export`).

### Low (security): escape sequence dari file import (`cli.py`, `_valid_entry`, `_valid_alias`, `cmd_import`)

`disabled_reason` dan `alias` dari file import hanya dicek tipenya. Escape ESC/OSC/CSI dari file buatan orang lain sampai ke terminal setiap kali `list` dijalankan, karena Rich hanya membuang BEL. Laporan `alias … dropped` juga mencetak alias mentah.

- Perbaikan: helper `_printable` (tanpa karakter kontrol) dipakai untuk email, `disabled_reason`, dan alias. Laporan `alias … dropped` kini memakai `{alias!r}`.
- Test: `test_import_rejects_malformed_entries` (escape lewat `disabled_reason`), `test_import_drops_invalid_alias_and_keeps_own_alias_on_force` (alias berisi escape dibuang, dan stdout tanpa `\x1b`).

### Low (security): cache `setup-uv` di job build rilis (`.github/workflows/publish.yml`)

`setup-uv` v6 menyalakan cache secara default, sehingga build tag bisa memulihkan cache dari push ke `master`.

- Perbaikan: `enable-cache: false` di job `build`.

### Celah test (dari `test-engineer`, mutasi yang hidup)

Setiap butir di bawah kini punya test, dan mutannya dibuktikan mati (18/18, lihat "Verifikasi"):

- Tombol baris saat toko kosong: `test_tui_row_keys_do_nothing_on_an_empty_store`. Mutasi yang membuang `if not row: return` di `n` membuat TUI crash.
- `tui=` di semua pesan CLI. `test_every_cli_instruction_reachable_from_the_tui_has_a_tui_wording` membaca AST `cli.py` dan menolak `SwapError` yang menyebut `` `agyswap `` atau flag tanpa `tui=`. Allowlist hanya untuk `--slot` dan `remove --yes`. `test_errors_give_cli_and_tui_their_own_instructions` kini juga mencakup `cmd_switch_strategy` dan `cmd_auto`.
- Folder `0750` juga dikencangkan (`test_existing_store_dir_is_tightened_and_must_be_ours`).
- `test_tui_alias_best_auto_export_import_reach_their_commands` mencakup:
  - semua tombol More (`b`, `u`, prompt `e`/`i` yang benar), dan More tertutup oleh `m` maupun `esc`;
  - `.strip()`, `~` di import, path kosong tidak menjalankan apa pun, alias lama terisi, email ditampilkan apa adanya;
  - set tombol footer `a d m n q r s x`.
- Error refresh di baris status tampil tanpa markup (`test_tui_shows_refresh_error_instead_of_exiting`).

## Tidak diperbaiki (masuk `TODO.md`)

- [Low] `_private_dir` memeriksa path, bukan fd. Ada celah symlink kalau `AGYSWAP_HOME` berada di bawah folder induk yang bisa ditulis user lain. Tidak berlaku untuk `~/.agyswap` default. Diverifikasi auditor: `AGYSWAP_HOME=/tmp` (milik root) ditolak.
- [Low] Export ke filesystem tanpa hard link (vfat/exFAT) gagal di `os.link`. Error-nya bersih.
- [Info] `b`/`u` mengganti akun tanpa konfirmasi; semua invariant `switch_account` tetap berlaku.

## Suggestion yang tidak diambil

- `getattr(self, f"action_{action}")()` di `action_more` bisa diganti `run_action`. `run_action` adalah coroutine, sedangkan callback `push_screen` sinkron, dan `action` hanya berasal dari daftar tetap `More.MORE`.
- `_private_dir` men-chmod folder tanpa pesan. Diganti dengan catatan di `README.md` (`AGYSWAP_HOME` harus folder sendiri, bukan `~` atau folder bersama).

## Yang wajib dicek

- Kehilangan token: tidak ada jalur baru yang menulis keyring. `b`/`u` lewat `cmd_switch_strategy`/`cmd_auto` → `switch_account`. Export dari TUI selalu `force=False`.
- Race di store: semua mutasi baru (alias, import) lewat `locked_store()`. Dua switch paralel dari `_run` diserialkan oleh lock.
- Kebocoran secret: `git grep -n -E 'GOCSPX-[A-Za-z0-9_-]{20,}'` kosong. Sdist dan wheel bebas bentuk `GOCSPX-`, `ya29.`, `1//`. Teks `e.tui` hanya berisi path, email, dan slot.
- Asumsi agy: tidak ada yang baru; agy tetap 1.3.1 seperti di `architecture/OBSERVE.md`.
- Probing keyring: tidak ada `busctl`.
- Jaringan: tidak ada request baru.
- Thread UI: semua aksi baru lewat `_run` (thread worker). `_show` hanya menyentuh widget.
- Exception lolos dari TUI: handler baru menangkap `Exception`, dan UI dipanggil di luar blok `except`.
- Klaim dokumen: `README.md`, `AGENTS.md`, dan `architecture/SPEC.md` diperbarui untuk default export dan aturan folder.

## Rilis

- Wheel hanya berisi `agyswap/*.py` dan dist-info. Sdist berisi `src/`, `tests/`, `README`, `LICENSE`, `pyproject.toml`, `uv.lock`, `.gitignore`.
- Workflow:
  - Action di-pin ke SHA penuh.
  - `permissions: {}` di level atas `publish.yml`, dan hanya job `publish` yang mendapat `id-token: write`, di bawah environment `pypi`.
  - Trusted publishing.
  - Diverifikasi lewat `gh api`: environment `pypi` mewajibkan reviewer `rasvanjaya21` dengan admin bypass mati, dan ruleset `release tags` (aktif, `refs/tags/v*`) menolak update, delete, dan force push.
- Dependency: `uv.lock` hanya dari registry PyPI. `uvx pip-audit` → `No known vulnerabilities found`. Build backend `hatchling==1.32.4`.
- `pyproject.toml` masih `0.2.0`. `publish.yml` menolak tag `v0.3.0` sampai versinya dinaikkan di `/agyswap-ship`.

## Verifikasi

- `uv run ruff format --check .`, `uv run ruff check .`, `uv run pytest -q` → 104 passed.
- Mutasi di salinan `/tmp` (dihapus setelahnya): 18/18 mati, termasuk:
  - `n` tanpa guard, `escape(e.tui)` dibuang, `.strip()` dibuang;
  - import tanpa `~`, `if path is not None`, prefill alias, email tanpa `escape`;
  - More tanpa `m`, footer `n` disembunyikan, `MORE` ditukar;
  - default export relatif, lock `_show` dibuang;
  - `0o077` → `0o007`, `_printable` dibuang di reason dan alias, `{alias!r}`;
  - sufiks `--ignore-running` dibuang di ketiga tempat.
- Test statis `tui=` dibuktikan menggigit: membuang `tui=` dari `No accounts stored` membuatnya gagal.
