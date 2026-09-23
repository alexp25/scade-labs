# Lab 5 — Software Design Principles in Safety-Critical Software Engineering

## Sources

Three instructor-supplied files, none committed to the repo:

- `Slides 5 with notes.pdf` — the lecture: why design matters more in
  safety-critical systems, how DO-178C/ISO 26262/EN 50716/IEC 62304/IEC 61508
  drive architecture, and the eight core principles (Top-Down Design,
  Modularity/Information Hiding, Traceability by Design, Strong Typing &
  Deterministic Design — including the Ariane 5 example, SOLID, DRY/KISS,
  Model-Based Design), plus a Best Practices/Common Mistakes slide.
- `Article for lesson 5.pdf` — Hackenbeck, C., Walz, A., Hirmer, P., Wagner,
  S., & Weyrich, M. (2025). *Semantic Interface Modeling for Automotive
  Architectures Using a Domain-Driven Approach*. IFAC-PapersOnLine, 59(25),
  125–130. DOI: [10.1016/j.ifacol.2025.11.936](https://doi.org/10.1016/j.ifacol.2025.11.936).
  A domain-driven-design methodology for semantically characterizing
  interfaces in automotive Software-Defined Vehicle architectures,
  demonstrated on a safety-critical Life Presence Detection (LPD) use case.
- `Lab 5.pdf` — the assignment: a connection table (studied principle → how
  it shows up in the article) plus a 10-question multiple-choice quiz with
  an answer key (1-A, 2-C, 3-B, 4-C, 5-A, 6-C, 7-A, 8-B, 9-A, 10-C).

## What was built

`docs/lab5/lab.md` and `docs/lab5/index.html`, following the "reading +
quiz only" shape (`.agents/lab-map.md` — no `src/lab5/`, no
starter/solution split).

`lab.md` was **revised after first being drafted** — the initial version
fully reproduced the slide deck's content (all 8 principle sections, the
Emergency Braking / Ariane 5 / Brake Controller worked examples, the
standards table) inside `lab.md` itself. Per explicit user feedback ("the
parts that are already in the course slides should not be repeated, only
summarized eventually... the lab should not repeat the course"), this was
cut down to match the condensed-recap pattern later established by Lab 6:

- A short **Recap** section (one bullet per principle, one line each) that
  explicitly says it is not a replacement for the slides, plus a
  **Course Slides** button in the page header (`course-slides-slot`, wired
  by `docs/assets/js/course-slides.js`, pointing at
  `docs/courses/lab5.pdf`) so students can open the full lecture in-page
  without leaving the lab.
- Part 1 — the actual lab content — reproduces `Lab 5.pdf`'s connection
  table verbatim (principle → connection to the Hackenbeck et al. paper)
  and cites the article (title, authors, DOI, ScienceDirect URL) with a
  short summary of its LPD use case and methodology. This is genuinely new
  material, not in the slides, so it is not condensed.
- The quiz reproduces `Lab 5.pdf`'s 10 questions **verbatim** — same
  wording, same A–D option order — with `data-correct` values matching the
  answer key exactly (1-a, 2-c, 3-b, 4-c, 5-a, 6-c, 7-a, 8-b, 9-a, 10-c).
  It reuses Lab 1's `initQuiz()`/`recordQuizAttempt()` scoring pattern,
  scoped to `#design-quiz` instead of `#intro-quiz`.

## Where it's wired in

- `docs/index.html` — new 5th lab card, `href="./lab5/"`, tags
  `Design Principles` / `Safety-Critical` (reusing the existing `.tag.intro`
  and `.tag.sdlc` CSS classes — no new styling needed).
- `.agents/lab-map.md` — Lab 5 column added to the Active labs table.
- `project_docs/labs/portfolio-map.md` — Lab 5 row added; also corrected the
  stale claim that Lab 1 was a disabled/empty card (it was filled in and
  activated in an earlier session — see the changelog's "Lab 1: created"
  entry — but this map had never been updated to reflect that).

## Validation performed

Reviewed the rendered Markdown/HTML by inspection (structure, table
rendering, quiz markup) against the working Lab 1 implementation this was
modeled on. **Not** run through Jekyll or opened in a browser this session —
no local build/serve step was performed, so visual rendering and the
scroll-spy/TOC/quiz JS were verified by code review, not by execution.
