# Report: Lab 3/4 restructuring around requirements, EARS, and traceability

Concise, requirement-by-requirement summary of the restructuring requested in
the original activity notes (Activity 2-3, "Simulation → Debug", requirements
engineering for Lab 3, splitting requirements-writing from implementation).
For full session-by-session detail (files touched, validation performed,
open items), see `project_docs/changelog.md` — this report is the map from
"what was asked for" to "where it landed," not a replacement for it.

## Starting point vs. end state

| | Before | After |
|---|---|---|
| Lab 3 | Scade One installation + Swan basics + Limiter/Counter modeling (no requirements content) | Requirements engineering (EARS) + Scade One/Swan basics + Limiter/Counter modeling **+ traceability, applied to Limiter/Counter and explained via real `.swan` source** |
| Lab 3.2 / Lab 4 | Cruise Control modeling only, one `#pragma requirement` link present out of the 7+ the activity described | Cruise Control modeling **+ traceability applied**, cross-referencing the requirement set Lab 3 now teaches how to write |
| Requirements | Existed only informally in Cruise Control's `lab.md` prose (REQ-01/02/04) | EARS-authored REQ set for Limiter (REQ-LIM-01..03), Counter (REQ-CNT-01..02), and Cruise Control (REQ-01/02/04/07/08), each traced into the Swan source |
| Traceability | Not taught; the one existing `#pragma requirement reQ2` link had a casing bug nobody had flagged | Taught explicitly (the mechanism, and the `reQ2`/`REQ-02` bug as a worked lesson), applied by students in-tool, and checkable by a script |

## Requirement-by-requirement

**T1 — new Lab 3: requirements for Limiter, Counter, Cruise Control; EARS; safety requirements; traceability + traceability matrix.**
Delivered as Lab 3's Parts 1–9 (`docs/lab3/lab.md`): EARS pattern theory +
quiz (Part 1), Limiter requirements → build → trace (Parts 2–3), Counter
requirements → build → trace (Parts 4–5), combinatorial-vs-sequential
comparison (Part 6), code generation + Python test scripts (Part 7), Cruise
Control requirement set in EARS form (Part 8), and a dedicated "How
Traceability Works in Scade One" part (Part 9) that reads real `#pragma
requirement` syntax out of this repo's own `CC_design.swan`, including its
casing bug, rather than describing the mechanism abstractly. The
SCADE-specific EARS course link was adapted, not copied — Lab 3 only teaches
the patterns (Ubiquitous/Event-driven/State-driven/Optional-feature/
Unwanted-behavior) that apply to Scade One's own requirements workflow.

*Not delivered as a separate artifact:* a formal traceability matrix
document. Traceability is instead demonstrated in-tool (Scade One's
Requirements panel) and checked directly against the `.swan` source (see
"traceability tooling" below) — the matrix exists implicitly as the set of
resolved `REQ ID → node` links, not as a standalone spreadsheet/table
artifact. Flagging this as an open gap against the original ask if a
standalone matrix document is still wanted.

**T1.1/T1.2/T1.3 — think about requirements; derive design and tests
independently; generate CSV test scenarios.**
Requirements-first ordering is now structural: each Lab 3 component (Limiter,
Counter) has students write the REQ IDs *before* building the operator, and
Lab 4's Cruise Control model is implemented against the REQ set Lab 3 already
produced. Test-case derivation from a requirement is taught explicitly (Lab 3
"From a requirement to a test case," working REQ-01 into a 2-row scenario
matching the real `tc03_brake_suspends.csv`, then Activity asks the student
to derive REQ-07's case themselves). CSV test scenarios exist for Cruise
Control (`src/lab4/starter/CruiseControl/scenarios/*.csv`, one file per test
case) and as generated traceability CSVs for Limiter/Counter
(`results/<operator>_traceability.csv`, produced by the advanced Python test
scripts).

**T2 — Lab 3.1/3.2 become Lab 4; new Lab 3 teaches requirements before
implementation; Lab 4 does implementation + traceability "applied."**
Done, in two renumbering passes (see `.agents/lab-map.md` "Numbering" and the
two oldest `changelog.md` entries for the mechanics): former Lab 3.1 → Lab
4.1 → merged into Lab 3; former Lab 3.2 → Lab 4.2 → plain Lab 4. Final shape:
**Lab 3** = requirements + Scade One/Swan setup + Limiter/Counter (small,
fully worked example of requirements → design → trace, so students see the
whole cycle once before tackling the larger system) + Cruise Control
requirement set. **Lab 4** = Cruise Control implementation, with traceability
applied against the Lab 3 requirement set (Activity 7A) and its own
worked-example cross-reference back to Lab 3 Part 9.

**Activity 1A as a quiz; requirement → test/traceability mapping made
explicit.**
Both done as a same-session follow-up: Activity 1A converted from free-text
to an auto-graded 4-question quiz; a new subsection plus Activity 9A
(renumbered from 5A) walks through deriving a test case from a requirement,
answering "how do these requirements map to testing and traceability"
directly rather than leaving it implicit.

## Traceability tooling (beyond what the notes asked for)

Two things were built that go past the literal request but serve it:

1. **Python traceability report** — `test_limiter.py`/`test_counter.py`
   (`_advanced` variants) parse `blocks.swan`'s `#pragma requirement` links,
   report PASS/FAIL per requirement (not just per test case), write a
   traceability CSV, and render a pass/fail-colored model diagram — filling
   the gap that Scade One Student Edition has no built-in coverage report.
2. **In-browser traceability checker** (`docs/lab3/index.html`) — lets a
   student upload/paste their own `blocks.swan` and see which REQ IDs
   resolve to which node, client-side (Skulpt), without needing Scade One
   installed. Explicitly scoped to traceability only — it cannot run the
   real compiled model in a browser (native `.dll`, no browser Python engine
   supports that); the page says so.

## Open items (not silently dropped, tracked for the maintainer)

- No standalone traceability-matrix *document* — traceability is queryable
  (in-tool panel, generated CSVs, the browser checker) but not rendered as a
  single matrix table. Confirm whether that's sufficient or a literal matrix
  artifact is still wanted.
- Cruise Control's own `CC_design.swan` still ships the pre-existing
  `#pragma requirement reQ2` casing bug unfixed (would require editing a
  diagram-format `.swan` file without a local Scade One install to verify) —
  kept intentionally as a live, real example of what Part 9 teaches, called
  out by name in both Lab 3 Part 9 and Lab 4 Activity 7A.
- `ansys-scadeone-core` remains unpinned in Lab 4's `requirements.txt`.
- CI/CD "upload Scade design, evaluate remotely" (from the raw notes) is not
  addressed by this restructuring — no CI pipeline exists in this repo
  (`AGENTS.md` confirms no `.github/workflows/`). Flagged as a genuinely
  separate, not-yet-started item, not something this pass silently punted on.
- The ISI lecture on requirements engineering (mentioning SCADE) referenced
  in the notes was not sourced/embedded — Lab 3's EARS content is instead
  built from the Ansys course link plus original material.

## Validation

Same caveats as every entry in `project_docs/changelog.md`: no local Scade
One install in this environment, so no lab's Scade One
modeling/simulation/code-generation was executed here. What *was* run and
verified: `bundle exec jekyll build`, Python test scripts against the
committed `.dll` reference builds (`src/lab3/solution/`), and the browser
traceability-checker's Python logic round-tripped through real CPython
outside the browser. See `.agents/testing.md` for the authoritative,
currently-accurate list of what "validated" means per artifact type in this
repo.
