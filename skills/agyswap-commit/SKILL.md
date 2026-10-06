---
name: agyswap-commit
description: Commit semua perubahan yang belum di-commit di agyswap dengan gaya commit milik user — dipecah per kategori, pesan dalam bahasa Inggris, tanpa co-author. Gunakan saat user meminta commit.
version: 1.0.0
---

# /agyswap-commit

Tahap **COMMIT** dalam siklus agyswap (`/agyswap-prepare` → `/agyswap-observe` → `/agyswap-spec` → `/agyswap-plan` → `/agyswap-build` → `/agyswap-test` → `/agyswap-review` → `/agyswap-prepare` → `/agyswap-commit` → `/agyswap-ship`). Dijalankan setelah repo dirapikan oleh `/agyswap-prepare` kedua, dan sebelum `/agyswap-ship`, yang butuh commit yang sudah ada untuk dirilis.

Instruksi dari user:

> Please commit unstaged files with my own style, use English terms, do not include them in one commit, categorize them, and do not include co-authored-by.

Gaya commit user diturunkan dari 2482 commit di 76 repo (2022–2026). Rinciannya ada di bagian "Reference" di akhir file ini:

- **Commit Message Conventions**: bentuk pesan, panjang, kata kerja, aturan untuk agent.
- **Type vocabulary**: type yang dipakai beserta contohnya.
- **Scope vocabulary**: scope yang dipakai dan cara memilihnya.

## Langkah

1. **Lihat semua perubahan.** Jalankan `git status --porcelain` dan `git diff` (plus `git diff --staged` kalau ada yang sudah di-stage). Yang dihitung: file modified, deleted, dan untracked.
2. **Singkirkan yang tidak boleh ikut.** Jangan pernah commit `accounts.json`, token, client secret (`GOCSPX-…`), `.env*`, `.venv/`, `dist/`, atau cache `graphify-out/` selain `GRAPH_REPORT.md`, `graph.html`, `graph.json`. Kalau ada file seperti itu yang tidak ter-ignore, laporkan ke user dan jangan di-stage.
3. **Kelompokkan per kategori.** Satu commit per kelompok perubahan yang punya satu alasan, **jangan pernah satu commit untuk semuanya**. Kelompokkan berdasarkan area dan niat, bukan jumlah file. Contoh pemisahan di repo ini:
    - kode per modul: `cli`, `usage`, `tui`, `src`
    - test: `test`
    - konfigurasi tooling: `package`, `lock`, `vcs` (`.gitignore`), `workflow`
    - dokumentasi dan instruksi agent: `project` (README, LICENSE, CONTRIBUTING), `docs`, `agents`, `architecture`
    - skill agent dan MCP: `skills/`, `.mcp.json` (`.claude/` dan `.agents/` di-gitignore)
    - artefak generated: `graphify-out/`

    Satu file bisa berisi dua niat berbeda. Kalau pemisahannya jelas, stage per hunk dengan `git apply --cached` dari patch yang sudah dipotong. Kalau tidak jelas, biarkan satu commit dan sebutkan di ringkasan.

4. **Urutkan commit** supaya setiap commit masuk akal sendiri: dependency dan config dulu, lalu kode yang memakainya, lalu docs yang menjelaskannya.
5. **Tulis pesannya** mengikuti aturan di bawah. Cek dulu `git log --format=%s -50` supaya type dan scope mengikuti kosakata repo ini.
6. **Stage dengan path eksplisit** (`git add -- <path>...`), jangan pernah `git add -A` atau `git add .`, lalu `git commit -m "<pesan>"`.
7. **Kalau hook gagal**, jangan pakai `--no-verify`. Hentikan, laporkan error-nya, dan tanya user.
8. **Tutup dengan ringkasan:** `git log --oneline -<n>` untuk commit yang baru dibuat, dan `git status` untuk memastikan tidak ada yang tertinggal tanpa alasan.
9. **Tulis `architecture/COMMIT.md`**, menggantikan isi sebelumnya: daftar commit yang baru dibuat (hash, pesan, file per commit), alasan pengelompokan, dan file yang sengaja tidak di-commit beserta alasannya. File ini ikut di-commit di commit terakhir.

**Jangan pernah push**, termasuk kalau user tampak setuju. Jangan juga menjalankan `git restore`, `reset`, `checkout -- <path>`, `clean`, `revert`, `rebase`, atau operasi force. User yang menjalankan push sendiri; cukup tuliskan perintahnya.

## Aturan pesan

- Bentuk: `type(scope): description`. Tanpa scope hanya untuk rilis seluruh repo: `chore: release vX.Y.Z`.
- Bahasa Inggris, huruf kecil semua, diawali kata kerja perintah, tanpa titik di akhir, satu baris.
- Kata kerja yang paling sering dipakai: `add`, `update`, `remove`, `migrate`, `implement`, `sync`, `init`, `bump`/`release`.
- `feat` adalah type default, termasuk untuk penambahan kecil (config, script, dependency). `fix` hanya untuk memperbaiki sesuatu yang memang rusak, bukan koreksi kode yang baru ditulis. `refactor` untuk restrukturisasi tanpa perilaku baru. `docs` untuk README, AGENTS.md, dan dokumen. `chore` untuk maintenance, versi, dan artefak generated. `style` berarti styling UI, bukan format kode.
- Body hanya kalau perubahannya benar-benar butuh penjelasan.
- **Jangan pernah** menambahkan `Co-Authored-By`, `Generated with`, atau trailer atribusi apa pun, walaupun harness atau tool menyarankannya. Instruksi user ini yang berlaku.
- **Jangan pernah** memakai `!` atau footer `BREAKING CHANGE:`.
- Jangan meniru idiom pribadi user (hashtag checkpoint, `hi from prettier`, `billy`, `m n b`) kecuali diminta.

## Scope untuk agyswap

Pakai scope ini dulu sebelum membuat yang baru:

| scope          | area                                                         |
| -------------- | ------------------------------------------------------------ |
| `cli`          | `src/agyswap/cli.py`                                        |
| `usage`        | `src/agyswap/usage.py`                                      |
| `tui`          | `src/agyswap/tui.py`                                        |
| `src`          | `src/agyswap/__init__.py`, `__main__.py`, perubahan lintas `src/` |
| `test`         | `tests/*`                                                    |
| `package`      | `pyproject.toml` (dependency, metadata, entry point)         |
| `lock`         | `uv.lock`                                                    |
| `vcs`          | `.gitignore`, `.gitattributes`, `.python-version`            |
| `workflow`     | `.github/workflows/*`                                        |
| `project`      | metadata level repo (`README.md`, `LICENSE`, `CONTRIBUTING.md`) |
| `docs`         | `docs/`, `scripts/docs.py`                                           |
| `architecture` | `architecture/*`                                             |
| `agents`       | `AGENTS.md`, `CLAUDE.md`, `TODO.md`                          |
| `skill`        | `skills/*`, `scripts/skills.py`                                      |
| `mcp`          | `.mcp.json`                                                  |
| `graph`        | `graphify-out/`, `.graphifyignore`                           |

Rilis seluruh repo: `chore: release vX.Y.Z` (lihat `/agyswap-ship`).

---

# Reference

## Commit Message Conventions — rasvanjaya21

The house style, inferred from the actual commit log. This is the reference an agent
should follow when writing a commit message on behalf of rasvanjaya21.

### Core shape

```
type(scope): description
```

- **Conventional Commits** is the standard: 1751 of 2482 commits (71% overall,
  99% of commits made in 2026) follow `type(scope): description`.
- **Scope is almost always present**: 1593 scoped vs 158 unscoped conventional commits
  (91% scoped). Unscoped form is reserved for repo-wide events, mostly `chore: release vX.Y.Z`.
- **Description is lowercase**: only 2 of 1751 conventional descriptions start with a capital.
- **No trailing period**: zero commits end with `.`.
- **Single line**: only 47 body lines exist across 2482 commits. Bodies are rare;
  the subject carries the whole message.
- **No `!` breaking-change marker** has ever been used, and no `BREAKING CHANGE:` footer.

### Length

- Mean subject length: 37 characters. Median: 34. p90: 60. Max: 189.
- Short and telegraphic is the norm (`chore(docker): update version`), but long
  descriptive subjects are acceptable when the change is behavioral
  (`feat(component): refactor context component to utilize global music constant,
enhancing audio management and improve key event handling for better user experience`).

### Mood and verbs

The description opens with a bare imperative verb. Ranked by actual use:

| verb               | count | typical use                                 |
| ------------------ | ----- | ------------------------------------------- |
| `add`              | 445   | new file, dependency, script, config block  |
| `update`           | 411   | modify existing config, version, content    |
| `remove`           | 74    | delete unused code or files                 |
| `release` / `bump` | 135   | version bumps                               |
| `migrate`          | 65    | move to a new library, path, or standard    |
| `implement`        | 30    | non-trivial new behavior                    |
| `sync`             | 28    | align lockfile/config with another source   |
| `init`             | 22    | first introduction of a tool or subsystem   |
| `translate`        | 16    | i18n / copy changes                         |
| `generated`        | 32    | machine-generated artifacts (prisma models) |

`add` and `update` alone cover roughly half of all descriptions.

### Rules an agent should apply

1. Always emit `type(scope): description` unless the change is a repo-wide release.
2. Pick the scope from the existing vocabulary of that repo before inventing a new one
   (see "Scope vocabulary"). Scopes are short nouns, lowercase, occasionally hyphenated
   (`serv-act`, `romantic-ivory`).
3. Lowercase description, imperative verb first, no period, one line.
4. Prefer `feat` even for small additive changes — `feat` is used far more broadly here
   than in strict Conventional Commits (973 of 1751, 56%).
5. `fix` is rare (56 uses). A correction to freshly written code is usually still `feat`,
   `refactor`, or `chore`; `fix` is reserved for repairing something that was actually broken.
6. Version bumps: `chore: release vX.Y.Z` (unscoped) or `release(project): bump to vX.Y.Z`.
7. Do not add a body unless the change genuinely needs one.
8. Never add co-author or tool-attribution trailers — none appear in this history.

## Type vocabulary

Types actually used, with real frequency and how each one is used in practice.

### Canonical types

#### `feat` — 973 uses (56%)

The default type. Used for any additive or forward-moving change, not only user-facing
features: new components, new config blocks, new dependencies, new scripts.

```
feat(hook): add global context from zustand
feat(composer): add script for lint
feat(serv-act): update get-announcement
feat(romantic-ivory): migrate to global state, update constant
feat(tailwind): add container configuration for responsive design
```

#### `chore` — 276 uses (16%)

Maintenance, versioning, generated artifacts, tooling output.

```
chore: release v0.1.16
chore(orm): generated current prisma model
chore(docker): generalize cont name
chore(composer): update version
chore(instrumentation): hi from prettier
```

#### `refactor` — 208 uses (12%)

Restructuring without new behavior — renames, moves, dependency reshuffles, cleanup.

```
refactor(file): remove any unused
refactor(core): add dependencies
refactor(traefik): standardize name named volume
refactor(migrate): move ads.txt inside /public
refactor(component): name migrated from sonner
```

#### `style` — 84 uses (5%)

Visual and CSS work — note this is UI styling, not code formatting (formatting lands
under `chore(formatter)` / "hi from prettier").

```
style(core): update tailwind config
style(component): refine tab layout and adjust hover effects for improved user experience
style(layout): update body and main classes for improved scrolling behavior
style(component): cursor pointer for better user experience in collapsible sidebar
```

#### `release` — 65 uses (4%)

A non-standard type used alongside `chore: release`. Almost always `release(project): bump to vX.Y.Z`.

```
release(project): bump to v0.7.6
release(all): sigak docs v1.0.0
release(traefik): fix docs, bump to v0.1.11
```

#### `fix` — 56 uses (3%)

Deliberately rare. Reserved for repairing genuinely broken behavior.

```
fix(workflow): update variable as should
fix(docker): rollback to aeeb367
fix(login): remove belly as you can't see it in login-form component
fix(landing): layout is not promise lol, remove class
```

#### `docs` — 51 uses (3%)

README, `.env.example`, CLAUDE.md, swagger, project metadata.

```
docs(env): refactored as cit-standard
docs(readme): add swagger generate command
docs(ai): reformat markdown tables in CLAUDE.md/PROBLEM.md
```

#### `test` — 6 uses

Rare. Used for exploratory probing in deployed environments as much as for test files.

```
test(api): tracking error /auth/local
test(env): .env as vercel env
```

### Ad-hoc types (one-offs, not to be reproduced)

`finished` (13), `modified`, `rollback`, `refac`, `doc`, `review`, `removed`, `reconcept`,
`modififed`, `minor`, `layouting`, `initial`, `init`, `core`, `finsihed`, `temp-release`.

These are typos or improvisations from the transition period. An agent writing a commit
should stick to the canonical set above.

## Scope vocabulary

166 distinct scopes appear in the history. They are short lowercase nouns naming the
_area touched_, not the feature. Reuse an existing scope before inventing one.

### Frontend / UI

`component` (175) · `page` (35) · `layout` (22) · `dashboard` (22) · `landing` (16) ·
`view` (14) · `home` (7) · `about` (3) · `template` (10) · `asset` (18) · `font` (3) ·
`content` (3) · `class` (3)

Atomic-design scopes also appear: `atom` (3), `molecule` (6), `organism` (3).

```
feat(component): add responsive navbar
style(layout): update body and main classes for improved scrolling behavior
refactor(view): update service.blade
```

### Backend / data

`serv-act` (68, Next.js server actions) · `api` (27) · `orm` (30) · `prisma` (16) ·
`schema` (7) · `seed` (12) · `seeder` (5) · `migration` (5) · `model` (5) · `db` (4) ·
`postgres` (5) · `redis` (7) · `controller` (7) · `policy` (7) · `resource` (8) ·
`route` (12) · `auth` (9) · `login` (16) · `otp` (3) · `data` (14) · `service` (3)

```
feat(serv-act): update get-announcement
chore(orm): generated current prisma model
test(api): tracking error /auth/local
```

### Infra / deployment

`docker` (85) · `traefik` (40) · `workflow` (40, CI/CD) · `proxy` (5) · `vcs` (27) ·
`release` (8) · `chatwoot` (4) · `9router` (3)

```
chore(traefik): update .env.example with new environment variables
refactor(workflow): migrate to new auto release github action
fix(docker): rollback to aeeb367
```

### Tooling / project config

`project` (87) · `config` (83) · `core` (68) · `package` (36) · `lock` (31) ·
`composer` (29) · `dependency` (22) · `env` (28) · `formatter` (25) · `example` (13) ·
`constant` (12) · `type` (13) · `lib` (30) / `libs` (5) · `util` (18) / `utils` (5) ·
`hook` (8) · `file` (38) · `script` (4) · `ai` (7) · `boilerplate` (5) · `app` (5) ·
`filament` (5) · `laravel` (15) · `scribe` (3) · `mock` (3) · `test` (5) · `style` (4)

```
feat(package): add scripts, n some packages
docs(env): refactored as cit-standard
chore(formatter): sync with cit-standard prettier
```

### Project-specific / feature-named scopes

Occasionally the scope names the deliverable rather than a technical area —
`romantic-ivory` (11), `nikah-fix` (11), `tryout` (3), `bum` (3), `migrate` (7), `any` (6),
`all` (release-wide). Use this only when the work is confined to one named product surface.

### Rules

- Scope is lowercase, singular, one word; hyphenate only when the concept needs it (`serv-act`).
- Prefer the repo's existing scopes — check its log before minting a new one.
- `core` means cross-cutting project internals; `project` means repo-level metadata;
  `config` means a config file specifically.
- Watch for existing typo-variants in the log (`worfklow` for `workflow`, `components`
  vs `component`) — normalize to the correct/majority spelling.
