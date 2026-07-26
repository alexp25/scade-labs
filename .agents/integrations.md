# External integrations / dependencies

No secrets, APIs, environment variables, or hosted backend services exist in
this repo. Only the following real external dependencies were found.

| Dependency | Purpose | Referenced in | Local or remote | When needed | Version | Notes |
|---|---|---|---|---|---|---|
| GitHub Pages | Hosts the published site | (no repo-visible config — `docs/` folder convention only) | remote | publish-time | — | Classic branch/`docs`-folder deploy inferred from absence of `.github/workflows/`; not confirmed against actual repo Settings |
| Jekyll 4.4.1 + `jekyll-theme-cayman` 0.2.0 + `webrick` 1.9.2 + `rouge` 4.7.0 | Static site build/serve | `docs/Gemfile`, `docs/Gemfile.lock`, `docs/_config.yml` | local (via Bundler) | build/preview-time | pinned in `Gemfile.lock` | Theme is configured but not applied to any page — see `.agents/publishing.md` |
| `marked.js` 9.1.6 | Renders `lab.md` to HTML in-browser | `docs/lab2/index.html`, `docs/lab3_1/index.html`, `docs/lab3_2/index.html` (cdnjs) | remote (CDN) | runtime, in every visitor's browser | pinned in the `<script src>` URL | If cdnjs is unreachable, lab pages fail to render their content (visible fallback error message in `docs/lab2/index.html`) |
| `highlight.js` 11.9.0 | Syntax highlighting of code blocks | same 3 lab pages (cdnjs) | remote (CDN) | runtime | pinned in URL | Same offline-availability caveat |
| Skulpt (`skulpt.min.js` + `skulpt-stdlib.js`) | In-browser Python execution for Lab 2's live editor | `docs/lab2/index.html` (skulpt.org) | remote (CDN, not vendored) | runtime, Lab 2 only | unpinned (whatever `skulpt.org` currently serves) | Lab 2's "Run" button is entirely non-functional offline or if skulpt.org is unreachable; the page already handles load failure by disabling the Run button |
| CodeMirror 5.65.16 (+ `python.min.js` mode, `dracula` theme) | Code editor widget for Lab 2 | `docs/lab2/index.html` (cdnjs) | remote (CDN) | runtime, Lab 2 only | pinned in URL | |
| `ansys-scadeone-core` | Scade One Python API (`ScadeOne`, `PythonWrapper`) used to generate Python wrappers from Scade One models | `src/lab3_1/solution/requirements.txt` (`==0.8.2`), `src/lab3_2/solution/CruiseControl/requirements.txt` (unpinned) | local (pip install) | authoring/regeneration-time, instructor/maintainer only | pinned in Lab 3.1, **unpinned in Lab 3.2** (inconsistency, not corrected — would require a maintainer decision on which version to pin) | Also requires a local Scade One Student Edition install (`v261`, per hardcoded install paths) — not just the pip package |
| Ansys Scade One Student Edition (desktop app) | Model editor, simulator, code generator | `docs/lab3_1/lab.md`, `docs/lab3_2/lab.md` (install links to ansys.com), `setup_wrapper.py`/`generate_python_wrapper.bat` (hardcoded install path) | local, proprietary desktop install | model-editing, simulation, and code-generation time | no version number stated beyond the `v261` install-path segment | Confirmed this session: does not require registration/license activation for the student edition (corrected from a prior inaccurate lab.md claim) |
| Ruby + Bundler | Runs Jekyll | `readme_local_setup.txt` | local | build/preview-time | not pinned beyond `Gemfile.lock`'s bundler version `4.0.10` | |
| Python 3.12 | Runs the Scade One wrapper-generation/test scripts | `setup_wrapper.py`, `generate_python_wrapper.bat`, both labs' `lab.md` (`py -3.12 ...`) | local | instructor/maintainer, Lab 3.1/3.2 only | explicitly `3.12` | Lab 2 has no stated Python version requirement (stdlib-only, ran successfully under 3.11.3 in this environment) |

## Offline / reproducibility concerns worth flagging to a maintainer

- Lab 2's live-editor path (Skulpt + CodeMirror + marked.js + highlight.js)
  depends on 3 different CDNs (skulpt.org, cdnjs.cloudflare.com ×3) with no
  local fallback/vendoring — a maintainer wanting a fully offline-capable
  lab would need to vendor these.
- `ansys-scadeone-core` version drift between Lab 3.1 (pinned) and Lab 3.2
  (unpinned) means a fresh install of Lab 3.2's wrapper generator could pick
  up a newer/incompatible API version than what `cc_wrapper.py` was
  generated against — the repo's own `lab.md` already warns "the exact class
  name and instantiation method depend on your Scade One version."
