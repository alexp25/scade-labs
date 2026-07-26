# ADR 0001: Canonical documentation lives in `project_docs/`, not `docs/`

**Date:** this session (repository documentation-structure task).

## Context

The task specification asked for concise agent-facing summaries under
`.agents/` and longer canonical documentation under `docs/`. Investigation
(see `.agents/publishing.md`) confirmed `docs/` is the actual GitHub Pages
publishing root for this repository's public Jekyll site — it's what
`https://alexp25.github.io/scade-labs/` serves.

## Decision

Put canonical maintainer/agent documentation under a new top-level
`project_docs/` directory instead, using the same information architecture
requested (`project_docs/architecture/`, `project_docs/labs/`,
`project_docs/verification/`, `project_docs/maintenance/`).

## Why

Putting internal architecture/verification write-ups inside `docs/` would
either (a) get published alongside the student-facing lab pages, mixing
maintainer-only detail (e.g. traceability gap analysis, generated-artifact
boundaries) into the public site, or (b) risk Jekyll attempting to process
unrelated Markdown as site content. `project_docs/` is a sibling of `docs/`
and `src/`, is never referenced by `docs/_config.yml`, and cannot be
confused with the publishing root.

## Consequences

- `.agents/README.md` and `AGENTS.md` point to `project_docs/`, not `docs/`,
  for canonical detail.
- Future agents adding "canonical documentation" per the working rules in
  `AGENTS.md` should default to `project_docs/`, not `docs/`.
