# Module 2 · Lab 1 — A Configuration Management Plan for a Scade One Project

Published at `/m2/lab1/` (`docs/m2/lab1/`). Lab ID `m2-lab1`. Created
2026-10-29 as a single lab (plan + GitHub); split on 2026-10-30 at the
maintainer's request — the GitHub part and its checker are now
[M2 Lab 2](m2-lab2-github-configuration.md). Decisions behind the layout and the checker:
`.agents/decisions/0003-module-2-labs-and-github-checker.md`.

## Sources

Instructor-supplied, kept unpublished in `project_docs/courses/m2/`:

- `M2 Slides 1.pdf` — Lesson 1 "Configuration Management" (Nirvana Popescu).
  Published copy for the slides viewer: `docs/courses/m2-lab1.pdf` — keep the
  two in sync by hand.
- `SW ENG Module 2.pdf` — module syllabus (Lesson 1: CM Tools, 2 h, "Git lab").
- `828-2012 1.pdf` — IEEE Std 828-2012, university-licensed. Published copy
  `docs/courses/ieee-828-2012.pdf` (maintainer decision, ADR 0003), linked from
  "The IEEE 828 CMP outline" section, which also explains what an annex is. The lab paraphrases Annex D (CMP content areas D.1–D.9),
  8.2.4/8.2.5 (naming, repositories, baselines) and Annex K (build naming).

Instructor brief (paraphrased): CMP draft per IEEE 828 covering identification,
branching, versioning, baselining; put an earlier lab's project under CM;
Word-document output; a select-option quiz ("name the versions like this or
that"); tasks = enrich, complete, quiz; then project + requirements on a
public GitHub repo, with a page checker that requests the repo's status from
GitHub, parses it, and evaluates it.

## Files

| Path | Role | Published |
|---|---|---|
| `docs/m2/lab1/lab.md` | Lesson content (single source of truth) | yes |
| `docs/m2/lab1/index.html` | Shell copied from Lab 5 (`../../` paths, `#cm-quiz`, upload-form CSS) | yes |
| `docs/m2/lab1/cmp-submit.js` | CMP upload form: POSTs the `.docx` to FormSubmit, which emails it to `MENTOR_EMAIL` | yes |
| `docs/m2/lab1/CMP_template_CruiseControl.docx` | Student CMP template (generated) | yes |
| `src/m2/lab1/tools/build_cmp_docs.py` | Generates both `.docx` files from one content definition | no |
| `src/m2/lab1/solution/CMP_CruiseControl_reference.docx` | Instructor reference CMP (generated) | **no — never under `docs/`** |
| `src/m2/lab1/README.md` | Maintainer notes | no |

## Structure

- Context, objectives, a short recap (not a slide reproduction).
- **The Configuration Management Plan:** Annex D outline table; Activities
  1A identification (CI ID convention `CC-<REQ|MDL|TST|GEN|TOOL|VER|DOC>-<nnn>`,
  classify every Lab 4 file as source / generated / record / not-a-CI), 1B
  branching (`main`, `develop`, `feature/REQ-<id>-…`, `release/x.y`), 1C
  versioning (`vMAJOR.MINOR.PATCH[-rcN]` with a worked table), 1D baselining
  (`baseline/req|des|ver-vX.Y` tags + release manifest), 1E complete/enrich
  the Word template and send it, 1F quiz.
- Summary with a "Next" link to M2 Lab 2.

## Quiz (`#cm-quiz`, 10 questions, self-authored from the instructor brief)

Answer key in `data-correct`: `a b c a c b b c d c`. Recorded as
`recordQuizAttempt('m2-lab1', 'cm-quiz', …)`.

## CMP submission (email)

End of Activity 1E: name, email (used by FormSubmit as reply-to), group,
repo URL (optional — students usually have no repo until Lab 2), `.docx` attachment, optional message → `https://formsubmit.co/<MENTOR_EMAIL>`.
**Before the lab is used:** set `MENTOR_EMAIL` in `cmp-submit.js` (currently
the placeholder `xxxx@upb.ro`), then send one test submission and confirm
FormSubmit's activation email at that address. Optional hardening: replace
the address in the `action` URL with FormSubmit's random alias (shown after
activation) so the real address is not visible in the page source.

Fallback: **Email it instead** builds a `mailto:` link to the same
`MENTOR_EMAIL` with subject and body pre-filled; the student attaches the
`.docx` manually (a `mailto:` link cannot carry attachments). Added after
FormSubmit was observed down (HTTP 521) on 2026-10-29.

## Grading model

Automated: the quiz. Manual: the CMP `.docx` content, against
`src/m2/lab1/solution/CMP_CruiseControl_reference.docx`. Whether the plan
was actually carried out is checked in Lab 2. No claim of compliance with
any safety standard is made or implied.

## Validation performed (2026-10-29)

See `.agents/testing.md` → "Module 2 · Lab 1" and "Module 2 · Labs 1–2 —
after the split". Not exercised in a real
browser; not exercised against a real student repository that follows the
lab end-to-end.
