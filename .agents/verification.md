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

## Lab 3.1 — no requirements exist

Grepped for requirement/trace/REQ/V&V language — no REQ-xx IDs and no
requirements framing anywhere. Test harnesses and Python tests check
hardcoded expected values ("Expected output: `value_out = 100.0`") with no
requirement statement behind them. This lab teaches tool mechanics, not
requirements engineering — do not invent a traceability angle for it.

## Lab 3.2 — mixed: one explicit mechanism, partially realized

- "The System (recap from Lab 2)" section restates the **state names and
  interface**, not the REQ-xx text.
- A 4-row state-transition table (`cc_disabled`/`cc_enabled`/`cc_active`/
  `cc_standby`) tags each transition with a REQ ID (REQ-01/02/04) — smaller
  than Lab 2's 6-row decision table but same shape.
- "Activity 7A — Traceability in Scade One" describes a **real tool
  feature**: Scade One's Requirements panel, used to link model elements to
  REQ IDs via `#pragma requirement`. Corroborated by
  `src/lab3_2/solution/CruiseControl/assets/CC_design.swan` containing
  exactly one such pragma (`#pragma requirement reQ2` on the `cruise_control`
  node) — **not** the four transition-level links the activity instructs
  students to create. **The shipped reference solution only partially
  demonstrates the mechanism it teaches.**
- "Activity 7B" is a pure reflection quiz (DO-178C/ISO 26262 discussion
  questions) — comprehension, not a trace artifact.
- The Python test script's REQ tags (in lab.md's instructional
  `test_cc_main.py` snippet) are **naming-based**: a label field in the test
  tuple, with no "this verifies REQ-X" sentence and no link to the in-tool
  Requirements panel.

## Test → requirement classification table

| Test | Exercises | REQ | Class | Evidence |
|---|---|---|---|---|
| TC-01..TC-07 (Lab 2) | full cruise-control state machine | REQ-01..04 | **EXPLICIT** | lab.md prose + `req`/`tid` fields in test tuples |
| limiter/counter tests (Lab 3.1) | clamp / increment behavior | none | **N/A** | no REQ IDs exist in Lab 3.1 |
| `test_cc_main.py` cases (Lab 3.2, instructional only) | cruise-control scenarios | REQ-01/02/04 | **NAMING-BASED** | label field only, no "verifies" statement, not file-backed |
| Activity 7A model-element links (Lab 3.2) | 4 transitions | REQ-01/02/04 | **EXPLICIT instruction, PARTIALLY REALIZED** (1 of 4 present) | `lab.md` Activity 7A vs. `CC_design.swan:2` |
| Scenario "S-03" (Lab 3.2 reflection quiz) | reactivation requires explicit `res` | REQ-04 (by analogy) | **INFERRED** — quiz answer describes behavior, never states the REQ ID | reflection quiz text only |

## Completion criteria per lab

- **Lab 2:** "Click ▶ Run. All 7 tests must print `PASS`." + runtime banner
  `"VALIDATION: ALL REQUIREMENTS MET."` vs. `"...ISSUES FOUND..."`.
- **Lab 3.1:** no single "done" banner; per-activity expected values (e.g.
  simulation tables) plus the generated test scripts' own
  `"ALL PASS"`/`"SOME TESTS FAILED"` print.
- **Lab 3.2:** no aggregate banner; completion is activity-based ("A
  successful build shows 0 errors...", "Confirm throttle equals accel
  (0.5)") and ends with a manual compare-and-discuss step, not a pass count.

## Safety-standard mentions — never a compliance claim

Grepped the whole repo for DO-178C, DO-331, ISO 26262, IEC 61508, EN 50128,
"certified"/"certification"/"compliance". Every hit (in `docs/lab2/lab.md`,
`docs/lab3_2/lab.md`, and the deprecated `docs/lab3_2/lab_old.md` /
`old/lab2_old/`) is either (a) a closing remark about what *industrial tools*
do ("this is what makes a system auditable and certifiable — this is exactly
what tools like Scade One automate"), or (b) an explicit reflection-quiz
question asking the student what "certified code generator" means under
DO-178C/ISO 26262. **Zero instances claim this repo, its models, or its tests
are themselves certified or compliant with any standard.** Do not introduce
such a claim.

## Gaps (infrastructure that does not exist — do not invent it)

- No requirements-management tool; REQ IDs are plain markdown/code text.
- No persisted traceability-matrix file — Lab 2's matrix is a markdown table
  + a dict the student fills into the editor, not a repo artifact.
- No code-coverage tool anywhere.
- No CI pipeline (no `.github/workflows/`).
- Lab 3.2's `Main_test.swant` harness scaffold is empty — described
  test-harness activities exist in lab.md but no committed `.swant` test
  vectors back them.
- Lab 3.1's Python tests are plain scripts (manual PASS/FAIL string
  comparison), not an assertion framework, and carry no requirement
  linkage (Lab 3.1 has no REQ IDs to link to).
