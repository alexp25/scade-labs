# Lab map

Published portfolio: https://alexp25.github.io/scade-labs/ (`docs/index.html`
has 4 cards: Lab 1, Lab 2, Lab 3, Lab 4 — all active).

## Active labs

| | Lab 1 | Lab 2 | Lab 3 | Lab 4 |
|---|---|---|---|---|
| Title | Introduction to Software Engineering | Applying the SDLC: Cruise Control Safety System | Software Requirements Engineering, Scade One & Traceability | Implementing a Cruise Control System with Scade One |
| Directory | `docs/lab1/` (no `src/lab1/` — reading + quiz only) | `docs/lab2/` + `src/lab2/` | `docs/lab3/` + `src/lab3/` | `docs/lab4/` + `src/lab4/` |
| Objective | Introduce the IEEE definition of software engineering, the SDLC, safety-critical-system requirements (predictability, traceability), Model-Based Design, and Ansys Scade One, ahead of the hands-on labs | Apply full SDLC (requirements→design→impl→V&V) to a cruise-control state machine, in pure Python | Learn EARS requirement writing, Scade One/Swan basics, and requirement traceability, all on two small components (Limiter, Counter) built and traced within this lab; also write the Cruise Control requirement set (REQ-01/02/04/07/08) used in Lab 4 | Model the full cruise-control system (state machine + PI regulator + car plant) in Scade One, trace REQ-01–REQ-08 to it, and cross-check against Lab 2 |
| Main tech | None — reading + client-side quiz | Python 3 (stdlib only), Skulpt (in-browser Python) | Scade One Student Edition, Swan, Python 3.12 + `ansys-scadeone-core==0.8.2` (Parts 2–7, 9); pen/paper or text editor for the pure-requirements parts (Parts 1, 8) | Same as Lab 3, `ansys-scadeone-core` (unpinned) |
| Student entry point | `docs/lab1/index.html` (instructions + 10-question quiz) | `docs/lab2/index.html` (live CodeMirror+Skulpt editor) | `docs/lab3/index.html` (instructions + two independent auto-graded quizzes) | `docs/lab4/index.html` (instructions + reflection quiz) |
| Starter materials | none | `src/lab2/starter/lab2_cruise_control_starter.py` | `src/lab3/starter/` — `requirements_template.md` (REQ IDs with `TODO` blanks, incl. Activity 9A test-case sketch) **plus** a Scade One project (`demo.sproj`, `blocks.swan`, `test.swant`, `counter_wrapper/`, `limiter_wrapper/`, `test_counter.py`, `test_limiter.py`, `setup_wrapper.py`, `requirements.txt`) — **`blocks.swan`/`test.swant` sit flat here (not under `assets/`), so Scade One does not discover them and this project opens empty; left as-is per maintainer instruction, see `.agents/scade-models.md`** | `src/lab4/starter/CruiseControl/` (`assets/{CC_design,Car_design,Simulation}.swan`, `cc_wrapper/`, `evaluate_cc.py`, `scenarios/*.csv`, `tester.py`, `generate_python_wrapper.bat`, `readme.txt`, `requirements.txt`) — populated, working, no separate `solution/` |
| Solution/reference | none (no exercise, only a quiz with answers embedded in `data-correct` attributes) | `src/lab2/solution/lab2_cruise_control_solution.py` (instructor-only) | `src/lab3/solution/requirements.md` (EARS answer set, unrelated to the Scade project below) **plus** `src/lab3/solution/{demo.sproj, assets/blocks.swan, assets/test.swant, counter_wrapper/, limiter_wrapper/, test_counter.py, test_limiter.py, setup_wrapper.py, requirements.txt}` — the same Scade One project as `starter/`, but with the correct `assets/` layout, so it actually opens in Scade One. **Use this one, not `starter/`, when you need a working project.** | see Starter materials above — `src/lab4/starter/CruiseControl/` doubles as the reference |
| Model files | none | none (pure Python) | `blocks.swan`: `function limiter(...)`, `node counter(...)` + `const init` (no requirement pragmas shipped — Activities 2G/4F have students add their own via the Requirements panel, not committed to this repo) | `CC_design.swan`: `node cruise_control` (nested automaton, `#pragma requirement reQ2` on the top node) + `node regulator` + `node limiter`; `Car_design.swan`: vehicle plant; `Simulation.swan`: closed-loop + open-loop wiring |
| Test/validation mechanism | Single auto-graded quiz (`#intro-quiz`, 10 questions, based on the assigned reading), same `initQuiz()` scoring widget pattern as Lab 4 | Embedded `run_tests()`, 7 hardcoded cases (TC-01…TC-07), PASS/FAIL printed in-browser or via `python lab2_cruise_control_starter.py` | Two auto-graded quizzes (`#ears-pattern-quiz`, Part 1 Activity 1A, 4 questions; `#reflection-quiz`, 7 questions), both wired by a generalized `initQuiz(containerId)` in `docs/lab3/index.html`; plus Scade One test harnesses (`limiter_harness`, `counter_harness` in `test.swant`) and `test_limiter.py`/`test_counter.py` (manual PASS/FAIL, no CI). No automated check of the written REQ IDs or the Activity 9A test-case sketch — instructor review against `src/lab3/solution/requirements.md` | Manual simulation + `evaluate_cc.py`, driven by scenario CSV files under `scenarios/` (writes per-scenario trace CSVs, a `results/summary.csv` PASS/FAIL report, and `results/plots/*.png` charts). `tester.py` (live console printout, no assertions) still exists alongside it. No `.swant` harness ships; `lab.md` Part 5 only briefly mentions Scade One test harnesses |
| Published route | `/lab1/` | `/lab2/` | `/lab3/` | `/lab4/` |
| Status | Active, complete | Active, complete | Active — substantially restructured this session (absorbed the former Lab 4.1's Scade One/Swan/Limiter/Counter content, added a `#pragma requirement`/traceability deep-dive using real `CC_design.swan` excerpts); not yet exercised by a real student | Active, complete but: 4 orphaned images in `img/`, orphaned `lab_old.md`, unpinned dependency version, only 1 of 4 traceability links from Activity 7A actually present in the shipped `.swan` (`#pragma requirement reQ2` on the top node only, and that pragma's casing doesn't match Lab 3's `REQ-02` spelling — pre-existing gap, now explicitly taught as a lesson in both Lab 3 Part 9 and Lab 4 Activity 7A rather than silently left unmentioned) |

Lab 1's source content is `Study_lab 1 2.pdf` (the 10-question quiz) and
`Slides 1 2.pdf` (the lecture slides on IEEE's software engineering
definition, the SDLC, safety-critical-system needs, Model-Based Design, and
Ansys Scade One) — both supplied by the instructor, not committed to the
repo. `docs/lab1/lab.md` synthesizes the slide content into prose sections
and reproduces the quiz verbatim with answers baked into `data-correct`.

## Numbering

This session made two numbering changes, in two passes:

1. **First pass:** the former Lab 3.1 (Scade One basics) and Lab 3.2 (cruise-control model) were renumbered to Lab 4.1/Lab 4.2, to make room for a new Lab 3 (pure requirements engineering) ahead of them.
2. **Second pass (this structure):** Lab 4.1's entire Scade One/Swan/Limiter/Counter content was merged into Lab 3 (per explicit user direction — "lab 3 should contain requirements + Scade One intro + the limiter/counter examples + traceability mechanics"), and Lab 4.1 was retired. Lab 4.2 was renumbered to plain **Lab 4** (no longer needs a decimal, since there is only one Scade One lab left). The portfolio is now **Lab 1 (disabled) / Lab 2 / Lab 3 / Lab 4** — four cards, no decimals.

Both passes **break previously published external links** — `/lab3_1/`, `/lab3_2/`, `/lab4_1/`, `/lab4_2/` all now 404 (GitHub Pages has no redirect mechanism configured in this repo). See `project_docs/changelog.md`'s two newest entries for the full detail of each pass.

## Legacy / superseded (not linked from any published page)

| Path | Tracked? | What it is |
|---|---|---|
| `old/lab2_old/` | Yes | Earlier version of the Lab 2 Python exercise (superseded by `src/lab2/`) |
| `old/scade_demo/` | Yes | Earlier Scade demo/project2 models, predates `src/lab3`/`src/lab4` |
| `scade_demo/` (repo root) | **No** — untracked | Local Scade One codegen job output (`CruiseControl/jobs/codegen_*/...`, a `.zip`) — WIP/scratch, not curriculum content |
