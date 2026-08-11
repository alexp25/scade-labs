# Publishing

## GitHub Pages / Jekyll

- `docs/` is the GitHub Pages publishing root. No `.github/workflows/*.yml`,
  `CNAME`, or `.nojekyll` exists anywhere in the repo — this is almost
  certainly classic GitHub Pages "Deploy from a branch: `main` / `/docs`"
  (**inference**, not confirmed against the actual GitHub repo Settings).
- `docs/_config.yml`: `theme: jekyll-theme-cayman`, `markdown: kramdown`,
  `highlighter: rouge`. `docs/Gemfile`/`Gemfile.lock` pin `jekyll (4.4.1)`,
  `jekyll-theme-cayman (0.2.0)`, `webrick (1.9.2)`, `rouge (4.7.0)`.
- **The theme is configured but not actually used by any page.** No file
  under `docs/` has Jekyll front matter (`---`) or Liquid tags (`{{ }}` /
  `{% %}`), and `docs/_layouts/` does not exist. Jekyll here just serves the
  static files as-is; `bundle exec jekyll build` succeeds but produces output
  functionally identical to the source `docs/` tree.

## Local preview (from `readme_local_setup.txt`)

```
cd docs
bundle install        # first time only
bundle exec jekyll serve
```
Open `http://localhost:4000/`.

## Root portfolio page (`docs/index.html`)

Plain static HTML (no front matter/Liquid). Four lab cards
(`.lab-num` 1/2/3/4), all active: Lab 1 links `./lab1/`, Lab 2 `./lab2/`,
Lab 3 `./lab3/`, Lab 4 `./lab4/` — all match real directories and
titles/H1s in each `lab.md`.

## Per-lab page mechanism

All four lab pages (`docs/lab1/index.html`, `docs/lab2/index.html`,
`docs/lab3/index.html`, `docs/lab4/index.html`) share one pattern: static
HTML shell → `fetch('lab.md')` → render with `marked.js` (loaded from
cdnjs) into `#lab-content`/`#lesson-content`, plus a client-side TOC
builder. **`lab.md` is therefore the actual published content** — editing
`index.html` changes only the page chrome/widget, not the lesson text.

Per-lab widget divergence (not a bug, just different content per lab):
- Lab 1 has only the reading + a single 10-question `#intro-quiz` — no
  other interactive widget, no starter code, no `src/lab1/`.
- Lab 2 additionally embeds a live CodeMirror + Skulpt Python editor.
- Lab 3 embeds **two independent** quiz widgets (`#ears-pattern-quiz` in
  Part 1, `#reflection-quiz` near the end) — `docs/lab3/index.html`'s
  `initQuiz(containerId)` is written to support more than one quiz on the
  same page (each container scopes its own `.quiz-submit`/`.quiz-reset`/
  `.quiz-score` and its questions' radio-button `name` prefixes) — plus a
  third, unrelated fixed widget: the **Requirement Traceability Checker**
  (`#trace-checker-section`), a Skulpt-powered in-browser Python tool that
  parses a pasted/uploaded `blocks.swan` for `#pragma requirement` links
  (mirrors `test_limiter_advanced.py`/`test_counter_advanced.py`'s
  `parse_operator`/`print_requirement_report`, ported to run without file
  I/O). It cannot run the actual generated model — that needs a compiled
  `.dll`, impossible in a browser sandbox — and says so on the page. See
  `docs/lab3/lab.md` Activity 7F and `.agents/integrations.md`.
- Lab 4 embeds a single reflection-quiz widget (same underlying pattern,
  single container).

## Duplicate/at-risk sources of truth

- `docs/lab4/lab_old.md` — an old draft of `lab.md`, **not fetched by any
  `index.html`** (only `lab.md` is). Orphaned; a future editor could
  mistakenly edit it expecting it to affect the site. Left in place (not
  explicitly asked to delete legacy content) but do not edit it expecting any
  effect.
- Lab 2's embedded `STARTER_CODE` in `docs/lab2/index.html` duplicates
  `src/lab2/starter/lab2_cruise_control_starter.py` byte-for-byte (aside from
  CRLF/LF). Keep both in sync if you change either.
- `readme.txt` and `readme_local_setup.txt` (repo root) both independently
  document the same local-run procedure — low risk, but if one changes,
  update the other.
- `docs/admin/index.html` and `docs/account/index.html` each carry their own
  `LAB_TITLES` map (`labId → display title`) — a third independent place lab
  names/IDs live, separate from `docs/index.html`'s cards and each lab's own
  `CURRENT_LAB_ID`. All three must agree on the `labId` strings (`lab2`,
  `lab3`, `lab4`).

## Adding a new lab (inferred safe procedure, based on the existing labs' shared shape — not separately documented anywhere in the repo)

1. Create `docs/labN/` with `index.html` (copy an existing lab's shell) and
   `lab.md`; add `img/` only if you have screenshots.
2. Create `src/labN/` with `solution/` (and `starter/` only if the lab has a
   student code stub, as Lab 2 does — Lab 3 and Lab 4 instead ship a single
   populated `starter/` Scade One project that doubles as the reference;
   Lab 3's `starter/` additionally has a `TODO`-blanked requirements
   template, since part of that lab's deliverable is free text).
3. Add a card to `docs/index.html` (`.lab-num`, title, `href="./labN/"`).
4. If the new lab needs to slot in *before* an existing numbered lab,
   decide whether to renumber the labs after it or use a sub-number/decimal
   scheme — renumbering breaks any already-published external links
   (GitHub Pages has no redirect mechanism here), so this is a real
   trade-off, not just a mechanical choice. If renumbering, every place in
   "Duplicate/at-risk sources of truth" above must be updated together, plus
   every `.agents/`/`project_docs/` file that names the old path.
5. Update `.agents/lab-map.md` and the corresponding `project_docs/labs/`
   page.

## Known publishing debt (verified, not yet fixed unless noted)

- `docs/assets/css/syntax.css` exists but is referenced by no page (no
  `docs/_layouts/`, no page links it) — dead CSS, harmless.
- `docs/lab3/img/scade_generate_python_wrapper.png` — present, never
  referenced in `lab3/lab.md`.
- `docs/lab4/img/` — 4 images never referenced anywhere
  (`scade_create_operator.png`, `scade_create_test_harness.png`,
  `scade_test_harness.png`, `scade_testing.png`), plus 2 more
  (`scade_system_model.png`, `scade_create_operator_crop.png`) referenced only
  inside HTML comments (never actually rendered).
- **Restructured across two sessions (not bug fixes — deliberate, user-approved
  restructures):** the portfolio originally used "3.1"/"3.2" for the two
  Scade One labs (`docs/lab3_1/`, `docs/lab3_2/`). A first pass renumbered
  these to Lab 4.1/Lab 4.2 (`docs/lab4_1/`, `docs/lab4_2/`) to make room for
  a new plain "Lab 3" (requirements engineering) ahead of them. A second
  pass merged Lab 4.1's entire Scade One/Swan/Limiter/Counter content into
  Lab 3, retired Lab 4.1, and renumbered Lab 4.2 down to plain **Lab 4**
  (`docs/lab4/`) — since there is now only one Scade One lab left, it no
  longer needs a decimal. Both passes **break previously published external
  links**: `/lab3_1/`, `/lab3_2/`, `/lab4_1/`, `/lab4_2/` all now 404
  (GitHub Pages has no redirect mechanism configured in this repo). See
  `project_docs/changelog.md`'s newest entries for the full detail of each
  pass.
