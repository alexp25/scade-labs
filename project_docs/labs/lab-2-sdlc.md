# Lab 2 — Applying the SDLC: Cruise Control Safety System

**Published:** `https://alexp25.github.io/scade-labs/lab2/` (`docs/lab2/index.html` + `docs/lab2/lab.md`)
**Source:** `src/lab2/{starter,solution}/`

## Purpose

Apply the full software development lifecycle (requirements → design →
implementation → verification & validation) to a small safety-critical
cruise-control state machine, entirely in Python, so students experience by
hand what tools like Scade One automate (per `docs/lab2/lab.md`'s own closing
remark).

## Prerequisites

None stated in `lab.md` (no `## Prerequisites` heading exists in this lab —
unlike Lab 3.1/3.2). The lab opens directly with Objectives → The Problem →
Structure.

## Learning outcomes (quoted, `docs/lab2/lab.md`)

- Apply all SDLC phases on a concrete safety-critical problem
- Explain why requirements must be precise and unambiguous
- Build a decision table as a design artifact and trace it back to requirements
- Implement a function whose logic is fully driven by a design — not intuition
- Run a structured V&V test suite and interpret the results
- Explain how traceability connects requirements, design, code, and tests
- Reflect on Waterfall, Agile, and V-Cycle in a safety-critical context

## Repository files

| File | Role |
|---|---|
| `docs/lab2/lab.md` | Published lesson content (requirements, decision table, instructions, traceability matrix) |
| `docs/lab2/index.html` | Page shell: fetches `lab.md`, embeds a CodeMirror+Skulpt live Python editor |
| `src/lab2/starter/lab2_cruise_control_starter.py` | Student starter (stub function + test harness) — identical to the browser's embedded `STARTER_CODE` |
| `src/lab2/solution/lab2_cruise_control_solution.py` | Instructor-only reference implementation |
| `src/lab2/README.md` | Short pointer back to the published page + local-run instructions |

No `docs/lab2/img/` directory exists — this lab uses the live editor instead
of screenshots.

## The problem (informal client description, quoted)

> "Cruise control must be safe. It should stop when needed, should not start
> in dangerous conditions, and if it stops for a safety reason the driver
> must be aware that they need to restart it manually."

## Requirements (quoted from `docs/lab2/lab.md`)

- **REQ-01** (functional): deactivate cruise control if the brake is pressed.
- **REQ-02** (functional): deactivate if speed exceeds 130 km/h.
- **REQ-03** (functional): refuse to activate if speed is below 30 km/h.
- **REQ-04** (functional): enter `SUSPENDED` (not `OFF`) when deactivated by a
  safety condition — requires an explicit reactivation, not just re-pressing
  "activate."
- **REQ-05** (non-functional): respond to any input in under 100 ms.
- **REQ-06** (non-functional): testable with simulated boolean inputs.

A markdown decision table maps `(current_state, brake_pressed, speed>130,
driver_activates, driver_reactivates)` → new state, tagged with the REQ(s)
each row implements.

## Student workflow

1. Read requirements + decision table in the rendered `lab.md`.
2. Implement `update_cruise_control(current_state, speed, brake_pressed,
   driver_activates, driver_reactivates)` — either in the browser's live
   editor (`docs/lab2/`) or locally in
   `src/lab2/starter/lab2_cruise_control_starter.py`.
3. Run — 7 test cases (TC-01…TC-07) must all print PASS.

## Instructor/reference assets

`src/lab2/solution/lab2_cruise_control_solution.py` — never linked from
`docs/` (verified this session via grep — no page under `docs/` references
`src/` or `solution`).

## Python architecture

See `project_docs/architecture/python-and-simulation.md` for the full
starter/solution/browser comparison. Summary: stdlib-only, no dependencies,
runs identically locally (Python 3.x) and in-browser (Skulpt).

## Test procedure and expected results (verified this session)

```
$ python src/lab2/solution/lab2_cruise_control_solution.py
```
→ all 7 tests print PASS; final banner `VALIDATION: ALL REQUIREMENTS MET.`
(actually executed this session with Python 3.11.3 — no dependencies
required).

```
$ python src/lab2/starter/lab2_cruise_control_starter.py
```
→ 3/7 PASS (TC-03, TC-05, TC-07), 4/7 FAIL, banner
`VALIDATION: ISSUES FOUND -- review your implementation.` (expected, since
the stub is unimplemented — confirms the harness discriminates correctly).

## Traceability

**Explicit**, both in prose and as data. `lab.md` states outright: "The REQ
column here is the Test → Requirements direction: 'This test case verifies
that REQ-X is met.'" Each test tuple in the code also carries a literal
`req` field printed at runtime (e.g. `TC-05 [REQ-04]`). A consolidated
REQ×TC traceability-matrix table appears later in `lab.md`. See
`project_docs/verification/requirements-and-traceability.md` for the full
table and how this compares to Lab 3.2's partial in-tool traceability.

## Known limitations

- No dedicated Prerequisites section (structural asymmetry vs. Lab 3.1/3.2 —
  documented, not "fixed," since this may be intentional given Lab 2 needs
  no special setup).
- Lab 2's in-browser path depends on 3 CDNs (skulpt.org + 2×cdnjs) with no
  offline fallback.

## Publishing route

`/lab2/` — see `project_docs/architecture/site-and-publishing.md`.
