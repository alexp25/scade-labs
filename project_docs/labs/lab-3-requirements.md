# Lab 3 — Software Requirements Engineering, Scade One &amp; Traceability

**Published:** `https://alexp25.github.io/scade-labs/lab3/` (`docs/lab3/index.html` + `docs/lab3/lab.md`)
**Source:** `src/lab3/starter/` (requirements template + a populated, working Scade One project), `src/lab3/solution/requirements.md` (instructor reference)

## Purpose

Originally a pure requirements-writing lab (EARS syntax only), **substantially
restructured this session** per explicit follow-up user direction to also
absorb the former Lab 4.1's entire content: Scade One installation, Swan
language basics, building and testing a Limiter (combinatorial) and Counter
(sequential), and — new — an explicit deep dive into how Scade One's
`#pragma requirement` traceability mechanism works, using real excerpts from
this repo's own `CC_design.swan`. Lab 3 now teaches, on two small worked
examples, everything a student needs before tackling the full Cruise Control
system in [Lab 4](lab-4-cruise-control.md): write a requirement, model it,
link it to the model, and turn it into a test case.

## Prerequisites

Recommended, not enforced: [Lab 2](lab-2-sdlc.md) (the informal cruise
control description and REQ-01..06 that Part 8's Cruise Control activity
builds on). Scade One Student Edition install + QuickStart video are Lab 3's
own first Prerequisites step (moved here from the former Lab 4.1 — this is
now the *only* place in the portfolio Scade One gets installed).

## Learning outcomes (quoted, `docs/lab3/lab.md`)

- Recognize the five EARS requirement patterns and pick the right one for a
  given behavior
- Rewrite an informal "SHALL" sentence as a precise EARS requirement
- Derive a complete software requirements set for a small component from its
  informal description
- Create Scade One projects, modules, and operators with typed interfaces
- Implement combinatorial logic (the Limiter) and sequential logic using
  delays (`pre`) (the Counter)
- Simulate models and build automated test harnesses
- Link a requirement ID to a model element via Scade One's Requirements
  panel, and explain what that link actually writes into the `.swan` source
- Explain, precisely, how a REQ ID stays traceable from requirement → design
  element → test case
- Turn a single requirement into a concrete test case (input sequence +
  expected result), in the same shape Lab 4's `evaluate_cc_full_report.py` consumes

## Repository files

| File | Role |
|---|---|
| `docs/lab3/lab.md` | Published lesson (Parts 1–9 — see "Structure" below) |
| `docs/lab3/index.html` | Page shell + generalized `initQuiz(containerId)` wiring two independent quiz widgets |
| `docs/lab3/img/` | 15 screenshots (moved from the former Lab 4.1's `img/`) |
| `src/lab3/starter/requirements_template.md` | Student fill-in template — all REQ IDs pre-listed, responses left as `TODO`, plus an Activity 9A test-case-sketch `TODO` |
| `src/lab3/starter/demo.sproj`, `blocks.swan`, `test.swant`, `counter_wrapper/`, `limiter_wrapper/`, `test_counter.py`, `test_limiter.py`, `setup_wrapper.py`, `requirements.txt` | Scade One project (moved from the former Lab 4.1's `src/lab4_1/starter/`, flattened — `assets/blocks.swan` → `blocks.swan`, `assets/test.swant` → `test.swant`). **This flattening broke Scade One's own convention for discovering `.swan` files — opening this project in Scade One shows it empty.** Left as-is, per maintainer instruction; see `.agents/scade-models.md` |
| `src/lab3/solution/requirements.md` | Instructor reference — full REQ-LIM/REQ-CNT/REQ-01/02/04/07/08 answer set, traceability preview, Activity 9A worked test-case answer |
| `src/lab3/solution/demo.sproj`, `assets/blocks.swan`, `assets/test.swant`, `counter_wrapper/`, `limiter_wrapper/`, `test_counter.py`, `test_limiter.py`, `setup_wrapper.py`, `requirements.txt` | **The same Scade One project as `starter/`, but with the correct `assets/` layout, so it actually opens.** Added this session specifically to fix the `starter/` breakage above without touching `starter/` itself (per explicit maintainer instruction). Use this copy, not `starter/`, whenever you need a working project |

## Structure (9 parts)

| Part | Topic |
|---|---|
| 1 | EARS patterns theory + Activity 1A quiz (auto-graded, 4 questions) |
| 2 | Limiter: write REQ-LIM-01..03, build the operator, Definition-vs-Expression/instance-block Swan concepts, simulate, **link REQ-LIM-01 via the Requirements panel (Activity 2G)** |
| 3 | Limiter test harness (`limiter_harness`) |
| 4 | Counter: write REQ-CNT-01..02, build the operator (sequential, `pre`), simulate, **link both REQ IDs (Activity 4F)** |
| 5 | Counter test harness (`counter_harness`) |
| 6 | Comparing combinatorial vs sequential logic |
| 7 | Code generation + Python wrapper generation + simple `test_limiter.py`/`test_counter.py` (each test tuple carries a `req` field); Activity 7F: run against your own project via `--project-dir`; Activity 7G: `test_limiter_advanced.py`/`test_counter_advanced.py` add a custom requirement-coverage CSV + pass/fail-colored model diagram, since Scade One Student Edition has no built-in equivalent |
| 8 | Cruise Control requirement set — rewrite REQ-01/02/04 as EARS, write new REQ-07/REQ-08, sanity-check against the state table |
| 9 | **"How Traceability Works in Scade One"** (new) — the `#pragma requirement` mechanism explained, a real excerpt from `CC_design.swan` (`reQ2` vs `REQ-02`), "From a requirement to a test case" walkthrough + Activity 9A, and a forward-reference table into Lab 4 |

Plus: Common Errors (moved from the former Lab 4.1, extended with a
requirement-ID-mismatch entry) and a 7-question reflection quiz.

## Requirements / traceability

**This is where REQ-LIM-01..03, REQ-CNT-01..02, and the EARS-form
REQ-01/02/04/07/08 are actually authored** — the first point in the repo
where requirement IDs are created rather than just referenced. It is also
now **the first point where the traceability mechanism itself is taught**,
not just used: Activities 2G and 4F have students link their own
Limiter/Counter to their own written REQ IDs via the Requirements panel,
before Part 9 explains what that click actually wrote into the `.swan`
source and shows the real `reQ2`/`REQ-02` casing gap in `CC_design.swan` as
a worked lesson in traceability discipline. See
`project_docs/verification/requirements-and-traceability.md` for the full
explicit/inferred classification.

## Test/verification procedure

**No automated check of the written requirements, the built Scade One
model's correctness beyond the harness/wrapper tests, or the Activity 9A
test-case sketch.** Automated components:
- `#ears-pattern-quiz` (Part 1, 4 questions) and `#reflection-quiz` (end of
  lesson, 7 questions) — both client-side scored via a shared
  `initQuiz(containerId)` function (`docs/lab3/index.html`), generalized
  this session to host two independent quiz widgets on one page (scoped by
  container id; radio `name` prefixes kept distinct: `a1q*` vs `q*`).
- `limiter_harness`/`counter_harness` (in-tool Scade One simulation) and
  four Python scripts, manual PASS/FAIL print, no assertion framework:
  `test_limiter.py`/`test_counter.py` (simple) and
  `test_limiter_advanced.py`/`test_counter_advanced.py` (same tests, plus
  writes `<project-dir>/results/<operator>_traceability.csv` and a
  `matplotlib`-rendered, pass/fail-colored model diagram — see Activity
  7G). All four accept `--project-dir` (Activity 7F) to run against a
  project generated/copied elsewhere. Both the harness and the Python
  scripts require a local Scade One install to actually run (the Python
  scripts, unlike the harness, can also run against the already-committed
  `solution/` wrapper `.dll`s without one).

Grading the requirements, the Requirements-panel links, and the Activity 9A
test-case sketch is instructor review against `src/lab3/solution/requirements.md`
and the working Scade One project under `src/lab3/solution/` (`starter/`
has the same files but doesn't open in Scade One — see "Repository files"
above).

## Known limitations

- **`src/lab3/starter/` does not open correctly in Scade One** —
  `blocks.swan`/`test.swant` were flattened out of `assets/` during the
  Lab 3/Lab 4 merge, which breaks Scade One's file-discovery convention;
  the project opens empty. Fixed by adding a correctly-laid-out copy under
  `src/lab3/solution/` instead of touching `starter/` (explicit maintainer
  instruction — `starter/` was left as-is).
- Substantially restructured this session — not yet exercised end-to-end by
  a real student in its merged form.
- No automated grading of free-text EARS wording, the Scade One model
  itself, or Requirements-panel link correctness.
- `src/lab3/starter/blocks.swan` carries no `#pragma requirement` pragmas —
  Activities 2G/4F ask students to add their own live in the tool; nothing
  is pre-populated or committable back to this repo from a student's local
  Scade One session. `src/lab3/solution/assets/blocks.swan` **does** carry
  the completed links (`REQ-LIM-01..03`, `REQ-CNT-01/02`) as the instructor
  answer key — previously present under the wrong IDs (`REQ1_Limiter` etc.)
  for the Limiter and missing entirely for the Counter; fixed this session
  (see changelog). `test_limiter.py`/`test_counter.py` now parse and report
  on these links at runtime instead of the traceability only existing
  inside the live Requirements panel.
- REQ-08's exact wording ("safe range") intentionally mirrors REQ-LIM-01..03
  rather than restating a numeric bound, since the actual `max_throttle`
  value lives in the Scade One model (Lab 4), not in this lab.
- One screenshot (`scade_generate_python_wrapper.png`, moved along with the
  rest of `img/`) remains unreferenced in `lab.md` — pre-existing debt,
  carried over from the former Lab 4.1.

## Publishing route

`/lab3/` — see `project_docs/architecture/site-and-publishing.md`.
