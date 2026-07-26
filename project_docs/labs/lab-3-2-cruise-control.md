# Lab 3.2 — Implementing a Cruise Control System with Scade One

**Published:** `https://alexp25.github.io/scade-labs/lab3_2/` (`docs/lab3_2/index.html` + `docs/lab3_2/lab.md`)
**Source:** `src/lab3_2/solution/CruiseControl/`

## Purpose

Model the same cruise-control system from Lab 2 — this time as a Scade One
graphical state machine plus a PI regulator and a vehicle plant model — and
cross-check its behavior against Lab 2's Python reference. Also introduces
Scade One's requirement-traceability mechanism (`#pragma requirement`).

## Prerequisites (quoted, `docs/lab3_2/lab.md`)

1. Install Scade One Student Edition — **no registration/license activation
   required** (corrected this session, same fix as Lab 3.1).
2. **Complete Lab 3.1 first** (hard prerequisite — corrected this session:
   the lab's own prose previously called this "Lab 3" and linked to a
   non-existent `../lab3/` path in 7 places; now consistently says "Lab 3.1"
   and links `../lab3_1/`).

## Learning outcomes (quoted)

- Create a Scade One project with a correctly typed operator interface
- Model the cruise control decision table as a graphical state machine
- Run the built-in Scade One simulator to verify behaviour
- Write a Python test script that calls the generated C code to reproduce
  the 7 test cases from Lab 2
- Explain how model-based design replaces the manual traceability
  maintained in Lab 2

## Repository files

| File | Role |
|---|---|
| `docs/lab3_2/lab.md` | Published lesson (Parts 1–7: orientation, car simulation, project setup, state machine, simulation/verification, Python test script, traceability & reflection) |
| `docs/lab3_2/lab_old.md` | **Orphaned** — an earlier draft, not fetched by `index.html`, do not edit expecting effect |
| `docs/lab3_2/img/` | 15 screenshots — 4 unreferenced anywhere, 2 more referenced only inside HTML comments (never rendered) |
| `src/lab3_2/solution/CruiseControl/CruiseControl.sproj` | Project manifest (plain JSON) |
| `src/lab3_2/solution/CruiseControl/assets/CC_design.swan` | `node cruise_control` (nested automaton) + `node regulator` + `node limiter` |
| `src/lab3_2/solution/CruiseControl/assets/Car_design.swan` | Vehicle plant model |
| `src/lab3_2/solution/CruiseControl/assets/Simulation.swan` | Closed-loop (`main`) and open-loop (`main_manual`) wiring |
| `src/lab3_2/solution/CruiseControl/assets/Main_test.swant` | **Empty** — version header only, no committed harness |
| `src/lab3_2/solution/CruiseControl/{generate_python_wrapper.bat, readme.txt, requirements.txt}` | Wrapper-generation driver docs (requires local Scade One) |
| `src/lab3_2/solution/CruiseControl/tester.py` | Live console demo (no assertions) |
| `src/lab3_2/solution/CruiseControl/cc_wrapper/` | **Generated** ctypes wrapper + compiled `.dll` — do not hand-edit |

No `src/lab3_2/starter/` — GUI-modeling, like Lab 3.1.

## Student workflow

1. Orient in the Scade One environment (skip if Lab 3.1 was just completed).
2. Inspect/simulate the provided `Car_design.swan` plant model manually.
3. Create the `CruiseControl` project, declare the `cruise_control` operator
   interface.
4. Build the nested state machine (`cc_disabled`/`cc_enabled` outer,
   `cc_active`/`cc_standby` inner) with the documented guard conditions.
5. Implement `regulator` (PI controller + limiter clamps) and wire
   `set_point` handling.
6. Simulate manually and trace the state hierarchy by hand.
7. Generate a Python wrapper and write/run a test script mirroring Lab 2's
   7 test cases; compare output to Lab 2's verification report.
8. **Activity 7A — Traceability in Scade One**: use the Requirements panel to
   link each state-machine transition to its REQ ID via `#pragma
   requirement`.
9. **Activity 7B**: reflection quiz (SDLC phases, "certified code generator"
   discussion — DO-178C/ISO 26262 mentioned only as discussion context, never
   as a compliance claim about this repo).

## Model architecture

See `project_docs/architecture/scade-projects.md`. Summary: `cruise_control`
(nested automaton, `#pragma requirement reQ2` on the top node only) +
`regulator` (PI + limiter clamps) + `limiter`, wired to the `Car_design`
plant via `Simulation.swan`'s `main`/`main_manual` nodes.

## Requirements

Restates Lab 2's state names/interface (not the REQ-xx text itself) in "The
System (recap from Lab 2)." Defines its own 4-row transition table
(`cc_disabled`/`cc_enabled`/`cc_active`/`cc_standby`) tagged with
REQ-01/02/04 (reused from Lab 2's numbering, not redefined).

## Test/simulation procedure and expected results

- **Manual simulation** (documented in `lab.md`; not independently re-run —
  requires Scade One): build shows 0 errors; `throttle` output equals
  `accel` (`0.5`) in the disabled/manual state.
- **Python wrapper test** (requires local Scade One + unpinned
  `ansys-scadeone-core` + regenerated `cc_wrapper` — **not runnable in this
  documentation-pass environment**): `tester.py` was syntax-checked
  (`python -m py_compile`, passed) but not executed; it is a live printout
  with no pass/fail signal, not an assertion-based test. The lab.md's own
  `test_cc_main.py` instructional snippet illustrates a hypothetical API that
  differs from the real generated `cc_wrapper.py` — see
  `project_docs/architecture/python-and-simulation.md`.
- **Harness**: `Main_test.swant` is an empty scaffold — no committed test
  vectors exist for this model, despite lab.md describing harness-building
  activities.

## Traceability

Mixed — see `project_docs/verification/requirements-and-traceability.md` for
the full breakdown. Summary: Activity 7A instructs students to create 4
transition-level `#pragma requirement` links via Scade One's Requirements
panel; the shipped reference solution only demonstrates **one** such pragma
(on the whole `cruise_control` node, tagged `reQ2`), not the four the
activity describes. This is a real, verified gap between instruction and
shipped reference — not a defect to silently "complete" by guessing what the
other three links should say, since that requires a maintainer/instructor
decision (and a Scade One install to actually add them).

## Known limitations

- `ansys-scadeone-core` unpinned in `requirements.txt` (Lab 3.1 pins
  `==0.8.2`) — version-drift risk against the shipped `cc_wrapper.*`.
- Empty `Main_test.swant` harness scaffold.
- 4 orphaned + 2 comment-only images in `docs/lab3_2/img/`.
- Orphaned `docs/lab3_2/lab_old.md`.
- Activity 7A traceability only 25% (1/4) demonstrated in the shipped model.

## Publishing route

`/lab3_2/` — see `project_docs/architecture/site-and-publishing.md`.
