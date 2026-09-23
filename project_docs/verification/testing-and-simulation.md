# Testing and simulation

No linter, formatter, type checker, test framework, or CI workflow exists in
this repository. Every validation mechanism below is a plain script a human
runs and reads printed text from, or a manual comparison against a
documented expected value.

## What was actually run during this documentation/investigation session

| Check | Working dir | Command | Result |
|---|---|---|---|
| Jekyll build (×3, after restructure, after lab4 link fixes, after moving `syntax.css`) | `docs/` | `bundle exec jekyll build --destination <tmp>` | **Succeeded all 3 times** — only pre-existing `jekyll-theme-cayman` Sass deprecation warnings, unrelated to this repo's content |
| HTML relative-link check | `docs/` | grep every `href="."` in the 4 `.html` files, confirm target exists | **All resolve** |
| lab.md image-reference check | `docs/` | grep every `img/...` reference in the 3 `lab.md` files, confirm target exists | **All resolve** (see `project_docs/architecture/site-and-publishing.md` for *unused*-but-present images, a separate content-debt note) |
| Lab 2 solution | repo root | `python src/lab2/solution/lab2_cruise_control_solution.py` | **7/7 PASS**, `VALIDATION: ALL REQUIREMENTS MET.` |
| Lab 2 starter (control check) | repo root | `python src/lab2/starter/lab2_cruise_control_starter.py` | **3/7 PASS**, 4 FAIL (TC-01, TC-02, TC-04, TC-06), `VALIDATION: ISSUES FOUND` — expected, confirms the harness discriminates a stub from a working implementation |
| Scade wrapper dependency check | repo root | `python -c "import ansys.scadeone.core"` | **`ModuleNotFoundError: No module named 'ansys'`** — package not installed in this environment |
| Syntax check of all Lab 3/Lab 4 Python files | repo root | `python -m py_compile` on every `.py` in `src/lab3/starter/`, `src/lab3/solution/`, and `src/lab4/starter/CruiseControl/` (incl. generated wrappers and `evaluate_cc_full_report.py`) | **All parse with no syntax errors** — does not prove runtime correctness (needs the sibling `.dll` + a Scade One install) |
| No student-facing solution exposure | `docs/` | grep for `src/` or `solution` across every `.html` and `.md` under `docs/` | **Zero hits** — confirmed no published page links to instructor solution content |

## What could NOT be run, and why

- **Scade One model simulation itself** (Lab 3's `limiter`/`counter`,
  Lab 4's `cruise_control`/`regulator`/`car`) — requires the Ansys Scade
  One Student Edition desktop application, a proprietary local install
  (hardcoded path `C:\Program Files\Ansys Inc\v261\Scade One Student\Scade
  One` in the repo's own scripts). Not available in this environment.
- **Generated Python-wrapper tests** (`test_counter.py`, `test_limiter.py`,
  `evaluate_cc_quick_tester.py`) — require `ansys-scadeone-core` (not installed here) *and* a
  compiled `.dll` that only Scade One's code generator can produce. Only
  syntax-checked, not executed.
- **Regenerating any wrapper** (`setup_wrapper.py`,
  `generate_python_wrapper.bat`) — same dependency, not attempted.

## Remaining manual validation procedure (documented by the repo itself, not run here)

1. Install Scade One Student Edition (no license/registration needed).
2. `pip install -r requirements.txt` inside `src/lab3/solution/` (Lab 3 —
   use `solution/`, not `starter/`, since `starter/`'s `.swan` files are
   flattened and won't open in Scade One) or `src/lab4/starter/CruiseControl/`
   (Lab 4 — `starter/` is the working project there, no separate `solution/`
   exists).
3. Regenerate the wrapper (`setup_wrapper.py` for Lab 3,
   `generate_python_wrapper.bat` for Lab 4).
4. Run `test_counter.py`/`test_limiter.py` (Lab 3, expect all PASS) or
   `evaluate_cc_full_report.py` (Lab 4, expect a `results/summary.csv` PASS/FAIL
   traceability report plus `results/plots/*.png` charts — the standalone
   `evaluate_cc_quick_tester.py` console demo still exists but is no longer the lesson's
   evaluation path).
5. Open the `.sproj` in Scade One and re-run the built-in simulator against
   the expected values stated per-activity in each lab's `lab.md`.

## Expected results (as stated by the repository — not independently re-verified where Scade One is required)

- Lab 3 limiter: `(5,0,10)→5`, `(20,0,10)→10`, `(-5,0,10)→0`; harness run:
  `value_out = 100.0`.
- Lab 3 counter: cycles `0→0,1→1,2→2,3→3`; wrapper test:
  `expected_sequence = [0,1,2,3,4,5]`.
- Lab 4: build shows 0 errors; manual-mode `throttle` equals `accel`
  (`0.5`); the `evaluate_cc_full_report.py` scenario checkpoints assert `throttle ==
  accel` for the deterministic `cc_disabled`/`cc_standby` cases only —
  `cc_active` regulator behavior is evaluated visually via the generated
  charts, not asserted (no automated diff against Lab 2 exists either way).

## Do not claim

- That any Scade One simulation, wrapper test, or generated-code output was
  validated in this session — it was not; the required tooling is
  unavailable.
- That a linter, type checker, formatter, or CI pipeline exists or was run —
  none exist in this repository.
