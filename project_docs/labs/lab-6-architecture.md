# Lab 6 — Software Architecture

**Published:** `https://alexp25.github.io/scade-labs/lab6/` (`docs/lab6/index.html` + `docs/lab6/lab.md`)
**Source:** none (`docs/lab6/` only — a short recap + two hands-on auto-graded diagram exercises + quiz, no `src/lab6/`)

## Purpose

Give students a short recap of the Lesson 6 lecture on software
architecture (already delivered separately, not re-taught here), then have
them place the Cruise Control system they already built in Lab 4 into a
whole-vehicle, SysML-style system view — treating it as a single known
component rather than re-deriving its internals — and extend that view
with an Automatic Emergency Braking feature. Both diagrams are
drag-and-connect canvases that grade themselves.

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
example) instead of reproducing the slides' tables and diagrams — per
explicit feedback, the lab's job is to apply the lecture, not repeat it.

Unlike Lab 5 (which had an instructor-supplied `Lab 5.pdf` quiz + answer
key), **no instructor quiz file was supplied for Lab 6.** The 10-question
quiz in `docs/lab6/lab.md` is self-authored from this lab's own content —
stated here explicitly so it is never mistaken for a transcribed
instructor answer key.

## Prerequisites (quoted, `docs/lab6/lab.md`)

Recommended: the Lesson 6 lecture/slides themselves (this lab assumes
they've already been covered) and [Lab 4](../lab4/) — Parts 1–2 (the
hands-on activities) require already knowing the Cruise Control system's
*interface* (what it takes in, what it outputs) from Lab 4, not its
internals. No install, no license — this lab needs no tool beyond a
browser.

## Learning outcomes (quoted)

- Recall why architecture matters, how it differs from design, and its
  four elements (components, connectors, interfaces, constraints)
- Apply the requirements-driven architecture pattern to a system already
  known from Lab 4
- Place a known component (the Cruise Control system) correctly inside a
  whole-vehicle, SysML-style system view
- Extend that system view with an Automatic Emergency Braking feature,
  including proposed requirements and a description of how it would be
  simulated

## Repository files

| File | Role |
|---|---|
| `docs/lab6/lab.md` | Published lesson — Context, Learning Objectives, a condensed "Recap" section (~7 bullets, not a slide reproduction, no diagrams), then **Part 1** (whole-vehicle, SysML-style system view — Activity 1A) and **Part 2** (Emergency Braking extension of Part 1's diagram — Activities 2A–2D), Summary, 10-question quiz. Both diagram activities (1A, 2D) are a ```` ```flowgraph ```` fenced JSON block (node list + `x`/`y` layout + an `expected` edge list), not a picture — see below. |
| `docs/lab6/index.html` | Page shell — same `fetch('lab.md')` + `marked.js` + TOC/scroll-spy pattern as every other lab's `index.html`, plus **Drawflow** (jsdelivr `drawflow@0.0.60`, CSS + JS) — a dependency-light vanilla-JS node/connector editor, chosen deliberately over React Flow: React Flow has no plain `<script>`/CDN build and this repo has no bundler anywhere (`.agents/architecture.md`), so using it would mean loading React + ReactDOM + `@xyflow/react` from an ESM CDN at runtime — a real architectural outlier versus every other page in this repo. Every ```` ```flowgraph ```` fence becomes a **live, auto-graded canvas** (`buildFlowEditors()`/`buildFlowEditorWidget()`): the fence's JSON `nodes` are placed on a `Drawflow` instance at their given `x`/`y`, unconnected; a **✓ Check** button compares the student's drawn connections (read via `editor.export()`, matched back to each node's semantic `key` — not Drawflow's own numeric ids — see "Auto-grading" below) against the fence's `expected` edge list and reports found/missing/unexpected; a **↺ Reset** button clears the canvas back to the unconnected starting layout, including zoom/pan. Each canvas also has **zoom controls** (`editor.zoom_in()`/`zoom_out()`/`zoom_reset()`, Drawflow's own built-in API — range 0.5×–1.6×, 0.1 steps — with a `%` label that resets on click) and a **custom minimap** in the canvas's bottom-right corner (Drawflow has no built-in one — see "Zoom and minimap" below for exactly how it's computed and kept in sync), draggable to pan the main view. Layout + connections persist per-diagram in `localStorage` (`lab6-flow-<index>`), client-side only — nothing is uploaded or reported to an instructor automatically. |

No `src/lab6/` — this lab produces a diagram deliverable (self-graded),
not code, same general shape as Lab 3's paper-only Parts 1/8 and all of
Lab 5, except the diagrams here are actually machine-checked.

## Scope and structure — one system-level part, extended, not an internals breakdown

This lab went through several revisions before landing on its current
two-part shape (see `project_docs/changelog.md` for the full sequence).
An earlier revision had a **Part 1** that broke the Cruise Control
system down into its internal components (Cruise Control Controller,
Regulator, two Limiter instances) and asked students to wire those up
directly. Per explicit feedback that this was "too confusing" (why are
the Controller and Regulator separate? why two Limiters?), **that part
was removed entirely**, not fixed — the internal breakdown is Lab 4's
job, already done there; this lab does not repeat it.

What remains is two parts, both operating at the *system* level, never
below the Cruise Control system's already-known Lab 4 interface:

- **Part 1** (was "Part 2" in the previous revision) — a whole-vehicle,
  SysML-style view where the Cruise Control system is a single "ECU" box.
  This is now the lab's *first* hands-on activity, not its second — the
  lab opens by leaning on what students already know (the ECU's
  interface) rather than asking them to reconstruct anything new about
  it.
- **Part 2** (was "Part 3") — extends Part 1's diagram, not a
  component-level one, with the Emergency Braking Controller and
  Obstacle/Distance Sensor. Since there's no internal-CC diagram left to
  extend, the two new components join the system the same way everything
  else in Part 1 already does: as participants on the shared signal bus,
  not through some new kind of special connector. The Emergency Braking
  Controller's `brake_override` overriding the ECU's `throttle` is
  described in prose (Activity 2A) as arbitration happening at the
  Powertrain Actuator, where both commands are actually consumed — not as
  a dedicated override wire in the diagram.

Every diagram activity now also opens with an **explicit bullet list of
every connection that should exist**, worded as a plain description of
data flow ("Driver → HMI — the driver presses buttons and pedals..."),
before the canvas itself. This was a second, separate piece of feedback:
students should only have to *transcribe* a described interaction into
connections, not reverse-engineer the wiring from an interface table
alone.

## Auto-grading — how it actually works

Each `flowgraph` fence's JSON has an `expected` array of `[fromKey, toKey]`
pairs, written in terms of the same short node keys as its `nodes` array
(e.g. `"ECU"`, `"Bus"`) — not Drawflow's own auto-incrementing numeric node
ids, which are an implementation detail of the editor, not something
authored in `lab.md`. At grading time, `buildFlowEditorWidget()`:

1. Calls `editor.export()` and, for every node in the result, reads back
   the `key` string that was stashed in Drawflow's own per-node `data`
   field at creation time (`editor.addNode(..., { key: n.key }, ...)`) —
   this is what makes grading independent of node-creation order, and
   correct after a save/reload round-trip (`editor.import()`), not just on
   a fresh page load.
2. Walks every node's `outputs[...].connections` list (Drawflow's own
   export shape — each entry's `node` field is the *target* node's id) and
   turns each `(sourceId, targetId)` pair into a `"sourceKey→targetKey"`
   string via the map from step 1.
3. Diffs that set against `expected` and reports counts plus the specific
   missing/unexpected pairs by name.

Port index is deliberately ignored — grading only checks "does a
connection exist from node A to node B," matching how the diagrams were
described in prose in each activity (arrows between components, not
labeled per-pin routing).

## Zoom and minimap

Drawflow ships zoom (`zoom_in()`/`zoom_out()`/`zoom_reset()`, backed by a
`zoom` property clamped to its own default `[0.5, 1.6]` range in `0.1`
steps) but **no minimap/overview widget** — confirmed against Drawflow
0.0.60's own source before building one. `buildFlowEditorWidget()`'s
minimap is custom, and kept in sync purely by re-deriving it from
Drawflow's own state on every relevant event (`zoom`, `translate`,
`nodeMoved`, `connectionCreated`, `connectionRemoved` — no separate
tracked copy of the layout):

- **Node dots:** for every node, `redrawMinimap()` reads its live
  `pos_x`/`pos_y` from `editor.export()` (so a dragged node's dot moves
  too, not just the static config positions), assumes a fixed on-screen
  footprint (`NODE_W`/`NODE_H` = 190×60px — Drawflow's export doesn't
  report rendered size), and scales the whole bounding box (+24px pad) to
  fit the 150×110px minimap box.
- **Viewport rectangle:** computed from Drawflow's own pan/zoom state.
  Drawflow applies `precanvas.style.transform = "translate(canvas_x px,
  canvas_y px) scale(zoom)"` (verified verbatim against the 0.0.60 tag's
  `zoom_refresh()`), which means a point in "diagram space" `(pos_x,
  pos_y)` lands on screen at `(pos_x·zoom + canvas_x, pos_y·zoom +
  canvas_y)`. Inverting that gives the diagram-space rectangle currently
  visible inside the canvas element, which gets the same scale/offset
  mapping as the node dots.
- **Click-and-drag-to-pan, continuously, not just on click:** Pointer
  Events (`pointerdown`/`pointermove`/`pointerup`/`pointercancel`, not
  `click` — unifies mouse/touch/pen and supports pointer capture) on the
  minimap invert the same mapping to get a diagram-space point at the
  cursor, then set `editor.canvas_x`/`canvas_y` so that point centers in
  the viewport and re-apply the same transform string Drawflow itself
  uses. `pointerdown` pans immediately (so a plain click/tap still jumps
  there); `pointermove` while a button/finger is down (`ev.buttons !== 0`)
  keeps re-panning in real time as the pointer moves, batched through a
  single `requestAnimationFrame` callback (`schedulePan()`/`flushPan()`)
  so a fast stream of move events can't queue more redraws than the
  browser can actually paint — the viewport rectangle and node dots follow
  the cursor smoothly instead of jumping once per click. Drawflow has no
  public "pan to" method — this directly mirrors `zoom_refresh()`'s own
  two lines rather than guessing at an undocumented one, and is scoped to
  the exact pinned version (`drawflow@0.0.60`) this was verified against.
  `minimap.setPointerCapture()` on `pointerdown` keeps receiving move
  events even if the cursor briefly leaves the small minimap box mid-drag.
- Zoom/pan are **not** part of what's persisted to `localStorage` — only
  `editor.export()`'s node/connection data is saved, so a reloaded page
  always starts back at 100%/centered regardless of where a student had
  panned to; the diagram content itself (positions + connections) still
  survives the reload.

## Student workflow

1. Have already seen the Lesson 6 lecture; read the Recap (~1 minute) as a
   reminder, not new material.
2. **Part 1** (Activity 1A): read the bullet-list description of how
   signals flow through the whole vehicle system (Driver → HMI → bus →
   ECU → actuator → vehicle → sensor, closing the loop; HMI status back to
   Driver), then draw the 9-box, 11-connection canvas — Driver/HMI, three
   sensors, the signal bus, the Cruise Control ECU (the Lab 4 system,
   treated as one box — its internals are *not* re-derived here), the
   throttle actuator, and the vehicle. Self-graded (exact match against
   the fence's `expected` list). Explicitly caveated in `lab.md` as a
   Drawflow stand-in for a real SysML tool export (this repo has no SysML
   tooling).
3. **Part 2** (Activities 2A–2D): propose an Emergency Braking Controller +
   Obstacle/Distance Sensor extension — new component/interface table, an
   arbitration description (both new components join the system as bus
   participants, exactly like the existing ones — no special override
   wire), two proposed EARS requirements (REQ-09/REQ-10, explicitly marked
   "proposed — not implemented"), a prose description of how it would
   extend Lab 4's `evaluate_cc_full_report.py` scenario-CSV approach, and
   (Activity 2D) an 11-box, 14-connection canvas that re-draws Part 1's 11
   connections plus 3 new ones (`Obstacle→Bus`, `Bus→Emergency`,
   `Emergency→Bus`), also self-graded. **No file under `src/lab4/` is
   created or modified by this activity or by this lab.**
4. Take the 10-question quiz (`#architecture-quiz`, self-authored, same
   `initQuiz()` scoring pattern as every other lab's quiz).

## Requirements

Lab 6 does not modify the existing REQ-01–REQ-08 set (`src/lab3/solution/
requirements.md`). Part 2 proposes REQ-09/REQ-10 for Automatic Emergency
Braking, explicitly and repeatedly marked as **proposed, paper-only, not
implemented in `CC_design.swan`, not added to `requirements.md`, and not
checked by any script** — adding them for real would need a separate
maintainer/instructor decision plus a live Scade One session, the same
boundary Lab 4's Activity 7A already draws around its own incomplete
traceability links.

## Test/validation procedure and expected results

- **Quiz:** `#architecture-quiz`, 10 questions, client-side scored, same
  `initQuiz()` widget as every other lab.
- **Parts 1–2 diagrams:** self-graded client-side (see "Auto-grading"
  above) — this is genuinely automated, unlike every other lab's written
  deliverables. Per follow-up feedback ("the diagrams should be counted
  just like quiz answers... and tracked to the user progress"), each
  **✓ Check** click now also calls `window.recordQuizAttempt('lab6',
  'diagram-1' | 'diagram-2', correctCount, expectedPairs.length)` — the
  exact same function and Firestore `quizAttempts` collection the
  `#architecture-quiz` uses (`docs/assets/js/auth-header.js`), so a
  signed-in student's diagram scores show up in `/account/` and
  `/admin/` next to their quiz scores. It's a no-op (same as the quiz) if
  nobody is signed in. `lab.md`'s instructions were updated to say this
  plainly instead of claiming nothing is ever uploaded — see
  `project_docs/changelog.md` for the earlier (now superseded) version of
  this decision.
- **Part 2's written tables:** free-form content, no automated check —
  instructor review, same grading model as Lab 3's requirements text and
  Lab 5's whole lesson.
- **Drawflow loading:** depends on the `drawflow.min.js`/`.css` CDN
  actually loading in the browser; if the script fails to load, each
  canvas widget still builds its toolbar/container but shows an inline
  "diagram tool failed to load" message instead of a canvas, rather than
  crashing the page (`buildFlowEditorWidget()` checks `window.Drawflow`
  before instantiating).
- **JSON validity:** both `flowgraph` fences were parsed and cross-checked
  this session (`node -e` script: every `expected` pair's node keys
  resolve to a real node in that block's `nodes` array) — 2 blocks, 9/11
  nodes and 11/14 expected edges respectively, all valid.

## Known limitations

- Quiz is self-authored, not instructor-supplied — see "Source material"
  above.
- Not opened in a real browser this session — the canvas's actual runtime
  behavior (Drawflow CDN load, drag-to-connect, the Check/Reset button
  wiring, `localStorage` round-trip via `editor.import()`/`export()`) was
  code-reviewed and JSON/syntax-validated, not visually confirmed. See
  `.agents/testing.md` for exactly what *was* run (`jekyll build`, inline
  `<script>` syntax check, `flowgraph` JSON validation).
- Drawflow is a new runtime dependency for this one lab page only; no
  other `docs/lab*/index.html` loads it.
- Diagram state is stored in the browser's own `localStorage`, keyed by
  diagram position in the page (`lab6-flow-0`, `lab6-flow-1`) — if a
  future edit reorders or adds/removes a ```` ```flowgraph ```` fence in
  `lab.md`, the index-based keys shift and a returning student's saved
  layout could load into the wrong canvas (or not be found at all). Not
  an issue as long as diagram order/count in `lab.md` stays stable; flag
  this if `lab.md`'s diagrams are ever reordered — which, notably, is
  exactly what happened during this session's restructuring, so any
  student who had saved progress under the old Part 1/2/3 numbering lost
  it (acceptable: this lab "not yet exercised by a real student" per
  `.agents/lab-map.md`, so no real student data was actually affected).
- No server-side/account-based save of the diagram *layout itself* — a
  student switching browsers or clearing site data loses their
  in-progress connections/positions, even though their *scores* are now
  tracked (see above). This is the same split the rest of the site
  already has for the quiz: `#architecture-quiz`'s selected radio buttons
  aren't saved either, only the resulting score is — `labOpens`/
  `quizAttempts` in Firestore were always "activity log," never "resume
  where you left off" (`.agents/architecture.md`'s Firebase section).
- The minimap assumes a fixed 190×60px node footprint (`NODE_W`/`NODE_H`
  in `buildFlowEditorWidget()`) since Drawflow's export doesn't report
  actual rendered node size — if a node's real width/height differs a lot
  (e.g. a very long label wraps to several lines), its minimap dot won't
  be pixel-accurate, though its *position* still will be.
- Zoom and pan are session-only (not saved to `localStorage`, unlike the
  diagram content) and directly poke two Drawflow instance properties
  (`canvas_x`/`canvas_y`) plus reapply its own transform string to
  implement pan, since Drawflow has no public "pan to" API — this was
  verified against the exact pinned version (`drawflow@0.0.60`)'s own
  source, not guessed, but it is coupled to that version's internals and
  would need re-checking before ever bumping the CDN version.
- The auto-grader checks node-to-node connectivity only, not port index,
  edge direction subtleties beyond source→target, or node position — a
  student who wires the right pairs but leaves boxes in odd positions (or
  uses a different output/input port than a "natural" layout would
  suggest) still passes.

## Publishing route

`/lab6/` — see `project_docs/architecture/scade-projects.md` for the
Cruise Control architecture facts Part 1's "ECU" box is built on, and
`.agents/publishing.md` → "Adding a new lab" for the registration
procedure this lab followed.
