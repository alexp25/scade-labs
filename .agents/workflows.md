# Workflows

Only workflows actually supported by files in this repo. Where the repo only
partially documents a step, that's stated explicitly.

## Learner: portfolio → lab

1. Open `https://alexp25.github.io/scade-labs/` → `docs/index.html`.
2. Click a lab card (`Lab 1` through `Lab 6` — 6 cards, all linked).
3. The lab's `index.html` fetches and renders its sibling `lab.md`.

## Learner: Lab 1 — introduction to software engineering

1. Open `docs/lab1/index.html`. No install/prerequisite step — this lab is
   reading + quiz only.
2. Read Parts 1–7 (IEEE's software engineering definition and its three
   qualifiers, why IT projects fail, software engineering vs. programming,
   characteristics of high-quality software, safety-critical-system needs,
   Model-Based Design, and an introduction to Ansys Scade One).
3. Part 8 points at the assigned external reading (a DOI-linked journal
   article) — not fetched or embedded, just referenced.
4. Take the 10-question `#intro-quiz` (auto-graded, same `initQuiz()`
   scoring widget pattern as Lab 4's reflection quiz — Check Answers/Try
   Again, correct answer embedded in each question's `data-correct`
   attribute).

## Learner: Lab 2 in-browser

1. Open `docs/lab2/index.html`.
2. Read the rendered `lab.md` (requirements → decision table → stub code).
3. Edit `update_cruise_control(...)` in the embedded CodeMirror editor
   (pre-filled from the `STARTER_CODE` literal, identical to
   `src/lab2/starter/lab2_cruise_control_starter.py`).
4. Click ▶ Run — Skulpt executes the code in-browser and prints the 7-test
   PASS/FAIL report + validation banner.

## Learner: Lab 2 locally

1. Download/open `src/lab2/starter/lab2_cruise_control_starter.py`.
2. Implement the stub.
3. `python lab2_cruise_control_starter.py` — same 7 test cases, printed to
   the console instead of the browser.

## Learner: Lab 3 — requirements, Scade One/Swan, and traceability (9 parts)

1. Open `docs/lab3/index.html`. Install Scade One Student Edition (no
   registration/license step required — corrected in an earlier session, see
   `.agents/publishing.md` history) and complete the QuickStart video, per
   the lab's Prerequisites section.
2. **Part 1:** read the EARS pattern table, then take the 4-question
   Activity 1A quiz (`#ears-pattern-quiz`) — auto-graded, same client-side
   scoring widget as the closing reflection quiz, scoped to its own
   container/radio-name prefix so the two quizzes don't interfere.
3. **Parts 2–3 (Limiter):** write REQ-LIM-02/03 (given REQ-LIM-01 as a
   worked example), then build the `limiter` operator in Scade One (Swan
   module creation, Definition-vs-Expression/instance-block concepts,
   interface, logic, simulation), then link REQ-LIM-01 to it via the
   Requirements panel (Activity 2G — the first real `#pragma requirement`
   the student writes), then build and run `limiter_harness`.
4. **Parts 4–5 (Counter):** same pattern for REQ-CNT-01/02 and the `counter`
   operator (sequential logic, `pre`), including linking both REQ IDs
   (Activity 4F) and running `counter_harness`.
5. **Part 6:** comparison table, combinatorial vs sequential.
6. **Part 7:** generate code + Python wrapper for both operators, write
   `test_limiter.py`/`test_counter.py` (each test tuple now carries a `req`
   field, same pattern as Lab 2), run both.
7. **Part 8:** write the Cruise Control requirement set — rewrite Lab 2's
   REQ-02/REQ-04 as EARS, write two new IDs REQ-07/REQ-08 for behavior that
   only exists once Lab 4's model separates the regulator/limiter out, and
   sanity-check against the state table.
8. **Part 9 ("How Traceability Works in Scade One"):** read the
   `#pragma requirement` mechanism explanation and the real `CC_design.swan`
   excerpt (`reQ2` vs `REQ-02` casing gap, used as a worked lesson), then the
   "From a requirement to a test case" walkthrough (REQ-01 → a
   scenario-CSV row, in the same shape `evaluate_cc_full_report.py` consumes), then
   sketch a test case for REQ-07 (Activity 9A) — free text, not auto-graded.
9. Take the 7-question reflection quiz (question topics: EARS pattern
   recognition, the `#pragma requirement` mechanism, the `reQ2`/`REQ-02`
   gap, and what ties an `evaluate_cc_full_report.py` scenario row back to a
   requirement).
10. The two auto-graded quizzes (Activity 1A, 4 questions; reflection, 7
    questions) are the only automated checks in this lab. The actual
    deliverable — REQ IDs, the built/traced Scade One model, and the
    Activity 9A test-case sketch — is instructor-graded against
    `src/lab3/solution/requirements.md` and the working Scade One project
    under `src/lab3/solution/` (`starter/` has the same files but doesn't
    open in Scade One — see `.agents/scade-models.md`).

## Learner: Lab 4 — Cruise Control design, implementation &amp; traceability

1. Complete [Lab 3](../lab3/) first — Lab 4 has no separate Scade One
   install step, and assumes the REQ-01–REQ-08 requirement set from Lab 3
   Part 8 is already written.
2. Parts 1–2: orientation recap (brief — Lab 3 already covered the tool),
   car plant model simulation.
3. Parts 3–4: create the `cruise_control` project/interface, build the
   state machine (`cc_disabled`/`cc_enabled`/`cc_active`/`cc_standby`), then
   the `regulator` PI controller (reusing the `limiter` operator from
   Lab 3).
4. Part 5: build/simulate, manual state-hierarchy trace.
5. Part 6 (Python evaluation script — detailed below): code generation,
   Python wrapper, scenario CSVs, `evaluate_cc_full_report.py`, charts.
6. Part 7: link REQ-01/02/04/07/08 to the relevant model elements via the
   Requirements panel (Activity 7A) — the real shipped `CC_design.swan`
   only has one such link (`reQ2` on the top node, casing-mismatched
   against `REQ-02`), explicitly flagged as a thing to *not* repeat, not a
   template to copy uncritically — then the reflection quiz (Activity 7B).

### Part 6 detail — Python evaluation script

1. Generate the code-generation job + Python wrapper (Activities 6A/6B —
   requires local Scade One, same prerequisite as the modeling workflow).
2. Define each test scenario as a CSV file under `scenarios/` (one row per
   simulation cycle; `set_point` is a real model input authored by hand per
   Activity 4E's "rising edge of `on` locks `set_point = v_speed`" rule;
   optional `expected_throttle`/`req`/`note` columns mark checkpoint rows).
   Six examples ship in `src/lab4/starter/CruiseControl/scenarios/`
   (`tc01`…`tc06`), each 12-14 cycles with `v_speed` ramped gradually rather
   than jumped between two values.
3. Run `evaluate_cc_full_report.py` — it prints progress per scenario as it runs, drives
   the wrapper cycle-by-cycle per scenario, writes `results/<tid>_trace.csv`,
   checks checkpoint rows, and writes `results/summary.csv` (the
   traceability report, REQ-tagged, PASS/FAIL, same banner style as Lab 2)
   plus `results/plots/<tid>.png` — two stacked subplots: `throttle`/
   `v_speed`/`set_point`/`brake` on top, boolean inputs (`on`/`set`/`res`)
   plus a Python-re-derived `cc state` (not read from the model) on the
   bottom. It also prints a final list of every file it generated.
4. Compare `results/summary.csv` and the charts to Lab 2's verification
   report (Activity 6F).

## Learner: Lab 6 — software architecture

1. Open `docs/lab6/index.html`. No install/prerequisite step — a short
   recap + hands-on written/diagram exercise + quiz. Recommended: have
   already seen the Lesson 6 lecture/slides (this lab does not re-teach
   them — see the "Recap" section, ~7 short bullets, not a slide
   reproduction) and complete [Lab 4](../lab4/) first, since Parts 1–3
   analyze its requirement set and Scade One model.
2. Read the Context, Learning Objectives, and Recap — the Recap is a
   reminder of vocabulary already covered in the lecture (why architecture
   matters, the ISO/IEC/IEEE 42010 definition, architecture vs design, the
   four elements, quality attributes, requirements-driven architecture,
   and a one-paragraph pointer to the lecture's medical-monitoring
   example), not new teaching content — nothing to produce here.
3. **Part 1 (hands-on):** write a component table, an interface table, and
   a constraints list documenting the *already-existing* architecture of
   the Lab 4 Cruise Control system (`Car_design`/`CC_design`/`Simulation`
   packages; `cruise_control`/`regulator`/`limiter`/`car` nodes), then
   **finish the component diagram directly in the page** — Activity 1D's
   diagram ships with boxes but no arrows (`%% TODO` comments), edited live
   in the built-in diagram editor. Instructor-graded, no fixed answer key
   beyond matching the real model.
4. **Part 2 (hands-on):** same pattern one level up — an incomplete
   whole-vehicle, SysML-*style* block diagram (Driver/HMI, sensors, the
   Part 1 box collapsed into one component, actuators, vehicle dynamics)
   with the connections left as an exercise, edited in the same widget —
   explicitly caveated in `lab.md` as a Mermaid stand-in, not real SysML
   tool output.
5. **Part 3 (hands-on):** propose an Emergency Braking Controller +
   Obstacle/Distance Sensor extension on paper — new component/interface
   table, two proposed EARS requirements (REQ-09/REQ-10, explicitly marked
   "proposed — not implemented in the shipped model"), a prose description
   of how it would extend Lab 4's scenario-CSV simulation approach, and
   (Activity 3D) wiring the two new components into a copy of the Part 1
   diagram in the editor. **No file under `src/lab4/` is created or
   modified.**
6. Read the Summary, then take the 10-question `#architecture-quiz`
   (self-authored — no instructor quiz file was supplied for this lab,
   unlike Lab 5's `Lab 5.pdf`), same `initQuiz()` scoring widget pattern as
   every other lab.
7. **All three exercise diagrams (Parts 1–3) are live editors** — Mermaid.js
   (loaded from cdnjs by `docs/lab6/index.html` — the first lab page in
   this repo to load it) renders a textarea's contents into a preview pane
   on a Render button click, Ctrl+Enter, or ~700ms after the student stops
   typing; a Reset button restores the original (deliberately incomplete,
   `%% TODO`-marked) text. Edits persist per-diagram in the browser's own
   `localStorage` (`lab6-diagram-<index>`) — never uploaded, never graded
   automatically. The Recap section has no diagrams at all, by design — it
   points back at the lecture instead of reproducing its figures.

## Maintainer: comparing student work against reference

1. `src/lab2/solution/lab2_cruise_control_solution.py` is the instructor-only
   reference for Lab 2 — never expose it under `docs/`.
2. `src/lab3/solution/requirements.md` is the instructor-only reference
   answer set for Lab 3 — same rule.
3. For Lab 4, `src/lab4/starter/CruiseControl/` is the reference Scade One
   project/wrapper — populated, working files that double as both starter
   and reference (no separate `solution/`). For Lab 3, use
   **`src/lab3/solution/`**, not `src/lab3/starter/` — both hold the same
   Scade One project, but `starter/`'s `blocks.swan`/`test.swant` are
   flattened out of `assets/`, which breaks Scade One's file discovery
   (the project opens empty there). `solution/` has the correct `assets/`
   layout and is the one that actually works — see `.agents/scade-models.md`.

## Maintainer: generating a Python wrapper for a Scade One model

**Requires a local Scade One installation — cannot be run in this
environment (see `.agents/testing.md`).**
1. `pip install -r requirements.txt` (`ansys-scadeone-core`, pinned `==0.8.2`
   for Lab 3, unpinned for Lab 4 — document this inconsistency, don't
   silently pin it without maintainer confirmation).
2. Lab 3: `py -3 setup_wrapper.py`, run from **`src/lab3/solution/`** (not
   `starter/` — see above), regenerates `counter_wrapper/`,
   `limiter_wrapper/`. Lab 4: run `generate_python_wrapper.bat`
   (regenerates `cc_wrapper/`).
3. Run the corresponding test script: `test_counter.py`/`test_limiter.py`
   for Lab 3 (locally-runnable once wrappers exist); for Lab 4,
   `evaluate_cc_full_report.py` (scenario-CSV-driven, writes `results/summary.csv` +
   charts) or `evaluate_cc_quick_tester.py` (still present, a live demo printout, not an
   assertion-based check).

## Maintainer: publishing a changed lab

1. Edit `docs/labN/lab.md` (the actual published content).
2. If Lab 2, also update `src/lab2/starter/lab2_cruise_control_starter.py`
   AND the `STARTER_CODE` literal in `docs/lab2/index.html` together — they
   must stay identical (see `.agents/architecture.md`).
3. `cd docs && bundle exec jekyll build` (or `serve`) to preview locally
   before pushing.
4. Push to `main` — GitHub Pages republishes from `/docs` (inferred deploy
   mechanism, see `.agents/publishing.md`).

## Maintainer: adding a new lab

Inferred from the existing labs' shared shape — see `.agents/publishing.md`
→ "Adding a new lab". Lab 3 went through this twice in close succession:
first added as a standalone requirements lab (requiring the two existing
Scade One labs to renumber 3.1→4.1, 3.2→4.2 to make room ahead of them),
then — per explicit follow-up user direction — had Lab 4.1's entire Scade
One/Swan/Limiter/Counter content merged into it, retiring Lab 4.1 and
renumbering Lab 4.2 down to plain Lab 4. See `project_docs/changelog.md`'s
two newest entries for the full list of files each pass touched (portfolio
page, both labs' prerequisite text, Firebase `LAB_TITLES` maps in
`docs/admin/index.html`/`docs/account/index.html`, every `.agents/` and
`project_docs/` file that named the old paths).

Lab 6 (reading + hands-on written exercise, no `src/lab6/`) is a worked
example of this procedure done in full within one session: portfolio card
in `docs/index.html`, `lab6` added to both `LAB_TITLES` maps, this file,
`.agents/lab-map.md`, `.agents/architecture.md`, `.agents/domain.md`,
`.agents/verification.md`, `.agents/testing.md`,
`project_docs/labs/lab-6-architecture.md`, and
`project_docs/labs/portfolio-map.md` were all updated together — contrast
with Lab 5 (created earlier the same day), which still lacks its
`LAB_TITLES` entries and a `.agents/workflows.md` section as of this
writing.

## Incomplete/partially documented workflows

- **Updating requirements/traceability**: Lab 2's process (edit lab.md's
  REQ/decision-table/matrix, keep the `req`/`tid` fields in the Python test
  tuples in sync) is inferable from its structure but not written down as a
  maintainer procedure anywhere. Lab 4's Requirements-panel workflow
  (Activity 7A) is described for students but the reference solution itself
  only partially followed it (see `.agents/verification.md`) — there is no
  maintainer note reconciling that gap.
- **Running the cruise-control car simulation end-to-end**: `Simulation.swan`
  wires `Car_design` + `CC_design` together (`node main`), but there is no
  documented command/script that runs this closed-loop simulation
  automatically outside the Scade One simulator UI — `evaluate_cc_quick_tester.py` only drives
  the standalone `cruise_control` wrapper, not the combined car+CC
  simulation.
