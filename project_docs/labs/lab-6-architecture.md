# Lab 6 — Software Architecture

**Published:** `https://alexp25.github.io/scade-labs/lab6/` (`docs/lab6/index.html` + `docs/lab6/lab.md`)
**Source:** none (`docs/lab6/` only — a short recap + three hands-on written/diagram exercises + quiz, no `src/lab6/`)

## Purpose

Give students a short recap of the Lesson 6 lecture on software
architecture (already delivered separately, not re-taught here), then have
them apply it directly to the repo's own Cruise Control system (Lab 4):
document its existing architecture (which was never written down before
Lab 4's design work began), sketch a whole-vehicle SysML-style view around
it, and extend it with an Automatic Emergency Braking feature.

## Source material

Built from one instructor-supplied file (not committed to the repo):
`Slides 6 with notes.pdf` — lecture on From Requirements to System
Structure, Why Architecture, What Is Architecture (ISO/IEC/IEEE 42010),
Architecture vs Design, Main Elements of Embedded Architecture, Quality
Attributes Drive Architecture, Requirements-Driven Architecture, Mapping
Requirements to Architecture, and a worked medical-monitoring-system
example.

**Deliberately not reproduced in full.** The lecture already covers this
material — `docs/lab6/lab.md`'s "Recap" section condenses it to ~7 short
bullets (why architecture matters, the 42010 definition, architecture vs
design, the four elements, quality attributes, requirements-driven
architecture, and a one-paragraph pointer to the medical-monitoring
example) instead of reproducing the slides' tables and diagrams. This was
a deliberate revision (see `project_docs/changelog.md`) after an initial
version repeated the lecture content near-verbatim across 9 parts — per
explicit feedback, the lab's job is to apply the lecture, not repeat it.

Unlike Lab 5 (which had an instructor-supplied `Lab 5.pdf` quiz + answer
key), **no instructor quiz file was supplied for Lab 6.** The 10-question
quiz in `docs/lab6/lab.md` is self-authored from this lab's own content —
stated here explicitly so it is never mistaken for a transcribed
instructor answer key.

## Prerequisites (quoted, `docs/lab6/lab.md`)

Recommended: the Lesson 6 lecture/slides themselves (this lab assumes
they've already been covered) and [Lab 4](../lab4/) — Parts 1–3 (the
hands-on activities) require knowing Lab 4's requirement set and Scade One
model. No install, no license — this lab needs no tool.

## Learning outcomes (quoted)

- Recall why architecture matters, how it differs from design, and its
  four elements (components, connectors, interfaces, constraints)
- Apply the requirements-driven architecture pattern to a system already
  known from Lab 4
- Produce a component/interface/constraint description of the Cruise
  Control system, plus a whole-vehicle SysML-style diagram
- Extend that architecture with an Automatic Emergency Braking feature,
  including proposed requirements and a description of how it would be
  simulated

## Repository files

| File | Role |
|---|---|
| `docs/lab6/lab.md` | Published lesson — Context, Learning Objectives, a condensed "Recap" section (~7 bullets, not a slide reproduction), then **Part 1** (Cruise Control architecture — Activities 1A–1D), **Part 2** (whole-system SysML-style view — Activity 2A), **Part 3** (Emergency Braking extension — Activities 3A–3D), Summary, 10-question quiz |
| `docs/lab6/index.html` | Page shell — same `fetch('lab.md')` + `marked.js` + TOC/scroll-spy pattern as Lab 5's `index.html`, plus Mermaid.js (cdnjs `mermaid@10.9.1`) — **the first lab page in this repo to load Mermaid**. Every ```` ```mermaid-edit ```` fence (the three Part 1–3 exercise diagrams — there are no plain ```` ```mermaid ```` fences in this lab; the Recap intentionally has no diagrams) becomes a **live editor widget** (`buildDiagramEditors()`/`buildDiagramEditorWidget()`): a textarea with the (intentionally incomplete, `%% TODO`-marked) diagram source, a Render/Reset toolbar, and a preview pane re-rendered via `mermaid.render()` (debounced on input, or Ctrl+Enter). Edits persist per-diagram in `localStorage` (`lab6-diagram-<index>`), client-side only, nothing uploaded or graded automatically. |

No `src/lab6/` — this lab produces a written/diagram deliverable
(instructor-graded), not code, same class of deliverable as Lab 3's
paper-only Parts 1/8 and all of Lab 5.

## Student workflow

1. Have already seen the Lesson 6 lecture; read the Recap (~1 minute) as a
   reminder, not new material.
2. **Part 1** (Activities 1A–1D): write a component table, an interface
   table, and a constraints list for the real Lab 4 Cruise Control system,
   using facts already documented in
   `project_docs/architecture/scade-projects.md`, then **build the
   component diagram by editing it directly in the page** — Activity 1D
   ships as an intentionally incomplete Mermaid diagram (five component
   boxes, `%% TODO` comments instead of arrows) inside the live diagram
   editor; the student fills in the wiring using the interface/constraints
   tables above it. Instructor-graded, no fixed answer key beyond "matches
   the model's actual nodes/signatures."
3. **Part 2** (Activity 2A): same pattern, one level up — an incomplete
   whole-vehicle, SysML-*style* block diagram (Driver/HMI, three sensors,
   the Part 1 box as one collapsed component, actuator, vehicle dynamics)
   with the connecting arrows left as `%% TODO`s for the student to add in
   the editor — explicitly caveated in `lab.md` as a Mermaid stand-in, not
   a real SysML tool export (this repo has no SysML tooling).
4. **Part 3** (Activities 3A–3D): propose an Emergency Braking Controller +
   Obstacle/Distance Sensor extension — new component/interface table, two
   proposed EARS requirements (REQ-09/REQ-10, explicitly marked
   "proposed — not implemented"), a prose description of how it would
   extend Lab 4's `evaluate_cc_full_report.py` scenario-CSV approach, and
   (Activity 3D) wiring the two new components into a copy of the Part 1
   diagram, again directly in the editor. **No file under `src/lab4/` is
   created or modified by this activity or by this lab.**
5. Take the 10-question quiz (`#architecture-quiz`, self-authored, same
   `initQuiz()` scoring pattern as every other lab's quiz).

## Requirements

Lab 6 does not modify the existing REQ-01–REQ-08 set (`src/lab3/solution/
requirements.md`). Part 3 proposes REQ-09/REQ-10 for Automatic Emergency
Braking, explicitly and repeatedly marked as **proposed, paper-only, not
implemented in `CC_design.swan`, not added to `requirements.md`, and not
checked by any script** — adding them for real would need a separate
maintainer/instructor decision plus a live Scade One session, the same
boundary Lab 4's Activity 7A already draws around its own incomplete
traceability links.

## Test/validation procedure and expected results

- **Quiz:** `#architecture-quiz`, 10 questions, client-side scored, same
  `initQuiz()` widget as every other lab.
- **Parts 1–3 deliverables:** free-form written/diagram content, no
  automated check — instructor review, same grading model as Lab 3's
  requirements text and Lab 5's whole lesson.
- **Mermaid rendering:** depends on the `mermaid.min.js` CDN script
  actually loading in the browser; if it fails (offline, CDN blocked), the
  diagram-editor widgets still build (they only need the DOM, not
  Mermaid), but the "Render" step shows an inline error message instead of
  a diagram rather than crashing the page.

## Known limitations

- Quiz is self-authored, not instructor-supplied — see "Source material"
  above.
- Not opened in a real browser this session — the diagram editor's actual
  rendering (Mermaid CDN load, `mermaid.render()` on user input, error
  display on invalid syntax) was code-reviewed, not visually confirmed. See
  `.agents/testing.md` for exactly what *was* run (`jekyll build`).
- Mermaid is a new runtime dependency for this one lab page only; no other
  `docs/lab*/index.html` loads it.
- Diagram edits are stored in the browser's own `localStorage`, keyed by
  diagram position in the page (`lab6-diagram-0`, `lab6-diagram-1`,
  `lab6-diagram-2`) — if a future edit reorders or adds/removes a
  ```` ```mermaid-edit ```` fence in `lab.md`, the index-based keys shift
  and a returning student's saved draft could load into the wrong diagram
  slot (or not be found at all). Not an issue as long as diagram
  order/count in `lab.md` stays stable; flag this if `lab.md`'s diagrams
  are ever reordered.
- No server-side/account-based save — a student switching browsers or
  clearing site data loses in-progress diagram edits. Consistent with the
  rest of the site's "login only tracks quiz scores/opens, never lab work
  product" model (`.agents/architecture.md`'s Firebase section).

## Publishing route

`/lab6/` — see `project_docs/architecture/scade-projects.md` for the
Cruise Control architecture facts Part 1 is built on, and
`.agents/publishing.md` → "Adding a new lab" for the registration
procedure this lab followed.
