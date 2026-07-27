# Requirements and traceability

## Lab 2 — explicit, dual-encoded

**Client description** (`docs/lab2/lab.md`): *"Cruise control must be safe.
It should stop when needed, should not start in dangerous conditions, and if
it stops for a safety reason the driver must be aware that they need to
restart it manually."*

**Requirements** (quoted): REQ-01 (deactivate on brake), REQ-02 (deactivate
above 130 km/h), REQ-03 (refuse activation below 30 km/h), REQ-04 (enter
`SUSPENDED`, requiring explicit reactivation), REQ-05 (response time <100ms,
non-functional), REQ-06 (testability, non-functional).

**Decision table**: markdown table, `(state, brake_pressed, speed>130,
driver_activates, driver_reactivates)` → new state, each row tagged with its
REQ(s).

**Test cases** (TC-01…TC-07): documented in `lab.md` itself (not only in
code), with an explicit direction statement: *"The REQ column here is the
Test → Requirements direction: 'This test case verifies that REQ-X is
met.'"* A consolidated REQ×TC traceability matrix table follows.

**Code-level encoding**: each test tuple in
`src/lab2/{starter,solution}/lab2_cruise_control_*.py` carries literal `tid`
and `req` fields (e.g. `"TC-05"`, `"REQ-04"`), printed at runtime.

**Classification: EXPLICIT.** Stated in prose and duplicated as data — not
an inference a reader has to construct.

## Lab 3.1 — no requirements exist

Grepped for requirement/trace/REQ/V&V/verification language across the
entire lab — zero REQ-xx identifiers, zero requirements framing. Test
harnesses and Python tests check hardcoded expected values only ("Expected
output: `value_out = 100.0`"). This lab teaches tool mechanics; there is
nothing to trace.

## Lab 3.2 — one real mechanism, partially realized

- Restates Lab 2's **state names and interface** (not its REQ-xx prose) in
  "The System (recap from Lab 2)."
- A 4-row transition table (`cc_disabled`/`cc_enabled`/`cc_active`/
  `cc_standby`) reuses REQ-01/02/04 from Lab 2 against specific guard
  conditions.
- **Activity 7A — Traceability in Scade One** describes a real tool feature:
  Scade One's Requirements panel, linking model elements to REQ IDs via
  `#pragma requirement`. Quoted: *"In Lab 2 you maintained a traceability
  matrix as a Python comment. In Scade One, open the Requirements panel and
  link the following model elements to their REQ IDs... This is what Lab 9
  of the original SCADE Suite training covered."*
- **Verified against the shipped solution**:
  `src/lab3_2/solution/CruiseControl/assets/CC_design.swan` contains exactly
  **one** `#pragma requirement` (`reQ2`, on the whole `cruise_control` node)
  — not the four transition-level links Activity 7A instructs students to
  create. The reference solution demonstrates the mechanism but does not
  fully exercise it.
- Activity 7B is a pure reflection quiz (DO-178C/ISO 26262 discussion
  questions) — comprehension, not a trace artifact.

## Test → requirement classification table

| Test | Exercises | REQ | Classification | Evidence |
|---|---|---|---|---|
| TC-01…TC-07 (Lab 2) | full cruise-control state machine | REQ-01…04 | **EXPLICIT** | lab.md prose + `req`/`tid` fields in code |
| limiter/counter tests (Lab 3.1) | clamp / increment behavior | — | **N/A** | no REQ IDs exist in Lab 3.1 |
| `evaluate_cc.py` scenario checkpoints (Lab 3.2) | cruise-control scenarios, one CSV file per scenario under `scenarios/` | REQ-01/02/04 | **NAMING-BASED, FILE-BACKED** | `req` column in each scenario CSV, written to `results/summary.csv`; no "verifies" sentence, but (unlike the prior `test_cc_main.py` instructional snippet) both `docs/lab3_2/lab.md` and `src/lab3_2/solution/CruiseControl/{scenarios/,evaluate_cc.py}` now exist as real files |
| Activity 7A model-element links (Lab 3.2) | 4 transitions | REQ-01/02/04 | **EXPLICIT instruction, 25% REALIZED** (1 of 4 present) | lab.md Activity 7A vs. `CC_design.swan` pragma |
| Reflection-quiz "Scenario S-03" (Lab 3.2) | reactivation requires explicit `res` | REQ-04 (by analogy) | **INFERRED** | quiz answer describes behavior, never states the REQ ID |

## Completion criteria per lab

- **Lab 2**: "All 7 tests must print PASS" + runtime banner
  `VALIDATION: ALL REQUIREMENTS MET.` — **verified this session** (see
  `project_docs/verification/testing-and-simulation.md`).
- **Lab 3.1**: no aggregate banner; per-activity expected values plus the
  generated test scripts' own `"ALL PASS"`/`"SOME TESTS FAILED"` print.
- **Lab 3.2**: activity-based through Part 5 ("0 errors" build, "`throttle`
  equals `accel` (0.5)"); Part 6 now ends with `evaluate_cc.py`'s own
  `"VALIDATION: ALL REQUIREMENTS MET."` / `"...ISSUES FOUND"` banner over the
  checkpoint scenarios (mirroring Lab 2's banner), followed by a manual
  compare-and-discuss step against Lab 2's report.

## Safety-standard mentions — never a compliance claim

Grepped the whole repo for DO-178C, DO-331, ISO 26262, IEC 61508, EN 50128,
"certified"/"certification"/"compliance." Zero hits for DO-331, IEC 61508, or
EN 50128. Every DO-178C/ISO 26262/"certified" hit found (in `docs/lab2/lab.md`,
`docs/lab3_2/lab.md`, and the deprecated `docs/lab3_2/lab_old.md` /
`old/lab2_old/`) is either:
(a) a closing remark about what commercial tools do at industrial scale, or
(b) an explicit reflection-quiz question asking the student to explain a
    concept.
**No instance claims this repository, its models, or its tests are
themselves certified or compliant with any standard.** Any future
documentation or lab content must preserve this — do not add a compliance
claim without explicit new evidence.

## Gaps (infrastructure that does not exist)

- No requirements-management tool — REQ IDs are plain markdown/code text.
- No persisted traceability-matrix file (Lab 2's matrix is a markdown table
  + a dict the student fills into the editor, not a repo artifact).
- No code-coverage tool anywhere in the repo.
- No CI pipeline (no `.github/workflows/`).
- Lab 3.2's `Main_test.swant` harness scaffold is empty.
- Lab 3.1's tests are plain scripts (manual string comparison), not an
  assertion framework, and carry no requirement linkage (none exist to link
  to).
