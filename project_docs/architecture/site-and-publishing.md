# Site and publishing architecture

## Publishing root and mechanism

`docs/` is the GitHub Pages publishing root for this repository, published at
`https://alexp25.github.io/scade-labs/` (repo: `github.com/alexp25/scade-labs`).
No `.github/workflows/*.yml`, `CNAME`, or `.nojekyll` file exists anywhere in
the repo (verified by search). This strongly suggests classic GitHub Pages
"Deploy from a branch: `main` / folder `/docs`" — **this is an inference from
the absence of a custom build workflow, not a confirmed reading of the
repository's actual GitHub Settings**, which cannot be inspected from local
files.

## Jekyll configuration vs. actual usage — an important mismatch

`docs/_config.yml` configures:
```yaml
title: SCADE Lab Portfolio 🤖✨
theme: jekyll-theme-cayman
markdown: kramdown
highlighter: rouge
```
`docs/Gemfile` / `docs/Gemfile.lock` pin `jekyll (4.4.1)`,
`jekyll-theme-cayman (0.2.0)`, `webrick (1.9.2)`, `rouge (4.7.0)`.

**However, no page under `docs/` actually uses this theme.** None of the four
`.html` files (`index.html` + 3 lab pages) has Jekyll front matter (`---`) or
Liquid tags (`{{ }}`/`{% %}`), and `docs/_layouts/` does not exist. Every page
is a fully self-contained static HTML document with its own inline
`<style>` block. Running `bundle exec jekyll build` (verified this session,
3 successful runs) produces output that is functionally identical to the
source tree — Jekyll is acting purely as a static-file build/serve tool here,
not a templating engine. A maintainer reading `_config.yml` and expecting
theme-driven page layout would be misled; this is worth knowing before
"fixing" anything theme-related, since there is nothing wired up to fix.

## The actual rendering pattern (identical across all 3 lab pages)

Each `docs/labN/index.html`:
1. Is static HTML with inline CSS (its own page chrome/header/footer).
2. Loads `marked.js` (v9.1.6, cdnjs) and, for Lab 2 only, `highlight.js`
   (11.9.0), CodeMirror (5.65.16), and Skulpt (skulpt.org).
3. On load, `fetch('lab.md')` retrieves the sibling Markdown file and
   `marked.parse(md)` renders it into a content `<div>`.
4. Builds a client-side table of contents from the rendered headings.

**`lab.md` is therefore the single source of truth for each lab's actual
content.** Editing `index.html` only changes the page shell/interactive
widget, never the lesson text itself.

Per-lab widget divergence:
- **Lab 2** adds a live CodeMirror + Skulpt Python editor (`STARTER_CODE`
  literal, "▶ Run" button, PASS/FAIL output pane).
- **Lab 3.1 / 3.2** add a reflection-quiz widget instead (`#reflection-quiz`,
  radio-button questions).

## Root portfolio page (`docs/index.html`)

Static HTML, 4 lab cards:
- Lab 1: `.disabled`, "Coming soon" badge, no `href` — **no `docs/lab1/`
  exists**; do not assume it does when reading older repo docs/comments that
  may still mention it.
- Lab 2 → `href="./lab2/"`
- Lab 3.1 → `href="./lab3_1/"`
- Lab 3.2 → `href="./lab3_2/"`

All three real cards' titles match each target lab's own `lab.md` H1 (verified
by direct comparison). There is no numbering mismatch on the portfolio page
itself (unlike inside `lab3_2/lab.md`'s own prose — see "Corrections made"
below).

## Local preview procedure (verified working this session)

```
cd docs
bundle install        # first time only
bundle exec jekyll serve
```
Then open `http://localhost:4000/`. Documented in `readme_local_setup.txt`
at the repo root; consistent across `README.md`, `readme.txt`, and
`readme_local_setup.txt`.

## Duplicate/at-risk sources of truth

| Pair | Risk | Which one is live |
|---|---|---|
| `docs/lab3_2/lab.md` vs `docs/lab3_2/lab_old.md` | An editor could open the wrong file | `lab.md` — `lab_old.md` is fetched by nothing |
| `src/lab2/starter/lab2_cruise_control_starter.py` vs the `STARTER_CODE` literal in `docs/lab2/index.html` | Editing one without the other desyncs the browser and local-run experience | Both — verified byte-identical (aside from CRLF/LF) this session; **keep them in sync manually, there is no build step that generates one from the other** |
| `readme.txt` vs `readme_local_setup.txt` (repo root) | Both document the same local-run steps independently | Neither is generated from the other |

## Corrections made this session (documentation-only, low-risk, unambiguous)

- `docs/lab3_2/lab.md` referred to its prerequisite lab as "Lab 3" and linked
  `../lab3/` (a directory that doesn't exist — the real directory is
  `lab3_1`) in 7 places, including a broken anchor
  `#part-0--scade-one-orientation` that never existed in `lab3_1/lab.md`.
  Fixed all 7 to say "Lab 3.1" and link `../lab3_1/`.
- `assets/css/syntax.css` was found sitting at the **repository root**
  (left behind by an earlier restructuring pass that moved the rest of the
  Jekyll site into `docs/` but missed this file). Moved into
  `docs/assets/css/syntax.css`. It remains unreferenced by any page (see
  "Known publishing debt" below) — moving it only fixes its *location*, not
  its unused status.

## Known publishing debt (documented, not corrected — needs a maintainer call)

- `docs/assets/css/syntax.css` — unreferenced by any page (no
  `docs/_layouts/`, nothing links it).
- `docs/lab3_1/img/scade_generate_python_wrapper.png` — present, never
  referenced in `lab3_1/lab.md`.
- `docs/lab3_2/img/` — 4 images never referenced at all
  (`scade_create_operator.png`, `scade_create_test_harness.png`,
  `scade_test_harness.png`, `scade_testing.png`) plus 2 more referenced only
  inside HTML comments and therefore never actually rendered
  (`scade_system_model.png`, `scade_create_operator_crop.png`).
- `docs/lab3_2/lab_old.md` — orphaned legacy draft, not deleted (deleting
  legacy content was not explicitly requested).

## Adding a new lab (inferred procedure — not written down elsewhere in the repo)

1. `docs/labN/index.html` (copy an existing lab's shell) + `lab.md` (+`img/`
   if there are screenshots).
2. `src/labN/solution/` (+ `starter/` only if there's a student code stub, as
   in Lab 2 — Lab 3.1/3.2 have none).
3. Add a card to `docs/index.html`.
4. Update `.agents/lab-map.md` and add a `project_docs/labs/` page.
