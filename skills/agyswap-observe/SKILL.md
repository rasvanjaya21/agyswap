---
name: agyswap-observe
description: Observasi penuh perilaku Antigravity CLI (agy) sebelum fitur agyswap dibuat, diperbaiki, atau diperbarui — lokasi dan format token, keyring, endpoint dan header, kode error, log, proses, efek login/logout, perubahan antar versi agy — lalu tulis petanya ke architecture/OBSERVE.md supaya implementasi meniru hasil observasi. Untuk fitur yang sudah ada, jalankan sambil dipantau dan fix src/ sampai tidak ada error. Gunakan sebelum /agyswap-spec setiap kali fitur bergantung pada perilaku agy, setelah agy naik versi, dan saat alur yang ada masih error.
version: 1.0.0
---

# /agyswap-observe

Tahap **OBSERVE** dalam siklus agyswap (`/agyswap-prepare` → `/agyswap-observe` → `/agyswap-spec` → `/agyswap-plan` → `/agyswap-build` → `/agyswap-test` → `/agyswap-review` → `/agyswap-prepare` → `/agyswap-commit` → `/agyswap-ship`).

agy tidak punya dokumentasi untuk cara ia menyimpan login atau membaca kuota. Semua yang dipakai agyswap adalah hasil observasi: binary `agy`, log-nya, keyring, dan request ke server Google. Sebelum fitur dibuat, diperbaiki, atau diperbarui, observasi dulu perilaku agy yang disentuhnya, supaya implementasi meniru cara kerja agy dan bukan tebakan.

Skill ini punya dua bagian:

- **A. Observasi** (selalu, sebelum fitur yang bergantung pada perilaku agy, dan setiap kali `agy --version` berbeda dengan versi di `architecture/OBSERVE.md`): kumpulkan bukti, lalu tulis petanya ke `architecture/OBSERVE.md`. `/agyswap-spec`, `/agyswap-plan`, dan `/agyswap-build` wajib mengikuti peta itu.
- **B. Validasi** (setelah fitur diimplementasi, atau untuk alur yang sudah ada dan masih error): jalankan alurnya terhadap agy sungguhan, pantau, debug dari bukti, fix `src/`, ulangi sampai tidak ada error. Perilaku baru yang ditemukan di B ditambahkan ke peta.

Mulai dengan membaca `AGENTS.md` (terutama "How agy stores auth" dan "Safety rules for agents") dan `architecture/OBSERVE.md`.

## Batas yang tidak boleh dilanggar

- **Jangan pernah mencetak nilai token** (access, refresh, id) atau client secret (`GOCSPX-…`). Cetak bentuknya saja: nama key, panjang string, nama claim. Simpan salinan sementara di `/tmp`, lalu `shred -u` setelah dipakai.
- **Jangan pernah memakai `busctl get-property` berulang** untuk menjelajahi item Secret Service. Pada 2026-10-06 cara itu membuat gnome-keyring 48 crash (`invoke_get_property_in_idle_cb: assertion failed`). Pakai `secret-tool lookup/store/clear` saja.
- **Tanya user dulu** sebelum aksi yang mengubah login sungguhan: menulis keyring, `/logout`, login akun lain, atau switch dengan store asli `~/.agyswap/`. Login dan logout di agy selalu dikerjakan user sendiri di terminalnya.
- **Request jaringan dengan token user hanya yang read-only**: refresh token, `fetchAvailableModels`, dan `retrieveUserQuotaSummary` (diizinkan user 2026-10-06), plus slash command read-only agy `agy -p "/quota|/usage|/credits" --output-format json`. Endpoint read-only lain ditanyakan ke user dulu. Jangan memanggil endpoint yang mengubah state akun (onboarding, setting, lisensi).
- Uji `agyswap` memakai `AGYSWAP_HOME=$(mktemp -d)`, dan hapus `accounts.json`-nya dengan `shred -u` setelah selesai.

## A. Observasi

### A1. Catat lingkungan

`agy --version`, path binary (`command -v agy`), OS dan versi gnome-keyring, serta apakah agy sedang login (`secret-tool lookup service gemini username antigravity | wc -c`).

### A2. Yang wajib diobservasi

Untuk setiap perilaku yang disentuh fitur:

1. **Penyimpanan login**: service dan user di keyring, format nilai (JSON, key apa saja, claim di `id_token`), dan fallback ke file kalau keyring gagal (path-nya).
2. **Siklus token**: kapan agy me-refresh, apakah refresh token berotasi, dan apakah agy menulis ulang keyring saat berjalan.
3. **Login dan logout**: apa yang berubah di keyring dan file setelah `/logout` dan login, dan apakah token lama masih bisa dipakai (pernah diverifikasi: tidak di-revoke).
4. **Endpoint**: URL, method, body, header yang wajib (User-Agent), bentuk respons, dan kode error (401, 403, 429, `invalid_grant`, `invalid_client`).
5. **Kuota**: field per model, cara model berbagi bucket, dan waktu reset.
6. **Proses**: proses agy apa saja yang berjalan (`pgrep -a -x agy`), mana yang menyentuh token (updater `--bg-updater` tidak).
7. **Log**: baris di `~/.gemini/antigravity-cli/log/cli-*.log` yang membuktikan perilaku di atas (`keyringAuth`, `ChainedAuth`, `token refreshed`, `applyAuthResult`).
8. **Perubahan versi**: string di binary yang hilang atau baru dibanding versi yang tercatat.

Setiap klaim di peta harus punya bukti: baris log, output perintah (sudah disensor), atau string di binary.

### A3. Tulis peta

Tulis `architecture/OBSERVE.md` dengan format di `# Reference`, menggantikan bagian untuk perilaku yang sama dan mempertahankan bagian lain. Hal yang belum bisa diobservasi dicatat di "Belum terobservasi", bukan ditebak.

Setelah itu `/agyswap-spec` → `/agyswap-plan` → `/agyswap-build` menyusun implementasi dari peta ini. Lalu kembali ke bagian B.

## B. Validasi: jalankan, pantau, fix

1. Jalankan alurnya dengan store sementara (`AGYSWAP_HOME=$(mktemp -d) uv run agyswap ...`). Untuk alur yang butuh dua akun sungguhan atau login/logout, tulis langkahnya untuk user dan minta user menjalankannya.
2. Setelah setiap langkah, cek dari bukti: keyring (bentuk saja), `accounts.json` (email dan slot saja), log agy terbaru, dan output `agyswap`.
3. Kalau ada error, temukan akar masalahnya dari bukti, perbaiki `src/` dengan test regresi (`/agyswap-test`), lalu ulangi langkahnya.
4. Selesai kalau seluruh alur jalan tanpa error dan agy masuk sebagai akun yang diharapkan.

Tulis hasil validasi ke `architecture/OBSERVE.md` bagian "Validasi": langkah, hasil, dan perbaikan yang dibuat.

---

# Reference

## Probe recipes

Semua resep hanya mencetak bentuk, tidak pernah nilai.

Bentuk token di keyring:

```bash
secret-tool lookup service gemini username antigravity > /tmp/.agy_tok
python3 - <<'EOF'
import json, base64
d = json.load(open('/tmp/.agy_tok'))
shape = lambda v: {k: shape(x) for k, x in v.items()} if isinstance(v, dict) else f"{type(v).__name__}({len(v) if isinstance(v, str) else ''})"
print(json.dumps(shape(d)))
p = d["id_token"].split(".")[1]
print(sorted(json.loads(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4)))))
EOF
shred -u /tmp/.agy_tok
```

Baris auth di log agy terbaru:

```bash
cd ~/.gemini/antigravity-cli/log && grep -h -E "keyring|OAuth|ChainedAuth|token refreshed|applyAuthResult" "$(ls -t | head -1)" | grep -v -E "ya29|eyJ|1//" | cut -c1-200
```

String di binary agy (endpoint, nama fungsi, pesan error):

```bash
python3 - <<'EOF'
import re, shutil
b = open(shutil.which("agy"), "rb").read()
for pat in [rb"v1internal:[a-zA-Z]+", rb"keyringAuth[^%]{0,60}", rb"cloudcode-pa[a-z.-]*googleapis\.com"]:
    print(pat.decode(), sorted({m.group().decode() for m in re.finditer(pat, b)})[:40])
EOF
```

Kuota akun yang sedang login (read-only):

```bash
uv run python - <<'EOF'
from agyswap import cli, usage
pools, _ = usage.account_usage(cli.read_token())
print([(p.label, round(p.used, 3), p.reset) for p in pools])
EOF
```

## Format `architecture/OBSERVE.md`

```markdown
# Observasi agy

- agy: <versi> (`<path binary>`), diobservasi <YYYY-MM-DD>
- Lingkungan: <OS>, gnome-keyring <versi>

## <Perilaku>

| Kondisi | Bukti | Implikasi untuk agyswap |
| ------- | ----- | ------------------------ |
| ...     | log/perintah/string binary | ... |

## Belum terobservasi

- ...

## Validasi

- <tanggal>: <alur> — <hasil>, <perbaikan>
```
