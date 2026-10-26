# Graph Report - agyswap  (2026-10-26)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 971 nodes · 1679 edges · 56 communities (50 shown, 6 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 327 edges (avg confidence: 0.94)
- Token cost: 3,964 input · 654 output

## Graph Freshness
- Built from commit: `d9af5198`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CLI Infrastructure
- Incremental Implementation Rules
- Security and Data Protection
- Accessibility and ARIA Standards
- Documentation and Path Handling
- TUI App Actions
- Planning and Definition of Done
- Commit Message Conventions
- Code Review Guidelines
- Testing Best Practices
- Backend and Caching Checklist
- Web Performance and Frontend
- Post-Launch Quality Standards
- LLM and Auth Security
- Token Store Operations
- Account State Validation
- Commit Grouping Logic
- Core Utilities and Logic
- Specification Lifecycle
- Environment Preparation Skills
- Observation and Validation Skills
- Development Tools and Dependencies
- CLI Entry Point
- Project README and Architecture
- Module Specifications
- TUI Input Handling
- Agent Workflow and Safety
- Account Management Tests
- Error Handling and TUI Tests
- Account Switching Logic Tests
- Quota and Token Refresh
- Implementation Roadmap
- CLI-TUI Parity Strategy
- Capability Map and Objectives
- Store Locking and Commands
- Release and Shipping Process
- Architecture and UI Decisions
- Project Preparation Checklist
- Interactive TUI Dashboard
- Usage Cache and Storage
- Quality Assurance Checklist
- Release Review and Verification
- Shipping and Versioning Skills
- Review Methodology Skills
- Five-Axis Review Criteria
- Review Process Steps
- Accessibility Content Checks
- Release Verification Tests
- TUI Export Security Fixes
- Import and Export Security
- CLI Interactive Prompts
- TUI Component Composition
- Build Tasks and Validation
- Manual Testing Procedures
- TUI Loading State Tests

## God Nodes (most connected - your core abstractions)
1. `setup()` - 63 edges
2. `make_token()` - 37 edges
3. `_add()` - 32 edges
4. `Gelombang v0.2.0` - 32 edges
5. `SwapError` - 28 edges
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
- `How agy stores auth (verified on agy 1.3.1, Linux)` --references--> `fetch_pools()`  [INFERRED]
  AGENTS.md → src/agyswap/usage.py
- `Kuota` --references--> `_post()`  [INFERRED]
  architecture/OBSERVE.md → src/agyswap/usage.py

## Import Cycles
- None detected.

## Communities (56 total, 6 thin omitted)

### Community 0 - "CLI Infrastructure"
Cohesion: 0.11
Nodes (11): Testing Strategy, account_text(), _ago(), build_parser(), cmd_list(), _color(), _countdown(), _emit() (+3 more)

### Community 1 - "Incremental Implementation Rules"
Cohesion: 0.05
Nodes (37): /agyswap-build, Common Rationalizations, Contract-First Slicing, Correctness, Definition of Done, Definition of Done vs. Acceptance Criteria, Documentation, How to Apply (+29 more)

### Community 2 - "Security and Data Protection"
Cohesion: 0.12
Nodes (17): AI / LLM Security, Authentication, Authorization, CORS Configuration, Data Protection, Dependency Security, Destructive Path Operations, Error Handling (+9 more)

### Community 3 - "Accessibility and ARIA Standards"
Cohesion: 0.20
Nodes (10): Accessibility Checklist, Accessible Lists, ARIA Roles, Buttons vs. Links, Common Anti-Patterns, Common HTML Patterns, Form Labels, Quick Reference: ARIA Live Regions (+2 more)

### Community 4 - "Documentation and Path Handling"
Cohesion: 0.09
Nodes (15): checkout(), md_page(), rst_pages(), rst_title(), run(), textual_pages(), expand(), toctree() (+7 more)

### Community 5 - "TUI App Actions"
Cohesion: 0.17
Nodes (4): AgySwapApp, done(), done(), done()

### Community 6 - "Planning and Definition of Done"
Cohesion: 0.06
Nodes (31): /agyswap-plan, Common Rationalizations, Correctness, Definition of Done, Definition of Done vs. Acceptance Criteria, Documentation, How to Apply, Integration (+23 more)

### Community 7 - "Commit Message Conventions"
Cohesion: 0.07
Nodes (28): Ad-hoc types (one-offs, not to be reproduced), /agyswap-commit, Aturan pesan, Backend / data, Canonical types, `chore` — 276 uses (16%), Commit Message Conventions — rasvanjaya21, Core shape (+20 more)

### Community 8 - "Code Review Guidelines"
Cohesion: 0.12
Nodes (17): Change Descriptions, Change Sizing, Code Review and Quality, Common Rationalizations, Dead Code Hygiene, Dependency Discipline, Handling Disagreements, Honesty in Review (+9 more)

### Community 9 - "Testing Best Practices"
Cohesion: 0.04
Nodes (45): /agyswap-test, API / Integration Testing, Browser Testing with DevTools, Common Assertions, Common Rationalizations, DAMP Over DRY in Tests, Decision Guide, Discover the Stack First (+37 more)

### Community 10 - "Backend and Caching Checklist"
Cohesion: 0.08
Nodes (26): API, Backend Checklist, Cache checklist, Caching Strategies, Common Anti-Patterns, Connection pooling, Core Web Vitals Targets, CSS (+18 more)

### Community 11 - "Web Performance and Frontend"
Cohesion: 0.08
Nodes (26): API, Backend Checklist, Cache checklist, Caching Strategies, Common Anti-Patterns, Connection pooling, Core Web Vitals Targets, CSS (+18 more)

### Community 12 - "Post-Launch Quality Standards"
Cohesion: 0.08
Nodes (25): Accessibility, Code Quality, Common Rationalizations, Documentation, Error Budget Release Gate, Error Reporting, Feature Flag Strategy, Infrastructure (+17 more)

### Community 13 - "LLM and Auth Security"
Cohesion: 0.12
Nodes (17): AI / LLM Security, Authentication, Authorization, CORS Configuration, Data Protection, Dependency Security, Destructive Path Operations, Error Handling (+9 more)

### Community 14 - "Token Store Operations"
Cohesion: 0.18
Nodes (20): Store, switch, remove, _export_file(), make_token(), refresh_of(), test_add_slot_never_overwrites_other_account(), test_auto_saves_unstored_live_login_first(), test_export_import_roundtrip(), test_force_skips_syncing_the_live_token() (+12 more)

### Community 15 - "Account State Validation"
Cohesion: 0.16
Nodes (18): Gelombang v0.2.0, setup(), test_add_clears_revoked_mark_but_keeps_alias_and_manual(), test_alias_set_clear_and_target(), test_corrupt_usage_cache_is_ignored(), test_import_drops_alias_taken_by_another_account(), test_import_rejects_unreadable_or_foreign_files(), test_import_rejects_whole_file_on_bad_entry() (+10 more)

### Community 16 - "Commit Grouping Logic"
Cohesion: 0.40
Nodes (4): Alasan pengelompokan, Commit, Commit, Tidak di-commit

### Community 17 - "Core Utilities and Logic"
Cohesion: 0.10
Nodes (18): Invariants, Penyimpanan login, Perilaku, Jalur yang belum dites otomatis, collect_usage(), one(), account_usage(), fetch_pools() (+10 more)

### Community 18 - "Specification Lifecycle"
Cohesion: 0.12
Nodes (15): /agyswap-spec, Common Rationalizations, Keeping the Spec Alive, Method, Overview, Phase 0: Scope Check, Phase 1: Specify, Phase 2: Plan (+7 more)

### Community 19 - "Environment Preparation Skills"
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

### Community 25 - "Module Specifications"
Cohesion: 0.04
Nodes (49): Bentuk store, Boundaries (gelombang ini), Dampak gabungan ke CLI dan TUI, Gelombang 2026-10-08: modul tersisa, Keamanan token, Keamanan token, Keamanan token, Keamanan token (+41 more)

### Community 27 - "Agent Workflow and Safety"
Cohesion: 0.06
Nodes (31): Agent workflow, Dev, How agy stores auth (verified on agy 1.3.1, Linux), Layout, Open work, Safety rules for agents, What this is, Belum terobservasi (+23 more)

### Community 28 - "Account Management Tests"
Cohesion: 0.13
Nodes (23): Review rilis v0.2.0, _add(), fake(), _fail(), _pools(), test_add_slot_move_keeps_alias_and_disable(), test_alias_can_change_case_on_same_account(), test_auto_json_reports_saved_slot_after_switch() (+15 more)

### Community 29 - "Error Handling and TUI Tests"
Cohesion: 0.08
Nodes (16): Jalur error dan TUI (dari ship dan review rilis v0.1.0), _run_tui(), test_dropped_connection_becomes_a_row_error(), test_fetch_pools_maps_http_errors(), boom(), test_invalid_grant_says_token_revoked(), test_post_keeps_http_errors_for_callers(), test_quota_429_is_named() (+8 more)

### Community 30 - "Account Switching Logic Tests"
Cohesion: 0.18
Nodes (15): _auto_setup(), _revoked_post(), _row(), test_account_text_shows_alias(), test_auto_leaves_a_disabled_active_account(), test_auto_refuses_while_agy_runs(), test_auto_stays_below_threshold(), test_auto_switches_when_active_is_over_threshold() (+7 more)

### Community 31 - "Quota and Token Refresh"
Cohesion: 0.17
Nodes (10): Apa yang dibuktikan setiap test, Kuota dan render, _expiring(), test_account_text_full_bucket_row_has_no_trailing_space(), test_account_text_groups_5h_and_weekly(), test_account_text_widens_group_column_for_long_names(), test_fetch_pools_reads_5h_and_weekly_windows(), fake_post() (+2 more)

### Community 32 - "Implementation Roadmap"
Cohesion: 0.11
Nodes (17): Checkpoint: Selesai, Checkpoint: Setelah Task 1–2, Checkpoint: Setelah Task 3–4, Implementation Plan: gelombang 2026-10-09 (paritas CLI–TUI dan rapikan TUI), Open Questions, Overview, Phase 1: Kursor dan pesan, Phase 2: Fitur CLI di TUI (+9 more)

### Community 33 - "CLI-TUI Parity Strategy"
Cohesion: 0.12
Nodes (24): Celah test (dari `test-engineer`, mutasi yang hidup), Yang wajib dicek, Code Style, Keamanan token, Testing Strategy, Gelombang 2026-10-09 (paritas CLI–TUI, persiapan 0.3.0), Test di agyswap, agy_running() (+16 more)

### Community 34 - "Capability Map and Objectives"
Cohesion: 0.08
Nodes (23): Boundaries, Capability Map: semua butir `TODO.md` yang bisa dikerjakan, Commands, Distribusi dan dokumentasi, Gelombang 2026-10-09: paritas CLI–TUI dan rapikan TUI, Kuota, Kursor, Objective (+15 more)

### Community 35 - "Store Locking and Commands"
Cohesion: 0.19
Nodes (19): Boundaries, Tombol, Aturan agyswap yang mengalahkan saran generik, Yang wajib dicek, yang terlewat oleh review generik, auto_message(), cmd_add(), cmd_alias(), cmd_disable() (+11 more)

### Community 36 - "Release and Shipping Process"
Cohesion: 0.20
Nodes (9): 0.3.1 (patch), Cek, Hasil publish, Keputusan: GO, Perintah rilis, Risiko yang diterima, Rollback, Ship (+1 more)

### Community 37 - "Architecture and UI Decisions"
Cohesion: 0.29
Nodes (3): Architecture Decisions, Suggestion yang tidak diambil, More

### Community 38 - "Project Preparation Checklist"
Cohesion: 0.18
Nodes (10): 1. TODO.md, 2. Memory Claude dan Antigravity, 3. Yang usang, 4. Sisa debug, 5. Docs, 6. Skills, 7. Pengetahuan, 8. Formatter, linter, test, build (+2 more)

### Community 39 - "Interactive TUI Dashboard"
Cohesion: 0.12
Nodes (3): Task 3: `n`, `m` More, `b`/`u`/`e`/`i` — selesai, _auto(), _switch_best()

### Community 40 - "Usage Cache and Storage"
Cohesion: 0.20
Nodes (10): Temuan review v0.2.0 (persiapan rilis 0.3.0) — selesai, Tidak diperbaiki (masuk `TODO.md`), load_usage(), _pool_json(), _private_dir(), _update_usage_cache(), usage_path(), _write_private() (+2 more)

### Community 41 - "Quality Assurance Checklist"
Cohesion: 0.20
Nodes (10): Correctness, Definition of Done, Definition of Done vs. Acceptance Criteria, Documentation, How to Apply, Integration, Quality, Red Flags (+2 more)

### Community 42 - "Release Review and Verification"
Cohesion: 0.22
Nodes (7): Diperbaiki, Important: dua refresh yang selesai bersamaan menggandakan kartu (`src/agyswap/tui.py`, `_show`), Low (security): cache `setup-uv` di job build rilis (`.github/workflows/publish.yml`), Review rilis 0.3.0 (2026-10-09), Rilis, Verifikasi, test_tui_overlapping_refreshes_never_duplicate_cards()

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

### Community 47 - "Accessibility Content Checks"
Cohesion: 0.33
Nodes (6): Content, Essential Checks, Forms, Keyboard Navigation, Screen Readers, Visual

### Community 48 - "Release Verification Tests"
Cohesion: 0.15
Nodes (9): Perbaikan temuan review dan ship (2026-10-08), test_add_slot_zero_is_rejected(), test_corrupt_store_is_a_swap_error(), test_keyring_read_failure_is_not_signed_out(), test_list_exits_1_when_every_account_fails(), test_locked_store_is_exclusive(), test_requests_never_follow_redirects(), test_save_store_leaves_no_temp_file() (+1 more)

### Community 49 - "TUI Export Security Fixes"
Cohesion: 0.36
Nodes (6): Perbaikan review rilis 0.3.0 — selesai, Medium (security): export dari TUI menaruh refresh token di cwd (`tui.py`, `action_export`), _abspath(), done(), _export(), test_tui_best_and_auto_use_the_cli_defaults_and_messages()

### Community 50 - "Import and Export Security"
Cohesion: 0.18
Nodes (11): Low (security): escape sequence dari file import (`cli.py`, `_valid_entry`, `_valid_alias`, `cmd_import`), cmd_import(), cmd_status(), email_of(), next_slot(), _printable(), _read_export(), slot_for_email() (+3 more)

### Community 51 - "CLI Interactive Prompts"
Cohesion: 0.31
Nodes (9): CLI, test_bare_agyswap_without_tty_exits_2(), test_email_of_garbage(), test_remove_asks_and_cancels_on_no(), test_remove_ctrl_d_or_ctrl_c_cancels(), test_remove_enter_defaults_to_no(), test_remove_warns_for_active_account_and_removes_on_yes(), test_remove_without_tty_needs_yes() (+1 more)

### Community 53 - "Build Tasks and Validation"
Cohesion: 0.14
Nodes (15): Build log: gelombang 2026-10-09 (paritas CLI–TUI dan rapikan TUI), Ditunda, Task 1: Kursor selalu terlihat — selesai, Task 2: Instruksi CLI dan TUI terpisah — selesai, Task 4: Default nama file export — selesai, Task 5: Loading, toast, scrollbar — selesai, Task 6: Dokumen — selesai, Validasi (+7 more)

## Knowledge Gaps
- **391 isolated node(s):** `Common Rationalizations`, `Contract-First Slicing`, `Correctness`, `Definition of Done vs. Acceptance Criteria`, `Documentation` (+386 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 514 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `locked_store()` connect `Store Locking and Commands` to `CLI Infrastructure`, `CLI-TUI Parity Strategy`, `Capability Map and Objectives`, `Usage Cache and Storage`, `Core Utilities and Logic`, `Import and Export Security`, `Module Specifications`?**
  _High betweenness centrality (0.128) - this node is a cross-community bridge._
- **Why does `Yang wajib dicek, yang terlewat oleh review generik` connect `Store Locking and Commands` to `CLI-TUI Parity Strategy`, `Review Methodology Skills`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Why does `/agyswap-review` connect `Review Methodology Skills` to `Store Locking and Commands`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Are the 31 inferred relationships involving `Gelombang v0.2.0` (e.g. with `cmd_add()` and `pick_account()`) actually correct?**
  _`Gelombang v0.2.0` has 31 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `SwapError` (e.g. with `Invariants` and `Temuan review v0.2.0 (persiapan rilis 0.3.0) — selesai`) actually correct?**
  _`SwapError` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Common Rationalizations`, `Contract-First Slicing`, `Correctness` to the rest of the system?**
  _391 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CLI Infrastructure` be split into smaller, more focused modules?**
  _Cohesion score 0.1076923076923077 - nodes in this community are weakly interconnected._