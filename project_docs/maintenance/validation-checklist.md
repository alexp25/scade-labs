# Validation checklist

Run whichever of these apply to your change. None of this is automated / CI-
gated — there is no pipeline in this repository.

## Any change under `docs/`

- [ ] `cd docs && bundle exec jekyll build` succeeds (verified working
      procedure this session; only expected output is
      `jekyll-theme-cayman`'s own Sass deprecation warnings).
- [ ] Every relative `href` you touched resolves to a real file/directory.
- [ ] Every `img/...` reference in the `lab.md` you touched resolves to a
      real file.
- [ ] If you touched `docs/lab2/index.html`'s `STARTER_CODE`, it still
      matches `src/lab2/starter/lab2_cruise_control_starter.py` (diff them,
      ignoring line endings).
- [ ] No page under `docs/` links to `src/` or anything under a `solution/`
      directory (grep `href.*src/\|href.*solution` across `docs/**/*.html`
      and `docs/**/*.md` — must return nothing).

## Lab 2 (Python) changes

- [ ] `python src/lab2/starter/lab2_cruise_control_starter.py` runs without
      a Python error (stub logic may legitimately FAIL tests — that's
      expected for an unimplemented starter).
- [ ] `python src/lab2/solution/lab2_cruise_control_solution.py` prints
      `VALIDATION: ALL REQUIREMENTS MET.` (all 7 PASS). This was the actual
      verified baseline this session — if it regresses, something broke the
      reference solution.
- [ ] If you changed a requirement or test case, update: the REQ text, the
      decision table, the TC table, the traceability matrix (all in
      `lab.md`), and the `req`/`tid` fields in both starter and solution
      code, together.

## Lab 3.1 / 3.2 (Scade One) changes — requires a local Scade One install

Not runnable in the environment used for this documentation pass — treat as
a manual maintainer procedure:
- [ ] Model builds with 0 errors in Scade One.
- [ ] Manual simulation matches the expected values stated in `lab.md`.
- [ ] Wrapper regenerated (`setup_wrapper.py` / `generate_python_wrapper.bat`)
      if the model changed.
- [ ] `python test_counter.py` / `test_limiter.py` (Lab 3.1) print all PASS.
- [ ] If you changed `CC_design.swan`'s automaton, re-check whether the
      `#pragma requirement` tags (currently only 1 of the 4 Activity 7A
      describes) still make sense, or explicitly note the gap remains.

Without Scade One, the minimum check available is:
- [ ] `python -m py_compile` on every changed `.py` file (catches syntax
      errors only, not runtime correctness).

## Any documentation change (`.agents/`, `project_docs/`, `AGENTS.md`)

- [ ] Every file path and symbol name you cite still exists (Glob/grep it —
      don't trust a prior write-up).
- [ ] You haven't turned an inferred/naming-based correspondence into a
      stated fact (see `.agents/verification.md` for the explicit/
      naming-based/inferred distinction — keep it).
- [ ] You haven't introduced a safety-standard compliance claim (DO-178C,
      ISO 26262, etc. are educational context only in this repo — see
      `project_docs/verification/requirements-and-traceability.md`).
