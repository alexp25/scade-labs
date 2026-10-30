# ADR 0003: Module 2 labs live under `docs/m2/`; the IEEE 828 PDF is published for course use; a client-side GitHub API checker

**Date:** 2026-10-29 (Module 2 · Lab 1 creation session).

## Context

The instructor supplied Module 2 ("Advanced Critical Software Engineering")
material by dropping three PDFs into `docs/courses/m2/` — inside the public
GitHub Pages root: the Lesson 1 slides, the module syllabus, and
**IEEE Std 828-2012**, a copy licensed to the university (every page carries
"Authorized licensed use limited to Polytechnic University of Bucharest").
The first Module 2 lab also asks students to submit a *public GitHub
repository* and have it checked by the page.

## Decisions

1. **Module layout.** Module 2 labs live at `docs/m2/labN/` (lab ID
   `m2-labN`, e.g. `m2-lab1`) under their own portfolio section in
   `docs/index.html` — mirroring how the SCADE AI labs already use
   `docs/SCADE_AI_labs/lab1/`. The original Labs 1–6 are not renumbered.
   Pages sit two levels deep, so every shared-asset path and `data-base`
   is `../../`. Slides for the existing `course-slides.js` widget are
   published as `docs/courses/m2-labN.pdf` (the widget derives the filename
   from `CURRENT_LAB_ID`, so no widget change is needed).
2. **Source PDFs.** The original instructor files live in
   `project_docs/courses/m2/` (unpublished). **Revised the same day at the
   maintainer's direction:** the IEEE 828-2012 copy *is* published, as
   `docs/courses/ieee-828-2012.pdf`, linked from the lab, because the lab
   is training material delivered by Universitatea Politehnica din
   București, the licensee. (The first version of this decision kept it
   unpublished and gitignored, since each page reads "Authorized licensed
   use limited to Polytechnic University of Bucharest" and GitHub Pages is
   publicly reachable. The maintainer owns that licensing call.)
3. **Repository checker runs client-side against the GitHub REST API**
   (`docs/m2/lab2/repo-checker.js` since the 2026-10-30 split; originally
   under `lab1/`), consistent with the repo's
   no-backend, static-site model. Unauthenticated calls are limited to
   60/hour per IP (one check = 8 calls, and a classroom NAT shares the
   limit), so the page offers an *optional* personal access token, stored
   only in `sessionStorage` and sent only to `api.github.com`. The grading
   function `evaluateRepo()` is pure and Node-loadable so it can be tested
   without a browser. Scores are recorded through the existing
   `recordQuizAttempt()` (quizId `repo-check`).

## Consequences

- Each Module 2 lab: `docs/m2/labN/`, ID `m2-labN`, slides
  `docs/courses/m2-labN.pdf`, both `LAB_TITLES` entries, a card in the
  Module 2 portfolio section. Applied on 2026-10-30 when the original lab
  was split into M2 Lab 1 (CM plan) and M2 Lab 2 (GitHub + checker); both
  use a copy of the same Lesson 1 deck.
- The checker depends on GitHub's API response shapes and rate limits at
  runtime; it verifies that CM *evidence* exists (branches, tags, releases,
  PRs, issues, traced commits), never the quality of the student's plan,
  and never implies standard compliance.
- Whether to publish any further licensed third-party document is the
  maintainer's call. Ask before publishing; do not decide silently either
  way.
