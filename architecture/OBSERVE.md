# Observasi agy

- agy: 1.3.1 (`~/.local/bin/agy`, binary Go), diobservasi 2026-10-08 (sebelumnya 1.3.0, 2026-10-06)
- Lingkungan: Fedora 43, `gnome-keyring-48.0-3.fc43` (Secret Service)
- Disusun dari sesi pembuatan agyswap dan tiga putaran `/agyswap-observe` (kuota per window, isolasi sesi, agy 1.3.1 dan kuota habis). Observasi ulang setiap kali `agy --version` berubah.

## Perubahan 1.3.0 → 1.3.1

| Kondisi | Bukti | Implikasi untuk agyswap |
| ------- | ----- | ------------------------ |
| Alur auth tidak berubah: `keyringAuth: loaded token … expired=true` → `token refreshed, new expiry=… m=+3600` → `ChainedAuth: authenticated via keyring (effective: keyring)` → `applyAuthResult: … authMethod=consumer` | Log `cli-20261007_163326.log` (`Language server version: 1.3.0`) dan `cli-20261007_222421.log` (`Language server version: 1.3.1`) | Tidak ada perubahan `src/` |
| Item keyring dan bentuk token sama: `{"token": {access_token, token_type, refresh_token, expiry}, "auth_method", "id_token"}`, claim `id_token` sama | Probe bentuk 2026-10-08 (panjang saja) | — |
| String binary yang dipakai agyswap masih ada: `zalando/go_keyring`, `composite_token_storage.go`, `v1internal:retrieveUserQuotaSummary`, `v1internal:fetchAvailableModels`, `remainingFraction`, host `cloudcode-pa` dan `daily-cloudcode-pa`; tetap dua client secret `GOCSPX-…` | Probe string binary 1.3.1 | `_agy_client_secrets` tetap bekerja |
| Binary 1.3.0 tidak tersimpan (hanya 1.1.28 di `~/.gemini/bin/agy`), dan changelog lokal (`~/.gemini/antigravity-cli/cache/CHANGELOG.md`) berhenti di 1.2.14 | `ls`, `--version`, `grep` heading changelog | Diff string penuh 1.3.0 → 1.3.1 tidak bisa dibuat; lihat "Belum terobservasi" |
| Saat start, agy mencatat `You are not logged into Antigravity.` sekitar 1 detik **sebelum** keyring selesai dibaca, walaupun login valid | Kedua log di atas: error pada 22:24:21.66, `loaded token` pada 22:24:22.44 | Baris itu di log bukan bukti logout; jangan dipakai untuk mendeteksi status login |

## Penyimpanan login

| Kondisi | Bukti | Implikasi untuk agyswap |
| ------- | ----- | ------------------------ |
| Token disimpan di Secret Service lewat zalando/go-keyring | String binary `zalando/go_keyring`, `keyringAuth: loaded token`; log `ChainedAuth: authenticated via keyring (effective: keyring)` | Baca dan tulis lewat `secret-tool` |
| Item keyring: `service=gemini`, `username=antigravity` | Atribut item gkr-compat ter-hash; md5 cocok dengan string `gemini` dan `antigravity` dari binary; `secret-tool lookup service gemini username antigravity` mengembalikan token | `SERVICE`/`USERNAME` di `cli.py` |
| Nilai berupa JSON `{"token": {access_token, token_type, refresh_token, expiry}, "auth_method", "id_token"}` | Bentuk dari `secret-tool lookup` (nilai tidak dicetak) | Satu blob per akun di `accounts.json` |
| `expiry` ditulis dengan presisi nanodetik dan offset lokal (`2026-10-06T17:57:51.458222684+07:00`) | Bentuk token, log `keyringAuth: loaded token, expiry=...` | `parse_time` memotong ke mikrodetik |
| Email ada di claim `email` milik `id_token`; `azp` = client ID | Claim `id_token`: `at_hash, aud, azp, email, email_verified, exp, family_name, given_name, iat, iss, name, picture, sub` | `email_of`, client ID untuk refresh |
| Penyimpanan token bersifat komposit (keyring dulu, lalu file). agy jatuh ke file kalau keyring timeout atau tidak terjangkau, melewati keyring kalau tidak ada D-Bus session bus, dan melewatinya selama satu jam setelah timeout (dicatat lewat file penanda keyring) | String binary `composite_token_storage`, `KeyringTokenStorage`, `Keyring SaveToken timed out after %v, falling back to file storage`, `DefaultKeyringMarkerPath`, `keyringRecentlyUnavailable`; changelog agy (bypass tanpa D-Bus, skip satu jam setelah timeout); log sesi uji tanpa D-Bus | Belum didukung. Kalau agy sedang memakai file, agyswap tidak melihat login itu. Lihat "Data dir dan isolasi sesi" |
| Antigravity IDE menyimpan login terpisah di `~/.config/Antigravity/User/globalStorage/state.vscdb` | Key `antigravityAuthStatus`, `antigravityUnifiedStateSync.oauthToken` | Di luar scope; jangan disentuh |

## Siklus token

| Kondisi | Bukti | Implikasi untuk agyswap |
| ------- | ----- | ------------------------ |
| Access token berlaku sekitar 1 jam; agy me-refresh saat start kalau sudah kedaluwarsa | Log `token refreshed, new expiry=... m=+3600` | Akun tidak aktif perlu di-refresh sebelum cek kuota |
| agy menyimpan token hasil refresh kembali ke keyring | String binary `Failed to save refreshed token`; expiry di keyring berubah setelah agy jalan | `switch` menyalin token keyring ke slot dulu; switch ditolak saat agy berjalan |
| Refresh lewat `https://oauth2.googleapis.com/token` dengan client ID agy (= claim `azp`) dan salah satu dari dua client secret `GOCSPX-…` di binary. Secret yang lain ditolak `invalid_client` | Probe refresh read-only dengan token sendiri | Secret dibaca dari binary saat runtime; coba satu per satu |
| Respons refresh tidak berisi `refresh_token` baru (tidak ada rotasi) | Key respons: `access_token, expires_in, id_token, scope, token_type` | Salinan di store tetap valid setelah refresh |

## Login dan logout

| Kondisi | Bukti | Implikasi untuk agyswap |
| ------- | ----- | ------------------------ |
| `/logout` di agy **tidak** me-revoke refresh token yang sudah disalin | Diverifikasi user 2026-10-06: add akun A, `/logout`, login akun B, add, lalu switch bolak-balik tanpa login ulang | Alur add: `/logout` → login akun berikutnya → `agyswap add` aman |
| agy tidak punya pemilih akun; ganti akun hanya lewat logout lalu login | Perilaku agy 1.3.0 | Berbeda dengan Claude Code; README menjelaskan alurnya |
| Tidak login: log berisi `error getting token source: You are not logged into Antigravity.` | Log CLI agy | Pesan `agy is not signed in` di `cmd_add` |

## Kuota

| Kondisi | Bukti | Implikasi untuk agyswap |
| ------- | ----- | ------------------------ |
| `POST https://cloudcode-pa.googleapis.com/v1internal:fetchAvailableModels`, body `{}`, header `Authorization: Bearer <access_token>` | String binary `v1internal:fetchAvailableModels`, `remainingFraction`, `quotaInfo`, `resetTime`; probe read-only | Dipakai sampai 2026-10-06; diganti `retrieveUserQuotaSummary` |
| User-Agent default `Python-urllib` ditolak 403; `User-Agent: antigravity` diterima | Probe: `quota request failed (HTTP 403)` lalu sukses setelah UA diganti | `_post` selalu mengirim UA `antigravity` |
| Respons `models.<id>.quotaInfo = {remainingFraction, resetTime}` plus `displayName`; model internal (`chat_*`) tanpa `displayName` dan tanpa `resetTime` | Probe dengan akun yang sedang login | Model tanpa nama atau tanpa reset dilewati |
| Model berbagi bucket: semua Gemini memakai satu fraction dan reset (sekitar 5 jam), Claude dan GPT-OSS satu bucket lain | `gemini-*` 0.946 reset 11:07Z; `claude-sonnet-4-6` dan `gpt-oss-120b-medium` 1.0 reset 15:18Z | Bar per bucket: `Gemini`, `Claude/GPT-OSS` |
| **`fetchAvailableModels` hanya melaporkan window 5 jam.** Window mingguan tidak terlihat di sana | Akun 1: `fetchAvailableModels` Gemini `remaining=1`, sedangkan `/quota` Gemini mingguan 56% dan Claude/GPT mingguan 42% | `list`/TUI sekarang menyesatkan (0% terpakai padahal mingguan 44–58% terpakai). `auto` wajib memakai `retrieveUserQuotaSummary` |
| Bucket 5 jam yang belum dipakai melaporkan `remainingFraction: 1` dengan `resetTime` sekitar sekarang + 5 jam yang terus bergeser; setelah dipakai, `resetTime` tetap. Window mulai saat pemakaian pertama | Slot 1 (penuh): reset dalam 4,9–5,0 jam di dua pembacaan; slot 2 (0.99916): reset tetap dalam 4,26 jam | Jangan memakai `resetTime` bucket penuh sebagai jadwal; abaikan reset untuk bucket dengan fraction 1 |

## Kuota per window (`retrieveUserQuotaSummary`)

| Kondisi | Bukti | Implikasi untuk agyswap |
| ------- | ----- | ------------------------ |
| `POST https://daily-cloudcode-pa.googleapis.com/v1internal:retrieveUserQuotaSummary`, body `{}`, `Authorization: Bearer`, UA `antigravity`. Juga jalan di `cloudcode-pa`, dan body `{"project": …}` memberi hasil yang sama | Log agy: `Cache(retrieveUserQuotaSummary) … Post "https://daily-cloudcode-pa.googleapis.com/v1internal:retrieveUserQuotaSummary"`; probe read-only 2026-10-06 untuk dua akun, keduanya HTTP 200 (diizinkan user) | Sumber kuota untuk `list`, TUI, dan `auto` |
| Respons: `{description, groups[]}`, `groups[] = {displayName, description, buckets[]}`, `buckets[] = {bucketId, displayName, window, resetTime, remainingFraction, description?}`. `window` bernilai `5h` atau `weekly`. `bucketId`: `gemini-5h`, `gemini-weekly`, `3p-5h`, `3p-weekly` | Bentuk respons probe 2026-10-06 dan 2026-10-08 (1.3.1, tidak berubah) | Satu bar per bucket, dikelompokkan per group |
| `agy -p /quota` dan `agy -p /usage` (`--output-format json`) memberi data yang sama dengan nama key snake_case: `command.data.groups[].buckets[] = {id, name, description?, window, remaining_fraction, reset_time}`. Nilainya cocok dengan endpoint (Gemini mingguan 0.91431904 di keduanya) | Probe 2026-10-08 | Kalau output agy pernah dipakai, key-nya berbeda dari respons API; agyswap tetap membaca API langsung |
| Grup: "Gemini Models" (Gemini Flash, Gemini Pro) dan "Claude and GPT models" (Claude Opus, Claude Sonnet, GPT-OSS). Teks agy: "models share a weekly limit and a 5-hour limit. Quota is consumed proportionally to the cost of the tokens … your weekly limit is tied directly to your individual tier" | `description` di respons `/quota` | Label grup diambil dari `displayName`, tidak di-hardcode |
| Window mingguan: `resetTime` tetap, bisa beberapa hari ke depan (slot 1: Gemini 2026-10-07T11:50:41Z, 3p 2026-10-11T06:25:12Z; slot 2: 2026-10-13) | Probe dua akun | Strategi yang mendahulukan akun dengan reset mingguan terdekat bisa memakai data ini |
| `description` bucket hanya ada kalau bucket sudah terpakai ("You have used some of your weekly limit, it will fully refresh in 1 day.") | Bucket `3p-weekly` slot 2 dengan fraction 1 tanpa `description` | Field opsional |
| AI credits terpisah dari kuota: `agy -p /credits` → `remaining_credits: 0` untuk akun ini | Output `/credits --output-format json` | Di luar scope `auto` untuk sekarang |
| agy menjawab `/quota`, `/usage`, `/credits` tanpa prompt lewat `agy -p "<cmd>" --output-format json`, hanya untuk akun yang sedang login | Probe 2026-10-06; changelog agy: "non-interactive answers … `-p "/usage"`, `/quota`, `/credits`" | Hanya cocok untuk akun aktif; untuk semua akun pakai endpoint langsung |

## Host dan rate limit

| Kondisi | Bukti | Implikasi untuk agyswap |
| ------- | ----- | ------------------------ |
| agy memakai host `daily-cloudcode-pa.googleapis.com` untuk semua endpoint (`loadCodeAssist`, `fetchAvailableModels`, `streamGenerateContent`, `retrieveUserQuotaSummary`) | Hitungan URL di 10 log terbaru | agyswap memakai `cloudcode-pa`; keduanya menjawab sama. Pertimbangkan mengikuti host agy |
| Saat model API mengembalikan retry delay, agy menunggu delay itu, dan **berhenti langsung** kalau delay > 30 detik atau kuota harian habis. Per-minute 429 di-retry otomatis dengan backoff | Changelog agy (rate-limit handling, transient `genai.APIError` 429); string binary `quotaResetDelay`, `Do not retry quota or capacity errors`, `QUOTA_EXHAUSTED`, `RATE_LIMIT_EXCEEDED` | Kuota habis terlihat di agy sebagai error yang menghentikan giliran. `auto` harus switch sebelum itu, bukan menunggu 429 |
| **Kuota habis terlihat di log**: `streamGenerateContent` gagal dengan `RESOURCE_EXHAUSTED (code 429): Individual quota reached. Please upgrade your subscription to increase your limits. Resets in 2h42m19s.`, dicatat dua kali (`agent executor error: generating and executing: …` lalu `generating and executing: …`), lalu giliran berhenti | 12 baris di 5 log 2026-10-04 (16:20–16:22 dan 23:39–23:40; pencarian 2026-10-06 terlewat), model `Gemini 3.8 Flash (High)` | Teks error berisi waktu reset relatif (`Resets in <h>h<m>m<s>s`); jendela < 5 jam, jadi ini window `5h` |
| Saat kuota habis, beberapa sesi agy yang berjalan bersamaan dengan akun yang sama gagal bersamaan, dan semuanya menghitung reset ke detik yang sama (23:39:00 + 2h42m19s = 23:39:52 + 2h41m27s = 02:21:19) | PID berbeda di `cli-20261004_220222.log`, `cli-20261004_144647.log`, `cli-20261004_233940.log` | Kuota per akun, bukan per sesi. Waktu reset absolut stabil dan bisa dipakai sebagai cooldown `auto` |
| Setelah 429, agy memanggil `quota_manager: doRefreshQuota` (terkadang `skipped (throttled)`); agy juga me-reload kuota (`force=true`) setiap ganti model dan saat start | `quota_manager.go:41/45` di log yang sama | agy sendiri tidak melakukan apa-apa selain menampilkan error; tidak ada switch otomatis |

## Proses

| Kondisi | Bukti | Implikasi untuk agyswap |
| ------- | ----- | ------------------------ |
| `agy --bg-updater --app_data_dir=antigravity-cli --gemini_dir=.gemini` di-spawn oleh sesi agy saat start (`auto_updater.go: Spawned background update process with PID …`) dan berhenti sendiri; saat tidak ada sesi, tidak ada proses agy sama sekali | `pgrep -a -f "agy\|antigravity"` kosong 2026-10-08; log `cli-20261007_222421.log`; `updater/update_status.json` | Diabaikan oleh `agy_running()` |
| **Sesi agy membaca keyring hanya sekali saat start**, lalu me-refresh token tiap jam dan menyimpannya ke keyring | Sesi terpanjang di log agy (sekitar 9 jam): `keyringAuth: loaded token` 1×, `token refreshed` 9×, `Failed to save refreshed token` 0× | Switch saat agy berjalan tidak berpengaruh ke sesi itu dan tertimpa saat refresh berikutnya (≤ 1 jam). `auto` hanya bisa switch saat tidak ada sesi agy |
| Kredensial yang ditolak definitif oleh server membuat agy sign out dan menghapus token tersimpan | Changelog agy: "the CLI now signs you out and clears the stale tokens" | Token mati di keyring bisa hilang sendiri; salinan di store tetap ada tapi juga mati |
| Sesi interaktif dan `agy -p` adalah proses `agy` biasa | `pgrep -a -x agy` | Switch ditolak selama ada proses selain updater |

## Data dir dan isolasi sesi

| Kondisi | Bukti | Implikasi untuk agyswap |
| ------- | ----- | ------------------------ |
| Flag tersembunyi `--gemini_dir=<dir>` membuat agy memakai data dir terpisah sepenuhnya (`<dir>/config`, `<dir>/antigravity-cli`: percakapan, log, cache, settings) | `agy --gemini_dir=/tmp/x -p /quota` 2026-10-06; proses updater berjalan dengan `--app_data_dir=antigravity-cli --gemini_dir=.gemini` | Bisa jadi dasar sesi per akun (perintah `run`) |
| Token **tidak** ikut terisolasi oleh `--gemini_dir`: agy tetap memakai item keyring yang sama (`authenticated via keyring`), walaupun `DBUS_SESSION_BUS_ADDRESS` di-unset | Log sesi uji: `keyringAuth: loaded token`, `authenticated as <email>` | Sesi paralel dengan akun berbeda tidak bisa hanya lewat `--gemini_dir` |
| Kalau D-Bus benar-benar tidak terjangkau (`DBUS_SESSION_BUS_ADDRESS=unix:path=/nonexistent/bus`), agy jatuh ke penyimpanan file (`composite_token_storage.go: Failed to load stored token from keyring, falling back to file`) dan meminta login OAuth karena file belum ada | Log sesi uji 2026-10-06; flow OAuth dibatalkan oleh timeout, tidak ada login yang terjadi | Kandidat isolasi token per sesi; path dan format file belum diketahui |
| `AGY_ACCOUNT` **bukan** untuk akun Google; env var ini memilih akun plugin untuk perintah sandbox (contoh di binary: `AGY_ACCOUNT=account-2 gh api user`) | String binary | Tidak dipakai |

## Belum terobservasi

- Respons `retrieveUserQuotaSummary` saat bucket benar-benar habis (diduga `remainingFraction` 0 atau field hilang). Kuota habis sudah terjadi 2026-10-04, tetapi agy tidak mencatat isi respons kuota ke log. Mengamatinya butuh probe read-only saat akun sedang habis.
- Body JSON error 429 `streamGenerateContent` (`quotaResetDelay`, `QUOTA_EXHAUSTED`, header `Retry-After`) dan teks yang ditampilkan agy di layar; log hanya menyimpan pesan `RESOURCE_EXHAUSTED (code 429): Individual quota reached … Resets in …`.
- Apakah `retrieveUserQuotaSummary` sendiri pernah menjawab 429, dan apakah ada header `Retry-After`. Belum pernah terjadi pada refresh tiap 2 menit.
- Kuota mingguan habis (hanya window `5h` yang pernah habis).
- Diff string binary dan changelog 1.3.0 → 1.3.1: binary lama tidak tersimpan dan changelog lokal berhenti di 1.2.14.
- Apakah kuota per window berbeda antar tier akun (free vs berbayar). Kedua akun yang diamati memakai tier yang sama.
- Kode error saat refresh token benar-benar di-revoke (diasumsikan `invalid_grant`, belum pernah terjadi).
- Perilaku di macOS (Keychain) dan Windows (Credential Manager).
- Path dan format file token saat agy memakai penyimpanan file (D-Bus tidak terjangkau), dan apakah file itu berada di dalam `--gemini_dir`. Mengamatinya butuh satu login OAuth di sesi terisolasi oleh user.

## Validasi

- 2026-10-08 (agy 1.3.1, setelah perbaikan temuan review dan ship): dengan store sementara, `add` → `Added account 1`, `list` exit 0 dengan empat bucket (Gemini mingguan 9%, Claude/GPT mingguan 58%), `status` → akun 1. Store dan `.lock` bermode `600`, tidak ada file temp tersisa, dan hash nilai keyring sama sebelum dan sesudah (keyring tidak ditulis). `retrieveUserQuotaSummary` cocok dengan `agy -p /quota`. Tidak ada perubahan `src/`.

- 2026-10-06 (user, TUI dua akun): akun 1 (tidak aktif) Gemini mingguan 43% (reset 23j 31m) dan Claude/GPT mingguan 58% (reset 4h 18j); akun 2 (aktif) semua 0%. Cocok dengan pembacaan `agy -p /quota` sebelumnya (sisa 57% dan 42%, reset 2026-10-07T11:50Z dan 2026-10-11T06:25Z). Kuota akun tidak aktif terbaca benar lewat token tersimpan.
- 2026-10-06 (build kuota per window): `usage.fetch_pools` dengan `retrieveUserQuotaSummary` cocok dengan `agy -p /quota` untuk akun aktif (terpakai dan reset sama di keempat bucket). `agyswap list` dengan store sementara menampilkan Gemini dan Claude/GPT, masing-masing `5h` dan `weekly` (reset mingguan `6d 22h`). Tidak ada perbaikan tambahan.
- 2026-10-06 (state saat ini, setelah prepare): agy masih 1.3.0 dan GNOME Keyring 48, jadi peta di atas tetap berlaku. Dengan store sementara, `add`, `status`, dan `list` berjalan tanpa error untuk akun yang sedang login, store bermode `600`, dan keyring tidak ditulis. `list` masih hanya menampilkan window 5 jam (Gemini dan Claude/GPT-OSS), sesuai `TODO.md` dan Task 1–2 di `architecture/PLAN.md`. Tidak ada perubahan `src/`.
- 2026-10-06: add dua akun sungguhan lewat `/logout` → login → `agyswap add`, lalu `agyswap switch` bolak-balik; agy masuk sebagai akun yang dipilih tanpa login ulang. Tidak ada perbaikan yang dibutuhkan.
- 2026-10-06 (observe isolasi sesi): `agy --gemini_dir=<tmp> -p /quota` jalan dengan data dir terpisah tapi token tetap dari keyring; dengan D-Bus tidak terjangkau, agy jatuh ke file dan meminta login (dibatalkan oleh timeout, tidak ada login). Folder uji dihapus, dan keyring asli tidak tersentuh. Tidak ada perubahan `src/`.
- 2026-10-06 (observe kuota per window): `retrieveUserQuotaSummary` di-probe read-only untuk dua akun atas izin user, dan hasilnya cocok dengan `agy -p /quota`. Ditemukan bahwa `list`/TUI hanya menampilkan window 5 jam; dicatat di `TODO.md`.
- 2026-10-06: `agyswap list` dengan akun sungguhan menampilkan `Gemini 5%` dan `Claude/GPT-OSS 0%`; refresh token yang sengaja dibuat kedaluwarsa berhasil dan `refresh_token` tidak berubah.
