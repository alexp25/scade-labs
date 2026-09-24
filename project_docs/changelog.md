# Changelog

Progress-tracking log of substantive changes to the lab content and its
maintainer documentation. One entry per work session. Newest first.

---

## 2026-09-24 — Lab 6: diagram checks now tracked to user progress, same as quiz answers

### Summary for reporting

Follow-up request: "the diagrams should be counted just like quiz answers
(how many connections they got right) and tracked to the user progress."
This directly reverses an earlier deliberate decision from this same
session (see the "Drawflow revision" entry below) that kept diagram
checks *out* of the site's Firebase tracking, on the reasoning that
`lab.md` told students nothing was uploaded automatically. That reasoning
no longer holds — the user explicitly wants this tracked — so both the
code and the student-facing claim were changed together, not just one of
them.

Every diagram canvas's **✓ Check** button now calls
`window.recordQuizAttempt('lab6', 'diagram-1' | 'diagram-2', correctCount,
expectedPairs.length)` inside `buildFlowEditorWidget()`'s `check()`
function — the exact same function, call shape, and Firestore
`quizAttempts` collection the `#architecture-quiz` already uses
(`docs/assets/js/auth-header.js`), reusing existing site infrastructure
rather than inventing a parallel tracking mechanism. Like the quiz, it's
a no-op when nobody is signed in (`recordQuizAttempt` returns early if
`!currentUser`). Recorded on **every** Check click, not just a final
passing one, mirroring how a student can click "Check Answers"/"Try
Again" on the quiz repeatedly — this gives whoever reviews `/admin/` a
progression over time, not just a single snapshot. `diagramIndex` is now
threaded through from `buildFlowEditors()`'s loop into
`buildFlowEditorWidget()` to build the `diagram-<N>` id (1-based, matching
which `flowgraph` fence a student is looking at).

Rewrote `docs/lab6/lab.md`'s diagram-instructions callout, which
previously promised "nothing is uploaded to an account or reported to
your instructor automatically" — now explicitly says Check records a
score to the student's account when signed in, same as a quiz, while the
diagram's actual layout/connections (for resuming later) still stay
`localStorage`-only either way. Updated
`project_docs/labs/lab-6-architecture.md` (Test/validation procedure,
Known limitations), `.agents/workflows.md`, and `.agents/architecture.md`
(Firebase `quizAttempts` collection description) to match — all of them
previously stated the diagram-check-is-untracked decision explicitly and
needed to be flipped, not just left stale.

### Files touched

```
docs/lab6/index.html                          (buildFlowEditors()/buildFlowEditorWidget() thread diagramIndex through; check() calls window.recordQuizAttempt())
docs/lab6/lab.md                              (diagram-instructions callout no longer claims nothing is uploaded)
project_docs/labs/lab-6-architecture.md       (Test/validation procedure and Known limitations sections corrected)
.agents/workflows.md                          (Lab 6 workflow step 6 corrected)
.agents/architecture.md                       (Firebase quizAttempts collection description mentions Lab 6 diagram checks)
project_docs/changelog.md                     (this entry)
```

### Validation performed

- Extracted both inline `<script>` blocks from `docs/lab6/index.html` and
  syntax-checked them with `new Function(...)` — both parse.
- Re-ran the Node script validating both `flowgraph` JSON blocks in
  `lab.md` — still 2 blocks, 9/11 nodes, 11/14 expected edges, unaffected
  (this change touched grading/reporting code, not the diagram configs).
- `bundle exec jekyll build --destination <tmp>` — succeeded, same
  pre-existing Sass warnings only.
- Read `docs/assets/js/auth-header.js`'s actual `recordQuizAttempt`
  implementation before calling it, to confirm the exact signature
  (`labId, quizId, score, total`), the Firestore collection/field names
  (`quizAttempts`, `userId`/`labId`/`quizId`/`score`/`total`/
  `submittedAt`), and that it already no-ops safely when signed out —
  not assumed from the existing `#architecture-quiz` call site alone.
- **Not verified:** actually clicking Check while signed in and confirming
  a new `quizAttempts` document appears, or that it renders correctly in
  `/account/`/`/admin/` — no live Firebase session in this environment.

---

## 2026-09-24 — Lab 6: removed the internal-component part entirely, restructured to two system-level parts

### Summary for reporting

Follow-up feedback, three points at once: (1) remove Part 1 (the Cruise
Control Controller/Regulator/Limiter internal breakdown) — "it's too
confusing"; (2) start the lab with the former Part 2 (whole-vehicle
system view) instead, "considering the background of the system"; (3)
describe each diagram's expected connections as a bullet list, not prose,
so it's unambiguous which connections the student should make.

This is a bigger structural change than the previous session's content
tweak (adding a prose walkthrough to the now-removed Part 1) — that
walkthrough was a genuine attempt to fix the confusion by explaining
*why* the Controller/Regulator/Limiter split exists; this feedback says
the split shouldn't be a separate diagram exercise for students at all,
since Lab 4 already builds and explains it. Rather than iterate on
explaining it better, removed it.

**Removed entirely:** the former Part 1 (Activities 1A–1D: component
table, interface table, constraints list, and a 5-node/6-edge diagram of
Cruise Control Controller/Regulator/2×Limiter/Driver) and its Reflection.

**Renumbered:** the former Part 2 (whole-vehicle SysML-style view) is now
**Part 1** — the lab's first and only entry point into hands-on work,
opening directly with the system view instead of an internal breakdown.
The former Part 3 (Emergency Braking extension) is now **Part 2**, with
its activities renumbered 3A–3D → 2A–2D.

**Part 2's diagram had to be redesigned, not just renumbered:** it
previously extended the (now-removed) internal-component diagram, with
the Emergency Braking Controller's override wired as `Emergency → CC`
directly into the Cruise Control Controller node. With no internal
CC diagram left to extend, Part 2 now extends **Part 1's system-level
diagram** instead — the Obstacle/Distance Sensor and Emergency Braking
Controller join the system the same way every other component in Part 1
already does: as participants on the shared signal bus (`Obstacle→Bus`,
`Bus→Emergency`, `Emergency→Bus`), not through a dedicated override wire.
Activity 2A's "Connector / arbitration" prose was rewritten accordingly:
arbitration (`brake_override` taking priority over the ECU's `throttle`)
now happens at the Powertrain Actuator, where both commands are actually
consumed. Part 1: 9 nodes/11 expected edges (unchanged from the former
Part 2). Part 2: 11 nodes/14 expected edges (was 7/9).

**Every diagram activity now opens with an explicit bullet list of every
expected connection**, worded as plain data-flow statements ("Driver →
HMI — the driver presses buttons and pedals on the dashboard"), replacing
the previous flowing-paragraph descriptions ("Here's how signals actually
flow through this system: the Driver operates the HMI..."). This was
distinct feedback from the part-removal — the goal is that a student can
read the list and directly transcribe it into connections without having
to parse prose for the actual edges.

Context, Learning Objectives, the Recap's closing sentence, the Summary,
and Quiz Q7/Q8/Q10 were all rewritten to match the new two-part shape and
stop referencing the removed internal-architecture framing (e.g. Q7
previously tested the Regulator's interface; now tests the system view's
Bus-as-connector distinction). Header duration dropped from "1 hour" to
"45–60 minutes" to reflect the smaller lab.

Updated `project_docs/labs/lab-6-architecture.md` (rewritten: new "Scope
and structure" section explaining the removal and the Part 2 diagram
redesign in one place, corrected node/edge counts and activity numbering
throughout), `.agents/lab-map.md`, `.agents/workflows.md`,
`.agents/verification.md`, `.agents/scade-models.md`, and
`.agents/testing.md` (old dated log entries left as a historical record
of what was run against the *previous* 3-part structure, not rewritten to
match the new one — a new dated entry added instead) to match.

### Files touched

```
docs/lab6/lab.md                              (Part 1 removed entirely; former Part 2→Part 1, Part 3→Part 2; Part 2's diagram redesigned around the bus; bullet-list connection descriptions; Context/Objectives/Recap/Summary/Quiz rewritten)
docs/lab6/index.html                          (one stale "Parts 1-3" code comment corrected to "Parts 1-2")
docs/index.html                               (Lab 6 card description updated to two exercises)
project_docs/labs/lab-6-architecture.md       (substantially rewritten for the new structure)
.agents/lab-map.md                            (Main tech, Starter materials, Solution/reference, Test/validation mechanism, Objective, Status cells)
.agents/workflows.md                          (Lab 6 learner workflow rewritten for two parts; note on the removed part added)
.agents/verification.md                       (Lab 6 section, table row, completion criterion — Part 3→Part 2 throughout)
.agents/scade-models.md                       (Lab 6 note rewritten — no longer describes reading .swan internals)
.agents/testing.md                            (header + new dated entry; old entries kept as historical record of the prior structure)
project_docs/changelog.md                     (this entry)
```

### Validation performed

- Re-ran the Node script that extracts and validates all `flowgraph` JSON
  blocks from `lab.md` — now 2 blocks (was 3): 9/11 nodes, 11/14 expected
  edges, all `expected` pairs resolving to real node keys.
- Grepped the repo for `Part 3`/`Activity 3[A-D]` tied to Lab 6 — only
  remaining hit is `project_docs/labs/lab-6-architecture.md`'s own
  intentional "(was 'Part 3')" historical annotation.
- Extracted both inline `<script>` blocks from `docs/lab6/index.html` and
  syntax-checked them with `new Function(...)` — both parse.
- `bundle exec jekyll build --destination <tmp>` — succeeded, same
  pre-existing Sass warnings only.
- **Not verified:** actually opening the page in a browser to confirm the
  redesigned Part 2 diagram (bus-based Emergency Braking wiring) renders
  and grades correctly — code-reviewed and JSON-validated, not executed.

---

## 2026-09-24 — Lab 6: explained the architecture in words before asking students to draw it

### Summary for reporting

Follow-up question/feedback: why are the Cruise Control Controller and
Regulator separate components (aren't they conceptually overlapping)?
Why two Limiter boxes? And: the student should only have to *make the
connections* on the diagram, not derive the whole architecture from
scratch.

Answered the conceptual questions first, then fixed the actual gap they
exposed — Activity 1D asked students to wire up 6 connections using only
the interface table (Activity 1B) and constraints list (Activity 1C),
with no explanation of *why* the system is shaped the way it is. That
made the exercise implicitly require reverse-engineering control-system
design reasoning (state machine vs. control law, anti-windup clamping)
from raw signatures — never the intent; the intent was practicing
architecture *notation* (turning a described interaction into boxes and
arrows), the same skill Part 2 and Part 3 already exercise.

Added an explicit prose walkthrough to the start of Activity 1D in
`docs/lab6/lab.md`, answering both questions directly:

- **Controller vs. Regulator:** two different jobs, not overlapping — the
  Controller is a *state machine* deciding *whether* cruise control should
  be regulating right now; the Regulator is a *PI control law* deciding
  *how much* throttle to apply once it's told to. The Controller only
  consults the Regulator while active, passing `set_point`/`speed` and
  using whatever `throttle` comes back — the same single-responsibility
  split Lab 5 already taught.
- **Two Limiter boxes:** the *same* Limiter component, instantiated twice
  with different bounds and chained one after another, not two separate
  designs — first a wide `[-100,100]` clamp on the Regulator's internal
  P+I sum (anti-windup), then the actuator's real `[0,100]` range.

The activity's instructions now read "drag a connection for every
interaction described above" instead of asking the student to infer the
wiring purely from tables. Added a matching short data-flow paragraph to
Part 2's Activity 2A (Driver→HMI→bus→ECU→actuator→vehicle→sensor loop,
in one sentence) for the same reason, applied consistently — Part 3's
Activity 3D already leaned on Activity 3A's existing explanation plus
Part 1's (now-explained) flow, so it didn't need a separate rewrite.

Updated `project_docs/labs/lab-6-architecture.md`'s Student workflow
step 2 to describe the walkthrough's presence and purpose.

### Files touched

```
docs/lab6/lab.md                              (Activity 1D gets a "how these components interact" walkthrough before the connect task; Activity 2A gets a short data-flow paragraph)
project_docs/labs/lab-6-architecture.md       (Student workflow step 2 updated)
project_docs/changelog.md                     (this entry)
```

### Validation performed

- Re-ran the Node script that extracts and validates all `flowgraph` JSON
  blocks from `lab.md` — still 3 blocks, 5/9/7 nodes, 6/11/9 expected
  edges, unchanged (this was a text-only change, no diagram config
  touched).
- `bundle exec jekyll build --destination <tmp>` — succeeded, same
  pre-existing Sass warnings only.

---

## 2026-09-24 — Lab 6: made the minimap draggable for smooth, real-time panning

### Summary for reporting

Follow-up request: "I'd like the zoomed out window to be responsive
(moving the zoom area freely, smoothly, in real time)." The previous
revision's minimap only supported click-to-jump (a single `click`
listener); this replaces that with continuous drag-panning.

Replaced the minimap's `click` handler in `docs/lab6/index.html` with
Pointer Events (`pointerdown`/`pointermove`/`pointerup`/`pointercancel`):
pressing down pans immediately (so a plain click/tap still works exactly
as before), then dragging keeps re-panning in real time as the pointer
moves, as long as a button/finger is held (`ev.buttons !== 0`).
`minimap.setPointerCapture()` on press keeps the drag tracking even if the
cursor briefly leaves the small 150×110px minimap box mid-gesture — without
it, a fast drag would drop out of "dragging" the moment the pointer
crossed the minimap's edge. Movement is batched through a single
`requestAnimationFrame` callback (`schedulePan()`/`flushPan()` — keeps
only the *latest* pending point and processes it once per animation
frame) so a fast mousemove/touchmove stream can't queue more pan+redraw
cycles than the browser can actually paint, which is what "smoothly"
requires in practice, not just "responds to more than one click." Added
`touch-action: none` and `user-select: none` to the minimap so dragging
doesn't also scroll the page or select surrounding text on touch devices,
and a `grab`/`grabbing` cursor swap for visual feedback while dragging.

Updated `docs/lab6/lab.md`'s diagram-instructions callout ("click, or
click-and-drag... in real time") and
`project_docs/labs/lab-6-architecture.md`'s "Zoom and minimap" section to
describe the drag mechanism precisely instead of the earlier click-only
one.

### Files touched

```
docs/lab6/index.html                          (minimap click handler replaced with pointer-drag handling + rAF batching; CSS cursor/touch-action additions)
docs/lab6/lab.md                              (diagram-instructions callout wording)
project_docs/labs/lab-6-architecture.md       ("Zoom and minimap" section rewritten for drag panning)
project_docs/changelog.md                     (this entry)
```

### Validation performed

- Extracted both inline `<script>` blocks from `docs/lab6/index.html` and
  syntax-checked them with `new Function(...)` — both parse.
- `bundle exec jekyll build --destination <tmp>` — succeeded, same
  pre-existing Sass warnings only.
- **Not verified:** actually dragging the minimap in a live browser to
  confirm the panning feels smooth and the rAF batching behaves as
  intended under a real, fast pointermove stream — this is inherently hard
  to fully verify without a live UI session; the logic was code-reviewed
  against documented Pointer Events / requestAnimationFrame semantics.

---

## 2026-09-24 — Lab 6: added zoom controls and a minimap overview to each diagram canvas

### Summary for reporting

Follow-up request: "there should be a zoom in / out control on each
diagram, and a zoomed out window at one corner to see the whole diagram
overview." Drawflow ships zoom (`zoom_in()`/`zoom_out()`/`zoom_reset()`,
`0.5`–`1.6` range) but no minimap — confirmed by fetching Drawflow
0.0.60's own tagged source before building one, rather than assuming.

Added a zoom control group to each canvas's toolbar (`−` / `100%` /
`+`, the `%` label resets zoom on click, wired straight to Drawflow's own
API) and a custom minimap in the canvas's bottom-right corner. The minimap
is fully derived from Drawflow's own live state on every relevant event
(`zoom`, `translate`, `nodeMoved`, `connectionCreated`,
`connectionRemoved`) rather than a separately tracked copy: node dots come
from `editor.export()`'s live `pos_x`/`pos_y` (so dragging a node moves
its dot too), and the viewport rectangle is computed by inverting
Drawflow's own `precanvas.style.transform = "translate(canvas_x px,
canvas_y px) scale(zoom)"` (quoted verbatim from the pinned tag's
`zoom_refresh()` — not guessed). Clicking the minimap re-centers the main
view by writing to `editor.canvas_x`/`canvas_y` and reapplying that same
transform string, since Drawflow has no public "pan to" method; this is
explicitly scoped to the pinned `drawflow@0.0.60` and flagged as needing
re-verification if that version is ever bumped.

The diagram "↺ Reset" button now also resets zoom/pan to 100%/centered
(previously only cleared connections and repositioned nodes). Zoom/pan
state itself is intentionally **not** persisted to `localStorage` — only
the diagram content (`editor.export()`'s node/connection data) is, same as
before — so a reloaded page always starts at 100%/centered even though a
student's actual connections and node positions survive.

Updated `project_docs/labs/lab-6-architecture.md` (new "Zoom and minimap"
section explaining the exact math and its version coupling, updated
Repository-files row and two new Known-limitations bullets) and
`docs/lab6/lab.md`'s diagram-instructions callout to mention the new
controls.

### Files touched

```
docs/lab6/index.html                          (zoom buttons + minimap DOM/CSS/logic in buildFlowEditorWidget(); Reset now also resets zoom/pan)
docs/lab6/lab.md                              (diagram-instructions callout mentions zoom/minimap)
project_docs/labs/lab-6-architecture.md       (new Zoom and minimap section; Repository files row; two new Known limitations bullets)
project_docs/changelog.md                     (this entry)
```

### Validation performed

- Fetched Drawflow's `zoom_in`/`zoom_out`/`zoom_reset`/`zoom_refresh`
  method bodies and constructor zoom defaults from the **exact pinned tag**
  (`0.0.60`, not `master`) on GitHub before writing against them — confirms
  the `translate(...)scale(...)` transform string and the `canvas_x`/
  `canvas_y`/`zoom` property semantics used by the minimap math.
- Confirmed (same fetch) that Drawflow has no built-in minimap — the
  overview widget is fully custom, not a misremembered library feature.
- Extracted both inline `<script>` blocks from `docs/lab6/index.html` and
  syntax-checked them with `new Function(...)` — both parse.
- `bundle exec jekyll build --destination <tmp>` — succeeded, same
  pre-existing Sass warnings only.
- **Not verified:** actually opening the page and confirming the minimap
  redraws correctly during a live drag/zoom/pan, or that click-to-pan lands
  where expected — the math was derived and cross-checked against
  Drawflow's real source, not exercised in a browser.

---

## 2026-09-24 — Lab 6: removed Scade-simulation-only components from the diagrams

### Summary for reporting

Follow-up feedback: "they should be simplified, there should not be
components that are purely scade oriented (like the pre block), and
simulation components, just the main blocks to be connected."

Simplified `docs/lab6/lab.md`'s Part 1 diagram (Activity 1D) and its reuse
in Part 3 (Activity 3D) down to the `CC_design` package's real,
shippable nodes only:

- **Removed** the Swan `pre` operator node (the 1-cycle feedback-delay
  block from `Simulation.swan`'s closed loop) — a Scade/Swan language
  construct, not an architectural component.
- **Removed** the `car`/Vehicle Plant node and its "Simulation Harness"
  framing — per Lab 4's own component table, `Car_design`'s `car` node is
  "never a code-generation target" and `Simulation`'s nodes are "never
  shipped/deployed." Both exist only so Scade One can simulate a vehicle
  for testing; neither belongs in a diagram of the real architecture.
- **Kept**: Cruise Control Controller, Regulator, Limiter (×2 stages), and
  the Driver as an external actor.

Part 1's node/edge count dropped from 7 nodes/9 expected connections to 5
nodes/6; Part 3's dropped from 9/12 to 7/9. Since there's no vehicle-plant
node left in Part 3 for the Emergency Braking Controller's override to act
on, its `expected` edge changed from `Emergency → Car` to
`Emergency → CC` — the override now connects directly into the Cruise
Control Controller, taking priority over its own regulated throttle;
Activity 3A's "Connector / arbitration" prose was reworded to match.
Activity 1A/1B's component/interface tables were trimmed to match (no more
Vehicle Plant row), and Activity 1C's "one-cycle feedback delay" constraint
bullet was removed along with it. Quiz Q7 was reworded (it previously
tested knowledge of the now-excluded Vehicle Plant's interface; now tests
the Regulator's interface instead, keeping the same "component vs.
interface vs. connector" learning objective).

**Explicitly not touched:** Part 2's whole-vehicle SysML-style view — at
that abstraction level "Vehicle Dynamics" is the real physical vehicle,
not a Scade simulation stand-in, so it correctly stays in the diagram.

Updated `project_docs/labs/lab-6-architecture.md` (new "Scope of the
diagrams" section explaining the exclusion rule and its Emergency→CC
knock-on effect, corrected node/edge counts throughout) and
`.agents/workflows.md`'s Lab 6 Part 1/3 steps.

### Files touched

```
docs/lab6/lab.md                              (Activities 1A-1D trimmed/rewired; Activity 3A arbitration text + 3D diagram updated; quiz Q7 reworded)
project_docs/labs/lab-6-architecture.md       (new Scope-of-the-diagrams section; workflow/counts corrected)
.agents/workflows.md                          (Lab 6 Part 1/3 steps corrected)
project_docs/changelog.md                     (this entry)
```

### Validation performed

- Re-ran the Node script that extracts all `flowgraph` JSON blocks from
  `lab.md`, parses each, and cross-checks every `expected` pair's node
  keys against that block's own `nodes` array — 3 blocks, now 5/9/7 nodes
  and 6/11/9 expected edges, all valid.
- `bundle exec jekyll build --destination <tmp>` — succeeded, same
  pre-existing Sass warnings only.
- Grepped the whole repo for `Vehicle Plant`, `Simulation Harness`,
  `one-cycle`/`1-cycle` delay wording tied to Part 1's diagram — none
  remain outside this changelog's own history and
  `project_docs/architecture/scade-projects.md` (which correctly still
  documents the real Scade project's `Car_design`/`Simulation` packages —
  those weren't removed from the *codebase*, only from this lab's
  simplified diagrams).
- **Not verified:** actually opening the page in a browser to drag the new
  connection layout — same limitation as the previous entry.

---

## 2026-09-24 — Lab 6: replaced the Mermaid diagram editors with an interactive, auto-graded Drawflow canvas

### Summary for reporting

Follow-up request: "instead of mermaid, make an interactive react flow (or
similar) canvas, with auto grading (evaluate correct connections)." React
Flow itself has no plain `<script>`/CDN build — it's npm/bundler-only —
and this repo has no build step anywhere (`.agents/architecture.md`), so
using it as asked would mean loading React + ReactDOM + `@xyflow/react`
from an ESM CDN at runtime, a real architectural outlier versus every
other page in this repo. Asked the user to choose between that literal
approach, a vanilla-JS alternative (**Drawflow**), or a canvas-based
vanilla-JS alternative (LiteGraph.js); **Drawflow** was chosen, matching
this repo's existing no-build-step, CDN-`<script>` pattern (same shape as
`marked.js`/`highlight.js`).

Replaced all three `docs/lab6/lab.md` diagram exercises (Activities 1D,
2A, 3D) with ```` ```flowgraph ```` fenced JSON blocks — a `nodes` array
(key/label/x/y) and an `expected` array of `[fromKey, toKey]` pairs — in
place of the previous ```` ```mermaid-edit ```` fences with hand-typed
`%% TODO` comments. `docs/lab6/index.html` now loads Drawflow (jsdelivr
`drawflow@0.0.60`, version confirmed to exist and ship
`dist/drawflow.min.{js,css}` via the jsdelivr package-data API before
pinning it) instead of Mermaid.js, and `buildFlowEditors()`/
`buildFlowEditorWidget()` replace the old `buildDiagramEditors()`/
`buildDiagramEditorWidget()`: each canvas places the fence's nodes with
zero connections (this *is* the incomplete starting state now — no more
hand-authored `%% TODO` comments needed), lets the student drag
connections between them, and a **✓ Check** button auto-grades the result
by diffing the student's connections (resolved back to semantic node
`key`s stashed in each node's Drawflow `data` field at creation time, not
Drawflow's own numeric ids — verified against Drawflow's actual
`addConnection`/export code, fetched from its GitHub source, to get the
`outputs[...].connections[].node` field semantics right) against the
fence's `expected` list, reporting missing/unexpected pairs by name. A
**↺ Reset** button clears back to the unconnected layout. State persists
per-diagram in `localStorage` (`lab6-flow-<index>`).

**Deliberately not wired into `recordQuizAttempt`/Firestore**, even though
the mechanism would have supported it trivially (same call shape as the
quiz) — `lab.md`'s own instructions tell students nothing is uploaded
automatically, so the implementation was written to actually match that
claim rather than silently contradict it.

Rewrote `project_docs/labs/lab-6-architecture.md` (new "Auto-grading"
section explaining the grading mechanism precisely, updated file/workflow/
limitations sections) and `.agents/lab-map.md`/`.agents/workflows.md`'s
Lab 6 entries to describe Drawflow instead of Mermaid and to correct the
"instructor-graded only, no automated check" claim about the diagrams —
that was true for the Mermaid version, it is no longer true now that Check
exists.

### Files touched

```
docs/lab6/lab.md                              (three flowgraph JSON blocks replace mermaid-edit fences; instructional text updated)
docs/lab6/index.html                          (Drawflow CDN CSS+JS replaces Mermaid; buildFlowEditors()/buildFlowEditorWidget() replace the Mermaid editor code; new .flow-* CSS)
project_docs/labs/lab-6-architecture.md       (rewritten: Auto-grading section, updated file/workflow/limitations)
.agents/lab-map.md                            (Main tech, Student entry point, Solution/reference, Test/validation mechanism cells)
.agents/workflows.md                          (Lab 6 learner workflow steps 3-5, 7)
project_docs/changelog.md                     (this entry)
```

### Validation performed

- Confirmed `drawflow@0.0.60` exists and ships `dist/drawflow.min.js` +
  `dist/drawflow.min.css` via the jsdelivr package-data API before pinning
  the CDN URLs.
- Fetched Drawflow's actual `addNode`/`addConnection`/export source from
  its GitHub repo to confirm exact API shapes used in
  `buildFlowEditorWidget()` (parameter order, the `{node, output}` /
  `{node, input}` connection-object field names, `connectionCreated`/
  `connectionRemoved` event payload shape, `.import()`/`.clear()` method
  names) — not implemented from memory/assumption.
- `npx marked@9.1.6` against a sample ` ```flowgraph ` fence — confirmed it
  emits `class="language-flowgraph"`, matching the DOM selector used in
  `index.html`.
- Wrote and ran a Node script that extracts all three `flowgraph` JSON
  blocks from `docs/lab6/lab.md`, parses each as JSON, and cross-checks
  every `expected` pair's node keys against that block's own `nodes` array
  — all 3 blocks valid (7/9/9 nodes, 9/11/12 expected edges).
- Extracted both inline `<script>` blocks from `docs/lab6/index.html` and
  syntax-checked them with `new Function(...)` — both parse.
- Re-ran `bundle exec jekyll build --destination <tmp>` — succeeded, same
  pre-existing Sass deprecation warnings only; confirmed `lab6/index.html`
  + `lab6/lab.md` still built.
- **Not verified:** actually opening the page in a browser and dragging a
  connection — the runtime drag-and-connect interaction, the Check/Reset
  button behavior, and the `localStorage` round-trip via
  `editor.import()`/`export()` were code-reviewed and API-verified against
  Drawflow's real source, not executed in a live browser.

---

## 2026-09-23 — New admin-only changelog page

### Summary for reporting

Added a curated, in-site changelog viewable only by admin accounts, per
user request ("add a changelog page, like a separate lab but only viewable
to admin"). Two open questions were resolved with the user first: (1) a
static file under `docs/` cannot be truly access-controlled the way
`docs/admin/index.html` is (that page's real security boundary is
Firestore rules, not its client-side check) — the user accepted a
UI-only gate; (2) content source and granularity — the user chose a
**curated static file** (not a Firestore-backed collection, not a mirror of
this maintainer changelog) with **high-level entries only** (no validation
notes, file lists, or session narration).

Created `docs/changelog/index.html` (same `isAdmin` redirect/check pattern
as `docs/admin/index.html`, reusing `firebase-client.js`) and
`docs/changelog/changelog.md` (hand-written summary of this repo's history,
condensed from this file's existing entries). Linked from
`docs/admin/index.html` via a new "Changelog →" button in its header.

Documented the new page and its security caveat in `.agents/architecture.md`
(repo-structure tree + a new bullet under "Backend (Firebase)" explicitly
warning that `changelog.md` is fetchable by anyone who has its URL, gate or
no gate), `.agents/publishing.md` ("Duplicate/at-risk sources of truth",
noting this is a deliberate narrow exception to ADR 0001 since the content
is purpose-written for in-site display, not a copy of this maintainer
changelog), and `project_docs/architecture/firebase-backend.md` (added to
the feature list with the same caveat).

### Validation performed

- `bundle exec jekyll build --destination <tmp>` from `docs/` — succeeded,
  same pre-existing Sass deprecation warnings only; confirmed
  `changelog/index.html` and `changelog/changelog.md` present in the output
  tree. Temp output deleted, not committed.
- Not opened in a real browser — the Firebase auth redirect/`isAdmin` check
  and markdown render were code-reviewed against the working
  `docs/admin/index.html` and lab-page patterns they reuse, not executed
  against a live Firebase project.

### Not addressed / carried over as open items

- `docs/changelog/changelog.md`'s entries were hand-condensed from this
  file's existing history as of this session; it will not update itself —
  future sessions adding a changelog entry here should also add a
  short, high-level line to `docs/changelog/changelog.md` if it's worth
  surfacing to admins in-site.
- No mechanism exists to actually restrict `docs/changelog/changelog.md` at
  the file level (GitHub Pages serves static files with no access control);
  this is a known, accepted limitation, not a bug to fix later.

---

## 2026-09-23 — Lab 5: cut the full slide reproduction down to a condensed Recap

### Summary for reporting

Per explicit user feedback — "the parts that are already in the course
slides should not be repeated, only summarized eventually... the lab should
not repeat the course" — `docs/lab5/lab.md` was rewritten. The original
version (this session's earlier "Lab 5: created" entry, below) had fully
reproduced the lecture: all 8 principle sections plus the Emergency
Braking, Ariane 5, and Brake Controller worked examples from
`Slides 5 with notes.pdf`.

That was replaced with a short **Recap** section (one line per principle,
explicitly framed as "not a replacement for the slides") plus the
already-available **Course Slides** in-page viewer button
(`course-slides-slot` / `docs/assets/js/course-slides.js`, pointing at
`docs/courses/lab5.pdf`) for students who need the full explanation. The
lab's actual content — Part 1's reading, the Hackenbeck et al. (2025)
citation and LPD summary, the principle→paper connection table, and the
10-question quiz — is unchanged, since none of that exists in the slides.
This mirrors the condensed-recap pattern already established by Lab 6
(see that entry below).

Updated `project_docs/labs/lab-5-design-principles.md` to describe the
revised structure and why it changed. No changes to `docs/index.html`,
`.agents/lab-map.md`, or the quiz's questions/answer key — only `lab.md`'s
theory content was cut down.

---

## 2026-09-23 — Lab 4: full-script reference (collapsible), no in-browser execution

### Summary for reporting

Investigated running Lab 4's Python scripts in-browser the way Lab 2's live
CodeMirror+Skulpt editor does, per a user request. Both
`evaluate_cc_full_report.py` and `evaluate_cc_quick_tester.py` import the
generated `cc_wrapper` — a compiled native DLL from Scade One's code
generator — which Skulpt (a pure-Python-in-browser interpreter) cannot load;
the full-report script additionally needs a local Scade One install
(`ansys.scadeone.core`) and `matplotlib`. Confirmed with the user this makes
a live/runnable in-browser editor infeasible for these two scripts, and
that the intended fix is read-only: make the full scripts expandable rather
than always visible.

Added a "Full script reference" subsection at the end of `docs/lab4/lab.md`
Part 6, after Activity 6F: both scripts' complete source, each inside a
collapsed `<details>`/`<summary>` block (collapsed by default, expandable on
click), styled via new CSS in `docs/lab4/index.html`
(`#lab-content details`/`summary`/`details pre`, dark box matching the
site's navy/sky palette, reusing the existing `#lab-content pre code`
highlight.js pass so expanded code still gets syntax highlighting).
`evaluate_cc_quick_tester.py` was previously never shown or mentioned
anywhere in the published lesson (only in `.agents/testing.md` and
`.agents/workflows.md`) — this closes that gap. Added a one-line mention of
`evaluate_cc_quick_tester.py` to Activity 6C's project-layout tree too.

While assembling the escaped script text, found and fixed a stale
self-referential comment in both `src/lab4/starter/CruiseControl/
evaluate_cc_full_report.py` (header still said `# evaluate_cc.py`, left over
from an earlier session's rename) and `evaluate_cc_quick_tester.py`
(a comment pointing at `evaluate_cc.py` instead of the renamed
`evaluate_cc_full_report.py`) — both now say the correct current filename.

### Validation performed

- `python -m py_compile` on both edited `.py` files — no syntax errors.
- `bundle exec jekyll build --destination <tmp>` from `docs/` — succeeded,
  same pre-existing Sass deprecation warnings as prior sessions, `lab4/`
  output tree confirmed present. Temp output deleted, not committed.
- Not opened in an actual browser this session — the `<details>` rendering
  and collapse/expand behavior were not visually confirmed, only reasoned
  about from the CSS and the existing `marked.js`/`hljs` render pipeline.

Updated `.agents/lab-map.md` (Lab 4's Test/validation mechanism row) and
`project_docs/labs/lab-4-cruise-control.md` (repository-files table) to
match.

---

## 2026-09-23 — Lab 6: created and fully registered (Software Architecture)

### Summary for reporting

Added a sixth lab, following the "reading + hands-on written exercise +
quiz" shape (no `src/lab6/`). Built from one instructor-supplied file (not
committed to the repo): `Slides 6 with notes.pdf` (lecture on From
Requirements to System Structure, Why Software Architecture, the ISO/IEC/
IEEE 42010 definition, Architecture vs Design, Main Elements of Embedded
Software Architecture, Quality Attributes Drive Architecture,
Requirements-Driven Architecture, Mapping Requirements to Architecture, a
worked medical-monitoring-system example, and Benefits/Summary). Unlike
Lab 5, no instructor quiz/answer-key file was supplied for Lab 6 — the
10-question `#architecture-quiz` is self-authored from this lab's content,
stated explicitly in `docs/lab6/lab.md`'s maintainer doc so it's never
mistaken for a transcribed answer key.

Created `docs/lab6/lab.md` and `docs/lab6/index.html`. `lab.md` synthesizes
the slide content into 9 theory parts (ending with the fully worked
medical-monitoring example, reproduced from the slides) plus three
hands-on parts that anchor on the repo's own Cruise Control system (Lab 4):
Part 10 has students document the CC model's existing architecture
(components/interfaces/constraints + a component diagram) using facts
already in `project_docs/architecture/scade-projects.md`; Part 11 asks for
a whole-vehicle, SysML-*style* block diagram broadening past the embedded-
software boundary (explicitly caveated as a Mermaid stand-in, not real
SysML tool output — this repo has none); Part 12 is a paper-only Automatic
Emergency Braking extension, proposing new REQ-09/REQ-10 (explicitly marked
"proposed — not implemented in the shipped model") and describing, in
prose only, how it would extend Lab 4's scenario-CSV simulation approach.
No file under `src/lab4/` is created or modified by this lab.

Diagrams use Mermaid — **the first lab page in this repo to load
Mermaid.js** (cdnjs `mermaid@10.9.1`), since `marked.js` alone renders
fenced code blocks as plain text, not diagrams. `docs/lab6/index.html`
converts `pre code.language-mermaid` blocks into `.mermaid` divs and calls
`mermaid.run()` after `marked.parse()`, same fetch/render/TOC/quiz pattern
as every other lab's page otherwise.

Added a 6th card to `docs/index.html` (`href="./lab6/"`, reusing existing
`.tag.intro`/`.tag.sdlc` CSS — no new styling). Unlike Lab 5 (created
earlier the same day, still missing its `LAB_TITLES` entries and a
`.agents/workflows.md` section), **Lab 6's registration was completed in
full in this session**: added `lab6` to both `docs/admin/index.html` and
`docs/account/index.html`'s `LAB_TITLES` maps; updated `.agents/lab-map.md`
(new Lab 6 column, portfolio card-count line), `.agents/workflows.md` (new
"Learner: Lab 6" section, "adding a new lab" note contrasting Lab 6's full
registration against Lab 5's partial one), `.agents/architecture.md`
(repository-structure tree), `.agents/domain.md` (component/connector/
interface/constraint/SysML-style-diagram vocabulary), `.agents/
verification.md` (new Lab 6 section classifying REQ-09/REQ-10 as
proposed/paper-only, plus a classification-table row and completion
criterion), `.agents/scade-models.md` (Lab 6 reads but never modifies the
Lab 4 `.swan` files), and `.agents/testing.md` (Lab 6 entry). Added
`project_docs/labs/lab-6-architecture.md` and a new
`project_docs/labs/portfolio-map.md` row.

Lab 5's own incomplete registration (missing `LAB_TITLES` entries, no
`.agents/workflows.md` section) was **not** touched this session — left
exactly as found, per explicit instruction to scope this session's work to
Lab 6 only.

### Files touched

```
docs/lab6/lab.md                              (new)
docs/lab6/index.html                          (new)
docs/index.html                               (added Lab 6 card)
docs/admin/index.html                         (added lab6 to LAB_TITLES)
docs/account/index.html                       (added lab6 to LAB_TITLES)
project_docs/labs/lab-6-architecture.md       (new)
project_docs/labs/portfolio-map.md            (added Lab 6 row)
.agents/lab-map.md                            (added Lab 6 column)
.agents/workflows.md                          (added Lab 6 learner workflow + maintainer note)
.agents/architecture.md                       (repo-structure tree + current/legacy boundary)
.agents/domain.md                             (architecture vocabulary entry)
.agents/verification.md                       (Lab 6 section, table row, completion criterion)
.agents/scade-models.md                       (Lab 6 read-only-reference note)
.agents/testing.md                            (Lab 6 test entry)
project_docs/changelog.md                     (this entry)
```

### Validation performed

- `cd docs && bundle exec jekyll build --destination <tmp>` — succeeded,
  only pre-existing `jekyll-theme-cayman` Sass deprecation warnings; output
  tree confirmed to contain `lab6/index.html` + `lab6/lab.md`. Temp output
  deleted after inspection, not committed.
- Grepped `href="./lab` in `docs/index.html` — all six cards
  (`./lab1/` … `./lab6/`) resolve to real directories.
- Confirmed by grep that no other `docs/**` file referenced `mermaid`
  before this session — Lab 6 is genuinely the first to need it.
- Confirmed `git status` shows no changes under `src/lab4/` from this
  session's work (Parts 10/12 are read-only analysis/proposals, not model
  edits).

### Not addressed / carried over as open items

- Not opened in an actual browser — Mermaid.js's CDN-loaded diagram
  rendering was not visually confirmed, only code-reviewed against the
  working `marked.js`/`highlight.js` pattern it extends.
- Quiz is self-authored, not instructor-supplied — flagged explicitly in
  `project_docs/labs/lab-6-architecture.md` so it isn't later mistaken for
  a transcribed answer key.
- Lab 5's pre-existing incomplete registration (LAB_TITLES,
  `.agents/workflows.md`) remains unaddressed, out of scope for this
  session.

### Follow-up in this same session — made every diagram a live, editable widget

Initial delivery rendered Mermaid diagrams statically (read-only). Per
explicit follow-up feedback ("it should be interactive, the students
should edit the diagrams"), reworked `docs/lab6/index.html` so every
` ```mermaid ` fence becomes a **live editor**: a textarea holding the
diagram source, a **Render**/**Reset** toolbar, and a preview pane that
re-renders via `mermaid.render()` on click, Ctrl+Enter, or ~700ms after the
student stops typing. Edits persist per-diagram in `localStorage`
(`lab6-diagram-<index>`, keyed by the diagram's position in the page) —
client-side only, nothing uploaded, nothing auto-graded.

Also rewrote the three hands-on diagrams in `docs/lab6/lab.md` (Parts 10,
11, and a new Part 12 Activity 12D) from finished answers into
intentionally incomplete skeletons — component boxes present, connecting
arrows replaced with `%% TODO` comments pointing at the table/activity
that answers them — so editing the diagram *is* the deliverable instead of
an optional way to view a diagram that was already correct. Parts 1, 7,
and 9 (the theory/worked-example diagrams) stay complete and correct by
default but are editable too, framed as "experiment if you want, not
graded." Added a short callout right before Part 1 explaining the editor
(Render/Reset, `localStorage`-only persistence, which diagrams are
exercises vs. references).

Updated `project_docs/labs/lab-6-architecture.md` (workflow description,
new "Known limitations" entries: index-based `localStorage` keys shift if
`lab.md`'s diagram order/count ever changes; no server-side save),
`.agents/workflows.md`'s Lab 6 section, `.agents/lab-map.md`'s Lab 6 "Main
tech" cell, and the `docs/index.html` card description.

**Validation:** re-ran `bundle exec jekyll build --destination <tmp>` —
succeeded, same pre-existing Sass warnings only; confirmed `lab6/index.html`
still built. Not opened in a real browser — the editor's actual DOM
behavior (render-on-input, error display for invalid Mermaid syntax,
`localStorage` round-trip) was code-reviewed, not executed.

**Correction, same session:** the first pass made *every* diagram
(including Parts 1/7/9's worked-example reference diagrams) editable.
Follow-up feedback ("the reference diagrams should not be editable")
corrected this: `lab.md` now uses two fence languages —
` ```mermaid ` for Parts 1/7/9 (rendered once, statically, via a new
`renderStaticDiagrams()`, not editable) and ` ```mermaid-edit ` for Parts
10–12 (the exercise diagrams, via `buildDiagramEditors()`). Verified
`marked@9.1.6` actually emits `class="language-mermaid-edit"` for a
` ```mermaid-edit ` fence (`npx marked@9.1.6` against a sample fence, exact
version pinned in `docs/lab6/index.html`'s CDN script tag) before relying
on that selector in the DOM code. Re-ran the Jekyll build again after the
fix — succeeded; confirmed 3 static + 3 editable fences by grep count.
Updated `project_docs/labs/lab-6-architecture.md`, `.agents/workflows.md`,
and `.agents/lab-map.md` to describe the two-path behavior instead of the
initial "every diagram is editable" version.

### Second correction, same session — condensed the lecture recap instead of repeating the course

Follow-up feedback: "the parts that are already in the course slides
should not be repeated, only summarized eventually, to provide context for
the lab, but the lab should not repeat the course." The first two passes
had reproduced `Slides 6 with notes.pdf` in close-to-full detail across 9
parts (tables, all three static diagrams, the full medical-monitoring
worked example) before ever reaching the hands-on content.

Rewrote `docs/lab6/lab.md`: the 9 theory parts collapsed into one short
**Recap** section (~7 bullets: why architecture matters, the ISO/IEC/IEEE
42010 definition, architecture vs design, the four elements, quality
attributes, requirements-driven architecture, and a one-paragraph pointer
to the lecture's medical-monitoring example instead of reproducing its
diagram/table) — framed explicitly as "a quick reminder of the lecture,
not a replacement for it." The three hands-on parts (formerly Part
10/11/12) were renumbered to **Part 1/2/3** and are now the bulk of the
lab; their activity numbering (10A→1A, 11A→2A, 12A–12D→3A–3D) and internal
cross-references were updated to match. The quiz's Q7/Q8/Q9 references to
"Part 10/11/12" were updated to "Part 1/2/3"; question content itself was
unchanged since the underlying concepts didn't change, only their
placement in the lesson.

Since the Recap has no diagrams at all (by design — it points back at the
lecture instead of reproducing its figures), all three remaining Mermaid
diagrams in the lab are now the ` ```mermaid-edit ` exercise diagrams from
Parts 1–3. This made the "static vs. editable" distinction in
`docs/lab6/index.html` (added in the previous correction) unnecessary —
removed `renderStaticDiagrams()` and the plain-`mermaid` code path
entirely, since no plain ` ```mermaid ` fence remains in `lab.md`; the page
now only builds diagram-editor widgets.

Header duration updated from "1.5 hours" to "1 hour" to reflect the
shorter reading load. Updated `project_docs/labs/lab-6-architecture.md`
(rewritten to match, with a "deliberately not reproduced in full" note
under Source material), `.agents/workflows.md`'s Lab 6 section,
`.agents/lab-map.md` (Main tech, Starter materials, Solution/reference,
Test/validation mechanism, Status cells), `.agents/verification.md` and
`.agents/scade-models.md` (Part 12→Part 3, Activity 12B→3B, Activity
12C→3C references), and `docs/index.html`'s card description.

**Validation:** re-ran `bundle exec jekyll build --destination <tmp>` —
succeeded, same pre-existing Sass warnings only. Grepped `lab.md` and
confirmed 0 plain ` ```mermaid ` fences and 3 ` ```mermaid-edit ` fences
remain (Parts 1D, 2A, 3D). Confirmed `git status` shows no `src/lab4/`
diffs beyond the pre-existing, unrelated set from before this session's
Lab 6 work.

---

## 2026-09-23 — Lab 5: created (Software Design Principles in Safety-Critical Software Engineering)

### Summary for reporting

Added a new fifth lab, following Lab 1's "reading + quiz only" shape (no
`src/lab5/`). Built from three instructor-supplied files (not committed to
the repo): `Slides 5 with notes.pdf` (lecture on Top-Down Design, Modularity/
Information Hiding, Traceability by Design, Strong Typing & Deterministic
Design incl. the Ariane 5 failure, SOLID, DRY/KISS, and Model-Based Design),
`Article for lesson 5.pdf` (Hackenbeck et al. 2025, *Semantic Interface
Modeling for Automotive Architectures Using a Domain-Driven Approach*,
IFAC-PapersOnLine 59(25), DOI 10.1016/j.ifacol.2025.11.936), and `Lab 5.pdf`
(the connection table plus a 10-question quiz and answer key).

Created `docs/lab5/lab.md` and `docs/lab5/index.html`. `lab.md` synthesizes
the lecture into 10 theory parts plus a reading section (Part 11) that cites
the article and reproduces `Lab 5.pdf`'s principle → paper connection table
verbatim. The quiz reproduces `Lab 5.pdf`'s 10 questions verbatim (same
wording and option order) with `data-correct` values matching its answer key
exactly, reusing Lab 1's `initQuiz()` scoring pattern under `#design-quiz`.

Added a 5th card to `docs/index.html` (`href="./lab5/"`, reusing existing
`.tag.intro`/`.tag.sdlc` CSS — no new styling). Updated `.agents/lab-map.md`
(new Lab 5 column) and `project_docs/labs/portfolio-map.md` (new Lab 5 row;
also corrected a stale claim there that Lab 1 was still a disabled/empty
card — it was activated in an earlier session but the map was never
updated). Added `project_docs/labs/lab-5-design-principles.md` with full
source/validation detail.

Not run through Jekyll or opened in a browser this session — reviewed by
code inspection against the working Lab 1 implementation it was modeled on,
not by execution.

---

## 2026-08-18 — Lab 4: renamed the two `CruiseControl` Python scripts for clarity

### Summary for reporting

Renamed, content otherwise unchanged:
- `src/lab4/starter/CruiseControl/tester.py` → `evaluate_cc_quick_tester.py`
  (the live console demo, no assertions).
- `src/lab4/starter/CruiseControl/evaluate_cc.py` → `evaluate_cc_full_report.py`
  (the instructor reference implementing lab.md Part 6 Activities 6C–6F —
  scenario CSVs in, `results/*.csv` + plots out).

Updated every reference to the old filenames across `docs/lab3/lab.md`,
`docs/lab4/lab.md`, `.agents/{architecture,domain,lab-map,python,testing,
verification,workflows}.md`, and `project_docs/{architecture/scade-projects,
architecture/python-and-simulation,labs/lab-3-requirements,
labs/lab-4-cruise-control,verification/requirements-and-traceability,
verification/testing-and-simulation}.md`. Pure rename — no behavior, test
expectations, or requirement content changed. This changelog's own prior
entries were left untouched (they describe what the files were named at the
time each entry was written, per this file's standing convention).

---

## 2026-08-11 — Lab 1: created (Introduction to Software Engineering)

### Summary for reporting

The Lab 1 portfolio card had shown "Coming soon" with no content since the
portfolio existed. The instructor supplied `Slides 1 2.pdf` (a lecture on
the IEEE definition of software engineering, the SDLC, why IT projects
fail, software engineering vs. programming, characteristics of
high-quality software, safety-critical-system needs, Model-Based Design,
and an introduction to Ansys Scade One) and `Study_lab 1 2.pdf` (a
10-question multiple-choice quiz tied to an assigned external reading).
Built Lab 1 from these two sources, following the existing Lab 3/Lab 4
`index.html` + `lab.md` page pattern (static shell fetches and renders
`lab.md` via `marked.js`, client-side TOC + scroll-spy, one auto-graded
quiz reusing Lab 4's `initQuiz()`/`.quiz-q`/`data-correct` widget pattern).

Added:
- `docs/lab1/lab.md` — 7 theory parts synthesizing the slide deck, a
  pointer to the assigned external reading (Part 8, DOI-linked, not
  embedded), a summary, and the 10-question quiz reproduced verbatim from
  the PDF with correct answers baked into each question's `data-correct`.
- `docs/lab1/index.html` — page shell, copied from `docs/lab4/index.html`
  (no trace-checker widget needed — Lab 1 has no Scade One model to
  parse).

Changed:
- `docs/index.html` — Lab 1 card un-disabled, description and tags updated
  to match the new content, `Open Lab →` link added.
- `docs/admin/index.html`, `docs/account/index.html` — added `lab1` to
  both `LAB_TITLES` maps so login/progress-tracking recognizes the new lab.
- `.agents/lab-map.md`, `.agents/workflows.md`, `.agents/publishing.md` —
  updated to describe Lab 1 as active (was documented as a disabled
  "Coming soon" card with "no content exists").

Not created: `src/lab1/` — Lab 1 has no exercise, only reading + a quiz, so
there is no starter/solution code to hold (consistent with how Lab 3/Lab 4
only ship `src/` for their hands-on parts).

Validation: not run — this is a static-HTML/Markdown change with no build
step; see `.agents/testing.md` for what "validated" means in this repo.
Did not serve the site locally or open the page in a browser this session.

---

## 2026-08-10 (seventh follow-up) — Lab 3: added an in-browser Requirement Traceability Checker (Skulpt), and two Scade One Traceability-panel screenshots to Activity 2G

### Summary for reporting

Follow-up to the previous session's `--project-dir` work: the user asked
for students to be able to "upload" their files and run a tester script
right on the lab page, "just like in lab 2." Lab 2's live editor works
in-browser because it uses Skulpt (pure client-side Python) on pure-Python
logic. Lab 3's actual test depends on a **compiled native `.dll`** loaded
via `ctypes` — no browser-based Python engine (Skulpt, Pyodide/WASM, or
otherwise) can execute a native OS binary inside a browser sandbox. This is
a hard platform limit, confirmed with the user via clarifying question
before building anything, and the user chose the achievable scope: a
**traceability-only** checker, not a claim of running the real simulation.

Added to `docs/lab3/index.html`:
- **`#trace-checker-section`** — a fixed widget (same visual pattern as Lab
  2's `#editor-section`) with a file-upload input, a plain `<textarea>` to
  paste/edit `blocks.swan` text, "Load starter example" (embeds
  `src/lab3/starter/blocks.swan` — starter material, not the solution
  answer key), and a "Check Traceability" button.
- Ported `parse_operator()`/`print_requirement_report()` from
  `test_limiter_advanced.py`/`test_counter_advanced.py` into a Python
  source string (`TRACE_CHECKER_PY`) with all file I/O removed — the swan
  text is injected as a string literal via `JSON.stringify()` (a JSON
  string literal is also a valid Python string literal for the escape
  sequences involved, so this is a safe, simple embedding). Runs via
  Skulpt, same engine/CDN as Lab 2.
- The page is explicit, in both `lab.md` (new paragraph in Activity 7F) and
  the widget's own on-page copy, that this only checks `#pragma
  requirement` links — it does **not** run the actual generated model, and
  says exactly why (native `.dll`, browser sandbox).

**Verified correctness before shipping** (not just "should work"): extracted
the actual `TRACE_CHECKER_PY`/`SAMPLE_SWAN` template-literal values from the
committed HTML via a small Node script (to get the true post-escape-processing
JS string, not the raw source text), substituted `%SWAN_TEXT%` exactly as the
page's `checkTraceability()` does, and ran the resulting Python source
through real CPython 3.11 — once against `src/lab3/solution/assets/blocks.swan`
(produced identical output to the local `test_limiter_advanced.py`/
`test_counter_advanced.py` run: all 5 REQ IDs correctly resolved to their
nodes) and once against the embedded starter sample (correctly printed
`NOT TRACED` for all 5, matching the starter's pre-Activity-2G/4F state).
This caught and fixed two real bugs before they ever reached a browser: (1)
an over-escaped regex — the initial JS template literal had doubled
backslashes in several `r"..."` patterns, which would have made every regex
match against a literal backslash instead of `\s`/`\d`/`\(`, breaking the
whole parser silently; (2) a wrong capture-group index (`group(4)` on a
3-group pattern, `IndexError: no such group`). Also confirmed the HTML has
balanced `<script>` tags and that Jekyll still builds it as a clean copy
(index.html is not Markdown, so `bundle exec jekyll build` mostly proves
no build-breaking syntax was introduced, not full runtime correctness —
that's what the Node+CPython extraction round-trip was for).

Also added two real Scade One UI screenshots the user provided
(`scade_traceability_define_requirements.png`, `_1.png`) to Activity 2G,
showing the actual right-click → Traceability panel → **+** → type-an-ID
flow. Flagged explicitly in the surrounding text that the screenshots show
`REQ1_Limiter` (the old, non-canonical ID this course used before last
session's rename to `REQ-LIM-01`) — framed as reinforcing the same
`reQ2`/`REQ-02` traceability-discipline lesson from Part 9, not
contradicting the activity's instruction to type the canonical ID.

Updated `.agents/integrations.md` (Skulpt now used by 2 pages, not 1) and
`.agents/publishing.md` (Lab 3's widget list) to match.

---

## 2026-08-10 (sixth follow-up) — Lab 3: split simple/advanced Python test scripts, added `--project-dir` so students can run against their own generated project

### Summary for reporting

Two changes to `src/lab3/{starter,solution}/`'s Python test scripts:

1. **Split each script into a simple and an advanced version.** The
   previous session had grown `test_limiter.py`/`test_counter.py` to
   include the requirement-traceability report plus CSV/diagram
   generation, which made the "just run the cycles and print PASS/FAIL"
   base case (what Activities 7C/7D actually ask students to build) harder
   to follow. Now:
   - `test_limiter.py`/`test_counter.py` — back to simple: cycle the
     operator, print `[req] ... PASS/FAIL` per test case, no `blocks.swan`
     parsing.
   - `test_limiter_advanced.py`/`test_counter_advanced.py` (new files) —
     the full traceability-report + CSV + diagram version from the
     previous session, unchanged in behavior.
2. **Added `--project-dir`/`-d` to all four scripts** (default: the
   script's own folder, so plain `python test_limiter.py` behaves exactly
   as before). This lets a student generate or copy/upload their own
   `blocks.swan` + wrapper folders into any directory and run the shared
   test scripts against it — `python test_limiter.py --project-dir
   path\to\their\project` — without needing to overwrite the files
   committed in this repo. The advanced scripts' `results/` output also
   moves under `--project-dir`, so a student's own run never overwrites
   the repo's committed reference `results/`.

Verified this session: all four scripts compile and run correctly from
`src/lab3/solution/` (advanced scripts reproduce the same
`ALL PASS`/CSV/diagram output as before); all four fail at the (expected,
missing) wrapper import from `src/lab3/starter/`, with the advanced
scripts' traceability report still printing `NOT TRACED` first since that
step only reads `blocks.swan`, not the `.dll`; and `--project-dir`
confirmed working end-to-end by copying `solution/`'s generated artifacts
into a scratch folder outside the repo and running both the simple and
advanced scripts against it.

Updated `docs/lab3/lab.md` Part 7: Activities 7C/7D now show the simple
scripts, new Activity 7F explains `--project-dir`, and the former Activity
7F (traceability CSV/diagram) is renumbered 7G. `.agents/scade-models.md`,
`.agents/verification.md`, `.agents/testing.md`, `.agents/python.md`, and
`project_docs/labs/lab-3-requirements.md` updated to match. Site rebuild
confirmed clean.

---

## 2026-08-10 (fifth follow-up) — Lab 3: added a custom requirement-coverage CSV + pass/fail-colored model diagram to the Python tests

### Summary for reporting

Scade One Student Edition has no requirement-coverage report and no way to
view the model colored by which requirements currently pass or fail —
following up on the previous session's fix (correct `#pragma requirement`
IDs + the scripts printing which node each REQ resolves to), this session
built the rest of that traceability tooling as a small custom add-on,
since the underlying data (the pragma links, plus each test case's
pass/fail) was already available.

`test_limiter.py`/`test_counter.py` (`starter/` and `solution/`) now, after
the cycle-by-cycle assertions:
- Aggregate a PASS/FAIL status per requirement (FAIL if any of its test
  cases failed).
- Write `results/<operator>_traceability.csv` — one row per test case
  (`tid, req, nodes, inputs, expected, actual, status`), same shape as Lab
  4's `results/summary.csv`.
- Render `results/<operator>_diagram.png` with `matplotlib`: one box per
  `blocks.swan` diagram node (laid out using the node's own `"xy"` pragma
  coordinates, wired per the `wire` statements), colored green if its
  linked requirement passed, red if it failed, gray if the node has no
  requirement link at all.
- Degrade gracefully if `matplotlib` isn't installed (still prints
  PASS/FAIL, skips the diagram with a one-line note) — `matplotlib` was
  added to both `requirements.txt` files, matching Lab 4's dependency.

Actually run this session against `src/lab3/solution/`'s committed `.dll`s:
both scripts produced `ALL PASS`, correct CSVs (verified by reading them),
and diagrams with every requirement-tagged node green (verified by viewing
the PNGs) — confirmed working before documenting it.

Added `docs/lab3/lab.md` Activity 7F describing this, with the two
generated diagrams committed to `docs/lab3/img/` (`limiter_diagram.png`,
`counter_diagram.png`) as concrete illustrations, and trimmed Activities
7C/7D's inlined code (which had grown to duplicate the full parser/report
functions twice) down to the essential test-loop shape, pointing at the
committed scripts for the rest. `.agents/scade-models.md`,
`.agents/verification.md`, and `.agents/testing.md` updated to match.
Verified the Jekyll site still builds and the new images publish correctly.

---

## 2026-08-10 (fourth follow-up) — Lab 3: fixed `blocks.swan` requirement-pragma naming, added counter links, and made the Python tests check traceability

### Summary for reporting

`src/lab3/solution/assets/blocks.swan` carried `#pragma requirement` links
on the `limiter` operator using ad hoc IDs (`REQ1_Limiter`, `REQ2_Limiter`,
`REQ3_Limiter`) that never matched the canonical `REQ-LIM-01`/`02`/`03`
spelling used everywhere else — `requirements.md`, `docs/lab3/lab.md`, and
`test_limiter.py`'s own `req` column. This is exactly the class of bug Lab
3 Part 9 uses the `reQ2`/`REQ-02` cruise-control example to warn about,
just previously present, unflagged, in this repo's own Limiter reference
model. The `counter` node had no `#pragma requirement` links at all.

Fixed:
- Renamed the Limiter pragmas to the canonical IDs and mapped them onto the
  nodes matching Activity 2E's "upper branch / lower branch / otherwise"
  description: `REQ-LIM-01` → the `>max` comparison and its if-then-else
  (upper branch), `REQ-LIM-02` → the `<min` comparison and its
  if-then-else (lower branch), `REQ-LIM-03` → the plain `value_in` leaf
  feeding the innermost else (pass-through).
- Added `REQ-CNT-01`/`REQ-CNT-02` to the Counter's `pre` node (initial
  branch) and `+` node (accumulation), matching Activity 4F's own
  "initial-value branch vs. accumulation branch" wording.
- `src/lab3/starter/blocks.swan` deliberately left untouched (no pragmas)
  — that absence is the pre-Activity-2G/4F state the starter is supposed
  to represent.
- Rewrote `test_limiter.py`/`test_counter.py` (both `starter/` and
  `solution/`) to parse `blocks.swan` for these pragmas at import time —
  before touching the generated wrapper, so it works even without a built
  `.dll` — and print which diagram node(s) each expected REQ ID resolves
  to, or `NOT TRACED` if the link is missing. Test-case tuples now carry a
  `req` field (matching `docs/lab3/lab.md`'s Activity 7C/7D code, which
  already showed this pattern but the committed scripts hadn't caught up
  to).
- Updated `docs/lab3/lab.md` Part 7's embedded code samples to match, and
  updated `.agents/scade-models.md`/`.agents/verification.md` (which
  previously stated the shipped `blocks.swan` had no requirement pragmas
  at all — now true only for `starter/`, not `solution/`) and
  `.agents/testing.md` (previously said Lab 3's Python side "cannot be
  executed" here — actually true only for *regenerating* the wrapper; the
  committed `.dll`s run fine via `ctypes` without the `ansys` package, and
  this session actually ran both scripts against both `starter/` and
  `solution/` and confirmed the expected PASS/NOT-TRACED behavior in each).

---

## 2026-08-10 (third follow-up) — Fixed: `src/lab3/starter/` opens empty in Scade One

### Summary for reporting

The previous restructuring pass (see the entry directly below) moved the
former Lab 4.1's Scade One project into `src/lab3/starter/`, flattening
`assets/blocks.swan`/`assets/test.swant` to sit directly beside `demo.sproj`
instead of under an `assets/` subfolder. The user reported this breaks the
project in Scade One — it opens with no operators visible, because Scade
One only discovers `.swan` files under the conventional `assets/` layout,
not flattened at the project root.

Per explicit instruction, **`src/lab3/starter/` was left exactly as-is**
(not "fixed" in place) — instead, a complete, correctly-laid-out copy of
the same project was added under `src/lab3/solution/`, alongside the
EARS-answer-key `requirements.md` already there:

```
src/lab3/solution/
├── demo.sproj
├── assets/blocks.swan       (correct location — was flattened in starter/)
├── assets/test.swant        (correct location — was flattened in starter/)
├── counter_wrapper/counter_wrapper.py
├── limiter_wrapper/limiter_wrapper.py
├── setup_wrapper.py
├── test_counter.py
├── test_limiter.py
├── requirements.txt
└── requirements.md          (EARS answer key, pre-existing, unrelated)
```

`src/lab3/solution/` is now the directory to actually open in Scade One or
point instructors at; `src/lab3/starter/` remains present with the same
(flattened, non-opening) files, unchanged.

### Files touched

```
src/lab3/solution/{demo.sproj,assets/blocks.swan,assets/test.swant,
                    counter_wrapper/,limiter_wrapper/,setup_wrapper.py,
                    test_counter.py,test_limiter.py,requirements.txt}   [new]
.agents/{scade-models,lab-map,architecture,verification,workflows,testing}.md
project_docs/labs/lab-3-requirements.md
project_docs/architecture/scade-projects.md
project_docs/maintenance/generated-artifacts.md
project_docs/verification/testing-and-simulation.md
```
`src/lab3/starter/` — untouched, per instruction.

### Validation performed

- `bundle exec jekyll build` — succeeded (unaffected by this change; no
  `docs/` files touched).
- Confirmed `src/lab3/solution/` now contains all 9 project files with
  `blocks.swan`/`test.swant` correctly under `assets/`.
- **Not verified:** actually opening `src/lab3/solution/` in Scade One
  (no local install in this environment) — the fix is based on the
  documented Scade One project convention (`.swan` modules under
  `assets/`), matching the layout Lab 4's `CruiseControl` project already
  uses successfully, not on live confirmation in the tool.

---

## 2026-08-10 (second follow-up) — Lab 4.1 merged into Lab 3; Lab 4.2 renumbered to plain Lab 4

### Summary for reporting

A second restructuring of the portfolio, per explicit user direction: Lab
4.1's entire content (Scade One installation, Swan language basics, the
Limiter and Counter — modeling, test harnesses, Python wrapper/test
scripts) was merged into Lab 3, which already held the EARS
requirements-writing content added in the first restructuring pass. Lab 4.1
was retired entirely; Lab 4.2 was renumbered to plain **Lab 4** (no longer
needs a decimal — it's now the only Scade One lab besides Lab 3). The
portfolio is now four cards: Lab 1 (disabled) / Lab 2 / Lab 3 / Lab 4.

The user's stated intent: Lab 3 should teach *both* requirements-writing
*and* the Scade One/Swan tool mechanics on small worked examples (Limiter,
Counter), ending with an explicit deep dive into how Scade One's
traceability mechanism actually works — reading real `.swan` source, not a
hypothetical description. Lab 4 should then apply the same
design/implementation/traceability skills to the full Cruise Control
system, with real Swan excerpts and a worked traceability example.

### 1. Restructured Lab 3 (`docs/lab3/lab.md`, full rewrite)

Old structure (5 parts, pure requirements, no tool) replaced with 9 parts:
1. EARS patterns + Activity 1A quiz (unchanged from the first pass)
2. Limiter: write REQ-LIM-01..03, build the operator in Scade One (module
   creation, Definition-vs-Expression/instance-block Swan concepts,
   interface, logic, simulation — moved from the former Lab 4.1's Parts
   1–2), then **link REQ-LIM-01 via the Requirements panel** (Activity 2G,
   new) — the first real `#pragma requirement` a student writes
3. Limiter test harness (moved from the former Lab 4.1's Part 3)
4. Counter: write REQ-CNT-01..02, build the operator (sequential logic,
   `pre` — moved from the former Lab 4.1's Part 4), then link both REQ IDs
   (Activity 4F, new)
5. Counter test harness (moved from the former Lab 4.1's Part 5)
6. Comparing combinatorial vs sequential logic (moved from the former
   Lab 4.1's Part 6)
7. Code generation + Python wrapper + `test_limiter.py`/`test_counter.py`
   (moved from the former Lab 4.1's Part 7; each test tuple now also
   carries a `req` field, same pattern as Lab 2)
8. Cruise Control requirements (the first pass's Part 4, renumbered) —
   rewrite REQ-01/02/04 as EARS, write new REQ-07/08, sanity-check against
   the state table
9. **"How Traceability Works in Scade One" (entirely new)** — explains the
   `#pragma requirement <ID> #end` mechanism precisely, then quotes the
   **real, unedited line** from this repo's own `CC_design.swan`
   (`node #pragma requirement reQ2 #end cruise_control (...)`) and uses its
   `reQ2`/`REQ-02` casing mismatch as a deliberate, named lesson: Scade One
   does not validate pragma text, so a typo/casing slip creates a link that
   looks present but won't match a canonical-ID search. Also includes the
   first pass's "From a requirement to a test case" walkthrough and
   Activity 9A (renumbered from 5A), plus an updated requirement→design→test
   forward-reference table that now points at Limiter/Counter's own
   Activities 2G/4F instead of "Looking Ahead" to a separate lab.

Common Errors (moved from the former Lab 4.1) gained a new entry:
"Requirement ID Doesn't Match Anything," directly referencing the Part 9
lesson. The reflection quiz grew from 6 to 7 questions (added: what linking
a requirement actually writes into the `.swan` source; what the real
`reQ2`/`REQ-02` mismatch demonstrates).

### 2. Retired Lab 4.1; renumbered Lab 4.2 → Lab 4

```
docs/lab4_1/           → merged into docs/lab3/ (index.html/lab.md deleted after content merge)
docs/lab4_1/img/*.png  → docs/lab3/img/ (15 files)
src/lab4_1/starter/    → src/lab3/starter/ (flattened: assets/blocks.swan → blocks.swan,
                          assets/test.swant → test.swant; demo.sproj, counter_wrapper/,
                          limiter_wrapper/, test_counter.py, test_limiter.py,
                          setup_wrapper.py, requirements.txt kept at the same relative shape)
docs/lab4_2/            → docs/lab4/    (git mv, all files incl. img/, lab_old.md)
src/lab4_2/             → src/lab4/     (git mv)
project_docs/labs/lab-4-1-scade-one-intro.md  → deleted (content now covered by lab-3-requirements.md)
project_docs/labs/lab-4-2-cruise-control.md   → project_docs/labs/lab-4-cruise-control.md (git mv)
```

`docs/lab4/lab.md`'s Activity 7A (traceability) was extended: the
Requirements-panel table now covers 7 element-level links (top node, 4
transitions, `regulator`, `limiter` instances) instead of 4
transition-only links, and explicitly walks through the real `CC_design.swan`
excerpt and its `reQ2`/`REQ-02` gap as a check-your-work step, cross-referencing
Lab 3 Part 9. All "Lab 4.1"/"Lab 4.2" prose, paths, and cross-links
throughout `docs/lab4/lab.md`, `docs/index.html`, `docs/admin/index.html`,
`docs/account/index.html` (Firebase `LAB_TITLES` maps, `lab4_1`/`lab4_2`
keys dropped, `lab4` key added) updated to match.

### 3. Documentation updated in the same pass

Per `AGENTS.md`'s "keep docs and content in sync" rule: `.agents/lab-map.md`,
`architecture.md`, `domain.md`, `workflows.md`, `publishing.md`,
`verification.md`, `testing.md`, `python.md`, `scade-models.md`,
`integrations.md`, `AGENTS.md` itself, and `project_docs/labs/lab-3-requirements.md`
(full rewrite), `portfolio-map.md` (full rewrite), `lab-4-cruise-control.md`,
`lab-2-sdlc.md`, plus `project_docs/architecture/*`, `verification/*`,
`maintenance/*` files that named the old paths. While touching these files,
also fixed incidental pre-existing drift encountered along the way: a
mid-edit `sed` pass initially produced several duplicate/garbled section
headers (from "Lab 4.1" → "Lab 3" colliding with text that already said
"Lab 3") — these were caught and manually rewritten, not left in the
committed result.

### Files touched

```
docs/lab3/{index.html,lab.md}                                   [full rewrite]
docs/lab4/{index.html,lab.md}                                    [renamed from lab4_2/, edited]
docs/index.html, docs/admin/index.html, docs/account/index.html
src/lab3/starter/{blocks.swan,test.swant,demo.sproj,counter_wrapper/,limiter_wrapper/,
                   test_counter.py,test_limiter.py,setup_wrapper.py,requirements.txt}  [moved from lab4_1/]
src/lab4/starter/CruiseControl/evaluate_cc.py                    [comment fixes]
.agents/{lab-map,architecture,domain,workflows,publishing,verification,testing,python,scade-models,integrations}.md
AGENTS.md
project_docs/labs/{lab-3-requirements,portfolio-map,lab-4-cruise-control,lab-2-sdlc}.md
project_docs/labs/lab-4-1-scade-one-intro.md                     [deleted]
project_docs/architecture/{scade-projects,system-overview,python-and-simulation,firebase-backend,site-and-publishing}.md
project_docs/verification/{requirements-and-traceability,testing-and-simulation}.md
project_docs/maintenance/{generated-artifacts,validation-checklist,adding-or-updating-a-lab}.md
```

### Validation performed

- `bundle exec jekyll build` — succeeded after each major edit pass in this
  session; final run confirmed output tree contains exactly `lab2/`,
  `lab3/`, `lab4/` (no stray old paths).
- Grepped every relative `href`/markdown link in `docs/index.html`,
  `docs/lab3/lab.md`, `docs/lab4/lab.md` and confirmed each target
  directory/anchor exists (anchor slugs computed by hand against each
  page's `slugify()` logic — not verified by loading the rendered page in a
  browser).
- Grepped every `img/*.png` reference in Lab 3/Lab 4's `lab.md` and
  confirmed each file exists on disk.
- Repo-wide grep for stale `lab3_1`/`lab3_2`/`lab4_1`/`lab4_2`/"Lab 3.1"/
  "Lab 3.2"/"Lab 4.1"/"Lab 4.2" — remaining hits are all intentional
  historical narrative (this changelog, `.agents/decisions/`, and the
  "Numbering"/"restructured this session" notes in `lab-map.md`,
  `publishing.md`, `portfolio-map.md`, `lab-3-requirements.md` describing
  the two renumbering passes) or generated Scade codegen logs under
  `src/lab4/starter/CruiseControl/jobs/`.

### Not addressed / carried over as open items

- Activity 7A's `#pragma requirement reQ2` casing gap itself is **not
  fixed** in `CC_design.swan` (would require a Scade One install to safely
  edit a diagram-format `.swan` file) — it is now explicitly taught as a
  lesson instead, in both Lab 3 Part 9 and Lab 4 Activity 7A.
- `ansys-scadeone-core` remains unpinned in Lab 4's `requirements.txt`.
- No migration of any pre-existing Firestore `labOpens`/`quizAttempts`
  records under the old `lab4_1`/`lab4_2` IDs — same standing limitation
  noted in the first restructuring pass's entry below.

---

## 2026-08-10 (follow-up) — Lab 3: Activity 1A converted to a quiz; requirement→test-case link made explicit

### Summary for reporting

Two follow-up changes to the new Lab 3 (see the entry directly below for its
initial addition), both requested after review:

1. **Activity 1A is now an auto-graded quiz**, not a free-text exercise.
   `docs/lab3/index.html`'s single-quiz JS (`initQuiz()`, hardcoded ids
   `quiz-submit`/`quiz-reset`/`quiz-score` and `#reflection-quiz` selector)
   was generalized to `initQuiz(containerId)`, scoped by container so two
   independent quiz widgets can coexist on one page without their
   radio-button groups or Check/Reset state interfering — the CSS moved
   from id selectors (`#quiz-submit`) to class selectors (`.quiz-submit`),
   and each question gained an explicit `data-name` (radio group name)
   instead of the old positional `name="q${i+1}"` derivation. Activity 1A's
   3 free-text sentences became 4 multiple-choice questions
   (`#ears-pattern-quiz`, radio names prefixed `a1q*` to avoid colliding
   with the reflection quiz's `q1`..`q6`), covering Ubiquitous/Event-driven/
   State-driven/Optional-feature (Unwanted-behavior was left to the existing
   reflection-quiz question 1, to avoid redundancy).
2. **Added an explicit requirement→test-case link**, answering "how do
   these requirements map to testing, and how do you write test cases" —
   this was previously only asserted in a one-line traceability-preview
   table, not walked through. New "From a requirement to a test case"
   subsection in Part 5: explains the `req`/`expected_throttle` columns in
   `evaluate_cc.py`'s scenario CSVs, then works through deriving REQ-01's
   test case as a 2-row scenario (matching the real
   `tc03_brake_suspends.csv`). New **Activity 5A** asks the student to do
   the same derivation for REQ-07, including the "no single expected value"
   case (checked visually, still traceable via the `req` tag). Reflection
   quiz gained a 6th question on the same theme. Learning Objectives and Key
   Takeaway both gained a line naming this skill explicitly.

### Files touched

```
docs/lab3/index.html                          (initQuiz generalized to initQuiz(containerId))
docs/lab3/lab.md                              (Activity 1A → quiz; new Part 5 subsection + Activity 5A; quiz Q6; objectives/takeaway lines)
src/lab3/solution/requirements.md             (Activity 1A answer-key prose replaced with a pointer to the self-checking quiz; new Activity 5A worked answer)
src/lab3/starter/requirements_template.md     (new Activity 5A TODO)
.agents/workflows.md, .agents/lab-map.md, .agents/verification.md, .agents/testing.md
project_docs/labs/lab-3-requirements.md
```

### Validation performed

- `bundle exec jekyll build` — succeeded (same pre-existing Sass warnings
  only).
- Checked for duplicate element `id`s and radio `name` collisions across
  `docs/lab3/lab.md` directly (grep) — none found; `#ears-pattern-quiz`'s
  4 questions use `a1q1`..`a1q4`, `#reflection-quiz`'s 6 questions use
  `q1`..`q6`, no overlap.
- **Not run:** no browser-based interaction test of the quiz JS (click
  Check/Reset, confirm scoring and `recordQuizAttempt` calls) — this
  environment has no browser to drive; verified by static reading of the
  generalized `initQuiz()` logic against the new markup instead.

---

## 2026-08-10 — New Lab 3 (requirements engineering); Lab 3.1/3.2 renumbered to Lab 4.1/4.2

### Summary for reporting

Added a new lab, **Lab 3 — Software Requirements Engineering: EARS &
Traceability**, teaching the EARS requirement-writing method and having
students derive the software requirements (REQ-LIM-01..03 for the Limiter,
REQ-CNT-01..02 for the Counter, and EARS rewrites of REQ-01/02/04 plus two
new IDs REQ-07/08 for the Cruise Control system) that the following two labs
build and test against. This required renumbering the two existing Scade
One labs so Lab 3 could slot in ahead of them: the former **Lab 3.1**
(Scade One basics) is now **Lab 4.1**, and the former **Lab 3.2**
(cruise-control model) is now **Lab 4.2**. This was a deliberate,
user-approved restructuring (the user chose "new lab becomes Lab 3, Labs
3.1/3.2 become 4.1/4.2" over an alternative that kept the old paths and
inserted a "Lab 3.0"), not a bug fix — and it **breaks any previously
published external links** to `/lab3_1/`/`/lab3_2/`, since GitHub Pages has
no redirect mechanism configured in this repo.

Scope was deliberately limited to an EARS primer plus guided practice
deriving requirements — a full traceability-matrix-construction activity
and a Scade One Requirements-panel walkthrough were considered and
explicitly excluded from Lab 3 itself (the existing Activity 7A in Lab 4.2
remains the only in-tool traceability exercise); Lab 3 only *previews* the
forward links in a table, it doesn't build them.

### 1. Directory renames

```
docs/lab3_1/  → docs/lab4_1/   (git mv, all files including img/)
docs/lab3_2/  → docs/lab4_2/   (git mv, all files including img/, lab_old.md)
src/lab3_1/   → src/lab4_1/    (git mv)
src/lab3_2/   → src/lab4_2/    (git mv)
project_docs/labs/lab-3-1-scade-one-intro.md → lab-4-1-scade-one-intro.md
project_docs/labs/lab-3-2-cruise-control.md  → lab-4-2-cruise-control.md
```

### 2. New Lab 3 content

- `docs/lab3/index.html` — page shell (copied and adapted from Lab 4.1's,
  same TOC/quiz-widget pattern), `CURRENT_LAB_ID = 'lab3'`.
- `docs/lab3/lab.md` — 5 parts: EARS pattern theory + classification
  activity; Limiter requirements (worked example + 2 to write); Counter
  requirements (worked example + 1 to write); Cruise Control requirements
  (rewrite REQ-01/02/04, write new REQ-07/08, cross-check against the state
  table); a forward-looking (not built-out) traceability preview table;
  5-question reflection quiz.
- `src/lab3/starter/requirements_template.md` — student fill-in template,
  every REQ ID pre-listed with `TODO` blanks.
- `src/lab3/solution/requirements.md` — instructor reference: full REQ set,
  traceability preview, Activity 1A answers.

### 3. Renumbering touch-points (Lab 3.1→4.1, Lab 3.2→4.2)

- `docs/index.html` — cards renumbered, new Lab 3 card inserted between Lab
  2 and Lab 4.1.
- `docs/lab4_1/{index.html,lab.md}`, `docs/lab4_2/{index.html,lab.md,lab_old.md}`
  — all internal "Lab 3.1"/"Lab 3.2" text, `lab3_1`/`lab3_2` path references,
  `CURRENT_LAB_ID`, quiz-attempt IDs, footer/meta "Lesson N" numbers bumped.
  Both labs' prerequisite lines now mention Lab 3; Lab 4.2 gained a short
  "Lab 3 connection" callout pointing at the REQ IDs Activity 7A/Part 6
  reference.
- `docs/admin/index.html`, `docs/account/index.html` — `LAB_TITLES` maps:
  `lab3_1`/`lab3_2` keys renamed to `lab4_1`/`lab4_2`, new `lab3` key added.
  Any pre-existing Firestore `labOpens`/`quizAttempts` records under the old
  `lab3_1`/`lab3_2` IDs are not migrated (no admin-side migration tooling
  exists) — they degrade gracefully to showing the raw ID string via the
  existing `LAB_TITLES[id] || id` fallback, not a crash.
- `src/lab4_2/starter/CruiseControl/evaluate_cc.py` — header comments
  updated ("Lab 3.2" → "Lab 4.2", "Lab 3.1" → "Lab 4.1").
- All current-state `.agents/*.md` and `project_docs/**/*.md` files that
  named the old paths/numbers: `lab-map.md`, `architecture.md`, `domain.md`,
  `workflows.md`, `publishing.md`, `verification.md`, `testing.md`,
  `python.md`, `scade-models.md`, `integrations.md`, `portfolio-map.md`, the
  renamed `labs/lab-4-1-*.md`/`lab-4-2-*.md`, `lab-2-sdlc.md`, and the
  `architecture/`, `verification/`, `maintenance/` subtrees under
  `project_docs/`. **Not touched:** this changelog's own prior entries and
  `.agents/decisions/*.md` — both are historical records of what was true
  at the time they were written, not current-state documentation.

### 4. Incidental drift fixed while touching these files

While renumbering, also corrected several pre-existing inaccuracies these
same files already had, unrelated to the renumbering itself:
- `src/lab4_1/starter/` and `src/lab4_2/starter/CruiseControl/` were still
  being called `.../solution/` in most `.agents/`/`project_docs/` prose,
  even though a prior session had already consolidated both labs down to a
  single populated `starter/` directory with no separate `solution/`. Fixed
  every such path reference; `.agents/lab-map.md` and `architecture.md` now
  explain the "populated starter/, doubles as reference" situation
  explicitly instead of asserting a `solution/` that doesn't exist.
- `Main_test.swant` was documented in several files as "present but empty" —
  it has since been removed from the tree entirely (predates this session).
  Fixed all such references.
- A stray self-contradiction in `project_docs/labs/lab-4-1-scade-one-intro.md`
  ("no `src/lab4_1/starter/`" directly under a table listing files inside
  that exact directory).

### Files touched

```
docs/index.html
docs/admin/index.html
docs/account/index.html
docs/lab3/{index.html,lab.md}                                [new]
docs/lab4_1/{index.html,lab.md}                                [renamed from lab3_1/, edited]
docs/lab4_2/{index.html,lab.md,lab_old.md}                     [renamed from lab3_2/, edited]
src/lab3/starter/requirements_template.md                      [new]
src/lab3/solution/requirements.md                               [new]
src/lab4_1/starter/                                             [renamed from lab3_1/starter/]
src/lab4_2/starter/CruiseControl/evaluate_cc.py                [renamed from lab3_2/, edited]
.agents/{lab-map,architecture,domain,workflows,publishing,verification,testing,python,scade-models,integrations}.md
project_docs/labs/{portfolio-map,lab-2-sdlc,lab-3-requirements[new],lab-4-1-scade-one-intro[renamed],lab-4-2-cruise-control[renamed]}.md
project_docs/architecture/{system-overview,firebase-backend,scade-projects,python-and-simulation,site-and-publishing}.md
project_docs/verification/{requirements-and-traceability,testing-and-simulation}.md
project_docs/maintenance/{generated-artifacts,validation-checklist,adding-or-updating-a-lab}.md
AGENTS.md
readme_local_setup.txt
```

### Validation performed

- `python -m py_compile` was **not** re-run this session (no Python content
  changed beyond a comment edit in `evaluate_cc.py`).
- Jekyll build: see this session's own note in
  `.agents/testing.md`/`project_docs/verification/testing-and-simulation.md`
  for whether it was actually run and what it found.
- **Not run / not possible in this environment:** Scade One simulator, code
  generation, wrapper regeneration — same standing limitation as every prior
  session (no local Scade One install here).

### Not addressed / carried over as open items

- Activity 7A's `#pragma requirement reQ2` casing still doesn't match either
  Lab 2's or Lab 3's `REQ-02` spelling, and still only covers 1 of 4
  transition-level links the activity instructs students to create —
  pre-existing gap, not touched by this session.
- `ansys-scadeone-core` remains unpinned in Lab 4.2's `requirements.txt`.
- No migration of any pre-existing Firestore `labOpens`/`quizAttempts`
  records under the old `lab3_1`/`lab3_2` IDs (see above) — flagged for the
  maintainer, no migration tooling exists in this repo to do it from here.

---

## 2026-07-27 — Lab 3.2: fixed generation/wrapper scripts and evaluate_cc.py against the real PyScadeOne 0.8.2 API

### Summary for reporting

The Lab 3.2 Python tooling added in the previous session (`generate_python_wrapper.bat`,
`evaluate_cc.py`, and the `tc02` scenario file) had never actually been run against a
live Scade One install; doing so this session surfaced several real bugs, now fixed in
both `src/lab3_2/starter/CruiseControl/` and `src/lab3_2/solution/CruiseControl/`, and
mirrored into `docs/lab3_2/lab.md` Activity 6D:

1. **`generate_python_wrapper.bat`** hardcoded an absolute `.sproj` path from an old
   repo location. Now resolves the project path relative to the script itself
   (`%~dp0`), so it works regardless of checkout location.
2. **`PythonWrapper` job argument.** `PythonWrapper(prj, job)` requires the job *name
   string*, not the `Job` object returned by `prj.get_job(...)` — passing the object
   crashed deep inside the library (`AttributeError` on `Job.__eq__`). Fixed to pass
   the job name string directly (matches the convention already used in
   `src/lab3_1/*/setup_wrapper.py` and `docs/lab3_1/lab.md`).
3. **No `PythonWrapper.get_operator_instance()` method exists** in PyScadeOne 0.8.2.
   The generated wrapper must be imported directly from
   `<output_dir>/<output_dir>.py` and its operator class instantiated (class name
   pattern `<operator>_<design>`), with inputs/outputs grouped under
   `.inputs.<name>` / `.outputs.<name>` rather than flat attributes — same API shape
   Lab 3.1's wrapper tests already use. `evaluate_cc.py` and `lab.md` updated
   accordingly.
4. **`set_point` is a plain input on the generated `cruise_control` node**, not
   something the node computes internally from a `set` trigger. `evaluate_cc.py` (and
   the `lab.md` listing) now reproduce Activity 4E's "rising edge of `on` locks
   `set_point = v_speed`" rule in Python and hold that value across cycles; the
   scenario CSVs' `set` column is accepted by `run_cycle()` but not fed to the model
   (it isn't part of this node's interface).
5. **`tc02_cc_active_regulates.csv`** had an unquoted comma inside its `note` field,
   which made `csv.DictReader` parse an 11th field and later crash
   `csv.DictWriter.writerows` (`dict contains fields not in fieldnames: None`). The
   field is now properly quoted.

No requirements, model files, or test expectations changed — this was a bugfix pass
on the Python glue code and its lab documentation, informed by actually exercising it.

---

## 2026-07-27 — Lab 3.2: Python-driven evaluation replaces Scade One test harness; Project Structure section added

### Summary for reporting

Updated Lab 3.2 (the Scade One cruise-control lab) in two ways:

1. **Replaced the in-tool test-harness exercise with a Python evaluation
   workflow.** Students now define test scenarios as simple CSV files,
   run a Python script that exercises the model and logs the results to
   CSV, and get an automatic pass/fail report plus charts showing how the
   system behaves over time — closer to real engineering practice and to
   how the students already worked in the earlier Python lab. A worked
   reference example (script + 6 sample scenarios) was added for
   instructors.
2. **Clarified the project's structure for students.** Added a short
   explanation, up front in the lesson, of the three parts of the Scade
   One project: the vehicle model (a stand-in, for simulation only), the
   cruise-control model (the actual thing students design and the only
   part that matters for the real system), and the simulation wiring
   (learning aid only, never shipped). This removes prior ambiguity about
   what students are actually being graded on.

No models, requirements, or existing test content were changed — this was
a lesson-flow and documentation update. Full technical detail below.

**Scope:** `docs/lab3_2/lab.md` (Parts 5–6, plus a new "Project Structure"
section) and its supporting reference material under
`src/lab3_2/solution/CruiseControl/`. Corresponding `.agents/` and
`project_docs/` maintainer documentation updated in the same pass per
`AGENTS.md`'s "keep docs and content in sync" rule.

### 1. Part 6 rewritten: Scade One test harness → Python evaluation script

- **Part 5** now only briefly mentions Scade One's in-tool Test Harnesses
  (`.swant`) before redirecting to Part 6; the harness-building framing was
  removed from the lesson's critical path (`Main_test.swant` stays as an
  unused, empty scaffold — not deleted, just no longer part of the taught
  workflow).
- **Part 6** ("Python Test Script" → "Python Evaluation Script") rewritten
  across Activities 6C–6F:
  - **6C** — test scenarios are now defined as CSV files under `scenarios/`
    (one file per test case, one row per simulation cycle), replacing
    inline hardcoded test tuples. Optional `expected_throttle`/`req`/`note`
    columns mark checkpoint rows.
  - **6D** — `evaluate_cc.py` reads every scenario, drives the generated
    wrapper cycle-by-cycle, writes a per-scenario trace CSV, and writes
    `results/summary.csv` as a traceability report (REQ-tagged, PASS/FAIL,
    same banner style as Lab 2's `VALIDATION: ALL REQUIREMENTS MET.`).
  - **6E** — adds a `matplotlib`-based charting step
    (`results/plots/<tid>.png`, throttle + `v_speed` vs. cycle on twin
    axes) so `cc_active`'s gradual PI-regulator convergence — not checkable
    as a single expected value — can be evaluated visually.
  - **6F** — run/compare step updated to point at `results/summary.csv` and
    the charts instead of a single console printout.
- Structure table: Part 6 time bumped 30 → 45 min to reflect the added
  scope.
- `requirements.txt` (both the in-lab.md example and the real
  `src/lab3_2/solution/CruiseControl/requirements.txt`) gained `matplotlib`.

**New reference files** (instructor-only, under
`src/lab3_2/solution/CruiseControl/`):
- `evaluate_cc.py` — full reference implementation of Activities 6C–6F.
  Syntax-verified with `python -m py_compile` (passes); cannot be executed
  in this environment — requires a local Scade One install to regenerate
  `cc_wrapper` first (same limitation as the pre-existing `tester.py`).
- `scenarios/tc01_cc_disabled_passthrough.csv` … `tc06_cc_off.csv` — six
  example scenarios covering REQ-01/02/04, mirroring Lab 2's test cases as
  short multi-cycle sequences.
- `tester.py` (pre-existing) kept as-is, no longer part of the taught
  workflow but not removed.

**Known caveat carried forward, not resolved this session:** `evaluate_cc.py`
and the lab.md snippet it's based on both use a simplified, hypothetical
wrapper attribute API (`cc.on`, `cc.brake`, `cc.cycle()`, `cc.throttle`)
that differs from the real generated `cc_wrapper.py` (which wraps the
closed-loop `main` node, not a standalone `cruise_control` instance). This
gap pre-dates this session (see `project_docs/architecture/python-and-simulation.md`)
and would require a Scade One install to fix and verify — flagged, not
silently patched.

### 2. New "Project Structure" section

Added a section (after the Structure table, before "The System") that
explains the `CruiseControl` project's three packages and their distinct
roles, matching what students see in Scade One's Model Explorer:

| Package | Role | Ships to the real system? |
|---|---|---|
| `Car_design` (`car`) | Stand-in plant model for a real vehicle — simulation aid only | No |
| `CC_design` (`cruise_control`/`regulator`/`limiter`) | **The actual deliverable** — what students design and what Part 6 generates code from | Yes |
| `Simulation` (`main`/`main_manual`) | Wiring scaffolding for interactive simulation only | No — never a code-generation target |

This also explains, in-lesson, *why* Activity 6A's code-generation job
targets `cruise_control` and not `main` — a rationale that was previously
implicit. A matching one-line note was added to the Optional Extension
section (closed-loop `main` wiring), and mirrored in `.agents/scade-models.md`
and `project_docs/architecture/scade-projects.md` for maintainers.

### Files touched

```
docs/lab3_2/lab.md                                          (Parts 5-6 rewrite, new Project Structure section)
src/lab3_2/solution/CruiseControl/requirements.txt          (+matplotlib)
src/lab3_2/solution/CruiseControl/evaluate_cc.py             [new]
src/lab3_2/solution/CruiseControl/scenarios/*.csv (x6)        [new]
.agents/lab-map.md
.agents/workflows.md
.agents/verification.md
.agents/testing.md
.agents/python.md
.agents/scade-models.md
project_docs/labs/lab-3-2-cruise-control.md
project_docs/architecture/python-and-simulation.md
project_docs/architecture/scade-projects.md
project_docs/verification/requirements-and-traceability.md
project_docs/verification/testing-and-simulation.md
```

### Validation performed

- `python -m py_compile` on every `.py` file under `src/lab3_1/solution/`
  and `src/lab3_2/solution/CruiseControl/` (including the new
  `evaluate_cc.py`) — all parse without error.
- `cd docs && bundle exec jekyll build` — succeeded twice this session
  (after the Part 6 rewrite, and again after the Project Structure
  addition); only pre-existing `jekyll-theme-cayman` Sass deprecation
  warnings, unrelated to this repo's content.
- **Not run / not possible in this environment:** the Scade One simulator,
  code generation, wrapper regeneration, or `evaluate_cc.py`/`tester.py`
  execution — all require a local Scade One Student Edition install, not
  available here (see `.agents/testing.md`).

### Not addressed / carried over as open items

- The wrapper-API mismatch caveat above (pre-existing, not newly
  introduced).
- `ansys-scadeone-core` remains unpinned in Lab 3.2's `requirements.txt`
  (inconsistent with Lab 3.1's `==0.8.2` pin) — untouched, per standing
  guidance not to invent a pin without maintainer confirmation.
- Activity 7A traceability gap (only 1 of 4 `#pragma requirement` links
  present in the shipped `.swan`) — untouched, out of scope for this
  session's changes.
- **Unrelated local working-tree state noticed but not made by this
  session:** at the time of writing, `git status` also shows the 9
  `docs/lab3_2/img/*.png` screenshots as modified (larger file sizes) and
  `src/lab3_2/solution/CruiseControl/assets/Main_test.swant` as deleted.
  Neither of these was touched by the changes described above — flagging
  for the maintainer to confirm intent before committing.
