# Graph Report - agyswap  (2026-10-08)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 915 nodes · 1593 edges · 49 communities (46 shown, 3 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 328 edges (avg confidence: 0.94)
- Token cost: 3,353 input · 579 output

## Graph Freshness
- Built from commit: `01c5bfed`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CLI Argument Parsing
- Incremental Build Rules
- AI and Application Security
- Accessibility and ARIA Standards
- Documentation and Path Utilities
- TUI and App Components
- Planning and Integration Rules
- Commit Message Conventions
- Code Review Best Practices
- Testing Standards and Guides
- Web Development Checklists
- Backend and Frontend Performance
- Quality and Monitoring Strategy
- Security and Input Validation
- Token and Store Management
- Release and Shipping Process
- Commit and Push Guidelines
- Usage and Quota Monitoring
- Specification Lifecycle Management
- Environment Preparation Skills
- Observation and Validation Skills
- Dependencies and Tooling
- CLI Tooling
- Project README and Architecture
- Module Specifications and Security
- Build Logs and Aliasing
- Agent Workflow and Contributing
- Release Review and Bugfixes
- Error Handling and Retries
- CLI Auto-Switch Logic
- Account Quarantine and Validation
- Implementation Roadmap
- Switch Strategy Implementation
- System Specifications and Boundaries
- Release Review and Invariants
- Export and Exception Handling
- Import and Export Commands
- System Preparation Checklist
- TUI Error Resilience Testing
- Usage Cache Management
- Definition of Done Checklist
- JSON Output and Status
- Shipping and Versioning Skills
- Review Methodology Skills
- Five-Axis Review Criteria
- Step-by-Step Review Process
- Accessibility Navigation Checks
- Manual Testing Procedures

## God Nodes (most connected - your core abstractions)
1. `setup()` - 62 edges
2. `make_token()` - 37 edges
3. `collect_usage()` - 32 edges
4. `Gelombang v0.2.0` - 32 edges
5. `_add()` - 31 edges
6. `switch_account()` - 24 edges
7. `locked_store()` - 23 edges
8. `SwapError` - 22 edges
9. `main()` - 20 edges
10. `Review rilis v0.2.0` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Kuota` --references--> `Pool`  [INFERRED]
  architecture/SPEC.md → src/agyswap/usage.py
- `Perilaku` --references--> `SwapError`  [INFERRED]
  architecture/SPEC.md → src/agyswap/cli.py
- `Testing Strategy` --references--> `account_usage()`  [INFERRED]
  architecture/SPEC.md → src/agyswap/usage.py
- `How agy stores auth (verified on agy 1.3.1, Linux)` --references--> `fetch_pools()`  [INFERRED]
  AGENTS.md → src/agyswap/usage.py
- `3. Yang usang` --references--> `_post()`  [INFERRED]
  architecture/PREPARE.md → src/agyswap/usage.py

## Import Cycles
- None detected.

## Communities (49 total, 3 thin omitted)

### Community 0 - "CLI Argument Parsing"
Cohesion: 0.15
Nodes (3): build_parser(), _countdown(), _percent()

### Community 1 - "Incremental Build Rules"
Cohesion: 0.05
Nodes (37): /agyswap-build, Common Rationalizations, Contract-First Slicing, Correctness, Definition of Done, Definition of Done vs. Acceptance Criteria, Documentation, How to Apply (+29 more)

### Community 2 - "AI and Application Security"
Cohesion: 0.12
Nodes (17): AI / LLM Security, Authentication, Authorization, CORS Configuration, Data Protection, Dependency Security, Destructive Path Operations, Error Handling (+9 more)

### Community 3 - "Accessibility and ARIA Standards"
Cohesion: 0.20
Nodes (10): Accessibility Checklist, Accessible Lists, ARIA Roles, Buttons vs. Links, Common Anti-Patterns, Common HTML Patterns, Form Labels, Quick Reference: ARIA Live Regions (+2 more)

### Community 4 - "Documentation and Path Utilities"
Cohesion: 0.09
Nodes (15): checkout(), md_page(), rst_pages(), rst_title(), run(), textual_pages(), expand(), toctree() (+7 more)

### Community 5 - "TUI and App Components"
Cohesion: 0.07
Nodes (5): Task 3: Tombol `x` — selesai, AgySwapApp, done(), Confirm, test_tui_x_toggles_disable_by_email()

### Community 6 - "Planning and Integration Rules"
Cohesion: 0.06
Nodes (31): /agyswap-plan, Common Rationalizations, Correctness, Definition of Done, Definition of Done vs. Acceptance Criteria, Documentation, How to Apply, Integration (+23 more)

### Community 7 - "Commit Message Conventions"
Cohesion: 0.07
Nodes (28): Ad-hoc types (one-offs, not to be reproduced), /agyswap-commit, Aturan pesan, Backend / data, Canonical types, `chore` — 276 uses (16%), Commit Message Conventions — rasvanjaya21, Core shape (+20 more)

### Community 8 - "Code Review Best Practices"
Cohesion: 0.12
Nodes (17): Change Descriptions, Change Sizing, Code Review and Quality, Common Rationalizations, Dead Code Hygiene, Dependency Discipline, Handling Disagreements, Honesty in Review (+9 more)

### Community 9 - "Testing Standards and Guides"
Cohesion: 0.04
Nodes (45): /agyswap-test, API / Integration Testing, Browser Testing with DevTools, Common Assertions, Common Rationalizations, DAMP Over DRY in Tests, Decision Guide, Discover the Stack First (+37 more)

### Community 10 - "Web Development Checklists"
Cohesion: 0.08
Nodes (26): API, Backend Checklist, Cache checklist, Caching Strategies, Common Anti-Patterns, Connection pooling, Core Web Vitals Targets, CSS (+18 more)

### Community 11 - "Backend and Frontend Performance"
Cohesion: 0.08
Nodes (26): API, Backend Checklist, Cache checklist, Caching Strategies, Common Anti-Patterns, Connection pooling, Core Web Vitals Targets, CSS (+18 more)

### Community 12 - "Quality and Monitoring Strategy"
Cohesion: 0.08
Nodes (25): Accessibility, Code Quality, Common Rationalizations, Documentation, Error Budget Release Gate, Error Reporting, Feature Flag Strategy, Infrastructure (+17 more)

### Community 13 - "Security and Input Validation"
Cohesion: 0.12
Nodes (17): AI / LLM Security, Authentication, Authorization, CORS Configuration, Data Protection, Dependency Security, Destructive Path Operations, Error Handling (+9 more)

### Community 14 - "Token and Store Management"
Cohesion: 0.20
Nodes (22): Store, switch, remove, make_token(), refresh_of(), setup(), test_add_slot_never_overwrites_other_account(), test_add_slot_zero_is_rejected(), test_auto_saves_unstored_live_login_first(), test_export_import_roundtrip() (+14 more)

### Community 15 - "Release and Shipping Process"
Cohesion: 0.18
Nodes (10): Cara rilis (dijalankan user), Cek sebelum GO, Hasil publish, Keputusan: **GO**, Rencana rollback, Risiko yang diterima, Riwayat, Ship: v0.1.0 (rilis pertama) (+2 more)

### Community 16 - "Commit and Push Guidelines"
Cohesion: 0.40
Nodes (4): Alasan pengelompokan, Commit, Push, Tidak di-commit

### Community 17 - "Usage and Quota Monitoring"
Cohesion: 0.05
Nodes (46): Belum terobservasi, Data dir dan isolasi sesi, Host dan rate limit, Kuota, Kuota per window (`retrieveUserQuotaSummary`), Login dan logout, Observasi agy, Penyimpanan login (+38 more)

### Community 18 - "Specification Lifecycle Management"
Cohesion: 0.12
Nodes (15): /agyswap-spec, Common Rationalizations, Keeping the Spec Alive, Method, Overview, Phase 0: Scope Check, Phase 1: Specify, Phase 2: Plan (+7 more)

### Community 19 - "Environment Preparation Skills"
Cohesion: 0.17
Nodes (11): 10. Ringkasan, 1. TODO.md, 2. Selaraskan memory Claude dan Antigravity, 3. Hapus yang usang, 4. Hapus sisa debug, 5. Update docs, 6. Update skills, 7. Update pengetahuan kamu (+3 more)

### Community 20 - "Observation and Validation Skills"
Cohesion: 0.18
Nodes (10): A1. Catat lingkungan, A2. Yang wajib diobservasi, A3. Tulis peta, A. Observasi, /agyswap-observe, B. Validasi: jalankan, pantau, fix, Batas yang tidak boleh dilanggar, Format `architecture/OBSERVE.md` (+2 more)

### Community 21 - "Dependencies and Tooling"
Cohesion: 0.60
Nodes (4): bunx, pytest, rich, textual

### Community 24 - "Project README and Architecture"
Cohesion: 0.15
Nodes (12): Architecture, Configuration, Credit, Deployment, Description, Development, Installation, Member (+4 more)

### Community 25 - "Module Specifications and Security"
Cohesion: 0.04
Nodes (46): Bentuk store, Boundaries (gelombang ini), Dampak gabungan ke CLI dan TUI, Gelombang 2026-10-08: modul tersisa, Keamanan token, Keamanan token, Keamanan token, Keamanan token (+38 more)

### Community 26 - "Build Logs and Aliasing"
Cohesion: 0.17
Nodes (14): Build log: gelombang 2026-10-08 (v0.2.0), Menunggu user, Task 12: Dokumen — selesai, Task 1: Alias — selesai, Task 2: Disable/enable — selesai, Verifikasi akhir, Architecture Decisions, Task 1 (selesai): Alias dan target lewat alias (+6 more)

### Community 27 - "Agent Workflow and Contributing"
Cohesion: 0.09
Nodes (19): Agent workflow, Dev, How agy stores auth (verified on agy 1.3.1, Linux), Layout, Open work, Safety rules for agents, What this is, Agent Tooling (+11 more)

### Community 28 - "Release Review and Bugfixes"
Cohesion: 0.12
Nodes (31): Celah test dari test-engineer (ditutup), Medium / Suggestion dari security dan code review (diperbaiki), Review rilis v0.2.0, _add(), _export_file(), _fail(), _pools(), test_add_slot_move_keeps_alias_and_disable() (+23 more)

### Community 29 - "Error Handling and Retries"
Cohesion: 0.08
Nodes (17): Task 6: Backoff 429 — selesai, Perbaikan temuan review dan ship (2026-10-08), test_corrupt_store_is_a_swap_error(), test_fetch_pools_maps_http_errors(), boom(), test_invalid_grant_says_token_revoked(), test_keyring_read_failure_is_not_signed_out(), test_list_exits_1_when_every_account_fails() (+9 more)

### Community 30 - "CLI Auto-Switch Logic"
Cohesion: 0.15
Nodes (23): Task 8: `auto` — selesai, CLI, _auto_setup(), fake(), _row(), test_auto_leaves_a_disabled_active_account(), test_auto_refuses_while_agy_runs(), test_auto_stays_below_threshold() (+15 more)

### Community 31 - "Account Quarantine and Validation"
Cohesion: 0.10
Nodes (18): Task 4: Karantina — selesai, Gelombang v0.2.0, _expiring(), _revoked_post(), test_account_text_shows_alias(), test_add_clears_revoked_mark_but_keeps_alias_and_manual(), test_alias_set_clear_and_target(), test_fresh_token_fails_when_no_client_is_accepted() (+10 more)

### Community 32 - "Implementation Roadmap"
Cohesion: 0.11
Nodes (17): Checkpoint: Selesai, Checkpoint: Setelah Task 1–3, Checkpoint: Setelah Task 7–9, Dependency Graph, Implementation Plan: gelombang 2026-10-08 (v0.2.0), Open Questions, Overview, Phase 1: account-flags (+9 more)

### Community 33 - "Switch Strategy Implementation"
Cohesion: 0.21
Nodes (15): Task 7: `switch --strategy` — selesai, Risks and Mitigations, Task 7 (selesai): `switch --strategy` dan `--threshold`, Task 8 (selesai): `agyswap auto`, Important (diperbaiki), agy_running(), auto_message(), cmd_auto() (+7 more)

### Community 34 - "System Specifications and Boundaries"
Cohesion: 0.12
Nodes (16): Boundaries, Capability Map: semua butir `TODO.md` yang bisa dikerjakan, Code Style, Commands, Distribusi dan dokumentasi, Kuota, Objective, Open Questions (+8 more)

### Community 35 - "Release Review and Invariants"
Cohesion: 0.20
Nodes (13): Invariants, Critical, Pengecekan yang bersih, Review rilis v0.2.0, Tidak diperbaiki (masuk `TODO.md`), Untuk rilis, Aturan agyswap yang mengalahkan saran generik, Yang wajib dicek, yang terlewat oleh review generik (+5 more)

### Community 36 - "Export and Exception Handling"
Cohesion: 0.26
Nodes (9): 5. Docs, Testing Strategy, cmd_export(), confirm_remove(), load_store(), read_token(), _secret_tool(), SwapError (+1 more)

### Community 37 - "Import and Export Commands"
Cohesion: 0.21
Nodes (9): Task 10–11: `export` / `import` — selesai, cmd_add(), cmd_import(), email_of(), next_slot(), _read_export(), slot_for_email(), _valid_entry() (+1 more)

### Community 38 - "System Preparation Checklist"
Cohesion: 0.17
Nodes (11): 1. TODO.md, 2. Memory Claude dan Antigravity, 3. Yang usang, 4. Sisa debug, 6. Skills, 7. Pengetahuan, 8. Formatter, linter, test, build, 9. Graphify (+3 more)

### Community 39 - "TUI Error Resilience Testing"
Cohesion: 0.20
Nodes (8): Apa yang dibuktikan setiap test, Jalur error dan TUI (dari ship dan review rilis v0.1.0), _run_tui(), test_dropped_connection_becomes_a_row_error(), test_secret_tool_timeout_is_a_swap_error(), test_tui_shows_refresh_error_instead_of_exiting(), test_tui_survives_refresh_on_empty_store(), test_tui_unexpected_refresh_error_shows_only_its_type()

### Community 40 - "Usage Cache Management"
Cohesion: 0.29
Nodes (8): Task 5: Cache `usage.json` — selesai, _ago(), load_usage(), _pool_json(), store_path(), _update_usage_cache(), usage_path(), _write_private()

### Community 41 - "Definition of Done Checklist"
Cohesion: 0.20
Nodes (10): Correctness, Definition of Done, Definition of Done vs. Acceptance Criteria, Documentation, How to Apply, Integration, Quality, Red Flags (+2 more)

### Community 42 - "JSON Output and Status"
Cohesion: 0.36
Nodes (7): Task 9: `--json` — selesai, Jalur yang belum dites otomatis, cmd_list(), cmd_status(), _emit(), main(), row_json()

### Community 43 - "Shipping and Versioning Skills"
Cohesion: 0.25
Nodes (7): /agyswap-ship, Cara rilis, Keputusan, Method, Realitas agyswap yang harus dicek sebelum GO, Reference, Tentukan versi (semver)

### Community 44 - "Review Methodology Skills"
Cohesion: 0.29
Nodes (6): /agyswap-review, Cakupan, Fan-out paralel, Lima sumbu, Method, Reference

### Community 45 - "Five-Axis Review Criteria"
Cohesion: 0.33
Nodes (6): 1. Correctness, 2. Readability & Simplicity, 3. Architecture, 4. Security, 5. Performance, The Five-Axis Review

### Community 46 - "Step-by-Step Review Process"
Cohesion: 0.33
Nodes (6): Review Process, Step 1: Understand the Context, Step 2: Review the Tests First, Step 3: Review the Implementation, Step 4: Categorize Findings, Step 5: Verify the Verification

### Community 47 - "Accessibility Navigation Checks"
Cohesion: 0.33
Nodes (6): Content, Essential Checks, Forms, Keyboard Navigation, Screen Readers, Visual

## Knowledge Gaps
- **392 isolated node(s):** `Common Rationalizations`, `Contract-First Slicing`, `Correctness`, `Definition of Done vs. Acceptance Criteria`, `Documentation` (+387 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 495 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Yang wajib dicek, yang terlewat oleh review generik` connect `Release Review and Invariants` to `Review Methodology Skills`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Why does `/agyswap-review` connect `Review Methodology Skills` to `Release Review and Invariants`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Why does `locked_store()` connect `Release Review and Invariants` to `CLI Argument Parsing`, `System Specifications and Boundaries`, `Export and Exception Handling`, `Import and Export Commands`, `Usage Cache Management`, `Usage and Quota Monitoring`, `Module Specifications and Security`, `Build Logs and Aliasing`, `Agent Workflow and Contributing`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `collect_usage()` (e.g. with `Task 1: Alias — selesai` and `Task 2: Disable/enable — selesai`) actually correct?**
  _`collect_usage()` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 31 inferred relationships involving `Gelombang v0.2.0` (e.g. with `cmd_add()` and `pick_account()`) actually correct?**
  _`Gelombang v0.2.0` has 31 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Common Rationalizations`, `Contract-First Slicing`, `Correctness` to the rest of the system?**
  _392 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Incremental Build Rules` be split into smaller, more focused modules?**
  _Cohesion score 0.05263157894736842 - nodes in this community are weakly interconnected._