# Workflows

Only workflows actually supported by files in this repo. Where the repo only
partially documents a step, that's stated explicitly.

## Learner: portfolio → lab

1. Open `https://alexp25.github.io/scade-labs/` → `docs/index.html`.
2. Click a lab card (`Lab 2`, `Lab 3.1`, or `Lab 3.2` — `Lab 1` is a disabled
   "Coming soon" card, no content exists).
3. The lab's `index.html` fetches and renders its sibling `lab.md`.

## Learner: Lab 2 in-browser

1. Open `docs/lab2/index.html`.
2. Read the rendered `lab.md` (requirements → decision table → stub code).
3. Edit `update_cruise_control(...)` in the embedded CodeMirror editor
   (pre-filled from the `STARTER_CODE` literal, identical to
   `src/lab2/starter/lab2_cruise_control_starter.py`).
4. Click ▶ Run — Skulpt executes the code in-browser and prints the 7-test
   PASS/FAIL report + validation banner.

## Learner: Lab 2 locally

1. Download/open `src/lab2/starter/lab2_cruise_control_starter.py`.
2. Implement the stub.
3. `python lab2_cruise_control_starter.py` — same 7 test cases, printed to
   the console instead of the browser.

## Learner: Lab 3.1 / 3.2 — Scade One modeling

1. Install Scade One Student Edition (no registration/license step required
   — corrected in this session, see `.agents/publishing.md` history).
2. Follow `lab.md`'s Parts/Activities inside the Scade One desktop app to
   build the operator(s) (`limiter`/`counter` for 3.1; `cruise_control`/
   `regulator`/`car` for 3.2).
3. Run the built-in simulator and compare against the expected values stated
   per activity in `lab.md`.
4. Lab 3.1: build a test harness (`.swant`) for automated in-tool checking —
   `test.swant` ships populated. Lab 3.2: `lab.md` Part 5 only briefly
   mentions Scade One test harnesses (`Main_test.swant` remains an empty,
   unused scaffold); automated evaluation is instead a Python script (Part
   6) — see the next workflow.

## Learner: Lab 3.2 — Python evaluation script (Part 6)

1. Generate the code-generation job + Python wrapper (Activities 6A/6B —
   requires local Scade One, same prerequisite as the modeling workflow).
2. Define each test scenario as a CSV file under `scenarios/` (one row per
   simulation cycle; `set_point` is a real model input authored by hand per
   Activity 4E's "rising edge of `on` locks `set_point = v_speed`" rule;
   optional `expected_throttle`/`req`/`note` columns mark checkpoint rows).
   Six examples ship in `src/lab3_2/starter/CruiseControl/scenarios/`
   (`tc01`…`tc06`), each 12-14 cycles with `v_speed` ramped gradually rather
   than jumped between two values.
3. Run `evaluate_cc.py` — it prints progress per scenario as it runs, drives
   the wrapper cycle-by-cycle per scenario, writes `results/<tid>_trace.csv`,
   checks checkpoint rows, and writes `results/summary.csv` (the
   traceability report, REQ-tagged, PASS/FAIL, same banner style as Lab 2)
   plus `results/plots/<tid>.png` — two stacked subplots: `throttle`/
   `v_speed`/`set_point`/`brake` on top, boolean inputs (`on`/`set`/`res`)
   plus a Python-re-derived `cc state` (not read from the model) on the
   bottom. It also prints a final list of every file it generated.
4. Compare `results/summary.csv` and the charts to Lab 2's verification
   report (Activity 6F).

## Maintainer: comparing student work against reference

1. `src/lab2/solution/lab2_cruise_control_solution.py` is the instructor-only
   reference for Lab 2 — never expose it under `docs/`.
2. `src/lab3_1/solution/` and `src/lab3_2/solution/CruiseControl/` are the
   reference Scade One projects/wrappers — same rule.

## Maintainer: generating a Python wrapper for a Scade One model

**Requires a local Scade One installation — cannot be run in this
environment (see `.agents/testing.md`).**
1. `pip install -r requirements.txt` (`ansys-scadeone-core`, pinned `==0.8.2`
   for Lab 3.1, unpinned for Lab 3.2 — document this inconsistency, don't
   silently pin it without maintainer confirmation).
2. Lab 3.1: `py -3 setup_wrapper.py` (regenerates `counter_wrapper/`,
   `limiter_wrapper/`). Lab 3.2: run `generate_python_wrapper.bat`
   (regenerates `cc_wrapper/`).
3. Run the corresponding test script: `test_counter.py`/`test_limiter.py`
   for Lab 3.1 (locally-runnable once wrappers exist); for Lab 3.2,
   `evaluate_cc.py` (scenario-CSV-driven, writes `results/summary.csv` +
   charts) or `tester.py` (still present, a live demo printout, not an
   assertion-based check).

## Maintainer: publishing a changed lab

1. Edit `docs/labN/lab.md` (the actual published content).
2. If Lab 2, also update `src/lab2/starter/lab2_cruise_control_starter.py`
   AND the `STARTER_CODE` literal in `docs/lab2/index.html` together — they
   must stay identical (see `.agents/architecture.md`).
3. `cd docs && bundle exec jekyll build` (or `serve`) to preview locally
   before pushing.
4. Push to `main` — GitHub Pages republishes from `/docs` (inferred deploy
   mechanism, see `.agents/publishing.md`).

## Maintainer: adding a new lab

Not separately documented anywhere in the repo — inferred from the existing
3 labs' shared shape. See `.agents/publishing.md` → "Adding a new lab".

## Incomplete/partially documented workflows

- **Updating requirements/traceability**: Lab 2's process (edit lab.md's
  REQ/decision-table/matrix, keep the `req`/`tid` fields in the Python test
  tuples in sync) is inferable from its structure but not written down as a
  maintainer procedure anywhere. Lab 3.2's Requirements-panel workflow
  (Activity 7A) is described for students but the reference solution itself
  only partially followed it (see `.agents/verification.md`) — there is no
  maintainer note reconciling that gap.
- **Running the cruise-control car simulation end-to-end**: `Simulation.swan`
  wires `Car_design` + `CC_design` together (`node main`), but there is no
  documented command/script that runs this closed-loop simulation
  automatically outside the Scade One simulator UI — `tester.py` only drives
  the standalone `cruise_control` wrapper, not the combined car+CC
  simulation.
