# Graph Report - agyswap  (2026-11-02)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 978 nodes · 1698 edges · 57 communities (51 shown, 6 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 335 edges (avg confidence: 0.94)
- Token cost: 3,691 input · 686 output

## Graph Freshness
- Built from commit: `f2b5018e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CLI and Argument Parsing
- Implementation Rules and DoD
- Security and Data Protection
- Accessibility and HTML Patterns
- Documentation and Path Utilities
- TUI Application Actions
- Planning and Integration Skills
- Commit Message Conventions
- Code Review and Quality
- Testing Strategy and Methods
- Web Development Checklist
- Backend and Frontend Checklist
- Shipping and Rollback Strategy
- Security and Input Validation
- Token and Account Management
- Account and Pool Testing
- Commit Guidelines
- Utility Functions and Usage
- Specification and Scoping Skills
- Project Preparation and Cleanup
- Observation and Validation Skills
- Development Tools and Dependencies
- CLI Tooling
- Project README and Architecture
- Module Specifications and Boundaries
- TUI Input Prompts
- Agent Workflow and Observation
- Pre-Launch Checklist
- Error Handling and TUI Tests
- Release Review and Keyring Tests
- Quota and Token Testing
- Implementation Plan and Milestones
- Error Handling and Storage
- Capability Map and Specifications
- Store and Command Validation
- Release and Shipping Process
- Architecture and UI Decisions
- Preparation and Maintenance Tasks
- Store Invariants and Cache
- Quality and Ship-Readiness
- Account Switching Logic
- Shipping and Versioning Skills
- Review Methodology Skills
- Five-Axis Review Criteria
- Review Process Steps
- Accessibility and Content Checks
- Review Findings and HTTP Tests
- Import and Export Actions
- TUI Automation Actions
- CLI Interaction and Removal
- TUI Confirmation Dialogs
- Build and Release Tasks
- Manual and Automated Testing
- Monitoring and Post-Launch
- Rollout and Rollback Sequence

## God Nodes (most connected - your core abstractions)
1. `setup()` - 64 edges
2. `make_token()` - 37 edges
3. `_add()` - 32 edges
4. `Gelombang v0.2.0` - 32 edges
5. `SwapError` - 29 edges
6. `AgySwapApp` - 25 edges
7. `locked_store()` - 24 edges
8. `collect_usage()` - 23 edges
9. `switch_account()` - 23 edges
10. `cmd_auto()` - 22 edges

## Surprising Connections (you probably didn't know these)
- `Perilaku` --references--> `SwapError`  [INFERRED]
  architecture/SPEC.md → src/agyswap/cli.py
- `Kuota` --references--> `Pool`  [INFERRED]
  architecture/SPEC.md → src/agyswap/usage.py
- `Testing Strategy` --references--> `account_usage()`  [INFERRED]
  architecture/SPEC.md → src/agyswap/usage.py
- `How agy stores auth (verified on agy 1.4.12, Linux)` --references--> `fetch_pools()`  [INFERRED]
  AGENTS.md → src/agyswap/usage.py
- `Kuota` --references--> `_post()`  [INFERRED]
  architecture/OBSERVE.md → src/agyswap/usage.py

## Import Cycles
- None detected.

## Communities (57 total, 6 thin omitted)

### Community 0 - "CLI and Argument Parsing"
Cohesion: 0.11
Nodes (10): Testing Strategy, account_text(), _ago(), build_parser(), cmd_list(), _color(), _countdown(), _emit() (+2 more)

### Community 1 - "Implementation Rules and DoD"
Cohesion: 0.05
Nodes (37): /agyswap-build, Common Rationalizations, Contract-First Slicing, Correctness, Definition of Done, Definition of Done vs. Acceptance Criteria, Documentation, How to Apply (+29 more)

### Community 2 - "Security and Data Protection"
Cohesion: 0.12
Nodes (17): AI / LLM Security, Authentication, Authorization, CORS Configuration, Data Protection, Dependency Security, Destructive Path Operations, Error Handling (+9 more)

### Community 3 - "Accessibility and HTML Patterns"
Cohesion: 0.20
Nodes (10): Accessibility Checklist, Accessible Lists, ARIA Roles, Buttons vs. Links, Common Anti-Patterns, Common HTML Patterns, Form Labels, Quick Reference: ARIA Live Regions (+2 more)

### Community 4 - "Documentation and Path Utilities"
Cohesion: 0.09
Nodes (15): checkout(), md_page(), rst_pages(), rst_title(), run(), textual_pages(), expand(), toctree() (+7 more)

### Community 5 - "TUI Application Actions"
Cohesion: 0.19
Nodes (3): Task 2: Instruksi CLI dan TUI terpisah — selesai, AgySwapApp, done()

### Community 6 - "Planning and Integration Skills"
Cohesion: 0.06
Nodes (31): /agyswap-plan, Common Rationalizations, Correctness, Definition of Done, Definition of Done vs. Acceptance Criteria, Documentation, How to Apply, Integration (+23 more)

### Community 7 - "Commit Message Conventions"
Cohesion: 0.07
Nodes (28): Ad-hoc types (one-offs, not to be reproduced), /agyswap-commit, Aturan pesan, Backend / data, Canonical types, `chore` — 276 uses (16%), Commit Message Conventions — rasvanjaya21, Core shape (+20 more)

### Community 8 - "Code Review and Quality"
Cohesion: 0.12
Nodes (17): Change Descriptions, Change Sizing, Code Review and Quality, Common Rationalizations, Dead Code Hygiene, Dependency Discipline, Handling Disagreements, Honesty in Review (+9 more)

### Community 9 - "Testing Strategy and Methods"
Cohesion: 0.04
Nodes (45): /agyswap-test, API / Integration Testing, Browser Testing with DevTools, Common Assertions, Common Rationalizations, DAMP Over DRY in Tests, Decision Guide, Discover the Stack First (+37 more)

### Community 10 - "Web Development Checklist"
Cohesion: 0.08
Nodes (26): API, Backend Checklist, Cache checklist, Caching Strategies, Common Anti-Patterns, Connection pooling, Core Web Vitals Targets, CSS (+18 more)

### Community 11 - "Backend and Frontend Checklist"
Cohesion: 0.08
Nodes (26): API, Backend Checklist, Cache checklist, Caching Strategies, Common Anti-Patterns, Connection pooling, Core Web Vitals Targets, CSS (+18 more)

### Community 12 - "Shipping and Rollback Strategy"
Cohesion: 0.20
Nodes (10): Common Rationalizations, Error Budget Release Gate, Feature Flag Strategy, Overview, Red Flags, Rollback Strategy, See Also, Shipping and Launch (+2 more)

### Community 13 - "Security and Input Validation"
Cohesion: 0.12
Nodes (17): AI / LLM Security, Authentication, Authorization, CORS Configuration, Data Protection, Dependency Security, Destructive Path Operations, Error Handling (+9 more)

### Community 14 - "Token and Account Management"
Cohesion: 0.21
Nodes (22): Store, switch, remove, _export_file(), make_token(), refresh_of(), setup(), test_add_slot_never_overwrites_other_account(), test_auto_saves_unstored_live_login_first(), test_email_of_and_cmd_add_support_agy_1_4_id_token_email() (+14 more)

### Community 15 - "Account and Pool Testing"
Cohesion: 0.10
Nodes (28): Gelombang v0.2.0, _add(), fake(), _pools(), _revoked_post(), test_account_text_shows_alias(), test_add_clears_revoked_mark_but_keeps_alias_and_manual(), test_alias_set_clear_and_target() (+20 more)

### Community 16 - "Commit Guidelines"
Cohesion: 0.40
Nodes (4): Alasan pengelompokan, Commit, Commit, Tidak di-commit

### Community 17 - "Utility Functions and Usage"
Cohesion: 0.09
Nodes (20): Perubahan 1.3.3 → 1.4.12 (Linux), Perilaku, Test di agyswap, collect_usage(), one(), _expiry(), account_usage(), _agy_client_ids() (+12 more)

### Community 18 - "Specification and Scoping Skills"
Cohesion: 0.12
Nodes (15): /agyswap-spec, Common Rationalizations, Keeping the Spec Alive, Method, Overview, Phase 0: Scope Check, Phase 1: Specify, Phase 2: Plan (+7 more)

### Community 19 - "Project Preparation and Cleanup"
Cohesion: 0.17
Nodes (11): 10. Ringkasan, 1. TODO.md, 2. Selaraskan memory Claude dan Antigravity, 3. Hapus yang usang, 4. Hapus sisa debug, 5. Update docs, 6. Update skills, 7. Update pengetahuan kamu (+3 more)

### Community 20 - "Observation and Validation Skills"
Cohesion: 0.18
Nodes (10): A1. Catat lingkungan, A2. Yang wajib diobservasi, A3. Tulis peta, A. Observasi, /agyswap-observe, B. Validasi: jalankan, pantau, fix, Batas yang tidak boleh dilanggar, Format `architecture/OBSERVE.md` (+2 more)

### Community 21 - "Development Tools and Dependencies"
Cohesion: 0.60
Nodes (4): bunx, pytest, rich, textual

### Community 24 - "Project README and Architecture"
Cohesion: 0.15
Nodes (12): Architecture, Configuration, Credit, Deployment, Description, Development, Installation, Member (+4 more)

### Community 25 - "Module Specifications and Boundaries"
Cohesion: 0.04
Nodes (49): Bentuk store, Boundaries (gelombang ini), Dampak gabungan ke CLI dan TUI, Gelombang 2026-10-08: modul tersisa, Keamanan token, Keamanan token, Keamanan token, Keamanan token (+41 more)

### Community 27 - "Agent Workflow and Observation"
Cohesion: 0.06
Nodes (30): Agent workflow, Dev, How agy stores auth (verified on agy 1.4.12, Linux), Layout, Open work, Safety rules for agents, What this is, Belum terobservasi (+22 more)

### Community 28 - "Pre-Launch Checklist"
Cohesion: 0.29
Nodes (7): Accessibility, Code Quality, Documentation, Infrastructure, Performance, Security, The Pre-Launch Checklist

### Community 29 - "Error Handling and TUI Tests"
Cohesion: 0.08
Nodes (15): Jalur error dan TUI (dari ship dan review rilis v0.1.0), _run_tui(), test_dropped_connection_becomes_a_row_error(), test_list_exit_code_ignores_disabled_accounts(), test_list_exits_1_when_every_account_fails(), test_list_json_marks_stale_and_disabled_reason(), test_malformed_cache_entry_is_not_shown(), test_post_keeps_http_errors_for_callers() (+7 more)

### Community 30 - "Release Review and Keyring Tests"
Cohesion: 0.14
Nodes (23): Review rilis v0.2.0, _auto_setup(), _fail(), _row(), test_add_slot_move_keeps_alias_and_disable(), test_agy_running_ignores_only_the_bg_updater(), test_alias_can_change_case_on_same_account(), test_auto_leaves_a_disabled_active_account() (+15 more)

### Community 31 - "Quota and Token Testing"
Cohesion: 0.13
Nodes (12): Apa yang dibuktikan setiap test, Kuota dan render, _expiring(), test_account_text_full_bucket_row_has_no_trailing_space(), test_account_text_groups_5h_and_weekly(), test_account_text_widens_group_column_for_long_names(), test_fetch_pools_reads_5h_and_weekly_windows(), fake_post() (+4 more)

### Community 32 - "Implementation Plan and Milestones"
Cohesion: 0.11
Nodes (17): Checkpoint: Selesai, Checkpoint: Setelah Task 1–2, Checkpoint: Setelah Task 3–4, Implementation Plan: gelombang 2026-10-09 (paritas CLI–TUI dan rapikan TUI), Open Questions, Overview, Phase 1: Kursor dan pesan, Phase 2: Fitur CLI di TUI (+9 more)

### Community 33 - "Error Handling and Storage"
Cohesion: 0.12
Nodes (17): Penyimpanan login, Code Style, Keamanan token, Testing Strategy, Jalur yang belum dites otomatis, cmd_export(), cmd_status(), confirm_remove() (+9 more)

### Community 34 - "Capability Map and Specifications"
Cohesion: 0.08
Nodes (23): Boundaries, Capability Map: semua butir `TODO.md` yang bisa dikerjakan, Commands, Distribusi dan dokumentasi, Gelombang 2026-10-09: paritas CLI–TUI dan rapikan TUI, Kuota, Kursor, Objective (+15 more)

### Community 35 - "Store and Command Validation"
Cohesion: 0.18
Nodes (23): Yang wajib dicek, Boundaries, Tombol, Aturan agyswap yang mengalahkan saran generik, Yang wajib dicek, yang terlewat oleh review generik, agy_running(), auto_message(), cmd_add() (+15 more)

### Community 36 - "Release and Shipping Process"
Cohesion: 0.20
Nodes (9): 0.3.1 (patch), Cek, Hasil publish, Keputusan: GO, Perintah rilis, Risiko yang diterima, Rollback, Ship (+1 more)

### Community 37 - "Architecture and UI Decisions"
Cohesion: 0.29
Nodes (3): Architecture Decisions, Suggestion yang tidak diambil, More

### Community 38 - "Preparation and Maintenance Tasks"
Cohesion: 0.18
Nodes (10): 1. TODO.md, 2. Memory Claude dan Antigravity, 3. Yang usang, 4. Sisa debug, 5. Docs, 6. Skills, 7. Pengetahuan, 8. Formatter, linter, test, build (+2 more)

### Community 40 - "Store Invariants and Cache"
Cohesion: 0.20
Nodes (11): Invariants, Temuan review v0.2.0 (persiapan rilis 0.3.0) — selesai, Tidak diperbaiki (masuk `TODO.md`), load_usage(), _pool_json(), _private_dir(), store_path(), _update_usage_cache() (+3 more)

### Community 41 - "Quality and Ship-Readiness"
Cohesion: 0.20
Nodes (10): Correctness, Definition of Done, Definition of Done vs. Acceptance Criteria, Documentation, How to Apply, Integration, Quality, Red Flags (+2 more)

### Community 42 - "Account Switching Logic"
Cohesion: 0.43
Nodes (5): cmd_auto(), _max_used(), pick_account(), ok(), _readable()

### Community 43 - "Shipping and Versioning Skills"
Cohesion: 0.25
Nodes (7): /agyswap-ship, Cara rilis, Keputusan, Method, Realitas agyswap yang harus dicek sebelum GO, Reference, Tentukan versi (semver)

### Community 44 - "Review Methodology Skills"
Cohesion: 0.29
Nodes (6): /agyswap-review, Cakupan, Fan-out paralel, Lima sumbu, Method, Reference

### Community 45 - "Five-Axis Review Criteria"
Cohesion: 0.33
Nodes (6): 1. Correctness, 2. Readability & Simplicity, 3. Architecture, 4. Security, 5. Performance, The Five-Axis Review

### Community 46 - "Review Process Steps"
Cohesion: 0.33
Nodes (6): Review Process, Step 1: Understand the Context, Step 2: Review the Tests First, Step 3: Review the Implementation, Step 4: Categorize Findings, Step 5: Verify the Verification

### Community 47 - "Accessibility and Content Checks"
Cohesion: 0.33
Nodes (6): Content, Essential Checks, Forms, Keyboard Navigation, Screen Readers, Visual

### Community 48 - "Review Findings and HTTP Tests"
Cohesion: 0.10
Nodes (14): Perbaikan temuan review dan ship (2026-10-08), test_add_slot_zero_is_rejected(), test_corrupt_store_is_a_swap_error(), test_fetch_pools_maps_http_errors(), boom(), test_invalid_grant_says_token_revoked(), test_keyring_read_failure_is_not_signed_out(), test_locked_store_is_exclusive() (+6 more)

### Community 49 - "Import and Export Actions"
Cohesion: 0.33
Nodes (4): _abspath(), done(), done(), done()

### Community 50 - "TUI Automation Actions"
Cohesion: 0.40
Nodes (3): Task 3: `n`, `m` More, `b`/`u`/`e`/`i` — selesai, _auto(), _switch_best()

### Community 51 - "CLI Interaction and Removal"
Cohesion: 0.31
Nodes (9): CLI, test_bare_agyswap_without_tty_exits_2(), test_email_of_garbage(), test_remove_asks_and_cancels_on_no(), test_remove_ctrl_d_or_ctrl_c_cancels(), test_remove_enter_defaults_to_no(), test_remove_warns_for_active_account_and_removes_on_yes(), test_remove_without_tty_needs_yes() (+1 more)

### Community 53 - "Build and Release Tasks"
Cohesion: 0.07
Nodes (36): Build log: gelombang 2026-10-09 (paritas CLI–TUI dan rapikan TUI), Ditunda, Perbaikan review rilis 0.3.0 — selesai, Task 1: Kursor selalu terlihat — selesai, Task 4: Default nama file export — selesai, Task 5: Loading, toast, scrollbar — selesai, Task 6: Dokumen — selesai, Validasi (+28 more)

### Community 55 - "Monitoring and Post-Launch"
Cohesion: 0.50
Nodes (4): Error Reporting, Monitoring and Observability, Post-Launch Verification, What to Monitor

### Community 56 - "Rollout and Rollback Sequence"
Cohesion: 0.50
Nodes (4): Rollout Decision Thresholds, Staged Rollout, The Rollout Sequence, When to Roll Back

## Knowledge Gaps
- **392 isolated node(s):** `Common Rationalizations`, `Contract-First Slicing`, `Correctness`, `Definition of Done vs. Acceptance Criteria`, `Documentation` (+387 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 517 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `locked_store()` connect `Store and Command Validation` to `CLI and Argument Parsing`, `Error Handling and Storage`, `Capability Map and Specifications`, `Store Invariants and Cache`, `Utility Functions and Usage`, `Build and Release Tasks`, `Module Specifications and Boundaries`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `Yang wajib dicek, yang terlewat oleh review generik` connect `Store and Command Validation` to `Review Methodology Skills`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Why does `/agyswap-review` connect `Review Methodology Skills` to `Store and Command Validation`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Are the 31 inferred relationships involving `Gelombang v0.2.0` (e.g. with `cmd_add()` and `pick_account()`) actually correct?**
  _`Gelombang v0.2.0` has 31 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `SwapError` (e.g. with `Invariants` and `Temuan review v0.2.0 (persiapan rilis 0.3.0) — selesai`) actually correct?**
  _`SwapError` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Common Rationalizations`, `Contract-First Slicing`, `Correctness` to the rest of the system?**
  _392 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CLI and Argument Parsing` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._