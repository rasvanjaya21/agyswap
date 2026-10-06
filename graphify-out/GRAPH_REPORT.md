# Graph Report - agyswap  (2026-10-06)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 745 nodes · 1072 edges · 27 communities (25 shown, 2 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 188 edges (avg confidence: 0.94)
- Token cost: 38,768 input · 373 output

## Graph Freshness
- Built from commit: `82927ef3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Switch Logic and Release Review
- Build Skill Methods
- Security Checklist Reference
- Ship Skill and Accessibility
- Repo Preparation Checklist
- Textual TUI Dashboard
- Plan Skill Methods
- Commit Message Conventions
- Code Review Quality Axes
- Test Skill Methods
- Performance Checklists
- Performance Checklists Duplicate
- Launch Readiness Checklist
- Review Skill Security Checklist
- Render Polish Build Log
- Ship v0.1.0 Decision
- Commit Record
- Quota Windows and Observation
- Spec Skill Phases
- Prepare Skill Steps
- Observe Skill Procedures
- MCP Docs Servers
- PyPI Distribution Name
- README Sections
- Render Polish Implementation Plan
- Agent Guide and Spec

## God Nodes (most connected - your core abstractions)
1. `collect_usage()` - 21 edges
2. `Code Review and Quality` - 19 edges
3. `setup()` - 18 edges
4. `AgySwapApp` - 17 edges
5. `cmd_switch()` - 17 edges
6. `locked_store()` - 16 edges
7. `make_token()` - 16 edges
8. `SwapError` - 15 edges
9. `fetch_pools()` - 15 edges
10. `Security Checklist` - 15 edges

## Surprising Connections (you probably didn't know these)
- `CLI dan TUI (pengganti accessibility)` --references--> `SwapError`  [INFERRED]
  architecture/SHIP.md → src/agyswap/cli.py
- `Kuota` --references--> `Pool`  [INFERRED]
  architecture/SPEC.md → src/agyswap/usage.py
- `Login dan logout` --references--> `cmd_add()`  [INFERRED]
  architecture/OBSERVE.md → src/agyswap/cli.py
- `Architecture Decisions` --references--> `cmd_remove()`  [INFERRED]
  architecture/PLAN.md → src/agyswap/cli.py
- `Phase 1: Baseline (selesai)` --references--> `locked_store()`  [INFERRED]
  architecture/PLAN.md → src/agyswap/cli.py

## Import Cycles
- None detected.

## Communities (27 total, 2 thin omitted)

### Community 0 - "Switch Logic and Release Review"
Cohesion: 0.07
Nodes (47): Invariants, Proses, Task 4: arti baru `--force`, `--ignore-running` baru — selesai, FYI, Important, Lima sumbu, Review rilis v0.1.0, Suggestion (+39 more)

### Community 1 - "Build Skill Methods"
Cohesion: 0.05
Nodes (37): /agyswap-build, Common Rationalizations, Contract-First Slicing, Correctness, Definition of Done, Definition of Done vs. Acceptance Criteria, Documentation, How to Apply (+29 more)

### Community 2 - "Security Checklist Reference"
Cohesion: 0.12
Nodes (17): AI / LLM Security, Authentication, Authorization, CORS Configuration, Data Protection, Dependency Security, Destructive Path Operations, Error Handling (+9 more)

### Community 3 - "Ship Skill and Accessibility"
Cohesion: 0.06
Nodes (33): Accessibility Checklist, Accessible Lists, /agyswap-ship, ARIA Roles, Buttons vs. Links, Cara rilis, Common Anti-Patterns, Common HTML Patterns (+25 more)

### Community 4 - "Repo Preparation Checklist"
Cohesion: 0.05
Nodes (31): Data dir dan isolasi sesi, Di luar rencana ini, 1. TODO.md, 2. Memory Claude dan Antigravity, 3. Yang usang, referensi proyek referensi, dan data pribadi, 4. Sisa debug, 5. Docs, 6. Skills (+23 more)

### Community 5 - "Textual TUI Dashboard"
Cohesion: 0.07
Nodes (8): AgySwapApp, done(), Confirm, Fitur yang belum ada, Platform, Rilis, Temuan review rilis (`architecture/REVIEW.md`), TODO

### Community 6 - "Plan Skill Methods"
Cohesion: 0.06
Nodes (31): /agyswap-plan, Common Rationalizations, Correctness, Definition of Done, Definition of Done vs. Acceptance Criteria, Documentation, How to Apply, Integration (+23 more)

### Community 7 - "Commit Message Conventions"
Cohesion: 0.07
Nodes (28): Ad-hoc types (one-offs, not to be reproduced), /agyswap-commit, Aturan pesan, Backend / data, Canonical types, `chore` — 276 uses (16%), Commit Message Conventions — rasvanjaya21, Core shape (+20 more)

### Community 8 - "Code Review Quality Axes"
Cohesion: 0.07
Nodes (29): 1. Correctness, 2. Readability & Simplicity, 3. Architecture, 4. Security, 5. Performance, Change Descriptions, Change Sizing, Code Review and Quality (+21 more)

### Community 9 - "Test Skill Methods"
Cohesion: 0.04
Nodes (45): /agyswap-test, API / Integration Testing, Browser Testing with DevTools, Common Assertions, Common Rationalizations, DAMP Over DRY in Tests, Decision Guide, Discover the Stack First (+37 more)

### Community 10 - "Performance Checklists"
Cohesion: 0.08
Nodes (26): API, Backend Checklist, Cache checklist, Caching Strategies, Common Anti-Patterns, Connection pooling, Core Web Vitals Targets, CSS (+18 more)

### Community 11 - "Performance Checklists Duplicate"
Cohesion: 0.08
Nodes (26): API, Backend Checklist, Cache checklist, Caching Strategies, Common Anti-Patterns, Connection pooling, Core Web Vitals Targets, CSS (+18 more)

### Community 12 - "Launch Readiness Checklist"
Cohesion: 0.08
Nodes (25): Accessibility, Code Quality, Common Rationalizations, Documentation, Error Budget Release Gate, Error Reporting, Feature Flag Strategy, Infrastructure (+17 more)

### Community 13 - "Review Skill Security Checklist"
Cohesion: 0.08
Nodes (23): /agyswap-review, AI / LLM Security, Authentication, Authorization, Cakupan, CORS Configuration, Data Protection, Dependency Security (+15 more)

### Community 14 - "Render Polish Build Log"
Cohesion: 0.07
Nodes (52): Build log: render-polish + cli-safety, Menunggu user, Setelah review (render-polish + cli-safety), Task 1: Render tanpa spasi di ujung, kolom grup dinamis — selesai, Task 2: Konfirmasi `remove` dengan `--yes`/`-y` — selesai, Task 3: Bare `agyswap` di luar TTY exit 2 — selesai, Task 4: arti baru `--force`, `--ignore-running` baru — selesai, Task 5: Dokumen — selesai (+44 more)

### Community 15 - "Ship v0.1.0 Decision"
Cohesion: 0.20
Nodes (8): Cek sebelum GO, CLI dan TUI (pengganti accessibility), Hasil publish, Keputusan: **NO-GO**, Langkah berikutnya, Rencana rollback, Ship: v0.1.0 (rilis pertama), Versi

### Community 16 - "Commit Record"
Cohesion: 0.33
Nodes (5): Alasan pengelompokan, Commit, Commit yang dibuat, File yang sengaja tidak di-commit, Hook

### Community 17 - "Quota Windows and Observation"
Cohesion: 0.05
Nodes (36): Build log: kuota 5 jam + mingguan, Commit, Menunggu user, Setelah review, Task 1: Ambil kuota dari `retrieveUserQuotaSummary` — selesai, Task 3: Perbarui dokumen ke perilaku baru — selesai, Verifikasi akhir, Belum terobservasi (+28 more)

### Community 18 - "Spec Skill Phases"
Cohesion: 0.12
Nodes (15): /agyswap-spec, Common Rationalizations, Keeping the Spec Alive, Method, Overview, Phase 0: Scope Check, Phase 1: Specify, Phase 2: Plan (+7 more)

### Community 19 - "Prepare Skill Steps"
Cohesion: 0.17
Nodes (11): 10. Ringkasan, 1. TODO.md, 2. Selaraskan memory Claude dan Antigravity, 3. Hapus yang usang, 4. Hapus sisa debug, 5. Update docs, 6. Update skills, 7. Update pengetahuan kamu (+3 more)

### Community 20 - "Observe Skill Procedures"
Cohesion: 0.18
Nodes (10): A1. Catat lingkungan, A2. Yang wajib diobservasi, A3. Tulis peta, A. Observasi, /agyswap-observe, B. Validasi: jalankan, pantau, fix, Batas yang tidak boleh dilanggar, Format `architecture/OBSERVE.md` (+2 more)

### Community 21 - "MCP Docs Servers"
Cohesion: 0.60
Nodes (4): bunx, pytest, rich, textual

### Community 24 - "README Sections"
Cohesion: 0.15
Nodes (12): Architecture, Configuration, Credit, Deployment, Description, Development, Installation, Member (+4 more)

### Community 26 - "Render Polish Implementation Plan"
Cohesion: 0.08
Nodes (27): Task 2: Tampilkan 5 jam dan mingguan di `list` dan TUI — selesai, Architecture Decisions, Catatan rilis, Checkpoint: Selesai, Checkpoint: Setelah Task 1–2, Checkpoint: Setelah Task 1–3, Dependency Graph, Implementation Plan: render-polish + cli-safety (+19 more)

### Community 27 - "Agent Guide and Spec"
Cohesion: 0.05
Nodes (35): Agent workflow, Dev, How agy stores auth (verified on agy 1.3.0, Linux), Layout, Open work, Safety rules for agents, What this is, Boundaries (+27 more)

## Knowledge Gaps
- **372 isolated node(s):** `FYI`, `Lima sumbu`, `Common Rationalizations`, `Contract-First Slicing`, `Correctness` (+367 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 444 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Yang wajib dicek, yang terlewat oleh review generik` connect `Switch Logic and Release Review` to `Review Skill Security Checklist`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Why does `/agyswap-review` connect `Review Skill Security Checklist` to `Switch Logic and Release Review`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Why does `Test di agyswap` connect `Switch Logic and Release Review` to `Test Skill Methods`, `Quota Windows and Observation`, `Render Polish Build Log`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `collect_usage()` (e.g. with `Architecture Decisions` and `Important`) actually correct?**
  _`collect_usage()` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `cmd_switch()` (e.g. with `Boundaries` and `Jalur yang belum dites otomatis`) actually correct?**
  _`cmd_switch()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `FYI`, `Lima sumbu`, `Common Rationalizations` to the rest of the system?**
  _372 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Switch Logic and Release Review` be split into smaller, more focused modules?**
  _Cohesion score 0.06790890269151138 - nodes in this community are weakly interconnected._