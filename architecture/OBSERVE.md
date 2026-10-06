# Observasi agy

- agy: 1.3.0 (`~/.local/bin/agy`, binary Go), diobservasi 2026-10-06
- Lingkungan: Linux dengan GNOME Keyring 48 (Secret Service)
- Disusun dari sesi pembuatan agyswap dan dua putaran `/agyswap-observe` (kuota per window, isolasi sesi). Observasi ulang setiap kali `agy --version` berubah.

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
| Respons: `groups[] = {displayName, description, buckets[]}`, `buckets[] = {bucketId, displayName, window, resetTime, remainingFraction, description?}`. `window` bernilai `5h` atau `weekly`. `bucketId`: `gemini-5h`, `gemini-weekly`, `3p-5h`, `3p-weekly` | Bentuk respons probe; `agy -p /quota --output-format json` memberi data yang sama (`command.data.groups[].buckets[]`) | Satu bar per bucket, dikelompokkan per group |
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
| Tidak ada jejak 429 atau kuota habis di 89 log yang ada | `grep` 429/`RESOURCE_EXHAUSTED`/`QUOTA_EXHAUSTED` di semua `cli-*.log` | Respons saat habis belum terobservasi |

## Proses

| Kondisi | Bukti | Implikasi untuk agyswap |
| ------- | ----- | ------------------------ |
| `agy --bg-updater --app_data_dir=antigravity-cli --gemini_dir=.gemini` selalu berjalan di background | `pgrep -a -f antigravity` | Diabaikan oleh `agy_running()` |
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

- Respons `retrieveUserQuotaSummary` dan `fetchAvailableModels` saat bucket benar-benar habis (diduga `remainingFraction` 0; belum pernah terjadi). Mengamatinya butuh satu akun yang kuotanya sengaja dihabiskan.
- Bentuk error `streamGenerateContent` saat kuota habis (`quotaResetDelay`, `QUOTA_EXHAUSTED`) dan pesan yang ditampilkan agy ke user.
- Apakah kuota per window berbeda antar tier akun (free vs berbayar). Kedua akun yang diamati memakai tier yang sama.
- Kode error saat refresh token benar-benar di-revoke (diasumsikan `invalid_grant`, belum pernah terjadi).
- Perilaku di macOS (Keychain) dan Windows (Credential Manager).
- Path dan format file token saat agy memakai penyimpanan file (D-Bus tidak terjangkau), dan apakah file itu berada di dalam `--gemini_dir`. Mengamatinya butuh satu login OAuth di sesi terisolasi oleh user.

## Validasi

- 2026-10-06 (user, TUI dua akun): akun 1 (tidak aktif) Gemini mingguan 43% (reset 23j 31m) dan Claude/GPT mingguan 58% (reset 4h 18j); akun 2 (aktif) semua 0%. Cocok dengan pembacaan `agy -p /quota` sebelumnya (sisa 57% dan 42%, reset 2026-10-07T11:50Z dan 2026-10-11T06:25Z). Kuota akun tidak aktif terbaca benar lewat token tersimpan.
- 2026-10-06 (build kuota per window): `usage.fetch_pools` dengan `retrieveUserQuotaSummary` cocok dengan `agy -p /quota` untuk akun aktif (terpakai dan reset sama di keempat bucket). `agyswap list` dengan store sementara menampilkan Gemini dan Claude/GPT, masing-masing `5h` dan `weekly` (reset mingguan `6d 22h`). Tidak ada perbaikan tambahan.
- 2026-10-06 (state saat ini, setelah prepare): agy masih 1.3.0 dan GNOME Keyring 48, jadi peta di atas tetap berlaku. Dengan store sementara, `add`, `status`, dan `list` berjalan tanpa error untuk akun yang sedang login, store bermode `600`, dan keyring tidak ditulis. `list` masih hanya menampilkan window 5 jam (Gemini dan Claude/GPT-OSS), sesuai `TODO.md` dan Task 1–2 di `architecture/PLAN.md`. Tidak ada perubahan `src/`.
- 2026-10-06: add dua akun sungguhan lewat `/logout` → login → `agyswap add`, lalu `agyswap switch` bolak-balik; agy masuk sebagai akun yang dipilih tanpa login ulang. Tidak ada perbaikan yang dibutuhkan.
- 2026-10-06 (observe isolasi sesi): `agy --gemini_dir=<tmp> -p /quota` jalan dengan data dir terpisah tapi token tetap dari keyring; dengan D-Bus tidak terjangkau, agy jatuh ke file dan meminta login (dibatalkan oleh timeout, tidak ada login). Folder uji dihapus, dan keyring asli tidak tersentuh. Tidak ada perubahan `src/`.
- 2026-10-06 (observe kuota per window): `retrieveUserQuotaSummary` di-probe read-only untuk dua akun atas izin user, dan hasilnya cocok dengan `agy -p /quota`. Ditemukan bahwa `list`/TUI hanya menampilkan window 5 jam; dicatat di `TODO.md`.
- 2026-10-06: `agyswap list` dengan akun sungguhan menampilkan `Gemini 5%` dan `Claude/GPT-OSS 0%`; refresh token yang sengaja dibuat kedaluwarsa berhasil dan `refresh_token` tidak berubah.
