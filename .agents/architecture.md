# Architecture

This is a static-content educational repository — the lab content itself is
served with **no** backend or deployment service beyond GitHub Pages; "the
architecture" is: a Jekyll-built static site + a parallel source tree +
legacy archives. As of ADR 0002
(`.agents/decisions/0002-firebase-backend-for-auth-and-progress.md`), the
site additionally has one external backend, added client-side only:
**Firebase** (Authentication + Firestore), used solely for optional login,
progress tracking, and the admin panel — see "Backend (Firebase)" below. Lab
content itself remains fully public and does not require login.

## Real repository structure

```
scade-labs/
├── README.md, readme.txt, readme_local_setup.txt   root pointers + local-run instructions
├── AGENTS.md, CLAUDE.md, .agents/, project_docs/    agent/maintainer documentation (this tree)
├── docs/                 GitHub Pages publishing root (Jekyll site) — PUBLIC
│   ├── Gemfile, Gemfile.lock, _config.yml           Jekyll/theme config
│   ├── index.html                                    portfolio page (static HTML, no front matter)
│   ├── assets/css/syntax.css                         Rouge syntax-highlight CSS (unreferenced by any page — see publishing.md)
│   ├── lab2/{index.html, lab.md}                     Lab 2 page (no img/)
│   ├── lab3_1/{index.html, lab.md, img/}              Lab 3.1 page
│   ├── lab3_2/{index.html, lab.md, lab_old.md, img/}  Lab 3.2 page (lab_old.md is unused/orphaned)
│   ├── assets/js/{firebase-config.js, firebase-client.js, auth-header.js}  Firebase bootstrap + shared auth/tracking widget (ADR 0002)
│   ├── account/index.html                            login/register + "my progress" page
│   └── admin/index.html                               admin-only progress view (protected by Firestore rules, not by hiding this URL)
├── firestore.rules       Firestore Security Rules source of truth — hand-pasted into the Firebase console, no deploy pipeline (ADR 0002)
├── src/                  lab source code — NOT published, not linked from docs/
│   ├── lab2/{starter, solution, README.md, .gitignore}
│   ├── lab3_1/solution/  (Swan model + Python wrapper, no starter/)
│   └── lab3_2/solution/CruiseControl/  (Swan model + C/Python wrapper, no starter/)
├── old/                  tracked legacy archive (old/lab2_old/, old/scade_demo/) — superseded, not linked from any published page
└── scade_demo/           untracked local Scade One codegen job output at repo root — not part of the curriculum, left as-is
```

## Backend (Firebase)

Per ADR 0002, `docs/` now optionally talks to a Firebase project client-side
(Firebase Web SDK loaded from `gstatic.com` as ES modules — no bundler, no
Firebase CLI, no build step). This does not change the Jekyll/static-hosting
model above; it is an additional runtime dependency loaded by the browser.

- **Auth**: Firebase Authentication, email/password only.
- **Data** (Firestore): three collections — `profiles/{uid}` (email,
  `isAdmin` flag), `labOpens/{uid}_{labId}` (per-user, per-lab open counts),
  `quizAttempts/{autoId}` (append-only score log for quizzes and Lab 2's
  code-run "test" results).
- **Admin model**: `isAdmin` can only be set to `true` via a maintainer
  manually editing the document in the Firebase console — no application
  code path can set it, so a client can never self-promote. Every read of
  another user's data is gated by `firestore.rules`' `isAdmin()` function,
  which re-derives admin status from the caller's own `profiles` document on
  the server side. `docs/admin/index.html`'s client-side redirect/checks are
  a UX convenience, not the actual security boundary.
- **Lab content stays public**: login is required only to record progress
  and to view `/admin/`; no lab page redirects anonymous visitors.
- Full setup/operational detail: `project_docs/integrations/firebase.md`.

## Publishing architecture

`docs/` is served by GitHub Pages. No `.github/workflows/`, `CNAME`, or
`.nojekyll` file exists, so this is almost certainly the classic "Deploy from
branch `main` / folder `/docs`" GitHub Pages mode (inference from absence of a
build workflow — not confirmed against the actual GitHub repo settings).

Jekyll (`jekyll-theme-cayman`, configured in `docs/_config.yml` /
`docs/Gemfile`) is present but **not actually applied to any page**: no page
under `docs/` has YAML front matter or Liquid tags (`{{ }}`/`{% %}`), and
`docs/_layouts/` does not exist. Every `.html` file (portfolio + 3 lab pages)
is a fully self-contained static HTML document with inline `<style>` and a
client-side `fetch('lab.md')` + `marked.js` render step. Jekyll here mainly
acts as a static-file build/serve tool, not a templating engine. Full detail:
[`publishing.md`](publishing.md).

## Source-vs-generated boundary

- **Hand-authored, edit freely:** `.swan`/`.swant` files, `.sproj` (plain JSON
  project manifests), `lab.md`, lab `index.html` shells, `setup_wrapper.py`,
  `test_counter.py`/`test_limiter.py`/`tester.py`, `generate_python_wrapper.bat`,
  `readme.txt`, `requirements.txt`.
- **Tool-generated, do not hand-edit:** `*_wrapper.py` (`counter_wrapper.py`,
  `limiter_wrapper.py`, `cc_wrapper.py`), `cc_wrapper.c`, `cc_wrapper.def`,
  `*.dll`, `py_wrapper_files.txt`, `swan_cg_files.txt` — all identified by an
  explicit `generated by PyScadeOne Wrapper 1.0` banner as their first line (or,
  for the manifests, by content matching the generator's own output list).
  `swan_config.h` is Ansys-supplied vendor runtime code (copyright header, no
  student-facing edit activity). `resources/main_inputs.sd` is a binary
  Scade One "SimulationData" resource, not hand-editable text.
  Full detail: [`scade-models.md`](scade-models.md).

## Current vs. legacy boundary

- **Current/active:** `docs/lab2/`, `docs/lab3_1/`, `docs/lab3_2/` and their
  matching `src/lab2/`, `src/lab3_1/`, `src/lab3_2/` — linked from
  `docs/index.html`.
- **Legacy/out of scope:** `old/lab2_old/` and `old/scade_demo/` (tracked,
  superseded), and root `scade_demo/` (untracked local SCADE codegen job
  output). None are referenced from any published page (verified: no
  `old/`/`scade_demo` hits anywhere under `docs/`).
- **Orphaned but still inside the published tree:** `docs/lab3_2/lab_old.md`
  is a stale earlier draft of `lab.md`, not fetched by any `index.html`
  (only `lab.md` is fetched) — a latent risk if a future editor edits the
  wrong file. Left in place (not explicitly asked to delete legacy content).

## Constraints agents must preserve

- Each lab's `lab.md` is the single source of truth for its content — its
  sibling `index.html` only provides the page shell, quiz/editor widget, and
  `fetch('lab.md')` call. Never edit rendered/cached HTML output as if it were
  source.
- Lab 2's browser-embedded `STARTER_CODE` (in `docs/lab2/index.html`) is
  currently a byte-for-byte duplicate (aside from CRLF/LF) of
  `src/lab2/starter/lab2_cruise_control_starter.py` — if you change one, change
  the other.
- Never place instructor solution content (`src/*/solution/`) under `docs/`.
- Never hand-edit generated Scade One wrapper/codegen output (see above).
