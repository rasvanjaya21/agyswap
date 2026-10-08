---
name: agyswap-build
description: Implementasikan task agyswap secara bertahap — red, green, verifikasi, commit. Tambahkan "auto" untuk menjalankan seluruh rencana yang sudah disetujui dalam satu putaran. Gunakan saat rencana sudah ada dan kode perlu ditulis.
version: 1.0.0
---

# /agyswap-build

Tahap **BUILD** dalam siklus agyswap (`/agyswap-prepare` → `/agyswap-observe` → `/agyswap-spec` → `/agyswap-plan` → `/agyswap-build` → `/agyswap-test` → `/agyswap-review` → `/agyswap-prepare` → `/agyswap-commit` → `/agyswap-ship`).

Kode yang bergantung pada perilaku agy meniru `architecture/OBSERVE.md`: nama service keyring, format token, endpoint, header, dan kode error diambil persis dari sana, tidak ditebak. Perilaku agy yang ditemukan saat build tapi belum ada di peta dicatat ke `OBSERVE.md` dulu.

## Mode

- `/agyswap-build` mengerjakan task berikutnya yang belum selesai, lalu berhenti.
- `/agyswap-build auto` mengerjakan semua task di rencana setelah satu kali persetujuan. Tidak lebih cepat per task; hanya menghilangkan jeda manusia di antara task. Butuh `architecture/SPEC.md`; kalau belum ada, minta user menjalankan `/agyswap-spec` dulu.

## Loop

1. Baca acceptance criteria task.
2. Muat konteks: kode, pola, dan fungsi yang sudah ada. Mulai dari `graphify query`, bukan grep.
3. Tulis test yang gagal untuk perilaku yang diharapkan (lihat `/agyswap-test`).
4. Implementasikan kode minimum sampai test lolos.
5. Jalankan `uv run ruff format .`, `uv run ruff check .`, dan `uv run pytest -q`. `uv build` hanya dijalankan kalau task menyentuh `pyproject.toml`, dependency, atau entry point.
6. Tandai task selesai di `architecture/PLAN.md`.
7. Commit hanya kalau user memintanya. Persetujuan `/agyswap-build auto` dihitung sebagai izin commit per task; stage hanya file yang disentuh task itu.

Catat hasilnya di `architecture/BUILD.md`: per task, apa yang diimplementasikan, test mana yang membuktikannya, dan apa yang sengaja ditunda. File itu adalah serah terima untuk task berikutnya.

## Aturan agyswap yang mengalahkan saran generik

- Baca `AGENTS.md` sebelum edit pertama, terutama bagian Invariants.
- Setiap perubahan store lewat `locked_store()` dan ditulis dengan `save_store()` (atomic, mode 0600). Jangan menulis `accounts.json` dengan cara lain.
- Hanya `switch_account` yang menulis keyring (lewat `switch`, `switch --strategy`, dan `auto`). Refresh usage, `import`, dan `export` tidak pernah menulis keyring.
- Jangan pernah menimpa login yang belum punya salinan di store.
- Jangan pernah mencetak nilai token (access, refresh, id) atau client secret, termasuk di log, pesan error, dan test.
- Client secret agy dibaca dari binary `agy` saat runtime. Jangan pernah meng-hardcode atau meng-commit-nya.
- Request jaringan selalu pakai timeout dan User-Agent non-default (lihat `usage._post`).
- Kerja yang memblokir (keyring, jaringan) di TUI dijalankan di worker thread, bukan di thread UI.
- Jangan menjalankan switch terhadap keyring sungguhan, dan jangan menyentuh `~/.agyswap/`, kecuali user memintanya. Uji manual memakai `AGYSWAP_HOME=$(mktemp -d)`.
- Pesan commit `type(scope): description`: huruf kecil, kalimat perintah, satu baris, tanpa trailer.

---

# Method

Prosedur di bawah di-vendor dari `addyosmani/agent-skills` (`skills/incremental-implementation`) pada commit `1401c8b`. Bagian agyswap di atas menang setiap kali keduanya bertentangan.

## Incremental Implementation

### Overview

Build in thin vertical slices — implement one piece, test it, verify it, then expand. Avoid implementing an entire feature in one pass. Each increment should leave the system in a working, testable state. This is the execution discipline that makes large features manageable.

### When to Use

- Implementing any multi-file change
- Building a new feature from a task breakdown
- Refactoring existing code
- Any time you're tempted to write more than ~100 lines before testing

**When NOT to use:** Single-file, single-function changes where the scope is already minimal.

### The Increment Cycle

```
┌──────────────────────────────────────┐
│                                      │
│   Implement ──→ Test ──→ Verify ──┐  │
│       ▲                           │  │
│       └───── Commit ◄─────────────┘  │
│              │                       │
│              ▼                       │
│          Next slice                  │
│                                      │
└──────────────────────────────────────┘
```

For each slice:

1. **Implement** the smallest complete piece of functionality
2. **Test** — run the test suite (or write a test if none exists)
3. **Verify** — confirm the slice works as expected (tests pass, build succeeds, manual check)
4. **Commit** -- save your progress with a descriptive message (see `git-workflow-and-versioning` for atomic commit guidance)
5. **Move to the next slice** — carry forward, don't restart

### Slicing Strategies

#### Vertical Slices (Preferred)

Build one complete path through the stack:

```
Slice 1: Create a task (DB + API + basic UI)
    → Tests pass, user can create a task via the UI

Slice 2: List tasks (query + API + UI)
    → Tests pass, user can see their tasks

Slice 3: Edit a task (update + API + UI)
    → Tests pass, user can modify tasks

Slice 4: Delete a task (delete + API + UI + confirmation)
    → Tests pass, full CRUD complete
```

Each slice delivers working end-to-end functionality.

#### Contract-First Slicing

When backend and frontend need to develop in parallel:

```
Slice 0: Define the API contract (types, interfaces, OpenAPI spec)
Slice 1a: Implement backend against the contract + API tests
Slice 1b: Implement frontend against mock data matching the contract
Slice 2: Integrate and test end-to-end
```

#### Risk-First Slicing

Tackle the riskiest or most uncertain piece first:

```
Slice 1: Prove the WebSocket connection works (highest risk)
Slice 2: Build real-time task updates on the proven connection
Slice 3: Add offline support and reconnection
```

If Slice 1 fails, you discover it before investing in Slices 2 and 3.

### Implementation Rules

#### Rule 0: Simplicity First

Before writing any code, ask: "What is the simplest thing that could work?"

After writing code, review it against these checks:
- Can this be done in fewer lines?
- Are these abstractions earning their complexity?
- Would a staff engineer look at this and say "why didn't you just..."?
- Am I building for hypothetical future requirements, or the current task?

```
SIMPLICITY CHECK:
✗ Generic EventBus with middleware pipeline for one notification
✓ Simple function call

✗ Abstract factory pattern for two similar components
✓ Two straightforward components with shared utilities

✗ Config-driven form builder for three forms
✓ Three form components
```

Three similar lines of code is better than a premature abstraction. Implement the naive, obviously-correct version first. Optimize only after correctness is proven with tests.

#### Rule 0.5: Scope Discipline

Touch only what the task requires.

Do NOT:
- "Clean up" code adjacent to your change
- Refactor imports in files you're not modifying
- Remove comments you don't fully understand
- Add features not in the spec because they "seem useful"
- Modernize syntax in files you're only reading

If you notice something worth improving outside your task scope, note it — don't fix it:

```
NOTICED BUT NOT TOUCHING:
- src/utils/format.ts has an unused import (unrelated to this task)
- The auth middleware could use better error messages (separate task)
→ Want me to create tasks for these?
```

#### Rule 1: One Thing at a Time

Each increment changes one logical thing. Don't mix concerns:

**Bad:** One commit that adds a new component, refactors an existing one, and updates the build config.

**Good:** Three separate commits — one for each change.

#### Rule 2: Keep It Compilable

After each increment, the project must build and existing tests must pass. Don't leave the codebase in a broken state between slices.

#### Rule 3: Feature Flags for Incomplete Features

If a feature isn't ready for users but you need to merge increments:

```typescript
// Feature flag for work-in-progress
const ENABLE_TASK_SHARING = process.env.FEATURE_TASK_SHARING === 'true';

if (ENABLE_TASK_SHARING) {
  // New sharing UI
}
```

This lets you merge small increments to the main branch without exposing incomplete work.

#### Rule 4: Safe Defaults

New code should default to safe, conservative behavior:

```typescript
// Safe: disabled by default, opt-in
export function createTask(data: TaskInput, options?: { notify?: boolean }) {
  const shouldNotify = options?.notify ?? false;
  // ...
}
```

#### Rule 5: Rollback-Friendly

Each increment should be independently revertable:

- Additive changes (new files, new functions) are easy to revert
- Modifications to existing code should be minimal and focused
- Database migrations should have corresponding rollback migrations
- Avoid deleting something in one commit and replacing it in the same commit — separate them

### Working with Agents

When directing an agent to implement incrementally:

```
"Let's implement Task 3 from the plan.

Start with just the database schema change and the API endpoint.
Don't touch the UI yet — we'll do that in the next increment.

After implementing, run the repository's test and build commands to
verify nothing is broken."
```

Be explicit about what's in scope and what's NOT in scope for each increment.

### Increment Checklist

After each increment, verify with the repository's own commands (see the test-driven-development skill's Discover the Stack First section):

- [ ] The change does one thing and does it completely
- [ ] All existing tests still pass (the repository's test command: `npm test`, `./gradlew test`, `pytest`, ...)
- [ ] The build succeeds (the repository's build command)
- [ ] Type checking passes, where the stack has one (`npx tsc --noEmit`, `mypy`, ...)
- [ ] Linting passes (the repository's lint command)
- [ ] The new functionality works as expected
- [ ] The change is committed with a descriptive message

**Note:** Run each verification command after a change that could affect it. After a successful run, don't repeat the same command unless the code has changed since — re-running on unchanged code adds no information.

### Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll test it all at the end" | Bugs compound. A bug in Slice 1 makes Slices 2-5 wrong. Test each slice. |
| "It's faster to do it all at once" | It *feels* faster until something breaks and you can't find which of 500 changed lines caused it. |
| "These changes are too small to commit separately" | Small commits are free. Large commits hide bugs and make rollbacks painful. |
| "I'll add the feature flag later" | If the feature isn't complete, it shouldn't be user-visible. Add the flag now. |
| "This refactor is small enough to include" | Refactors mixed with features make both harder to review and debug. Separate them. |
| "Let me run the build command again just to be sure" | After a successful run, repeating the same command adds nothing unless the code has changed since. Run it again after subsequent edits, not as reassurance. |

### Red Flags

- More than 100 lines of code written without running tests
- Multiple unrelated changes in a single increment
- "Let me just quickly add this too" scope expansion
- Skipping the test/verify step to move faster
- Build or tests broken between increments
- Large uncommitted changes accumulating
- Building abstractions before the third use case demands it
- Touching files outside the task scope "while I'm here"
- Creating new utility files for one-time operations
- Running the same build/test command twice in a row without any intervening code change

### Verification

After completing all increments for a task:

- [ ] Each increment was individually tested and committed
- [ ] The full test suite passes
- [ ] The build is clean
- [ ] The feature works end-to-end as specified
- [ ] No uncommitted changes remain

### See Also

Per-increment verification is the local check. Before declaring a task done, apply the project-wide Definition of Done as the final gate, the standing bar every increment clears regardless of the task. See the **Definition of Done** section under "Reference" at the end of this file.

---

# Reference

## Definition of Done

A standing, project-wide bar that every change must clear before it counts as done. Unlike acceptance criteria, which vary per task and answer "did we build the right thing?", the Definition of Done is the same every time and answers "is this finished to our standard?". Use it as the final gate in `planning-and-task-breakdown`, `incremental-implementation`, and `shipping-and-launch`.

### Definition of Done vs. Acceptance Criteria

| | Acceptance Criteria | Definition of Done |
|---|---|---|
| Scope | Specific to one task or spec | Applies to every increment |
| Changes | Different for each item | Fixed and reused |
| Answers | "Did we build *this thing*?" | "Is it *ready*?" |
| Owner | Defined when planning the task | Defined once for the project |
| Example | "User can reset password via email link" | "Tests pass, no regressions, docs updated" |

The two are complementary. A task is done only when **its** acceptance criteria are met **and** the standing Definition of Done is satisfied. Skipping either leaves work that looks finished but is not.

### The Standing Checklist

Apply this to every change before declaring it done.

#### Correctness
- [ ] All acceptance criteria for the task are met
- [ ] Code runs and behaves as intended, verified at runtime, not just compiled or typechecked
- [ ] New behavior is covered by tests that fail without the change and pass with it
- [ ] Existing tests still pass; no regressions introduced
- [ ] Edge cases and error paths are handled, not just the happy path

#### Quality
- [ ] Code reveals intent through naming and structure; no comments needed to explain *what* it does
- [ ] No duplicated business logic
- [ ] No dead code, debug output, or commented-out blocks left behind
- [ ] Changes are scoped to the task; no unrelated refactors snuck in
- [ ] Linting and formatting pass

The depth behind these items lives in `code-review-and-quality` (the five-axis review) and `code-simplification` (reducing complexity without changing behavior).

#### Integration
- [ ] Change works with the rest of the system, not just in isolation
- [ ] Database migrations, config changes, and feature flags are accounted for
- [ ] Backward compatibility considered for any public interface or API change

#### Documentation
- [ ] Public interfaces, APIs, and user-facing behavior are documented
- [ ] Architectural decisions worth preserving are recorded (see `documentation-and-adrs`)
- [ ] Documentation describes the current state in timeless language, not the change history

#### Ship-readiness
- [ ] Security implications reviewed for any untrusted input, auth, or data handling (see `security-and-hardening`)
- [ ] Observability in place for new critical paths (logs, metrics, traces) (see `observability-and-instrumentation`)
- [ ] Rollback path exists for anything risky (see `shipping-and-launch`)
- [ ] The human has reviewed and approved before merge or deploy

### How to Apply

- **Per task**: confirm the Correctness and Quality sections before checking the task off.
- **Per feature**: confirm Integration and Documentation before considering the feature complete.
- **Per release**: the full checklist is the floor; `shipping-and-launch` adds the deploy-specific gates on top.

Tailor the list to the project once, then reuse it unchanged. A Definition of Done that is renegotiated every sprint is not a Definition of Done.

### Red Flags

- "It's done, I just haven't run it yet": unverified work is not done.
- "Tests pass" used as a synonym for done while docs, regressions, or runtime verification are skipped.
- A different bar applied depending on deadline pressure.
- Acceptance criteria treated as the whole bar, with no standing quality floor.
- "Done" declared before human review on changes that need it.
