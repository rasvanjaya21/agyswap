# Graph Report - agyswap  (2026-10-06)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 701 nodes · 975 edges · 27 communities (25 shown, 2 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 139 edges (avg confidence: 0.94)
- Token cost: 37,949 input · 379 output

## Graph Freshness
- Built from commit: `0613f238`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Switch Safety & Review
- Incremental Build Skill
- Security Checklist Reference
- Ship Skill & Accessibility
- Agy Auth Observation
- Textual TUI App
- Task Planning Skill
- Commit Message Conventions
- Code Review Method
- Test-Driven Development Skill
- Performance Checklist
- Performance Checklist Copy
- Launch Readiness Checklist
- Review Security Checklist
- Render Polish Build Log
- Agent & Contributor Guides
- Quota Fetching Plan
- Spec-Driven Development
- Prepare Skill Steps
- Observe Skill Recipes
- MCP Docs Servers
- Agyswap Package
- README Sections
- Prepare Run Report
- Dual-Window Quota Build
- Feature Capability Spec

## God Nodes (most connected - your core abstractions)
1. `Code Review and Quality` - 19 edges
2. `cmd_switch()` - 18 edges
3. `AgySwapApp` - 17 edges
4. `collect_usage()` - 16 edges
5. `locked_store()` - 15 edges
6. `setup()` - 15 edges
7. `fetch_pools()` - 15 edges
8. `Security Checklist` - 15 edges
9. `Security Checklist` - 15 edges
10. `Test-Driven Development` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Kuota` --references--> `Pool`  [INFERRED]
  architecture/SPEC.md → src/agyswap/usage.py
- `Architecture Decisions` --references--> `cmd_remove()`  [INFERRED]
  architecture/PLAN.md → src/agyswap/cli.py
- `Phase 1: Baseline (selesai)` --references--> `locked_store()`  [INFERRED]
  architecture/PLAN.md → src/agyswap/cli.py
- `Penyimpanan` --references--> `locked_store()`  [INFERRED]
  architecture/SPEC.md → src/agyswap/cli.py
- `Success Criteria` --references--> `test_force_still_saves_an_unstored_login()`  [INFERRED]
  architecture/SPEC.md → tests/test_swap.py

## Import Cycles
- None detected.

## Communities (27 total, 2 thin omitted)

### Community 0 - "Switch Safety & Review"
Cohesion: 0.06
Nodes (45): Invariants, Setelah review (render-polish + cli-safety), Login dan logout, Penyimpanan login, Proses, Task 4: arti baru `--force`, `--ignore-running` baru — selesai, FYI, Important (+37 more)

### Community 1 - "Incremental Build Skill"
Cohesion: 0.06
Nodes (34): Common Rationalizations, Contract-First Slicing, Correctness, Definition of Done, Definition of Done vs. Acceptance Criteria, Documentation, How to Apply, Implementation Rules (+26 more)

### Community 2 - "Security Checklist Reference"
Cohesion: 0.12
Nodes (17): AI / LLM Security, Authentication, Authorization, CORS Configuration, Data Protection, Dependency Security, Destructive Path Operations, Error Handling (+9 more)

### Community 3 - "Ship Skill & Accessibility"
Cohesion: 0.06
Nodes (35): Accessibility Checklist, Accessible Lists, /agyswap-ship, ARIA Roles, Buttons vs. Links, Cara rilis, Common Anti-Patterns, Common HTML Patterns (+27 more)

### Community 4 - "Agy Auth Observation"
Cohesion: 0.07
Nodes (25): How agy stores auth (verified on agy 1.3.0, Linux), Belum terobservasi, Data dir dan isolasi sesi, Host dan rate limit, Kuota per window (`retrieveUserQuotaSummary`), Observasi agy, Siklus token, Validasi (+17 more)

### Community 5 - "Textual TUI App"
Cohesion: 0.08
Nodes (3): AgySwapApp, done(), Confirm

### Community 6 - "Task Planning Skill"
Cohesion: 0.06
Nodes (31): /agyswap-plan, Common Rationalizations, Correctness, Definition of Done, Definition of Done vs. Acceptance Criteria, Documentation, How to Apply, Integration (+23 more)

### Community 7 - "Commit Message Conventions"
Cohesion: 0.07
Nodes (28): Ad-hoc types (one-offs, not to be reproduced), /agyswap-commit, Aturan pesan, Backend / data, Canonical types, `chore` — 276 uses (16%), Commit Message Conventions — rasvanjaya21, Core shape (+20 more)

### Community 8 - "Code Review Method"
Cohesion: 0.07
Nodes (29): 1. Correctness, 2. Readability & Simplicity, 3. Architecture, 4. Security, 5. Performance, Change Descriptions, Change Sizing, Code Review and Quality (+21 more)

### Community 9 - "Test-Driven Development Skill"
Cohesion: 0.04
Nodes (45): /agyswap-test, API / Integration Testing, Browser Testing with DevTools, Common Assertions, Common Rationalizations, DAMP Over DRY in Tests, Decision Guide, Discover the Stack First (+37 more)

### Community 10 - "Performance Checklist"
Cohesion: 0.08
Nodes (26): API, Backend Checklist, Cache checklist, Caching Strategies, Common Anti-Patterns, Connection pooling, Core Web Vitals Targets, CSS (+18 more)

### Community 11 - "Performance Checklist Copy"
Cohesion: 0.08
Nodes (26): API, Backend Checklist, Cache checklist, Caching Strategies, Common Anti-Patterns, Connection pooling, Core Web Vitals Targets, CSS (+18 more)

### Community 12 - "Launch Readiness Checklist"
Cohesion: 0.08
Nodes (25): Accessibility, Code Quality, Common Rationalizations, Documentation, Error Budget Release Gate, Error Reporting, Feature Flag Strategy, Infrastructure (+17 more)

### Community 13 - "Review Security Checklist"
Cohesion: 0.10
Nodes (19): AI / LLM Security, Authentication, Authorization, CORS Configuration, Data Protection, Dependency Security, Destructive Path Operations, Error Handling (+11 more)

### Community 14 - "Render Polish Build Log"
Cohesion: 0.12
Nodes (34): Build log: render-polish + cli-safety, Menunggu user, Task 1: Render tanpa spasi di ujung, kolom grup dinamis — selesai, Task 2: Konfirmasi `remove` dengan `--yes`/`-y` — selesai, Task 3: Bare `agyswap` di luar TTY exit 2 — selesai, Task 4: arti baru `--force`, `--ignore-running` baru — selesai, Task 5: Dokumen — selesai, Verifikasi akhir (+26 more)

### Community 15 - "Agent & Contributor Guides"
Cohesion: 0.13
Nodes (12): Agent workflow, Dev, Layout, Open work, Safety rules for agents, What this is, Agent Tooling, Commit Conventions (+4 more)

### Community 17 - "Quota Fetching Plan"
Cohesion: 0.06
Nodes (35): Task 1: Ambil kuota dari `retrieveUserQuotaSummary` — selesai, Kuota, Architecture Decisions, Catatan rilis, Checkpoint: Selesai, Dependency Graph, Implementation Plan: agyswap baseline v0.1.0, Open Questions (+27 more)

### Community 18 - "Spec-Driven Development"
Cohesion: 0.14
Nodes (14): Common Rationalizations, Keeping the Spec Alive, Method, Overview, Phase 0: Scope Check, Phase 1: Specify, Phase 2: Plan, Phase 3: Tasks (+6 more)

### Community 19 - "Prepare Skill Steps"
Cohesion: 0.17
Nodes (11): 10. Ringkasan, 1. TODO.md, 2. Selaraskan memory Claude dan Antigravity, 3. Hapus yang usang, 4. Hapus sisa debug, 5. Update docs, 6. Update skills, 7. Update pengetahuan kamu (+3 more)

### Community 20 - "Observe Skill Recipes"
Cohesion: 0.18
Nodes (10): A1. Catat lingkungan, A2. Yang wajib diobservasi, A3. Tulis peta, A. Observasi, /agyswap-observe, B. Validasi: jalankan, pantau, fix, Batas yang tidak boleh dilanggar, Format `architecture/OBSERVE.md` (+2 more)

### Community 21 - "MCP Docs Servers"
Cohesion: 0.60
Nodes (4): bunx, pytest, rich, textual

### Community 24 - "README Sections"
Cohesion: 0.15
Nodes (12): Architecture, Configuration, Credit, Deployment, Description, Development, Installation, Member (+4 more)

### Community 25 - "Prepare Run Report"
Cohesion: 0.17
Nodes (11): 1. TODO.md, 2. Memory Claude dan Antigravity, 3. Yang usang, 4. Sisa debug, 5. Docs, 6. Skills, 7. Pengetahuan, 8. Formatter, linter, test, build (+3 more)

### Community 26 - "Dual-Window Quota Build"
Cohesion: 0.06
Nodes (34): Build log: kuota 5 jam + mingguan, Commit, Menunggu user, Setelah review, Task 2: Tampilkan 5 jam dan mingguan di `list` dan TUI — selesai, Task 3: Perbarui dokumen ke perilaku baru — selesai, Verifikasi akhir, Architecture Decisions (+26 more)

### Community 27 - "Feature Capability Spec"
Cohesion: 0.08
Nodes (23): Boundaries, Boundaries, Capability Map: semua butir `TODO.md` yang bisa dikerjakan, Code Style, Commands, Dampak ke CLI dan TUI, Distribusi dan dokumentasi, Keamanan token (+15 more)

## Knowledge Gaps
- **361 isolated node(s):** `Important`, `Loop`, `Mode`, `Common Rationalizations`, `Contract-First Slicing` (+356 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 423 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `/agyswap-review` connect `Switch Safety & Review` to `Review Security Checklist`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Why does `locked_store()` connect `Switch Safety & Review` to `Quota Fetching Plan`, `Feature Capability Spec`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `cmd_switch()` (e.g. with `Lima sumbu` and `Boundaries`) actually correct?**
  _`cmd_switch()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `collect_usage()` (e.g. with `Architecture Decisions` and `Jalur yang belum dites otomatis`) actually correct?**
  _`collect_usage()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `locked_store()` (e.g. with `Invariants` and `Phase 1: Baseline (selesai)`) actually correct?**
  _`locked_store()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Important`, `Loop`, `Mode` to the rest of the system?**
  _361 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Switch Safety & Review` be split into smaller, more focused modules?**
  _Cohesion score 0.06448412698412699 - nodes in this community are weakly interconnected._