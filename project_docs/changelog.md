# Changelog

Progress-tracking log of substantive changes to the lab content and its
maintainer documentation. One entry per work session. Newest first.

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
