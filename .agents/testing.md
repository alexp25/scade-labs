# Testing / validation

**No linter, formatter, static type checker, test framework (pytest, unittest
runner, etc.), or CI workflow exists in this repository.** Do not invent one.
All "tests" below are plain scripts a human runs and reads printed PASS/FAIL
text from.

## Root site build (RUN THIS SESSION — passed)

- **Working directory:** `docs/`
- **Prerequisites:** Ruby + Bundler (already available in this environment)
- **Command:** `bundle exec jekyll build --destination <tmp>`
- **Expected result:** builds without error; output tree mirrors `docs/`
  (portfolio `index.html` + `lab2/`, `lab3_1/`, `lab3_2/` each with
  `index.html`+`lab.md`).
- **Actually run this session:** yes, 3 times (after the initial restructure,
  after the lab3_2 link fixes, and after moving `assets/css/syntax.css` into
  `docs/`) — all 3 succeeded. Only output was pre-existing Sass deprecation
  warnings from the `jekyll-theme-cayman` gem itself (`@import`/`invert()`
  deprecations), unrelated to this repo's own content.

## Link/asset integrity (RUN THIS SESSION — passed after fixes)

- **Working directory:** `docs/`
- **Command:** grepped every relative `href="."` in the 4 `.html` files and
  confirmed each target exists on disk; grepped every `img/...` reference in
  the 3 `lab.md` files and confirmed each image file exists.
- **Result:** all `.html` hrefs resolve. All image references resolve (no
  missing images; note `.agents/publishing.md` still lists *unused* images —
  present but never referenced, which is a content-debt note, not a broken
  link). The 7 broken `../lab3/` links inside `lab3_2/lab.md` found during
  this session's investigation were fixed and re-verified as resolving to
  `../lab3_1/`.

## Lab 2 — Python (RUN THIS SESSION — passed)

- **Working directory:** repo root (no install needed — stdlib only)
- **Prerequisites:** Python 3 (verified with the environment's Python 3.11.3;
  the repo does not pin a specific version for Lab 2)
- **Commands and actual output:**
  ```
  python src/lab2/solution/lab2_cruise_control_solution.py
  ```
  → all 7 tests PASS, `VALIDATION: ALL REQUIREMENTS MET.` (verified this
  session, exact transcript in `project_docs/labs/lab-2-sdlc.md`).
  ```
  python src/lab2/starter/lab2_cruise_control_starter.py
  ```
  → 3/7 PASS, 4/7 FAIL (TC-01, TC-02, TC-04, TC-06), `VALIDATION: ISSUES
  FOUND` — expected, since the starter's function body is an unimplemented
  stub. This confirms the test harness itself works correctly and
  discriminates a real implementation from a stub.

## Lab 3.1 / 3.2 — Scade One Python wrappers (NOT RUN — missing dependency)

- **Attempted:** `python -c "import ansys.scadeone.core"` → `ModuleNotFoundError:
  No module named 'ansys'`.
- **Why it can't run here:** `ansys-scadeone-core` requires a local Scade One
  Student Edition installation (`setup_wrapper.py`/`generate_python_wrapper.bat`
  both hardcode `C:\Program Files\Ansys Inc\v261\Scade One Student\Scade One`),
  which is proprietary desktop software not present in this environment.
- **What WAS verified this session instead:** `python -m py_compile` on every
  `.py` file in `src/lab3_1/solution/` and
  `src/lab3_2/solution/CruiseControl/` (including the generated
  `counter_wrapper.py`/`limiter_wrapper.py`/`cc_wrapper.py`, and this
  session's new `evaluate_cc.py`) — all parse with no syntax errors. This
  only proves the files are syntactically valid Python; it does **not**
  prove they execute correctly (that requires the sibling `.dll`, which in
  turn requires Scade One's code generator to have produced it — and, for
  `evaluate_cc.py`, also `matplotlib`, not verified installed here).
- **Remaining manual validation procedure** (from the repo's own
  `readme.txt`/`generate_python_wrapper.bat`, not executed here):
  1. Install Scade One Student Edition.
  2. `pip install -r requirements.txt` inside `src/lab3_1/solution/` or
     `src/lab3_2/solution/CruiseControl/` (Lab 3.2's now also installs
     `matplotlib`).
  3. Run `setup_wrapper.py` (Lab 3.1) or `generate_python_wrapper.bat`
     (Lab 3.2) to regenerate the wrapper + `.dll`.
  4. `python test_counter.py` / `python test_limiter.py` (Lab 3.1) — expect
     printed PASS for all cases (hardcoded expected values documented in
     `.agents/python.md`).
  5. `python evaluate_cc.py` (Lab 3.2) — reads `scenarios/*.csv`, expects a
     `"VALIDATION: ALL REQUIREMENTS MET."` banner over the checkpoint rows,
     `results/summary.csv`, and `results/plots/*.png`. `python tester.py`
     still exists separately — prints a live 1000-cycle trace with no
     pass/fail signal, visual inspection only.

## Scade One model simulation itself

Cannot be run or verified from this environment — requires the Scade One
desktop application and a license/install, neither of which is available
here. The expected values documented per-activity in `docs/lab3_1/lab.md`
and `docs/lab3_2/lab.md` (e.g. "Expected output: `value_out = 100.0`") are
the repository's own stated expectations, not independently re-verified by
this session.

## Manual/visual checks

- No student-facing page exposes instructor solution content: confirmed by
  directory separation (`src/*/solution/` is never referenced from any file
  under `docs/` — grepped for `solution` across `docs/**/*.html`,
  `docs/**/*.md`: no hits) and by the fact that `src/` is never linked from
  any `docs/` page.
- New/edited `.agents/` and `project_docs/` files were checked against actual
  repo paths (Glob/Read) before being written, per the sanity-check pass
  described in this session's task instructions.
