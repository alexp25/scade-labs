# Portfolio map

Published at `https://alexp25.github.io/scade-labs/` (`docs/index.html`).

| Card | Directory | Status | Overview |
|---|---|---|---|
| Lab 1 | `docs/lab1/` (no `src/lab1/` — reading + quiz only) | Active | — |
| Lab 2 | `docs/lab2/` + `src/lab2/` | Active | [lab-2-sdlc.md](lab-2-sdlc.md) |
| Lab 3 | `docs/lab3/` + `src/lab3/` | Active — substantially restructured this session | [lab-3-requirements.md](lab-3-requirements.md) |
| Lab 4 | `docs/lab4/` + `src/lab4/` | Active | [lab-4-cruise-control.md](lab-4-cruise-control.md) |
| Lab 5 | `docs/lab5/` (no `src/lab5/` — reading + quiz only) | Active — created earlier this session | [lab-5-design-principles.md](lab-5-design-principles.md) |
| Lab 6 | `docs/lab6/` (no `src/lab6/` — reading + hands-on written exercise + quiz) | Active — created this session, fully registered (portfolio card, both `LAB_TITLES` maps, `.agents/lab-map.md`) | [lab-6-architecture.md](lab-6-architecture.md) |

## Sequencing

Lab 4's own `lab.md` lists Lab 2 (conceptual) and Lab 3 (hard prerequisite —
Scade One install, Swan basics, and the REQ-01–REQ-08 requirement set all
come from there) as prerequisites. Lab 3 recommends Lab 2 (conceptual, for
the informal cruise-control description and REQ-01..06). There is no
enforced sequencing mechanism (no locking/gating) anywhere — this is
instructional guidance in prose only.

## Legacy (not part of the portfolio, not linked from `docs/index.html`)

- `old/lab2_old/` — earlier version of Lab 2.
- `old/scade_demo/` — earlier Scade demo/project2 models.
- `scade_demo/` (repo root, untracked) — local Scade One codegen job output,
  not curriculum content.

## Numbering note

**Restructured across two sessions.** The portfolio originally used
"3.1"/"3.2" for the two Scade One labs. A first pass renumbered these to
Lab 4.1/Lab 4.2 to make room for a new plain "Lab 3" (requirements
engineering) ahead of them. A second pass — per explicit follow-up user
direction — merged Lab 4.1's entire Scade One/Swan/Limiter/Counter content
into Lab 3, retired Lab 4.1 entirely, and renumbered Lab 4.2 down to plain
**Lab 4** (no longer needs a decimal — there's only one Scade One lab left).
Neither pass was a bug fix — both were deliberate, user-approved
restructures (see `project_docs/changelog.md`'s two newest entries). Both
**break previously published external links**: `/lab3_1/`, `/lab3_2/`,
`/lab4_1/`, `/lab4_2/` all now 404 — GitHub Pages has no redirect mechanism
configured in this repo.

The portfolio is now six cards, no decimals: **Lab 1 / Lab 2 / Lab 3 / Lab 4 /
Lab 5 / Lab 6** (Lab 1 was later filled in and activated; see
`project_docs/changelog.md`'s "Lab 1: created" entry. Lab 6 — Software
Architecture — was added this session; unlike Lab 5, its registration
(portfolio card + both `LAB_TITLES` maps + `.agents/lab-map.md`) was
completed in the same session it was created, so it does not carry Lab 5's
"unfinished registration" gap forward).
