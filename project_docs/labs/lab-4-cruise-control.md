# Lab 4 — Implementing a Cruise Control System with Scade One

**Published:** `https://alexp25.github.io/scade-labs/lab4/` (`docs/lab4/index.html` + `docs/lab4/lab.md`)
**Source:** `src/lab4/starter/CruiseControl/`

## Purpose

Model the same cruise-control system from Lab 2 — this time as a Scade One
graphical state machine plus a PI regulator and a vehicle plant model — and
cross-check its behavior against Lab 2's Python reference. Also introduces
Scade One's requirement-traceability mechanism (`#pragma requirement`).

## Prerequisites (quoted, `docs/lab4/lab.md`)

1. Install Scade One Student Edition — **no registration/license activation
   required** (corrected this session, same fix as Lab 3).
2. **Complete Lab 3 first** (hard prerequisite — corrected this session:
   the lab's own prose previously called this "Lab 3" and linked to a
   non-existent `../lab3/` path in 7 places; now consistently says "Lab 3"
   and links `../lab3/`).

## Learning outcomes (quoted)

- Create a Scade One project with a correctly typed operator interface
- Model the cruise control decision table as a graphical state machine
- Run the built-in Scade One simulator to verify behaviour
- Write a Python evaluation script, driven by scenario files, that calls the
  generated C code to reproduce the test cases from Lab 2 and reports
  results as CSV files and charts
- Explain how model-based design replaces the manual traceability
  maintained in Lab 2

## Repository files

| File | Role |
|---|---|
| `docs/lab4/lab.md` | Published lesson (Parts 1–7: orientation, car simulation, project setup, state machine, simulation/verification, Python evaluation script, traceability & reflection). Part 6 previously rewritten to replace Scade One test-harness building with a scenario-file-driven Python script (CSV output, traceability report, charts); this session added a "Full script reference" subsection at the end of Part 6 — both `evaluate_cc_full_report.py` and `evaluate_cc_quick_tester.py` (the latter not previously referenced anywhere in the published lesson, only in `.agents/`) are now shown in full inside collapsed `<details>` blocks, styled in `docs/lab4/index.html`. No live/runnable editor was added — the scripts import the generated `cc_wrapper` compiled DLL, which a browser-side Python interpreter (Skulpt, used by Lab 2) cannot load, so this is read-only reference text, not execution |
| `docs/lab4/lab_old.md` | **Orphaned** — an earlier draft, not fetched by `index.html`, do not edit expecting effect |
| `docs/lab4/img/` | 15 screenshots — 4 unreferenced anywhere, 2 more referenced only inside HTML comments (never rendered) |
| `src/lab4/starter/CruiseControl/CruiseControl.sproj` | Project manifest (plain JSON) |
| `src/lab4/starter/CruiseControl/assets/CC_design.swan` | `node cruise_control` (nested automaton) + `node regulator` + `node limiter` |
| `src/lab4/starter/CruiseControl/assets/Car_design.swan` | Vehicle plant model |
| `src/lab4/starter/CruiseControl/assets/Simulation.swan` | Closed-loop (`main`) and open-loop (`main_manual`) wiring |
| `src/lab4/starter/CruiseControl/{generate_python_wrapper.bat, readme.txt, requirements.txt}` | Wrapper-generation driver docs (requires local Scade One). `requirements.txt` now also lists `matplotlib` (added this session for the chart step) |
| `src/lab4/starter/CruiseControl/evaluate_cc_quick_tester.py` | Live console demo (no assertions), kept alongside the main evaluation script. This session: fixed a stale in-file comment still naming the pre-rename `evaluate_cc.py`, and added it to the published lesson's new "Full script reference" section (previously it existed in the tree and in `.agents/`, but `lab.md` never showed or mentioned it) |
| `src/lab4/starter/CruiseControl/evaluate_cc_full_report.py` | **New this session** — instructor reference implementing lab.md's Part 6 Activities 6C–6F: reads `scenarios/*.csv`, drives the wrapper cycle-by-cycle, writes `results/<tid>_trace.csv` + `results/summary.csv` + `results/plots/<tid>.png` |
| `src/lab4/starter/CruiseControl/scenarios/*.csv` | **New this session** — 6 example scenario files (`tc01`…`tc06`) covering REQ-01/02/04, mirroring Lab 2's test cases as short multi-cycle sequences |
| `src/lab4/starter/CruiseControl/cc_wrapper/` | **Generated** ctypes wrapper + compiled `.dll` — do not hand-edit |

`src/lab4/starter/CruiseControl/` is a populated, working reference project
(not a fill-in-the-blank stub) — this lab is GUI-modeling in the Scade One
desktop app, same shape as Lab 3's Scade One content.

## Student workflow

1. Orient in the Scade One environment (skip if Lab 3 was just completed).
2. Inspect/simulate the provided `Car_design.swan` plant model manually.
3. Create the `CruiseControl` project, declare the `cruise_control` operator
   interface.
4. Build the nested state machine (`cc_disabled`/`cc_enabled` outer,
   `cc_active`/`cc_standby` inner) with the documented guard conditions.
5. Implement `regulator` (PI controller + limiter clamps) and wire
   `set_point` handling.
6. Simulate manually and trace the state hierarchy by hand.
7. Generate a Python wrapper; define test scenarios as CSV files under
   `scenarios/`; run `evaluate_cc_full_report.py` to produce per-scenario trace CSVs, a
   `results/summary.csv` traceability report, and `results/plots/*.png`
   charts; compare the summary to Lab 2's verification report.
8. **Activity 7A — Traceability in Scade One**: use the Requirements panel
   (same mechanism practiced in Lab 3 Activities 2G/4F) to link the
   `cruise_control` node, each of its 4 transitions, the `regulator` node,
   and its internal `limiter` instances to their REQ IDs via `#pragma
   requirement` — 7 element-level links total. The activity also has
   students check the real shipped `CC_design.swan` excerpt (`reQ2` vs
   `REQ-02`) against Lab 3 Part 9's explanation, as a check-your-work step
   against a real casing gap, not a template to copy uncritically.
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
REQ-01/02/04 (reused from Lab 2's numbering, not redefined). As of
[Lab 3](lab-3-requirements.md), those same IDs — rewritten in EARS syntax —
plus two new ones (REQ-07 regulator behavior, REQ-08 throttle clamp, both
specific to this Scade One model) are authored ahead of this lab in
`docs/lab3/lab.md` / `src/lab3/solution/requirements.md`. This lab's own
Activity 7A table (extended this session) now also names REQ-07/08
explicitly, mapped to the `regulator` node and its internal `limiter`
instances respectively — the state-transition table itself still only
carries REQ-01/02/04, since REQ-07/08 aren't transition-level.

## Test/simulation procedure and expected results

- **Manual simulation** (documented in `lab.md`; not independently re-run —
  requires Scade One): build shows 0 errors; `throttle` output equals
  `accel` (`0.5`) in the disabled/manual state.
- **Python wrapper test** (requires local Scade One + unpinned
  `ansys-scadeone-core` + regenerated `cc_wrapper` — **not runnable in this
  documentation-pass environment**): `evaluate_cc_quick_tester.py` and the new `evaluate_cc_full_report.py`
  were syntax-checked (`python -m py_compile`, passed) but not executed.
  `evaluate_cc_quick_tester.py` is a live printout with no pass/fail signal. `evaluate_cc_full_report.py`
  illustrates the same hypothetical wrapper API as before (`cc.on`,
  `cc.brake`, `cc.cycle()`, `cc.throttle`), which still differs from the real
  generated `cc_wrapper.py` — see
  `project_docs/architecture/python-and-simulation.md`.
- **Harness**: no `.swant` test-harness file ships for this model at all
  (the earlier empty `Main_test.swant` scaffold has since been removed from
  the tree). lab.md's Part 5 only briefly mentions test harnesses as an
  in-tool alternative, redirecting to the Python evaluation script in Part 6.

## Traceability

Mixed — see `project_docs/verification/requirements-and-traceability.md` for
the full breakdown. Summary: Activity 7A instructs students to create 7
element-level `#pragma requirement` links via Scade One's Requirements
panel (top node, 4 transitions, `regulator`, `limiter` instances); the
shipped reference model only demonstrates **one** such pragma (on the whole
`cruise_control` node, tagged `reQ2`) — not the other six, and that one's
casing (`reQ2`) doesn't match the canonical `REQ-02` spelling. This is a
real, pre-existing gap between instruction and shipped reference. As of this
session, it is **not** silently left for a curious student to discover —
both Lab 3 Part 9 and this lab's Activity 7A now name it explicitly as a
worked lesson in traceability discipline. Still not "completed" by guessing
what the other six links should say, since that requires a
maintainer/instructor decision (and a Scade One install to actually add
them).

## Known limitations

- `ansys-scadeone-core` unpinned in `requirements.txt` (Lab 3 pins
  `==0.8.2`) — version-drift risk against the shipped `cc_wrapper.*`.
- No `.swant` test-harness file ships for this model (removed from the tree;
  not part of the lesson flow).
- `evaluate_cc_full_report.py`'s wrapper API is illustrative, not verified against the
  real generated `cc_wrapper.py` (same pre-existing gap as the snippet it
  replaces — see `project_docs/architecture/python-and-simulation.md`).
- 4 orphaned + 2 comment-only images in `docs/lab4/img/`.
- Orphaned `docs/lab4/lab_old.md`.
- Activity 7A traceability only ~14% (1/7) demonstrated in the shipped
  model, and that one link has a casing mismatch — both facts are now
  explicitly taught rather than silently left as an inconsistency.

## Publishing route

`/lab4/` — see `project_docs/architecture/site-and-publishing.md`.
