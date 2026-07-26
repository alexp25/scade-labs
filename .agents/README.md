# `.agents/` index

`.agents/` holds concise, agent-facing operational summaries (each file is
meant to be scannable in under a minute). Longer canonical detail — full lab
write-ups, architecture rationale, verification/traceability tables — lives in
[`project_docs/`](../project_docs/), not in `docs/`.

**Why not `docs/`:** `docs/` is the live GitHub Pages publishing root for this
repository's Jekyll site (see `.agents/publishing.md`). Putting internal
documentation there would either get published to students or get swept into
Jekyll's build. See `.agents/decisions/0001-canonical-docs-location.md`.

If `.agents/` and `project_docs/` ever disagree, verify against the actual
files/models/scripts and correct both; until corrected, `project_docs/` is the
intended canonical source.

## Files

- [`architecture.md`](architecture.md) — real repository structure, publishing architecture, source-vs-generated and current-vs-legacy boundaries.
- [`lab-map.md`](lab-map.md) — one row per active lab: objective, tech, files, tests, published route, status.
- [`domain.md`](domain.md) — the project's actual instructional/engineering vocabulary (requirement, decision table, limiter, counter, traceability, etc.).
- [`publishing.md`](publishing.md) — GitHub Pages/Jekyll setup, local preview, per-lab page mechanism, how to add a lab, known publishing debt.
- [`python.md`](python.md) — every maintained Python entry point, starter/solution/browser boundaries, dependencies, expected output.
- [`scade-models.md`](scade-models.md) — Scade One project layout, Swan sources, generated-vs-hand-authored boundary, binary/opaque files.
- [`verification.md`](verification.md) — requirements, decision tables, test↔requirement traceability (explicit vs. inferred), completion criteria, gaps.
- [`workflows.md`](workflows.md) — real end-to-end maintainer/learner workflows with file references.
- [`testing.md`](testing.md) — every verified validation command, working directory, and expected result; explicitly states what does NOT exist (no CI, no linter, no test framework).
- [`integrations.md`](integrations.md) — every real external dependency (CDN JS, Jekyll theme/gems, Ansys package), where it's referenced, and offline limitations.
- [`decisions/`](decisions/) — ADRs for decisions made while building this documentation structure.
