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

## Local preview (from `readme_local_setup.txt`, verified working this session)

```
cd docs
bundle install        # first time only
bundle exec jekyll serve
```
Open `http://localhost:4000/`. `bundle exec jekyll build` was run twice during
this session's restructuring and once after the lab3_2 link fixes — all three
succeeded with only pre-existing Sass deprecation warnings from the
`jekyll-theme-cayman` gem itself (unrelated to this repo's content).

## Root portfolio page (`docs/index.html`)

Plain static HTML (no front matter/Liquid). Four lab cards
(`.lab-num` 1/2/3.1/3.2): Lab 1 is rendered `.disabled` with a "Coming soon"
badge and no href (lines ~296-312) — there is no `docs/lab1/` and none should
be assumed to exist. Labs 2/3.1/3.2 link `./lab2/`, `./lab3_1/`, `./lab3_2/`
— all match real directories and titles/H1s in each `lab.md`.

## Per-lab page mechanism

All three lab pages (`docs/lab2/index.html`, `docs/lab3_1/index.html`,
`docs/lab3_2/index.html`) share one pattern: static HTML shell →
`fetch('lab.md')` → render with `marked.js` (loaded from cdnjs) into
`#lab-content`/`#lesson-content`, plus a client-side TOC builder. **`lab.md`
is therefore the actual published content** — editing `index.html` changes
only the page chrome/widget, not the lesson text.

Per-lab widget divergence (not a bug, just different content per lab):
- Lab 2 additionally embeds a live CodeMirror + Skulpt Python editor.
- Lab 3.1 / 3.2 additionally embed a reflection-quiz widget.

## Duplicate/at-risk sources of truth

- `docs/lab3_2/lab_old.md` — an old draft of `lab.md`, **not fetched by any
  `index.html`** (only `lab.md` is). Orphaned; a future editor could
  mistakenly edit it expecting it to affect the site. Left in place (not
  explicitly asked to delete legacy content) but do not edit it expecting any
  effect.
- Lab 2's embedded `STARTER_CODE` in `docs/lab2/index.html` duplicates
  `src/lab2/starter/lab2_cruise_control_starter.py` byte-for-byte (verified
  this session, aside from CRLF/LF). Keep both in sync if you change either.
- `readme.txt` and `readme_local_setup.txt` (repo root) both independently
  document the same local-run procedure — low risk, but if one changes,
  update the other.

## Adding a new lab (inferred safe procedure, based on the existing 3 labs' shared shape — not separately documented anywhere in the repo)

1. Create `docs/labN/` with `index.html` (copy an existing lab's shell) and
   `lab.md`; add `img/` only if you have screenshots.
2. Create `src/labN/` with `solution/` (and `starter/` only if the lab has a
   student code stub, as Lab 2 does — Lab 3.1/3.2 do not).
3. Add a card to `docs/index.html` (`.lab-num`, title, `href="./labN/"`).
4. Update `.agents/lab-map.md` and the corresponding `project_docs/labs/`
   page.

## Known publishing debt (verified, not yet fixed unless noted)

- `docs/assets/css/syntax.css` exists but is referenced by no page (no
  `docs/_layouts/`, no page links it) — dead CSS, harmless. *(This file was
  found at the repo root during this session — misplaced from an earlier
  restructure — and has been moved into `docs/assets/css/` to keep it inside
  the publishing root where the rest of the Jekyll site lives; it remains
  unreferenced.)*
- `docs/lab3_1/img/scade_generate_python_wrapper.png` — present, never
  referenced in `lab3_1/lab.md`.
- `docs/lab3_2/img/` — 4 images never referenced anywhere
  (`scade_create_operator.png`, `scade_create_test_harness.png`,
  `scade_test_harness.png`, `scade_testing.png`), plus 2 more
  (`scade_system_model.png`, `scade_create_operator_crop.png`) referenced only
  inside HTML comments (never actually rendered).
- **Fixed this session:** `docs/lab3_2/lab.md` previously linked to a
  non-existent `../lab3/` path (and a non-existent `#part-0--scade-one-orientation`
  anchor) in 7 places, calling its prerequisite "Lab 3" instead of "Lab 3.1"
  (the actual directory name). Corrected to `../lab3_1/` / "Lab 3.1" throughout.
