# Module 2 · Lab 2 — Putting a Scade One Project Under Configuration on GitHub

Published at `/m2/lab2/` (`docs/m2/lab2/`). Lab ID `m2-lab2`. Created
2026-10-30 by splitting the original single M2 lab at the maintainer's
request: this is its former Part 2, the CM plan stayed in
[M2 Lab 1](m2-lab1-configuration-management.md). Decisions behind the layout
and the checker: `.agents/decisions/0003-module-2-labs-and-github-checker.md`.

## Sources

Same as M2 Lab 1 (Lesson 1 slides; the instructor brief's second half:
"project, requirements, included into GitHub — request status from GitHub;
parser, evaluate input; public GitHub repo ⇒ paste their link into the
checker"). Slides: `docs/courses/m2-lab2.pdf`, a copy of the same deck as
`m2-lab1.pdf`.

## Files

| Path | Role | Published |
|---|---|---|
| `docs/m2/lab2/lab.md` | Lesson content (single source of truth) | yes |
| `docs/m2/lab2/index.html` | Shell copied from M2 Lab 1 (no quiz function, checker CSS) | yes |
| `docs/m2/lab2/repo-checker.js` | GitHub checker (`fetchSnapshot`, pure `evaluateRepo`, UI) | yes |

No `src/m2/lab2/` — there is no student code and no reference solution;
the checker rules are the reference.

## Structure

- Context (link back to Lab 1), objectives, a recap table mapping each CMP
  decision to its GitHub mechanism and to the activity that implements it.
- **Getting Started with Git** (added 2026-10-30 at the maintainer's request;
  numbered Steps, not Activities, so 2A–2E keep their numbers): Step 1
  install (Git for Windows / `winget`, macOS developer tools / Homebrew,
  apt/dnf), Step 2 `git config` (name, email, `init.defaultBranch main` —
  needed so cloning the empty repo in 2A gives `main`, optional
  `core.editor`, how to leave Vim), Step 3 GitHub account + HTTPS sign-in
  (Git Credential Manager on Windows, `gh auth login` on macOS/Linux; PAT
  and SSH mentioned), Step 4 the four places (working tree, staging area,
  local repo, remote) + commit/branch/tag/remote, Step 5 command table,
  Step 6 scratch-repo practice script, and a "When something goes wrong"
  recovery table ending with the CM rule: never rewrite pushed history or
  move baseline/release tags.
- **Put the Cruise Control Project Under Configuration:** 2A repo layout
  (Lab 4 `CruiseControl/` folder kept intact because
  `evaluate_cc_full_report.py` expects `cc_wrapper/` and `scenarios/` beside
  it; plus `requirements/`, `verification/`, `docs/`) and `.gitignore`; 2B
  requirements baseline tag + branch protection; 2C issue → feature branch →
  traced commits → PR → develop → main → `v1.0.0` + GitHub Release (release
  notes carry the Lab 1 Activity 1D manifest); 2D traceability chain; 2E
  checker.
- Summary; hand-in = repository URL with `docs/CMP_CruiseControl.docx`.

## Checker rules (`evaluateRepo`, 14 rules)

public · README.md + .gitignore at root · `requirements/` has a file ·
`*.sproj` + `*.swan` anywhere · file under a `scenarios/` or `tests/` folder ·
`docs|documentation/**/*{cmp,configuration}*.docx` · branches `main` +
`develop` (also accepts `dev`/`development`) · a `feature/*` branch or a merged
PR from one · a `baseline/*` tag · a `vX.Y.Z[-rcN]` tag · ≥1 GitHub Release ·
≥1 merged PR · an issue (not PR) mentioning `REQ-…` · ≥3 commits on the default
branch and ≥50 % mention `REQ-…` or `#n`.

REQ ID regex: `\bREQ-(?:[A-Z]+-)*\d+\b` (matches `REQ-07`, `REQ-LIM-01`,
`REQ-SAFE-021`). API calls per check: 8 (repo, recursive tree, branches,
tags, releases, commits, closed pulls, issues; `per_page=100`, no paging).
Limits: only the default branch's last 100 commits, first 100 of each list.
Recorded as `recordQuizAttempt('m2-lab2', 'repo-check', passed, 14)` (was
`m2-lab1` before the split; the lab was unpublished/uncommitted then, so no
stored progress is affected). Optional token kept in `sessionStorage` under
`m2-lab2-gh-token`.

## Grading model

Automated: the checker (evidence of the CM process exists). It cannot judge
the quality of the plan — that is graded on the Lab 1 `.docx`. No claim of
compliance with any safety standard is made or implied.

## Validation performed

See `.agents/testing.md` → "Module 2 · Lab 1" (checker logic and live API
run, 2026-10-29) and "Module 2 · Labs 1–2 — after the split" (2026-10-30,
including the Git section).
Not exercised in a real browser; not exercised against a real student
repository that follows the lab end-to-end.
