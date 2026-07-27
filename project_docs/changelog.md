# Changelog

Progress-tracking log of substantive changes to the lab content and its
maintainer documentation. One entry per work session. Newest first.

---

## 2026-07-27 — Lab 3.2: fixed generation/wrapper scripts and evaluate_cc.py against the real PyScadeOne 0.8.2 API

### Summary for reporting

The Lab 3.2 Python tooling added in the previous session (`generate_python_wrapper.bat`,
`evaluate_cc.py`, and the `tc02` scenario file) had never actually been run against a
live Scade One install; doing so this session surfaced several real bugs, now fixed in
both `src/lab3_2/starter/CruiseControl/` and `src/lab3_2/solution/CruiseControl/`, and
mirrored into `docs/lab3_2/lab.md` Activity 6D:

1. **`generate_python_wrapper.bat`** hardcoded an absolute `.sproj` path from an old
   repo location. Now resolves the project path relative to the script itself
   (`%~dp0`), so it works regardless of checkout location.
2. **`PythonWrapper` job argument.** `PythonWrapper(prj, job)` requires the job *name
   string*, not the `Job` object returned by `prj.get_job(...)` — passing the object
   crashed deep inside the library (`AttributeError` on `Job.__eq__`). Fixed to pass
   the job name string directly (matches the convention already used in
   `src/lab3_1/*/setup_wrapper.py` and `docs/lab3_1/lab.md`).
3. **No `PythonWrapper.get_operator_instance()` method exists** in PyScadeOne 0.8.2.
   The generated wrapper must be imported directly from
   `<output_dir>/<output_dir>.py` and its operator class instantiated (class name
   pattern `<operator>_<design>`), with inputs/outputs grouped under
   `.inputs.<name>` / `.outputs.<name>` rather than flat attributes — same API shape
   Lab 3.1's wrapper tests already use. `evaluate_cc.py` and `lab.md` updated
   accordingly.
4. **`set_point` is a plain input on the generated `cruise_control` node**, not
   something the node computes internally from a `set` trigger. `evaluate_cc.py` (and
   the `lab.md` listing) now reproduce Activity 4E's "rising edge of `on` locks
   `set_point = v_speed`" rule in Python and hold that value across cycles; the
   scenario CSVs' `set` column is accepted by `run_cycle()` but not fed to the model
   (it isn't part of this node's interface).
5. **`tc02_cc_active_regulates.csv`** had an unquoted comma inside its `note` field,
   which made `csv.DictReader` parse an 11th field and later crash
   `csv.DictWriter.writerows` (`dict contains fields not in fieldnames: None`). The
   field is now properly quoted.

No requirements, model files, or test expectations changed — this was a bugfix pass
on the Python glue code and its lab documentation, informed by actually exercising it.

---

## 2026-07-27 — Lab 3.2: Python-driven evaluation replaces Scade One test harness; Project Structure section added

### Summary for reporting

Updated Lab 3.2 (the Scade One cruise-control lab) in two ways:

1. **Replaced the in-tool test-harness exercise with a Python evaluation
   workflow.** Students now define test scenarios as simple CSV files,
   run a Python script that exercises the model and logs the results to
   CSV, and get an automatic pass/fail report plus charts showing how the
   system behaves over time — closer to real engineering practice and to
   how the students already worked in the earlier Python lab. A worked
   reference example (script + 6 sample scenarios) was added for
   instructors.
2. **Clarified the project's structure for students.** Added a short
   explanation, up front in the lesson, of the three parts of the Scade
   One project: the vehicle model (a stand-in, for simulation only), the
   cruise-control model (the actual thing students design and the only
   part that matters for the real system), and the simulation wiring
   (learning aid only, never shipped). This removes prior ambiguity about
   what students are actually being graded on.

No models, requirements, or existing test content were changed — this was
a lesson-flow and documentation update. Full technical detail below.

**Scope:** `docs/lab3_2/lab.md` (Parts 5–6, plus a new "Project Structure"
section) and its supporting reference material under
`src/lab3_2/solution/CruiseControl/`. Corresponding `.agents/` and
`project_docs/` maintainer documentation updated in the same pass per
`AGENTS.md`'s "keep docs and content in sync" rule.

### 1. Part 6 rewritten: Scade One test harness → Python evaluation script

- **Part 5** now only briefly mentions Scade One's in-tool Test Harnesses
  (`.swant`) before redirecting to Part 6; the harness-building framing was
  removed from the lesson's critical path (`Main_test.swant` stays as an
  unused, empty scaffold — not deleted, just no longer part of the taught
  workflow).
- **Part 6** ("Python Test Script" → "Python Evaluation Script") rewritten
  across Activities 6C–6F:
  - **6C** — test scenarios are now defined as CSV files under `scenarios/`
    (one file per test case, one row per simulation cycle), replacing
    inline hardcoded test tuples. Optional `expected_throttle`/`req`/`note`
    columns mark checkpoint rows.
  - **6D** — `evaluate_cc.py` reads every scenario, drives the generated
    wrapper cycle-by-cycle, writes a per-scenario trace CSV, and writes
    `results/summary.csv` as a traceability report (REQ-tagged, PASS/FAIL,
    same banner style as Lab 2's `VALIDATION: ALL REQUIREMENTS MET.`).
  - **6E** — adds a `matplotlib`-based charting step
    (`results/plots/<tid>.png`, throttle + `v_speed` vs. cycle on twin
    axes) so `cc_active`'s gradual PI-regulator convergence — not checkable
    as a single expected value — can be evaluated visually.
  - **6F** — run/compare step updated to point at `results/summary.csv` and
    the charts instead of a single console printout.
- Structure table: Part 6 time bumped 30 → 45 min to reflect the added
  scope.
- `requirements.txt` (both the in-lab.md example and the real
  `src/lab3_2/solution/CruiseControl/requirements.txt`) gained `matplotlib`.

**New reference files** (instructor-only, under
`src/lab3_2/solution/CruiseControl/`):
- `evaluate_cc.py` — full reference implementation of Activities 6C–6F.
  Syntax-verified with `python -m py_compile` (passes); cannot be executed
  in this environment — requires a local Scade One install to regenerate
  `cc_wrapper` first (same limitation as the pre-existing `tester.py`).
- `scenarios/tc01_cc_disabled_passthrough.csv` … `tc06_cc_off.csv` — six
  example scenarios covering REQ-01/02/04, mirroring Lab 2's test cases as
  short multi-cycle sequences.
- `tester.py` (pre-existing) kept as-is, no longer part of the taught
  workflow but not removed.

**Known caveat carried forward, not resolved this session:** `evaluate_cc.py`
and the lab.md snippet it's based on both use a simplified, hypothetical
wrapper attribute API (`cc.on`, `cc.brake`, `cc.cycle()`, `cc.throttle`)
that differs from the real generated `cc_wrapper.py` (which wraps the
closed-loop `main` node, not a standalone `cruise_control` instance). This
gap pre-dates this session (see `project_docs/architecture/python-and-simulation.md`)
and would require a Scade One install to fix and verify — flagged, not
silently patched.

### 2. New "Project Structure" section

Added a section (after the Structure table, before "The System") that
explains the `CruiseControl` project's three packages and their distinct
roles, matching what students see in Scade One's Model Explorer:

| Package | Role | Ships to the real system? |
|---|---|---|
| `Car_design` (`car`) | Stand-in plant model for a real vehicle — simulation aid only | No |
| `CC_design` (`cruise_control`/`regulator`/`limiter`) | **The actual deliverable** — what students design and what Part 6 generates code from | Yes |
| `Simulation` (`main`/`main_manual`) | Wiring scaffolding for interactive simulation only | No — never a code-generation target |

This also explains, in-lesson, *why* Activity 6A's code-generation job
targets `cruise_control` and not `main` — a rationale that was previously
implicit. A matching one-line note was added to the Optional Extension
section (closed-loop `main` wiring), and mirrored in `.agents/scade-models.md`
and `project_docs/architecture/scade-projects.md` for maintainers.

### Files touched

```
docs/lab3_2/lab.md                                          (Parts 5-6 rewrite, new Project Structure section)
src/lab3_2/solution/CruiseControl/requirements.txt          (+matplotlib)
src/lab3_2/solution/CruiseControl/evaluate_cc.py             [new]
src/lab3_2/solution/CruiseControl/scenarios/*.csv (x6)        [new]
.agents/lab-map.md
.agents/workflows.md
.agents/verification.md
.agents/testing.md
.agents/python.md
.agents/scade-models.md
project_docs/labs/lab-3-2-cruise-control.md
project_docs/architecture/python-and-simulation.md
project_docs/architecture/scade-projects.md
project_docs/verification/requirements-and-traceability.md
project_docs/verification/testing-and-simulation.md
```

### Validation performed

- `python -m py_compile` on every `.py` file under `src/lab3_1/solution/`
  and `src/lab3_2/solution/CruiseControl/` (including the new
  `evaluate_cc.py`) — all parse without error.
- `cd docs && bundle exec jekyll build` — succeeded twice this session
  (after the Part 6 rewrite, and again after the Project Structure
  addition); only pre-existing `jekyll-theme-cayman` Sass deprecation
  warnings, unrelated to this repo's content.
- **Not run / not possible in this environment:** the Scade One simulator,
  code generation, wrapper regeneration, or `evaluate_cc.py`/`tester.py`
  execution — all require a local Scade One Student Edition install, not
  available here (see `.agents/testing.md`).

### Not addressed / carried over as open items

- The wrapper-API mismatch caveat above (pre-existing, not newly
  introduced).
- `ansys-scadeone-core` remains unpinned in Lab 3.2's `requirements.txt`
  (inconsistent with Lab 3.1's `==0.8.2` pin) — untouched, per standing
  guidance not to invent a pin without maintainer confirmation.
- Activity 7A traceability gap (only 1 of 4 `#pragma requirement` links
  present in the shipped `.swan`) — untouched, out of scope for this
  session's changes.
- **Unrelated local working-tree state noticed but not made by this
  session:** at the time of writing, `git status` also shows the 9
  `docs/lab3_2/img/*.png` screenshots as modified (larger file sizes) and
  `src/lab3_2/solution/CruiseControl/assets/Main_test.swant` as deleted.
  Neither of these was touched by the changes described above — flagging
  for the maintainer to confirm intent before committing.
