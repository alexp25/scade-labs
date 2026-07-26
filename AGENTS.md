# Project Agent Instructions

SCADE Lab Portfolio — an educational repository of safety-critical software
engineering labs (Python + Ansys Scade One), published as a static site at
https://alexp25.github.io/scade-labs/ (repo: https://github.com/alexp25/scade-labs).

Before making changes, inspect the affected lab and read the relevant
documentation listed below.

## Always read

- `.agents/architecture.md`
- `.agents/lab-map.md`
- `.agents/domain.md`

## Read when relevant

- Website or publishing changes: `.agents/publishing.md`
- Python exercises or simulations: `.agents/python.md`
- Scade One models or generated artifacts: `.agents/scade-models.md`
- Requirements, tests, or traceability: `.agents/verification.md`
- Lab instructions or learning flow: `.agents/workflows.md`
- Validation commands: `.agents/testing.md`
- External tools or remotely loaded resources: `.agents/integrations.md`
- Architectural or instructional decisions: `.agents/decisions/`

## Working rules

- Inspect the affected source, model, script, and published page before editing.
- Make focused changes and preserve the educational objective of each lab.
- Follow the conventions of the specific lab; do not assume every lab has the
  same structure. Lab 2 is pure Python with a starter/solution split and no
  `img/`; Lab 3.1/3.2 are Scade One GUI labs with no starter code and no
  student-facing local Python entry point, only reference `solution/` assets.
- Keep student starter material (`src/lab2/starter/`) separate from
  instructor/reference solutions (`src/*/solution/`).
- Do not expose solution content from `docs/` (the published site) or from any
  student-facing page or file.
- `docs/` is the GitHub Pages publishing root (classic branch/`docs`-folder
  deploy — no `.github/workflows/`, no `CNAME`, no `.nojekyll`). Do not put
  internal/maintainer documentation there; use `project_docs/` instead (see
  `.agents/decisions/0001-canonical-docs-location.md`).
- Treat Scade One project metadata and generated output according to the
  source/generated boundaries documented in `.agents/scade-models.md`.
- Do not manually edit generated artifacts (`*_wrapper.py`, `cc_wrapper.c`,
  `cc_wrapper.def`, `*.dll`, generator manifest `.txt` files) unless the
  repository explicitly treats them as maintained source.
- Preserve requirement identifiers, model interfaces, state semantics, test
  expectations, and traceability links unless the requested change requires
  updating them.
- When behavior changes, update the corresponding requirements, model or Python
  implementation, tests, expected results, lab instructions, and traceability
  artifacts together.
- Keep `lab.md` (the file actually fetched and rendered by each lab's
  `index.html`), the embedded browser code (Lab 2's `STARTER_CODE` in
  `docs/lab2/index.html`), and the standalone starter/solution files in `src/`
  synchronized — verify they still match before finishing, they are currently
  identical and should stay that way.
- Do not claim that a model, simulation, test, Jekyll build, or published page
  was validated unless that validation was actually performed.
- Clearly distinguish validation performed locally from validation requiring
  Scade One or other unavailable proprietary tooling.
- Do not claim compliance with a safety standard or certification objective
  (DO-178C, ISO 26262, etc. appear only as educational/reflection context in
  this repo, never as a compliance claim) unless the repository contains
  explicit supporting evidence.
- Run all applicable checks documented in `.agents/testing.md`.
- Summarize changed files, generated artifacts, and validation performed.
- If a change affects architecture, publishing, a lab workflow, Python logic,
  a Scade One model, requirements, verification, or traceability, update the
  corresponding `.agents/` and `project_docs/` files in the same task.
- Treat stale documentation as a regression because future agents are expected
  to trust it.
