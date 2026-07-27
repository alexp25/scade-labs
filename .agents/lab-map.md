# Lab map

Published portfolio: https://alexp25.github.io/scade-labs/ (`docs/index.html`
has 4 cards: Lab 1 "Coming soon" [no content exists], Lab 2, Lab 3.1, Lab 3.2).

## Active labs

| | Lab 2 | Lab 3.1 | Lab 3.2 |
|---|---|---|---|
| Title | Applying the SDLC: Cruise Control Safety System | Introduction to Scade One: Modeling Combinatorial and Sequential Logic | Implementing a Cruise Control System with Scade One |
| Directory | `docs/lab2/` + `src/lab2/` | `docs/lab3_1/` + `src/lab3_1/` | `docs/lab3_2/` + `src/lab3_2/` |
| Objective | Apply full SDLC (requirements→design→impl→V&V) to a cruise-control state machine, in pure Python | Learn Scade One modeling basics: typed operator interfaces, combinatorial logic (limiter), sequential logic (counter, `pre`), test harnesses | Model the full cruise-control system (state machine + PI regulator + car plant) in Scade One and cross-check against Lab 2 |
| Main tech | Python 3 (stdlib only), Skulpt (in-browser Python) | Scade One Student Edition, Swan, Python 3.12 + `ansys-scadeone-core==0.8.2` | Same as 3.1, `ansys-scadeone-core` (unpinned) |
| Student entry point | `docs/lab2/index.html` (live CodeMirror+Skulpt editor) | `docs/lab3_1/index.html` (instructions only — modeling happens in the Scade One desktop app) | `docs/lab3_2/index.html` (same pattern) |
| Starter materials | `src/lab2/starter/lab2_cruise_control_starter.py` | **none** — GUI-driven, no code stub | **none** |
| Solution/reference | `src/lab2/solution/lab2_cruise_control_solution.py` (instructor-only) | `src/lab3_1/solution/` (`assets/blocks.swan`, `assets/test.swant`, `demo.sproj`, `counter_wrapper/`, `limiter_wrapper/`, `test_counter.py`, `test_limiter.py`, `setup_wrapper.py`, `requirements.txt`) | `src/lab3_2/solution/CruiseControl/` (`assets/{CC_design,Car_design,Simulation}.swan`, `assets/Main_test.swant` [empty scaffold], `cc_wrapper/`, `tester.py`, `generate_python_wrapper.bat`, `readme.txt`, `requirements.txt`) |
| Model files | none (pure Python) | `blocks.swan`: `function limiter(...)`, `node counter(...)` + `const init` | `CC_design.swan`: `node cruise_control` (nested automaton) + `node regulator` + `node limiter`; `Car_design.swan`: vehicle plant; `Simulation.swan`: closed-loop + open-loop wiring |
| Test/validation mechanism | Embedded `run_tests()`, 7 hardcoded cases (TC-01…TC-07), PASS/FAIL printed in-browser or via `python lab2_cruise_control_starter.py` | Manual simulation (lab.md states expected values per activity) + `test_counter.py`/`test_limiter.py` (manual PASS/FAIL, no CI) + populated `test.swant` harness | Manual simulation + `evaluate_cc.py`, driven by scenario CSV files under `scenarios/` (writes per-scenario trace CSVs, a `results/summary.csv` PASS/FAIL report, and `results/plots/*.png` charts) — replaces the prior file-less `test_cc_main.py` snippet as of this session. `tester.py` (live console printout, no assertions) still exists alongside it. `Main_test.swant` is present but empty and no longer part of the lesson flow (Part 5 only briefly mentions Scade One test harnesses now) |
| Published route | `/lab2/` | `/lab3_1/` | `/lab3_2/` |
| Status | Active, complete | Active, complete | Active, complete but: 4 orphaned images in `img/`, orphaned `lab_old.md`, unpinned dependency version, only 1 of 4 traceability links from Activity 7A actually present in the shipped `.swan` (`#pragma requirement reQ2` on the top node only). Part 6 rewritten this session (harness → Python scenario/CSV/chart workflow), with a matching reference `evaluate_cc.py` + `scenarios/*.csv` now added under `src/lab3_2/solution/` |

## Legacy / superseded (not linked from any published page)

| Path | Tracked? | What it is |
|---|---|---|
| `old/lab2_old/` | Yes | Earlier version of the Lab 2 Python exercise (superseded by `src/lab2/`) |
| `old/scade_demo/` | Yes | Earlier Scade demo/project2 models, predates `src/lab3_1`/`src/lab3_2` |
| `scade_demo/` (repo root) | **No** — untracked | Local Scade One codegen job output (`CruiseControl/jobs/codegen_*/...`, a `.zip`) — WIP/scratch, not curriculum content |
