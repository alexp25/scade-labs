# Testing / validation

**No linter, formatter, static type checker, test framework (pytest, unittest
runner, etc.), or CI workflow exists in this repository.** Do not invent one.
All "tests" below are plain scripts a human runs and reads printed PASS/FAIL
text from.

## Root site build

- **Working directory:** `docs/`
- **Prerequisites:** Ruby + Bundler (available in this environment —
  `bundle exec jekyll build --destination <tmp>`)
- **Expected result:** builds without error; output tree mirrors `docs/`
  (portfolio `index.html` + `lab1/`, `lab2/`, `lab3/`, `lab4/` each with
  `index.html`+`lab.md`).
- **Actually run in the Lab-3-restructuring session (2026-08-10):** yes,
  after both the initial renumbering pass and the follow-up pass that merged
  the former Lab 4.1 into Lab 3 — succeeded both times. Only output was
  pre-existing Sass deprecation warnings from the `jekyll-theme-cayman` gem
  itself (`@import`/`invert()` deprecations), unrelated to this repo's own
  content. Output tree confirmed to contain exactly `lab2/`, `lab3/`,
  `lab4/` (no stray `lab3_1/`, `lab3_2/`, `lab4_1/`, or `lab4_2/`). Temp
  output directories were deleted after inspection, not committed.
- **Actually run in the Lab-1-creation session (2026-08-11):** yes —
  `bundle exec jekyll build --destination <tmp>` succeeded (same
  pre-existing Sass deprecation warnings only), and the output tree was
  confirmed to contain `lab1/index.html` + `lab1/lab.md`. Temp output
  directory deleted after inspection, not committed.

## Link/asset integrity

- **Working directory:** `docs/`
- **Command:** grepped every relative `href="./...">` in the 4 `.html`
  pages and confirmed each target directory exists; grepped every
  `img/*.png` reference in each `lab.md` (Lab 2 has no `img/`) and confirmed
  each file exists on disk; grepped every `../labN/` cross-link in
  `lab3/lab.md`/`lab4/lab.md` and confirmed each target directory exists.
- **Actually run in the Lab-3-restructuring session (2026-08-10):** yes —
  all portfolio-card hrefs (`./lab2/`, `./lab3/`, `./lab4/`) resolve; all
  cross-lab links (`../lab2/`, `../lab3/`, `../lab4/`, including in-page
  anchor links from Lab 3 into Lab 4's Activity 7A heading and vice versa)
  resolve; every `img/*.png` reference in Lab 3/Lab 4's `lab.md` resolves to
  a real file. Anchor slugs were computed by hand against the `slugify()`
  logic in each `index.html` (lowercase, strip non-word/space/hyphen chars,
  collapse whitespace to a single hyphen) — not verified by actually loading
  the rendered page in a browser.

## Lab 2 — Python (RUN THIS SESSION — passed)

- **Working directory:** repo root (no install needed — stdlib only)
- **Prerequisites:** Python 3 (verified with the environment's Python 3.11.3;
  the repo does not pin a specific version for Lab 2)
- **Commands and actual output:**
  ```
  python src/lab2/solution/lab2_cruise_control_solution.py
  ```
  → all 7 tests PASS, `VALIDATION: ALL REQUIREMENTS MET.` (verified this
  session, exact transcript in `project_docs/labs/lab-2-sdlc.md`).
  ```
  python src/lab2/starter/lab2_cruise_control_starter.py
  ```
  → 3/7 PASS, 4/7 FAIL (TC-01, TC-02, TC-04, TC-06), `VALIDATION: ISSUES
  FOUND` — expected, since the starter's function body is an unimplemented
  stub. This confirms the test harness itself works correctly and
  discriminates a real implementation from a stub.

## Lab 3 — requirements text (no automated test) + Scade One Python wrappers

- Lab 3's *requirements* deliverable is free-text markdown
  (`src/lab3/starter/requirements_template.md` filled in, graded against
  `src/lab3/solution/requirements.md`). There is no script or harness to
  run for this part — the automated components are two in-page quizzes
  (`#ears-pattern-quiz` for Activity 1A, `#reflection-quiz` at the end),
  both client-side scored via a shared `initQuiz(containerId)` function in
  `docs/lab3/index.html`, same underlying mechanism as Lab 4's single quiz
  but generalized to host two independent widgets on one page. Neither quiz
  checks the student's own written REQ IDs or test-case sketch — both are
  fixed-answer comprehension checks. Both markdown files are plain text; no
  syntax to validate beyond "the file parses as markdown."
- Lab 3's *Scade One modeling* deliverable (Limiter, Counter, and their
  Python wrapper tests): regenerating the wrapper (`setup_wrapper.py`) needs
  the proprietary Scade One Student Edition install and cannot be done in
  this environment (`python -c "import ansys.scadeone.core"` →
  `ModuleNotFoundError: No module named 'ansys'`). **But** `src/lab3/solution/`
  already ships a pre-built `limiter_wrapper/limiter_wrapper.dll` and
  `counter_wrapper/counter_wrapper.dll` committed alongside the generated
  `.py` wrappers, and those wrappers load the `.dll` directly via `ctypes`
  — they do **not** import `ansys` at runtime, only `setup_wrapper.py` (the
  regeneration step) does. So all four test scripts (`test_limiter.py`,
  `test_counter.py`, and their `_advanced` counterparts) **can** and
  **were** actually run in this environment against the committed solution
  artifacts:
  - **Actually run this session (2026-08-10, updated):**
    `python test_limiter.py` / `python test_counter.py` (simple — cycle +
    `[req] ... PASS/FAIL` print, no `blocks.swan` parsing) both printed
    `ALL PASS`. `python test_limiter_advanced.py` /
    `python test_counter_advanced.py` (`PYTHONIOENCODING=utf-8` needed —
    the scripts print a `→` arrow character the default Windows console
    codepage (cp1252) can't encode; this is cosmetic, pre-existing, and
    unrelated to correctness) each printed a "REQUIREMENT TRACEABILITY"
    report (parsed live from `assets/blocks.swan`'s `#pragma requirement`
    annotations) showing `REQ-LIM-01/02/03` and `REQ-CNT-01/02` each
    resolved to the diagram node(s) that implement them, followed by
    `ALL PASS` on every test case, then wrote
    `results/limiter_traceability.csv` / `results/counter_traceability.csv`
    (one row per test case: `tid`, `req`, `nodes`, `inputs`, `expected`,
    `actual`, `status` — same shape as Lab 4's `results/summary.csv`) and
    rendered `results/limiter_diagram.png` / `results/counter_diagram.png`
    with `matplotlib` — one box per `blocks.swan` diagram node, laid out
    using the node's own `"xy"` pragma coordinates and colored green/red by
    whether the requirement it's linked to passed or failed (gray if
    untraced). This is a custom stand-in for the requirement-coverage
    report/colored-diagram view Scade One Student Edition doesn't provide;
    see `docs/lab3/lab.md` Activity 7G. Confirmed by inspection (`Read` on
    both CSVs and both PNGs) that the output matches the reference model:
    3/3 and 4/4 rows `PASS`, all boxes green, no red or unexpectedly-gray
    requirement-tagged nodes.
  - **`--project-dir` (Activity 7F) confirmed working:** copied
    `src/lab3/solution/`'s `assets/`, `limiter_wrapper/`, and
    `counter_wrapper/` into a scratch folder outside the repo and ran
    `python test_limiter.py --project-dir <scratch-folder>` (from the
    simple script) and `python test_limiter_advanced.py --project-dir
    <scratch-folder>` (from the advanced one) — both found the wrapper and
    `blocks.swan` at the given path instead of next to the script, ran
    `ALL PASS`, and (advanced) wrote `<scratch-folder>/results/*` instead
    of the repo's own `results/` — i.e. a student pointing this at their
    own generated/uploaded project works and doesn't touch the repo's
    reference output.
  - **Also run against `src/lab3/starter/`:** no `.dll` exists there (never
    generated), so all four scripts fail at the wrapper import as
    expected — but the advanced scripts' traceability report still runs
    first (it only reads `blocks.swan`, not the `.dll`) and correctly
    prints `NOT TRACED` for every expected REQ ID, since the starter's
    `blocks.swan` intentionally ships without `#pragma requirement` links
    (those are added by Activities 2G/4F, which this repo can't perform
    without the live Scade One Requirements panel). The CSV/diagram step is
    never reached in this case since it runs after the (missing) wrapper
    import.
  - `python -m py_compile` was also run across every `.py` file in
    `src/lab3/starter/`, `src/lab3/solution/`, and
    `src/lab4/starter/CruiseControl/` (including the generated
    `counter_wrapper.py`/`limiter_wrapper.py`/`cc_wrapper.py`, and
    `evaluate_cc_full_report.py`) — all parse with no syntax errors.
  - **Not verified this session:** Lab 4's `evaluate_cc_full_report.py` (needs
    `matplotlib`, not confirmed installed) and the Scade One model/GUI
    itself (see below) — only Lab 3's already-generated wrapper `.dll`s
    were exercised.
  - **Full regeneration procedure** (from the repo's own
    `readme.txt`/`generate_python_wrapper.bat`, not needed for the above
    but required if the model changes and the wrapper needs rebuilding):
    1. Install Scade One Student Edition.
    2. `pip install -r requirements.txt` inside **`src/lab3/solution/`**
       (not `starter/` — that copy's `blocks.swan`/`test.swant` are
       flattened out of `assets/` and won't open in Scade One, see
       `.agents/scade-models.md`) or `src/lab4/starter/CruiseControl/`
       (Lab 4's now also installs `matplotlib`).
    3. Run `setup_wrapper.py` from `src/lab3/solution/` (Lab 3) or
       `generate_python_wrapper.bat` (Lab 4) to regenerate the wrapper +
       `.dll`.
    4. `python test_counter.py` / `python test_limiter.py` (Lab 3) — expect
       printed PASS for all cases (hardcoded expected values documented in
       `.agents/python.md`).
    5. `python evaluate_cc_full_report.py` (Lab 4) — reads `scenarios/*.csv`, expects a
       `"VALIDATION: ALL REQUIREMENTS MET."` banner over the checkpoint
       rows, `results/summary.csv`, and `results/plots/*.png`. `python
       evaluate_cc_quick_tester.py` still exists separately — prints a live 1000-cycle trace
       with no pass/fail signal, visual inspection only.

## Scade One model simulation itself

Cannot be run or verified from this environment — requires the Scade One
desktop application and a license/install, neither of which is available
here. The expected values documented per-activity in `docs/lab3/lab.md`
and `docs/lab4/lab.md` (e.g. "Expected output: `value_out = 100.0`") are
the repository's own stated expectations, not independently re-verified by
this session. The `#pragma requirement` traceability links Activities
2G/4F/7A ask students to create via the live Requirements panel likewise
cannot be added or verified here — Lab 3 Part 9 and Lab 4 Activity 7A's
discussion of the `CC_design.swan` excerpt instead uses the file already
committed to this repo as evidence.

## Lab 6 — quiz is auto-graded server-uninvolved; Parts 1–2's diagrams are self-graded client-side; Part 2's written tables are not

**Current structure (as of the 2026-09-24 restructuring — see
`project_docs/changelog.md`): two diagram activities, Part 1 (Activity 1A,
9 nodes/11 expected edges) and Part 2 (Activity 2D, 11 nodes/14 expected
edges). An earlier revision had three diagram activities across three
parts; the log entries below predate the restructuring and describe that
earlier shape — kept as a historical record of what was actually run, not
edited to match the current structure.**

- Lab 6's Part 2 written component/interface tables are free-text
  markdown — no script or harness to run, same completion model as Lab 3's
  requirements text and all of Lab 5. The diagrams (Activities 1A/2D) are
  a different case: each is a Drawflow canvas with a **✓ Check** button
  that self-grades the student's connections against the
  ```` ```flowgraph ```` fence's own `expected` edge list, entirely
  client-side (see `project_docs/labs/lab-6-architecture.md` →
  "Auto-grading" for exactly how). The other automated component is the
  client-side `#architecture-quiz` (self-authored, not from an
  instructor-supplied answer key).
- **Actually run this session (2026-09-24, part-removal/renumbering
  revision):** re-ran the same Node JSON-validation script described below
  — now 2 blocks (was 3): block 1 (Part 1) 9 nodes/11 expected edges,
  block 2 (Part 2) 11 nodes/14 expected edges, both valid, every
  `expected` pair resolving to a real node key. Extracted both inline
  `<script>` blocks from `docs/lab6/index.html` and syntax-checked each
  with `new Function(...)` — both parse. `bundle exec jekyll build
  --destination <tmp>` succeeded — same pre-existing Sass warnings only.
- **Actually run this session (2026-09-24, Drawflow revision):**
  - Confirmed `drawflow@0.0.60` exists on jsdelivr and ships
    `dist/drawflow.min.js` + `dist/drawflow.min.css` (checked via the
    jsdelivr package-data API) before pinning the CDN URLs in
    `docs/lab6/index.html`.
  - Fetched Drawflow's real `addNode`/`addConnection`/export source from
    GitHub to confirm the exact API shapes (`addNode` parameter order, the
    `{node, output}`/`{node, input}` connection-object field names used
    inside `outputs[...].connections`/`inputs[...].connections`, the
    `connectionCreated`/`connectionRemoved` event payload shape,
    `.import()`/`.clear()` method names) before writing
    `buildFlowEditorWidget()` against them.
  - `npx marked@9.1.6` against a sample ` ```flowgraph ` fence — confirmed
    it emits `class="language-flowgraph"`, matching the DOM selector
    `buildFlowEditors()` queries for.
  - Wrote and ran a Node script that extracts all three `flowgraph` JSON
    blocks from `docs/lab6/lab.md`, `JSON.parse`s each, and cross-checks
    every `expected` pair's node keys against that block's own `nodes`
    array — all 3 valid (block 1: 7 nodes/9 expected edges; block 2: 9
    nodes/11 edges; block 3: 9 nodes/12 edges).
  - Extracted both inline `<script>` blocks from `docs/lab6/index.html`
    and syntax-checked each with `new Function(...)` — both parse cleanly.
  - `cd docs && bundle exec jekyll build --destination <tmp>` succeeded —
    same pre-existing Sass deprecation warnings only. Output tree confirmed
    to contain `lab6/index.html` and `lab6/lab.md`. Temp output directory
    deleted after inspection, not committed.
- **Link check:** grepped `href="./lab` in `docs/index.html` — six cards
  (`./lab1/` … `./lab6/`), all resolve to real directories.
- **Not verified this session:** the page was not opened in an actual
  browser — Drawflow's CDN load, the actual drag-to-connect interaction,
  the Check/Reset button click handlers, and the `localStorage`
  round-trip via `editor.import()`/`export()` were code-reviewed and
  API-verified against Drawflow's real source (see above), not exercised
  live in a browser.

## Module 2 · Lab 1 — CMP generator, repo checker, page render (run 2026-10-29)

- `python src/m2/lab1/tools/build_cmp_docs.py` → writes both `.docx`;
  read back with python-docx: both have the 9 Annex D sections + document
  history and 6 tables; template has 100+ `TODO` markers, reference **0**.
- **Checker, pure logic (Node):** `evaluateRepo()` on a hand-built
  compliant snapshot → 14/14 pass; on an empty-repo snapshot → only
  `public` passes; `REQ-SAFE-021` in an issue body is recognised;
  `v2.0.0-rc1` accepted, `release-1` rejected; `parseRepoUrl` handles
  `https://github.com/a/b`, a `.git` suffix, a `/tree/main` suffix and
  `a/b`, and rejects garbage. Load with
  `require('<repo>/docs/m2/lab2/repo-checker.js')` (moved there by the
  2026-10-30 split; at the time of this run it was under `lab1/`).
- **Checker, live (Node 24, real GitHub API, unauthenticated):**
  `fetchSnapshot('alexp25','scade-labs')` parsed every endpoint (280 blob
  paths, 55 commits, 0 tags/PRs/issues); a nonexistent repo → `notfound`.
  This live run exposed an over-broad CMP rule (any `.docx` under `docs/`
  passed) — tightened to require `cmp`/`configuration` in the file name.
- `lab.md` rendered with `marked@9.1.6` (the version the page loads) in
  Node: 10 quiz questions / 40 radios, answer key `abcacbbcdc`, the
  `#repo-checker` placeholder, the `.docx` link, no escaped HTML.
- `bundle exec jekyll build --destination <tmp>` succeeded (only the
  pre-existing Cayman Sass deprecation warnings); output contains
  `m2/lab1/{index.html, lab.md, repo-checker.js, CMP_template_CruiseControl.docx}`
  and `courses/m2-lab1.pdf`, and no `courses/m2/`.
- Relative links/assets from `docs/m2/lab1/` (`../../`, both shared JS
  files, `repo-checker.js`, `../../lab3/`, `../../lab4/`) resolve; no
  `*reference*.docx` under `docs/`. (The IEEE PDF is published on purpose
  as `docs/courses/ieee-828-2012.pdf`, link checked in the follow-up session.)
- CMP upload form (`cmp-submit.js`, added later the same day): `node --check`
  passes; `lab.md` renders the `#cmp-submit` placeholder and the in-page
  link to Activity 1E (slug checked against `slugify()`). **No real
  submission was sent** — the recipient is a placeholder, and the first
  FormSubmit POST to a new address triggers an activation email.
  formsubmit.co itself returned HTTP 521 (Cloudflare: origin down) on
  2026-10-29 for every URL, checked from PowerShell. The `mailto:`
  fallback was tested in Node with a stubbed DOM: recipient, subject and
  body (name/group/repo/message/attachment reminder) are encoded correctly.
- **Not done:** loading the page in a real browser (checker UI/CORS, quiz
  clicks, slides modal); a full student walk-through on a repo following
  Part 2; the rate-limit (403) and token paths were code-reviewed only.

## Module 2 · Labs 1–2 — after the split into two labs (run 2026-10-30)

- Both `lab.md` files rendered with `marked@9.1.6` in Node: Lab 1 has 10
  quiz questions / 40 radios, key `abcacbbcdc`, the `.docx` link, no
  `#repo-checker`; Lab 2 has the `#repo-checker` placeholder, no quiz; no
  escaped HTML in either; heading lists as expected (1A–1F, 2A–2E).
- Checker fixtures re-run from `docs/m2/lab2/repo-checker.js`: compliant
  14/14, empty repo passes only `public`, `parseRepoUrl` ok.
- `node --check` on `cmp-submit.js`, `repo-checker.js` and the inline
  `<script>` of both `index.html` files.
- `bundle exec jekyll build` succeeded; output has `m2/lab1/{index.html,
  lab.md, cmp-submit.js, CMP_template_CruiseControl.docx}`,
  `m2/lab2/{index.html, lab.md, repo-checker.js}`, `courses/m2-lab{1,2}.pdf`.
- Every relative `href`/`src`/markdown link in both pages and both
  `lab.md` files resolves on disk.
- Lab 2 "Getting Started with Git" (added the same day): page re-rendered
  (no escaped HTML; Steps 1–6 + recovery table before Activity 2A); the
  skip link's anchor matches `slugify()`; the **Step 6 practice script was
  extracted from `lab.md` and run with real Git** (Git for Windows, bash,
  `set -e`) in a scratch folder — every command succeeded, final log shows
  REQ-01..03 on `main` after a fast-forward merge. Install commands
  (`winget`, `brew`, `apt`, `dnf`) and the GitHub sign-in flows were not
  executed.
- Scroll-spy fix (all 9 lab `index.html` files): `node --check` on every
  page's inline scripts passes. The scrolling behaviour itself was **not**
  checked in a browser — diagnosis is from the code (see changelog).
- **Not done:** either page in a real browser.

## SCADE AI · Lab 2 — native Keras quantization example

- Use the repository `.venv/bin/python` (tested: Keras 3.15.1 / TensorFlow
  2.21.0). Run the imports/options defining `val_70`, `CLASS_NAMES`,
  `IMAGE_SIZE`, `BATCH_SIZE`, `TRAIN_SEED`, the `load_images` and
  `prepare_resnet_input` definitions, then both code cells under
  `Quantization example`. Do not execute data splitting/training/tuning or
  pruning as part of validation.
- Requires the existing `resnet50_murmur_detection_copy.keras` and validation
  PNG directories. The default rewrites ordinary channels-last Conv2D as
  patch extraction plus Dense, then quantizes every Dense kernel. Check
  float32 rewrite equivalence, actual INT8 kernel dtypes, save/reload output
  equivalence, and that the original source model's hash is unchanged.
- Confirm the generated `resnet50_murmur_detection_copy_int8.keras` is a ZIP
  archive containing `config.json`, `metadata.json`, and `model.weights.h5`.
  In a fresh process, load using `tf.keras.models.load_model(...,
  compile=False)` without custom objects and compare predictions. This
  catches the previous error of writing TFLite bytes with a `.keras` suffix.
- Exercise `QUANTIZE_CONVOLUTIONS = False` in a temporary directory: two
  Dense kernels must be INT8 and six Conv2D kernels must stay float32, with
  successful save/reload/inference. For the convolution rewrite, compare
  float32 outputs for 1x1/3x3 kernels, stride 1/2, dilation 1/2,
  same/valid padding, bias/no bias, and ReLU/linear activations; unsupported
  grouped convolutions must raise explicitly.
- **Run 2026-11-23 (current example):** both notebook cells executed unchanged
  against the real model and eight preprocessed validation images. Float32
  rewrite check and quantized save/reload check passed; all eight kernels
  were INT8. Original file: 453.6 KiB; native quantized Keras file: 228.6 KiB.
  Maximum score difference from the original on these eight images:
  0.028426. The original file hash was unchanged. The genuine `.keras`
  output was kept in the notebook directory, replacing the old misnamed
  TFLite artifact. Fresh-process loading/inference with `tf.keras` passed.
  Six convolution rewrite geometry cases, grouped-convolution rejection,
  and the Dense-only fallback's dtype/save/reload checks also passed.
  The AST-based helper extraction emitted TensorFlow AutoGraph source-code
  lookup warnings; execution completed successfully.
- Notebook JSON, unique cell IDs and all code-cell syntax validated; all
  cells before the quantization heading preserved exactly. The separate
  cruise-control Lab 2 browser `STARTER_CODE` still matches its standalone
  starter. `git diff --check` passed.
- This model retains float32 biases/scales/batch normalization/residuals and
  float32 I/O. Full float32-versus-INT8 accuracy comparison, runtime
  performance, Scade One import and embedded deployment have not been
  validated. The saved INT8 model test-set evaluation is recorded below.
  No published AI Lab 2 page exists to rebuild/synchronize.
- **Historical, superseded example (also 2026-11-23):** the original TFLite
  full integer conversion passed with 200 training calibration images and
  INT8/INT32 tensors only (117.7 KiB). It was replaced by the native Keras
  mixed-precision example above; its calibration/interpreter procedure is
  no longer the notebook workflow.

## SCADE AI · Lab 2 — test the saved INT8 model

- Under `Test the saved models`, the active cell selects
  `resnet50_murmur_detection_copy_int8`, loads the native `.keras` file into
  `int8_resnet50_model`, and assigns it to `model` for the existing loop.
  Every original testing line is preserved, either active or commented.
- Run imports/options plus the `load_images` and `prepare_resnet_input`
  definitions first. The latter appears later in the notebook, so execute
  its definition before returning to the testing section. The quantization
  cells need not rerun if the genuine saved artifact already exists.
- Keep `test_70`, `shuffle=False`, ResNet input preprocessing, threshold 0.5,
  Normal=0/Murmur=1, and the original prediction/report logic. Inputs remain
  float32 RGB; no INT8 casting or TFLite scaling/dequantization is needed.
- **Run 2026-11-23:** the updated cell executed unchanged using the real
  saved model and all 1,279 images in the configured testing folder (1,047
  Normal, 232 Murmur). Confusion matrix: `[[970, 77], [110, 122]]`; accuracy
  approximately 85.4%, Murmur precision 61.3%, Murmur recall 52.6%.
  This evaluates the quantized model only, not its change from float32.
- Verified float32, three-channel inputs; finite predictions; both classes;
  one raw-score row per test image; confusion-matrix total matches the test
  count; model file hash unchanged. Raw predictions were saved to
  `resnet50_murmur_detection_copy_int8_test_predictions.txt`; the report and
  confusion matrix were appended to
  `resnet50_murmur_detection_copy_int8.txt`. Both outputs remain in the
  notebook directory. Reruns overwrite predictions and append a new report.
- Notebook JSON and every code cell parse; only the testing instructions
  and active test cell changed in this follow-up. Original lines are
  preserved verbatim, active or commented; other cells/metadata preserved.
  Stale test outputs cleared. `git diff --check` and the separate published
  cruise-control Lab 2 browser/starter consistency check passed. No site or
  Scade One source changed, so no Jekyll build or proprietary-tool check
  applies to this edit.

## SCADE AI — Raspberry Pi audio-to-C pipeline

- From repo root: `.venv/bin/python src/SCADE_AI_labs/raspberry_pi/check_pipeline.py`.
  On a configured Pi, `python3 check_pipeline.py` inside that directory is
  equivalent. This is a plain assert/PASS script, not a new test framework.
- Run `python -m py_compile` on `config.py`, `preprocessing.py`,
  `inference.py`, `run.py`, and `check_pipeline.py` in the new directory.
- **Run 2026-11-24 on the local desktop:** all smoke checks passed:
  PCM16/PCM24/float WAV decode, stereo-to-mono and preserved sample rate;
  filter agreement with the notebook's direct form at 4 kHz and finite
  second-order-section output at 2/44.1/48 kHz; STFT shape/dB/silence;
  600x400 plot and both model input formats; proxy reset/cycle/HWC copy
  through a temporary Python stub; Normal/Murmur threshold boundary and
  invalid-score rejection; worker error propagation; integrated runner
  timing/RAM-report fields with stub inference. No TensorFlow, Keras,
  librosa or Numba was imported by that smoke-check process.
- **Separate desktop parity check, run 2026-11-24:** all 16 profile names,
  input shapes and single sigmoid outputs matched the actual Lab 2 Keras
  ZIP metadata. Synthetic audio at 4 kHz/3.4 s, 44.1 kHz/2 s, 4 kHz/0.08 s
  and 2 kHz/62 s produced exactly matching dB matrices and 600x400 RGB
  plots compared with librosa STFT/amplitude_to_db/specshow in the same
  environment (using the intended 6x4 inch/100 dpi figure). For every
  profile, final 64x64 tensors exactly matched TensorFlow PNG grayscale
  decoding, bilinear resize, CNN normalization and ResNet preprocessing.
  This used existing desktop NumPy 2.5.4, SciPy 1.18.1, Matplotlib 3.11.2,
  librosa 1.0.0 and TensorFlow 2.21.0; it did not run model inference or
  retrain/alter any model. Other rendering environments may differ.
- Existing cruise-control Lab 2 browser and standalone starter content
  compared after ignoring their pre-existing terminal blank-line
  difference. AI notebook JSON/code-cell syntax and `git diff --check`
  also checked. No published source changed, so Jekyll/browser checks
  and proprietary model-generation checks do not apply to this task.
- **Pending:** generated models/proxies have not been supplied. No real
  C inference, ARM64 loader/build, Scade import (including INT8 operation
  compatibility), target package install, Pi RAM fit or Pi 60-second
  performance was validated. Once artifacts arrive, inspect actual
  module/class/input/output names, use the Linux ARM64 native library,
  configure the relevant profile, and run `/usr/bin/time -v python3 run.py`
  on the actual Pi/SD card. Internal total includes scientific imports
  through classification; external wall time also includes interpreter
  startup/output/shutdown. Record the first font-cache run and subsequent
  fresh-process measurements. The target is measured, not enforced.

## Manual/visual checks

- No student-facing page exposes instructor solution content: confirmed by
  directory separation (`src/lab2/solution/` and `src/lab3/solution/` are
  never referenced from any file under `docs/` — grepped for `solution`
  across `docs/**/*.html`, `docs/**/*.md`: no hits) and by the fact that
  `src/` is never linked from any `docs/` page.
- New/edited `.agents/` and `project_docs/` files were checked against
  actual repo paths (Glob/Read) before being written.
