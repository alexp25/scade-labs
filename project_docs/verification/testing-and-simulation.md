# Testing and simulation

No linter, formatter, type checker, test framework, or CI workflow exists in
this repository. Every validation mechanism below is a plain script a human
runs and reads printed text from, or a manual comparison against a
documented expected value.

## What was actually run during this documentation/investigation session

| Check | Working dir | Command | Result |
|---|---|---|---|
| Jekyll build (×3, after restructure, after lab3_2 link fixes, after moving `syntax.css`) | `docs/` | `bundle exec jekyll build --destination <tmp>` | **Succeeded all 3 times** — only pre-existing `jekyll-theme-cayman` Sass deprecation warnings, unrelated to this repo's content |
| HTML relative-link check | `docs/` | grep every `href="."` in the 4 `.html` files, confirm target exists | **All resolve** |
| lab.md image-reference check | `docs/` | grep every `img/...` reference in the 3 `lab.md` files, confirm target exists | **All resolve** (see `project_docs/architecture/site-and-publishing.md` for *unused*-but-present images, a separate content-debt note) |
| Lab 2 solution | repo root | `python src/lab2/solution/lab2_cruise_control_solution.py` | **7/7 PASS**, `VALIDATION: ALL REQUIREMENTS MET.` |
| Lab 2 starter (control check) | repo root | `python src/lab2/starter/lab2_cruise_control_starter.py` | **3/7 PASS**, 4 FAIL (TC-01, TC-02, TC-04, TC-06), `VALIDATION: ISSUES FOUND` — expected, confirms the harness discriminates a stub from a working implementation |
| Scade wrapper dependency check | repo root | `python -c "import ansys.scadeone.core"` | **`ModuleNotFoundError: No module named 'ansys'`** — package not installed in this environment |
| Syntax check of all Lab 3.1/3.2 Python files | repo root | `python -m py_compile` on every `.py` in `src/lab3_1/solution/` and `src/lab3_2/solution/CruiseControl/` (incl. generated wrappers) | **All parse with no syntax errors** — does not prove runtime correctness (needs the sibling `.dll` + a Scade One install) |
| No student-facing solution exposure | `docs/` | grep for `src/` or `solution` across every `.html` and `.md` under `docs/` | **Zero hits** — confirmed no published page links to instructor solution content |

## What could NOT be run, and why

- **Scade One model simulation itself** (Lab 3.1's `limiter`/`counter`,
  Lab 3.2's `cruise_control`/`regulator`/`car`) — requires the Ansys Scade
  One Student Edition desktop application, a proprietary local install
  (hardcoded path `C:\Program Files\Ansys Inc\v261\Scade One Student\Scade
  One` in the repo's own scripts). Not available in this environment.
- **Generated Python-wrapper tests** (`test_counter.py`, `test_limiter.py`,
  `tester.py`) — require `ansys-scadeone-core` (not installed here) *and* a
  compiled `.dll` that only Scade One's code generator can produce. Only
  syntax-checked, not executed.
- **Regenerating any wrapper** (`setup_wrapper.py`,
  `generate_python_wrapper.bat`) — same dependency, not attempted.

## Remaining manual validation procedure (documented by the repo itself, not run here)

1. Install Scade One Student Edition (no license/registration needed).
2. `pip install -r requirements.txt` inside the relevant lab's solution
   folder.
3. Regenerate the wrapper (`setup_wrapper.py` for Lab 3.1,
   `generate_python_wrapper.bat` for Lab 3.2).
4. Run `test_counter.py`/`test_limiter.py` (Lab 3.1, expect all PASS) or
   `tester.py` (Lab 3.2, expect a live trace with no explicit pass/fail
   signal — visual inspection only).
5. Open the `.sproj` in Scade One and re-run the built-in simulator against
   the expected values stated per-activity in each lab's `lab.md`.

## Expected results (as stated by the repository — not independently re-verified where Scade One is required)

- Lab 3.1 limiter: `(5,0,10)→5`, `(20,0,10)→10`, `(-5,0,10)→0`; harness run:
  `value_out = 100.0`.
- Lab 3.1 counter: cycles `0→0,1→1,2→2,3→3`; wrapper test:
  `expected_sequence = [0,1,2,3,4,5]`.
- Lab 3.2: build shows 0 errors; manual-mode `throttle` equals `accel`
  (`0.5`); Python wrapper trace should visually match Lab 2's behavior at
  equivalent inputs (no automated diff exists to confirm this).

## Do not claim

- That any Scade One simulation, wrapper test, or generated-code output was
  validated in this session — it was not; the required tooling is
  unavailable.
- That a linter, type checker, formatter, or CI pipeline exists or was run —
  none exist in this repository.
