# Adding or updating a lab

This procedure is **inferred** from the shared shape of the 3 existing labs
— it is not separately documented anywhere else in the repository. If you
find it wrong once you actually try it, correct this file.

## Adding a new lab

1. Create `docs/labN/` with:
   - `index.html` — copy an existing lab's shell (e.g. `docs/lab3_1/index.html`
     if the new lab has no live editor; `docs/lab2/index.html` if it needs
     one). Keep the `fetch('lab.md')` + `marked.js` render pattern — this is
     what every published page uses (see
     `project_docs/architecture/site-and-publishing.md`).
   - `lab.md` — the actual lesson content. This is what gets rendered; the
     `index.html` shell only provides chrome/widgets.
   - `img/` — only if you have screenshots. (Lab 2 has none; it uses a live
     editor instead.)
2. Create `src/labN/`:
   - `solution/` — reference implementation/model (never link this from
     `docs/`).
   - `starter/` — only if the lab has a student-editable code stub, as
     Lab 2 does. Lab 3.1/3.2 are GUI-modeling exercises with no starter.
3. Add a card to `docs/index.html` (see the existing 4 `.lab-num` cards for
   the pattern — `href="./labN/"`, matching title).
4. Update `.agents/lab-map.md` and add a `project_docs/labs/labN-*.md` page
   following the shape of the existing 3.
5. `cd docs && bundle exec jekyll build` (or `serve`) to preview before
   pushing.

## Updating an existing lab

1. Edit `docs/labN/lab.md` — this is the single source of truth for content.
2. **If it's Lab 2**: also update
   `src/lab2/starter/lab2_cruise_control_starter.py` AND the `STARTER_CODE`
   JS literal in `docs/lab2/index.html` together. They are currently
   byte-identical (verified this session, aside from CRLF/LF) — there is no
   build step that generates one from the other, so keep them manually in
   sync.
3. If behavior/requirements changed: update the corresponding requirements
   text, decision table, test cases, and traceability matrix in the same
   `lab.md`, plus the Python/Swan implementation and its tests, together —
   see `.agents/verification.md`'s "gaps" section for what's *not*
   auto-checked (nothing cross-validates lab.md's stated requirements
   against the code).
4. If Scade One models changed: regenerate the wrapper via
   `setup_wrapper.py` (Lab 3.1) or `generate_python_wrapper.bat` (Lab 3.2) —
   requires a local Scade One install — and re-run the corresponding test
   script. Never hand-edit the generated `*_wrapper.py`/`.c`/`.def`/`.dll`
   files (see `project_docs/architecture/scade-projects.md`).
5. Run the checks in
   `project_docs/maintenance/validation-checklist.md` before publishing.

## Do not

- Put maintainer/architecture documentation under `docs/` — it's the public
  GitHub Pages root (see `.agents/decisions/0001-canonical-docs-location.md`).
- Delete `old/`, `docs/lab3_2/lab_old.md`, or root `scade_demo/` as part of a
  routine lab update — these are legacy/out-of-scope, flagged for a
  maintainer decision, not something to silently remove.
- Invent a version pin for `ansys-scadeone-core` in Lab 3.2's
  `requirements.txt` to "match" Lab 3.1 — the correct pin depends on which
  Scade One/API version actually produced the shipped `cc_wrapper.*` files,
  which requires maintainer confirmation.
