# Portfolio map

Published at `https://alexp25.github.io/scade-labs/` (`docs/index.html`).

| Card | Directory | Status | Overview |
|---|---|---|---|
| Lab 1 | *(none)* | "Coming soon" — disabled card, no `href`, no content exists anywhere in the repo | — |
| Lab 2 | `docs/lab2/` + `src/lab2/` | Active | [lab-2-sdlc.md](lab-2-sdlc.md) |
| Lab 3.1 | `docs/lab3_1/` + `src/lab3_1/` | Active | [lab-3-1-scade-one-intro.md](lab-3-1-scade-one-intro.md) |
| Lab 3.2 | `docs/lab3_2/` + `src/lab3_2/` | Active | [lab-3-2-cruise-control.md](lab-3-2-cruise-control.md) |

## Sequencing

Lab 3.2's own `lab.md` states Lab 3.1 as a hard prerequisite ("Complete
Lab 3.1 first") and Lab 2 as a conceptual prerequisite (state machine reused
as the modeling target). Lab 2 has no stated prerequisite. There is no
enforced sequencing mechanism (no locking/gating) — this is instructional
guidance in prose only.

## Legacy (not part of the portfolio, not linked from `docs/index.html`)

- `old/lab2_old/` — earlier version of Lab 2.
- `old/scade_demo/` — earlier Scade demo/project2 models.
- `scade_demo/` (repo root, untracked) — local Scade One codegen job output,
  not curriculum content.

## Numbering note

The portfolio page consistently uses "3.1"/"3.2". `docs/lab3_2/lab.md`'s own
prose previously called its prerequisite "Lab 3" and linked to a
non-existent `../lab3/` path in 7 places — this was a real inconsistency,
fixed during this documentation pass (see
`project_docs/architecture/site-and-publishing.md` → "Corrections made this
session").
