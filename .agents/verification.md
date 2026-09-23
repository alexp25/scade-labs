# Verification, requirements, traceability

Do not treat every REQ-xx mention as a confirmed trace link — classify each
one. See the table below.

## Lab 2 — explicit, both in prose and in data

- Informal client description (`docs/lab2/lab.md`): *"Cruise control must be
  safe. It should stop when needed, should not start in dangerous conditions,
  and if it stops for a safety reason the driver must be aware that they need
  to restart it manually."*
- REQ-01..REQ-04 (functional) + REQ-05/06 (non-functional: response time,
  testability) — full "SHALL" statements in lab.md's SRS activity.
- A markdown decision table (state × condition → new state × REQ) is the
  design artifact between requirements and code.
- 7 test cases (TC-01…TC-07) are documented **in lab.md itself** (not just in
  code) with an explicit statement: *"The REQ column here is the Test →
  Requirements direction: 'This test case verifies that REQ-X is met.'"* A
  consolidated REQ×TC traceability matrix table follows.
- The same linkage is carried as literal data in the code: each test tuple in
  `src/lab2/starter/lab2_cruise_control_starter.py` carries both a `tid`
  (e.g. `"TC-05"`) and a `req` (e.g. `"REQ-04"`) field, printed at runtime.
- **Verdict: EXPLICIT.** Stated in words and duplicated as data — not
  something a human must infer by cross-reading two artifacts.

## Lab 3 — requirements authored + traceability mechanism taught, both explicit; automated checks are comprehension-only

- `docs/lab3/lab.md` is where REQ-LIM-01..03 (Limiter), REQ-CNT-01..02
  (Counter), and the EARS rewrites of REQ-01/02/04 (plus new REQ-07/08 for
  Cruise Control) actually get authored, in EARS syntax, by the student.
  `src/lab3/solution/requirements.md` is the instructor reference answer set.
- There is **no automated check** of the free-text requirements (or the
  Activity 9A test-case sketch) a student writes. The lab has two automated
  components, both comprehension-only quizzes, same shape as Lab 4's
  reflection quiz: Activity 1A (`#ears-pattern-quiz`, Part 1, 4 questions,
  pattern recognition on canned example sentences) and the closing
  reflection quiz (`#reflection-quiz`, Part 9 area, 7 questions — several
  specifically test the `#pragma requirement` mechanism and the `reQ2`/`REQ-02`
  casing gap, see below). Neither quiz grades the student's *own* written
  REQ IDs, model, or test-case sketch — both use fixed example content with a
  single correct answer. Grading the requirements, the Limiter/Counter model,
  and the Activity 9A test-case sketch is all instructor review against the
  reference file/model.
- **Requirements panel usage is now a real, graded-by-instructor activity,
  not just described in prose.** Activities 2G and 4F have students link
  `REQ-LIM-01` and `REQ-CNT-01/02` to their own Limiter/Counter operators via
  Scade One's Requirements panel — the same `#pragma requirement <ID> #end`
  mechanism used later in Lab 4. Part 9 ("How Traceability Works in Scade
  One") explains this mechanism explicitly and shows the **real** existing
  excerpt from `src/lab4/starter/CruiseControl/assets/CC_design.swan`
  (`node #pragma requirement reQ2 #end cruise_control (...)`), using its
  `reQ2`/`REQ-02` casing mismatch as a deliberate, named teaching example of
  an un-validated traceability link — not a hidden defect being glossed
  over.
- **Verdict: EXPLICIT authorship of requirements AND explicit teaching of
  the traceability mechanism, but no automated verification of either the
  authored content or the student's own Requirements-panel links.** This is
  the first point in the repo where REQ IDs are *created*, and the first
  point where the `#pragma requirement` mechanism is explained rather than
  just used.

## Lab 4 — mixed: one explicit mechanism, partially realized (pre-existing gap, now explicitly taught)

- "The System (recap from Lab 2)" section restates the **state names and
  interface**, not the REQ-xx text.
- A 4-row state-transition table (`cc_disabled`/`cc_enabled`/`cc_active`/
  `cc_standby`) tags each transition with a REQ ID (REQ-01/02/04) — smaller
  than Lab 2's 6-row decision table but same shape.
- "Activity 7A — Traceability in Scade One" describes a **real tool
  feature**: Scade One's Requirements panel, used to link model elements to
  REQ IDs via `#pragma requirement` — the same mechanism Lab 3's Activities
  2G/4F already had students practice. Corroborated by
  `src/lab4/starter/CruiseControl/assets/CC_design.swan` containing exactly
  one such pragma (`#pragma requirement reQ2` on the `cruise_control` node)
  — **not** the seven element-level links (4 transitions + the top-level
  node + the `regulator` node + the internal `limiter` instances) the
  activity now instructs students to create, and its casing (`reQ2`) doesn't
  match the canonical `REQ-02` spelling used everywhere else (Lab 2, Lab 3,
  `evaluate_cc_full_report.py`'s `req` column). **The shipped reference model only
  partially demonstrates the mechanism it teaches, and the one pragma it
  does have is a near-miss on the canonical REQ ID string.** This gap
  pre-dates this session; what changed this session is that it's now
  **explicitly named and explained** (Lab 3 Part 9, Lab 4 Activity 7A) as a
  worked lesson on traceability discipline, rather than being an
  undocumented inconsistency a curious student might stumble on.
- "Activity 7B" is a pure reflection quiz (DO-178C/ISO 26262 discussion
  questions) — comprehension, not a trace artifact.
- The Python evaluation script's REQ tags (a `req` column in each
  `scenarios/*.csv` file, read by `evaluate_cc_full_report.py` and written into
  `results/summary.csv`) are **naming-based**: a label field, with no "this
  verifies REQ-X" sentence and no link to the in-tool Requirements panel.
  `evaluate_cc_full_report.py` and its `scenarios/*.csv` are real, committed files under
  `src/lab4/starter/CruiseControl/`. Lab 3 Part 9 now walks through exactly
  how a requirement becomes one of these scenario rows (worked example:
  REQ-01 → `tc03_brake_suspends.csv`-equivalent), so this is no longer an
  implicit convention students have to reverse-engineer.

## Lab 6 — proposed requirements only, explicitly not implemented or checked

- Lab 6 does not modify REQ-01–REQ-08 (`src/lab3/solution/requirements.md`)
  and does not touch `CC_design.swan`'s existing `#pragma requirement reQ2`
  link.
- Part 3 (Activity 3B) has students author two **new, proposed** REQ IDs
  — REQ-09/REQ-10, for an Automatic Emergency Braking extension — in EARS
  syntax, directly in `docs/lab6/lab.md`. These are explicitly and
  repeatedly labeled "proposed — not implemented in the shipped model":
  they are not added to `src/lab3/solution/requirements.md`, not linked via
  `#pragma requirement` anywhere, and not referenced by any
  `scenarios/*.csv` row or Python script.
- Activity 3C describes (in prose only) how Lab 4's existing scenario-CSV
  approach *would* be extended to exercise REQ-09 (a new
  `obstacle_distance` column, checkpoint rows tagged `req = REQ-09`,
  checked by trend rather than a single value — the same style already
  used for REQ-07 in `tc02_cc_active_regulates.csv`). No such column, CSV
  row, or script change actually exists in `src/lab4/`.
- **Verdict: REQ-09/REQ-10 are PROPOSED, PAPER-ONLY — not implemented, not
  traced, not automatically checked.** Do not treat their appearance in
  `docs/lab6/lab.md` as evidence they exist anywhere in the Lab 4 model or
  scripts.
- Parts 1–2's component/interface/constraint tables and diagrams *describe*
  the existing REQ-01–08-driven Lab 4 architecture; they don't add new
  trace links to it, and aren't themselves automatically checked
  (instructor-graded against the real model, same as Lab 3's free-text
  requirements deliverable).

## Test → requirement classification table

| Test | Exercises | REQ | Class | Evidence |
|---|---|---|---|---|
| TC-01..TC-07 (Lab 2) | full cruise-control state machine | REQ-01..04 | **EXPLICIT** | lab.md prose + `req`/`tid` fields in test tuples |
| `limiter_harness`/`counter_harness` (Lab 3) | clamp / increment behavior | REQ-LIM-01..03, REQ-CNT-01..02 (via Activities 2G/4F pragma links; `src/lab3/solution/assets/blocks.swan` carries these as the completed reference — see below) | **EXPLICIT instruction, student-performed; reference answer committed** | `docs/lab3/lab.md` Activities 2G/4F/3E/5C |
| `test_limiter.py`/`test_counter.py` (Lab 3, Part 7) | cycle the generated operator, per-test-case PASS/FAIL | REQ-LIM-01..03, REQ-CNT-01..02 | **EXPLICIT** — `req` field per test tuple, printed with each result; no `blocks.swan` parsing | `src/lab3/solution/test_limiter.py`, `test_counter.py`; `docs/lab3/lab.md` Activities 7C/7D |
| `test_limiter_advanced.py`/`test_counter_advanced.py` (Lab 3, Part 7) | same, plus static traceability + coverage reporting | REQ-LIM-01..03, REQ-CNT-01..02 | **EXPLICIT, machine-checked** — each script parses `blocks.swan` for `#pragma requirement <ID> #end` and prints which diagram node(s) each REQ ID resolves to (or `NOT TRACED` if missing); after the cycle-by-cycle assertions it also writes `<project-dir>/results/<operator>_traceability.csv` (tid/req/nodes/inputs/expected/actual/status per test case) and a `matplotlib` diagram of the model colored green/red by per-requirement pass/fail (Activity 7G) — this repo's own stand-in for the requirement-coverage view Scade One Student Edition doesn't provide. Both the simple and advanced scripts accept `--project-dir` (Activity 7F) so a student can point them at a project generated/copied elsewhere instead of only the one shipped in this repo | `src/lab3/solution/test_limiter_advanced.py`, `test_counter_advanced.py`; `docs/lab3/lab.md` Activity 7G |
| `evaluate_cc_full_report.py` scenario checkpoints (Lab 4) | cruise-control scenarios | REQ-01/02/04 | **NAMING-BASED** | `req` column in each `scenarios/*.csv`, written to `results/summary.csv`; no "verifies" statement, but file-backed |
| Activity 7A model-element links (Lab 4) | top node, 4 transitions, `regulator`, `limiter` instances | REQ-01/02/04/07/08 | **EXPLICIT instruction, PARTIALLY REALIZED** (1 of 7 present, and that 1 has a casing mismatch) | `lab.md` Activity 7A vs. `CC_design.swan:2` |
| Scenario "S-03" (Lab 4 reflection quiz) | reactivation requires explicit `res` | REQ-04 (by analogy) | **INFERRED** — quiz answer describes behavior, never states the REQ ID | reflection quiz text only |
| Lab 6 Activity 3B (proposed REQ-09/REQ-10) | Emergency Braking Controller | REQ-09/REQ-10 (new, proposed) | **PROPOSED, PAPER-ONLY — not implemented, not traced, not checked** | `docs/lab6/lab.md` Part 3 text only; no `.swan`, `requirements.md`, or `scenarios/*.csv` entry |

## Completion criteria per lab

- **Lab 2:** "Click ▶ Run. All 7 tests must print `PASS`." + runtime banner
  `"VALIDATION: ALL REQUIREMENTS MET."` vs. `"...ISSUES FOUND..."`.
- **Lab 3:** no single automated "done" banner — completion is a composite
  of: (a) wrote all REQ IDs and the Activity 9A test-case sketch
  (instructor-graded against `src/lab3/solution/requirements.md`); (b) built
  and simulated the Limiter/Counter per the per-activity expected values;
  (c) `limiter_harness`/`counter_harness` run correctly; (d)
  `test_limiter.py`/`test_counter.py` print `ALL PASS`; (e) both quiz scores
  (`#ears-pattern-quiz`, `#reflection-quiz`).
- **Lab 4:** completion is activity-based through Part 5 ("A successful
  build shows 0 errors...", "Confirm throttle equals accel (0.5)"); Part 6
  ends with `evaluate_cc_full_report.py`'s own "VALIDATION: ALL REQUIREMENTS MET." /
  "...ISSUES FOUND" banner over the checkpoint scenarios; Part 7 adds the
  Requirements-panel linking activity (no automated check) and a reflection
  quiz.
- **Lab 6:** no single automated "done" banner — completion is a composite
  of: (a) Parts 1–3's written/diagram deliverable (instructor-graded, no
  fixed answer key beyond matching the real Lab 4 model); (b) the
  `#architecture-quiz` score. Nothing in this lab is machine-checked against
  the student's own written content, same completion model as Lab 3's
  requirements text and Lab 5's whole lesson.

## Safety-standard mentions — never a compliance claim

Grepped the whole repo for DO-178C, DO-331, ISO 26262, IEC 61508, EN 50128,
"certified"/"certification"/"compliance". Every hit (in `docs/lab2/lab.md`,
`docs/lab4/lab.md`, and the deprecated `docs/lab4/lab_old.md` /
`old/lab2_old/`) is either (a) a closing remark about what *industrial tools*
do ("this is what makes a system auditable and certifiable — this is exactly
what tools like Scade One automate"), or (b) an explicit reflection-quiz
question asking the student what "certified code generator" means under
DO-178C/ISO 26262. **Zero instances claim this repo, its models, or its tests
are themselves certified or compliant with any standard.** Do not introduce
such a claim.

## Gaps (infrastructure that does not exist — do not invent it)

- No requirements-management tool; REQ IDs are plain markdown/code text.
- No persisted traceability-matrix file — Lab 2's matrix and Lab 3's
  traceability-preview table (Part 9) are markdown tables (the latter filled
  into `src/lab3/starter/requirements_template.md` by the student), not
  machine-readable repo artifacts.
- No code-coverage tool anywhere.
- No CI pipeline (no `.github/workflows/`).
- Lab 4 ships no `.swant` test-harness file at all (an earlier, empty
  `Main_test.swant` scaffold was removed) — Part 5 only briefly mentions
  Scade One test harnesses before redirecting to the Python evaluation
  script in Part 6.
- `src/lab3/starter/blocks.swan` carries no `#pragma requirement` pragmas —
  Activities 2G/4F ask students to add their own via the live Requirements
  panel, and the starter is deliberately shipped pre-linking so
  `test_limiter.py`/`test_counter.py`'s traceability report prints
  `NOT TRACED` until the student does that. `src/lab3/solution/assets/blocks.swan`
  **does** carry the completed links (`REQ-LIM-01`/`02`/`03` on the
  max-clamp/min-clamp/pass-through nodes, `REQ-CNT-01`/`02` on the `pre`
  node's initial branch and the `+` accumulation node) as the instructor
  reference — this is the one exception to "nothing is pre-populated,"
  since it's the answer key, not student-facing starter material. There is
  still no mechanism to commit a *student's own* local Scade One project
  state back to this repo.
- Lab 3 has no mechanism to check that a student's free-text EARS wording,
  Scade One model, or Requirements-panel links actually match the intended
  answer — grading is entirely manual, against `src/lab3/solution/requirements.md`
  and the working Scade One project under `src/lab3/solution/` (note:
  `src/lab3/starter/` has the same project files but a flattened layout that
  doesn't open in Scade One — see `.agents/scade-models.md`).
