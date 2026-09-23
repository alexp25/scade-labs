# Testing / validation

**No linter, formatter, static type checker, test framework (pytest, unittest
runner, etc.), or CI workflow exists in this repository.** Do not invent one.
All "tests" below are plain scripts a human runs and reads printed PASS/FAIL
text from.

## Root site build

- **Working directory:** `docs/`
- **Prerequisites:** Ruby + Bundler (available in this environment —
  `bundle exec jekyll build --destination <tmp>`)
- **Expected result:** builds without error; output tree mirrors `docs/`
  (portfolio `index.html` + `lab1/`, `lab2/`, `lab3/`, `lab4/` each with
  `index.html`+`lab.md`).
- **Actually run in the Lab-3-restructuring session (2026-08-10):** yes,
  after both the initial renumbering pass and the follow-up pass that merged
  the former Lab 4.1 into Lab 3 — succeeded both times. Only output was
  pre-existing Sass deprecation warnings from the `jekyll-theme-cayman` gem
  itself (`@import`/`invert()` deprecations), unrelated to this repo's own
  content. Output tree confirmed to contain exactly `lab2/`, `lab3/`,
  `lab4/` (no stray `lab3_1/`, `lab3_2/`, `lab4_1/`, or `lab4_2/`). Temp
  output directories were deleted after inspection, not committed.
- **Actually run in the Lab-1-creation session (2026-08-11):** yes —
  `bundle exec jekyll build --destination <tmp>` succeeded (same
  pre-existing Sass deprecation warnings only), and the output tree was
  confirmed to contain `lab1/index.html` + `lab1/lab.md`. Temp output
  directory deleted after inspection, not committed.

## Link/asset integrity

- **Working directory:** `docs/`
- **Command:** grepped every relative `href="./...">` in the 4 `.html`
  pages and confirmed each target directory exists; grepped every
  `img/*.png` reference in each `lab.md` (Lab 2 has no `img/`) and confirmed
  each file exists on disk; grepped every `../labN/` cross-link in
  `lab3/lab.md`/`lab4/lab.md` and confirmed each target directory exists.
- **Actually run in the Lab-3-restructuring session (2026-08-10):** yes —
  all portfolio-card hrefs (`./lab2/`, `./lab3/`, `./lab4/`) resolve; all
  cross-lab links (`../lab2/`, `../lab3/`, `../lab4/`, including in-page
  anchor links from Lab 3 into Lab 4's Activity 7A heading and vice versa)
  resolve; every `img/*.png` reference in Lab 3/Lab 4's `lab.md` resolves to
  a real file. Anchor slugs were computed by hand against the `slugify()`
  logic in each `index.html` (lowercase, strip non-word/space/hyphen chars,
  collapse whitespace to a single hyphen) — not verified by actually loading
  the rendered page in a browser.

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

## Lab 3 — requirements text (no automated test) + Scade One Python wrappers

- Lab 3's *requirements* deliverable is free-text markdown
  (`src/lab3/starter/requirements_template.md` filled in, graded against
  `src/lab3/solution/requirements.md`). There is no script or harness to
  run for this part — the automated components are two in-page quizzes
  (`#ears-pattern-quiz` for Activity 1A, `#reflection-quiz` at the end),
  both client-side scored via a shared `initQuiz(containerId)` function in
  `docs/lab3/index.html`, same underlying mechanism as Lab 4's single quiz
  but generalized to host two independent widgets on one page. Neither quiz
  checks the student's own written REQ IDs or test-case sketch — both are
  fixed-answer comprehension checks. Both markdown files are plain text; no
  syntax to validate beyond "the file parses as markdown."
- Lab 3's *Scade One modeling* deliverable (Limiter, Counter, and their
  Python wrapper tests): regenerating the wrapper (`setup_wrapper.py`) needs
  the proprietary Scade One Student Edition install and cannot be done in
  this environment (`python -c "import ansys.scadeone.core"` →
  `ModuleNotFoundError: No module named 'ansys'`). **But** `src/lab3/solution/`
  already ships a pre-built `limiter_wrapper/limiter_wrapper.dll` and
  `counter_wrapper/counter_wrapper.dll` committed alongside the generated
  `.py` wrappers, and those wrappers load the `.dll` directly via `ctypes`
  — they do **not** import `ansys` at runtime, only `setup_wrapper.py` (the
  regeneration step) does. So all four test scripts (`test_limiter.py`,
  `test_counter.py`, and their `_advanced` counterparts) **can** and
  **were** actually run in this environment against the committed solution
  artifacts:
  - **Actually run this session (2026-08-10, updated):**
    `python test_limiter.py` / `python test_counter.py` (simple — cycle +
    `[req] ... PASS/FAIL` print, no `blocks.swan` parsing) both printed
    `ALL PASS`. `python test_limiter_advanced.py` /
    `python test_counter_advanced.py` (`PYTHONIOENCODING=utf-8` needed —
    the scripts print a `→` arrow character the default Windows console
    codepage (cp1252) can't encode; this is cosmetic, pre-existing, and
    unrelated to correctness) each printed a "REQUIREMENT TRACEABILITY"
    report (parsed live from `assets/blocks.swan`'s `#pragma requirement`
    annotations) showing `REQ-LIM-01/02/03` and `REQ-CNT-01/02` each
    resolved to the diagram node(s) that implement them, followed by
    `ALL PASS` on every test case, then wrote
    `results/limiter_traceability.csv` / `results/counter_traceability.csv`
    (one row per test case: `tid`, `req`, `nodes`, `inputs`, `expected`,
    `actual`, `status` — same shape as Lab 4's `results/summary.csv`) and
    rendered `results/limiter_diagram.png` / `results/counter_diagram.png`
    with `matplotlib` — one box per `blocks.swan` diagram node, laid out
    using the node's own `"xy"` pragma coordinates and colored green/red by
    whether the requirement it's linked to passed or failed (gray if
    untraced). This is a custom stand-in for the requirement-coverage
    report/colored-diagram view Scade One Student Edition doesn't provide;
    see `docs/lab3/lab.md` Activity 7G. Confirmed by inspection (`Read` on
    both CSVs and both PNGs) that the output matches the reference model:
    3/3 and 4/4 rows `PASS`, all boxes green, no red or unexpectedly-gray
    requirement-tagged nodes.
  - **`--project-dir` (Activity 7F) confirmed working:** copied
    `src/lab3/solution/`'s `assets/`, `limiter_wrapper/`, and
    `counter_wrapper/` into a scratch folder outside the repo and ran
    `python test_limiter.py --project-dir <scratch-folder>` (from the
    simple script) and `python test_limiter_advanced.py --project-dir
    <scratch-folder>` (from the advanced one) — both found the wrapper and
    `blocks.swan` at the given path instead of next to the script, ran
    `ALL PASS`, and (advanced) wrote `<scratch-folder>/results/*` instead
    of the repo's own `results/` — i.e. a student pointing this at their
    own generated/uploaded project works and doesn't touch the repo's
    reference output.
  - **Also run against `src/lab3/starter/`:** no `.dll` exists there (never
    generated), so all four scripts fail at the wrapper import as
    expected — but the advanced scripts' traceability report still runs
    first (it only reads `blocks.swan`, not the `.dll`) and correctly
    prints `NOT TRACED` for every expected REQ ID, since the starter's
    `blocks.swan` intentionally ships without `#pragma requirement` links
    (those are added by Activities 2G/4F, which this repo can't perform
    without the live Scade One Requirements panel). The CSV/diagram step is
    never reached in this case since it runs after the (missing) wrapper
    import.
  - `python -m py_compile` was also run across every `.py` file in
    `src/lab3/starter/`, `src/lab3/solution/`, and
    `src/lab4/starter/CruiseControl/` (including the generated
    `counter_wrapper.py`/`limiter_wrapper.py`/`cc_wrapper.py`, and
    `evaluate_cc_full_report.py`) — all parse with no syntax errors.
  - **Not verified this session:** Lab 4's `evaluate_cc_full_report.py` (needs
    `matplotlib`, not confirmed installed) and the Scade One model/GUI
    itself (see below) — only Lab 3's already-generated wrapper `.dll`s
    were exercised.
  - **Full regeneration procedure** (from the repo's own
    `readme.txt`/`generate_python_wrapper.bat`, not needed for the above
    but required if the model changes and the wrapper needs rebuilding):
    1. Install Scade One Student Edition.
    2. `pip install -r requirements.txt` inside **`src/lab3/solution/`**
       (not `starter/` — that copy's `blocks.swan`/`test.swant` are
       flattened out of `assets/` and won't open in Scade One, see
       `.agents/scade-models.md`) or `src/lab4/starter/CruiseControl/`
       (Lab 4's now also installs `matplotlib`).
    3. Run `setup_wrapper.py` from `src/lab3/solution/` (Lab 3) or
       `generate_python_wrapper.bat` (Lab 4) to regenerate the wrapper +
       `.dll`.
    4. `python test_counter.py` / `python test_limiter.py` (Lab 3) — expect
       printed PASS for all cases (hardcoded expected values documented in
       `.agents/python.md`).
    5. `python evaluate_cc_full_report.py` (Lab 4) — reads `scenarios/*.csv`, expects a
       `"VALIDATION: ALL REQUIREMENTS MET."` banner over the checkpoint
       rows, `results/summary.csv`, and `results/plots/*.png`. `python
       evaluate_cc_quick_tester.py` still exists separately — prints a live 1000-cycle trace
       with no pass/fail signal, visual inspection only.

## Scade One model simulation itself

Cannot be run or verified from this environment — requires the Scade One
desktop application and a license/install, neither of which is available
here. The expected values documented per-activity in `docs/lab3/lab.md`
and `docs/lab4/lab.md` (e.g. "Expected output: `value_out = 100.0`") are
the repository's own stated expectations, not independently re-verified by
this session. The `#pragma requirement` traceability links Activities
2G/4F/7A ask students to create via the live Requirements panel likewise
cannot be added or verified here — Lab 3 Part 9 and Lab 4 Activity 7A's
discussion of the `CC_design.swan` excerpt instead uses the file already
committed to this repo as evidence.

## Lab 6 — no automated test beyond the quiz

- Lab 6's Parts 10–12 deliverable is free-text/diagram markdown — no script
  or harness to run, same completion model as Lab 3's requirements text and
  all of Lab 5. The only automated component is the client-side
  `#architecture-quiz` (self-authored, not from an instructor-supplied
  answer key — see `project_docs/labs/lab-6-architecture.md`).
- **Actually run this session (2026-09-23):**
  `cd docs && bundle exec jekyll build --destination <tmp>` succeeded —
  same pre-existing Sass deprecation warnings only (`jekyll-theme-cayman`'s
  own `@import`/`invert()` usage, unrelated to this repo's content). Output
  tree confirmed to contain `lab6/index.html` and `lab6/lab.md` alongside
  the existing `lab1`–`lab5` and `account`/`admin` directories. Temp output
  directory deleted after inspection, not committed.
- **Link check:** grepped `href="./lab` in `docs/index.html` — six cards
  (`./lab1/` … `./lab6/`), all resolve to real directories.
- **Not verified this session:** the page was not opened in an actual
  browser, so Mermaid.js's CDN-loaded rendering of Lab 6's diagrams (the
  first use of Mermaid in this repo) was not visually confirmed — only
  code-reviewed against the working `marked.js`/`highlight.js` pattern the
  rest of `docs/lab6/index.html` reuses from Lab 5.

## Manual/visual checks

- No student-facing page exposes instructor solution content: confirmed by
  directory separation (`src/lab2/solution/` and `src/lab3/solution/` are
  never referenced from any file under `docs/` — grepped for `solution`
  across `docs/**/*.html`, `docs/**/*.md`: no hits) and by the fact that
  `src/` is never linked from any `docs/` page.
- New/edited `.agents/` and `project_docs/` files were checked against
  actual repo paths (Glob/Read) before being written.
