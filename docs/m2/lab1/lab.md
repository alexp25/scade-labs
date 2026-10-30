# Module 2 · Lab 1 — A Configuration Management Plan for a Scade One Project

- **Course:** Advanced Critical Software Engineering (Module 2)
- **Lesson:** 1 — Configuration Management Tools
- **Duration:** 2 hours
- **Tools:** Microsoft Word (or any editor that saves `.docx`); your Lab 4 `CruiseControl/` folder; Scade One only if you want to re-open the model
- **Work mode:** Individual
- **Prerequisites:** [Lab 3](../../lab3/) (the Cruise Control requirements REQ-01, REQ-02, REQ-04, REQ-07, REQ-08) and [Lab 4](../../lab4/) (the Cruise Control Scade One project). Have seen the Module 2 Lesson 1 slides — open them any time with the **Course Slides** button above.

---

# Context

In Lab 4 you built a working Cruise Control model, generated code from it, and verified it against scenario CSVs. Right now, though, that project exists as a folder on your disk. Nobody — including you in three months — can answer these questions about it:

- *Which* version of the requirements was the model built against?
- *Which* model version produced the wrapper that passed the tests?
- *What* changed since the last time it worked, *who* changed it, and *why*?

Configuration Management (CM) is the discipline that makes those questions answerable. In this lab you write a draft **Configuration Management Plan (CMP)** for the Cruise Control project, using the content areas of **IEEE Std 828-2012** (its Annex D — the standard's list of what a CM Plan must contain, explained below), and focusing on four decisions: **identification, branching, versioning, baselining**. You complete a pre-filled Word template, send it to your mentor, and take a short quiz.

In [Module 2 · Lab 2](../lab2/) you then carry the plan out: you put the project under configuration on **GitHub** and let the page check your public repository against the plan.

---

# Learning Objectives

By the end of this lab you will be able to:

- Decide which artifacts of a Scade One project are **configuration items (CIs)** and give each a unique identifier.
- Define a **branching strategy** that keeps the approved configuration stable.
- Apply a **versioning** scheme (`vMAJOR.MINOR.PATCH`, release candidates) consistently.
- Define **baselines** (requirements, design, verification, release) — when they are created, what they contain, and who approves them.
- Structure a CM plan along the IEEE 828 CMP outline.

---

# Recap — Configuration Management in One Page

A reminder of the lecture vocabulary — not a replacement for it.

- **What it is.** CM is the systematic identification, organization, tracking and maintenance of *all* software artifacts across the SDLC — not just source code.
- **Why it matters.** Software in critical systems keeps changing. Without CM: *change → inconsistency → loss of traceability → uncontrolled risk*. CM lets you answer: **what changed, who changed it, why, and which version contains it?**
- **A real failure.** The 2015 Airbus A400M crash near Seville was linked to engine-control software *configuration data* improperly installed — not to a flaw in the control algorithm. Correct software, wrongly configured, can still fail catastrophically.
- **Standards.** Safety standards such as DO-178C (airborne), ISO 26262 (automotive), IEC 62304 (medical) and EN 50716 (railway) all expect controlled CIs, version and change control, baselines, status accounting, reproducible builds and traceable changes. *This lab practises those ideas; it does not make the project compliant with any of them — and neither does GitHub on its own.*
- **Configuration item.** *If an artifact can influence the behavior, the verification or the safety argument of the software, its version should be controlled.*
- **Baseline.** An identified, approved configuration used as a reference point. *Same controlled inputs + same controlled tools → reproducible software.*
- **Git** gives versioning and history (repository → commit → branch → merge → tag); **GitHub** adds the control workflow around it (issues, pull requests, reviews, releases). Scade One stays the engineering environment.

---

# The Configuration Management Plan

## The IEEE 828 CMP outline

> **Reference document:** [IEEE Std 828-2012 — Configuration Management in Systems and Software Engineering (PDF)](../../courses/ieee-828-2012.pdf), provided for this course by Universitatea Politehnica din București. You do not need to read all of it — the parts used in this lab are listed below.

**What is an "annex"?** An IEEE standard has a main body (numbered clauses 1–14 in IEEE 828, which say what CM *must do*) followed by **annexes** — appendices labelled A, B, C, … An annex is either *normative* (mandatory — you must follow it to conform to the standard) or *informative* (explanation and examples only). In IEEE 828:

- **Annex D (normative)** — *the table of contents of a CM Plan*: the sections D.1–D.9 every CMP must contain. **This is the skeleton of the Word template you will complete.**
- **Annex K (informative)** — examples of how to name software builds and versions; Activity 1C is based on it.
- **Clause 8** (main body) — configuration identification: how to structure, name and store CIs, and how to define baselines (Activities 1A and 1D).

IEEE Std 828-2012 defines CM as a set of lower-level processes — planning, management, configuration identification, change control, status accounting, auditing, interface control, supplier control and release management — and, in **Annex D**, the content areas a CM Plan must cover (either in the plan itself or by reference to another controlled document). Summarised in our own words:

| Annex D | Content area | What it answers for the Cruise Control project |
|---|---|---|
| D.1 | Introduction — purpose, scope, relationship to the organization, key terms, references | Why the plan exists, which artifacts and life-cycle phases it covers |
| D.2 | Criteria for identifying CIs | What goes under CM and what doesn't |
| D.3 | Limitations and assumptions | Tool versions, available infrastructure |
| D.4 | CM responsibilities and authorities | Who may approve a change to a baseline |
| D.5 | Project organization | Which roles/units take part |
| D.6 | CM responsibilities | Role → CM activity matrix |
| D.7 | Applicable policies and procedures | Commit-message rules, "no direct push to main", generated-code policy |
| D.8 | Planned activities, schedule and resources | Identification, branching, versioning, baselines, change control, status accounting, audits, milestones, tools |
| D.9 | CMP maintenance | Who updates the plan, how changes to it are approved |

> **Your deliverable for this lab** is that plan, as a Word document. Download the template — it already follows this outline, is partially filled in for the Cruise Control project, and marks every gap with a red **TODO**:
>
> **[⬇ CMP_template_CruiseControl.docx](CMP_template_CruiseControl.docx)**
>
> When it is complete, send it to your mentor with the upload form at the end of [Activity 1E](#activity-1e-complete-and-enrich-the-plan).

Activities 1A–1D below walk through the four decisions that matter most. Read each one, then complete the corresponding section of the template.

## Activity 1A — Configuration identification

IEEE 828 asks for three things here: a **structure** of CIs, a **naming convention** that makes each one unique (and can accommodate multiple versions), and a **controlled repository** they live in.

Naming convention used in the template: `CC-<category>-<nnn>` with categories `REQ`, `MDL` (models), `TST` (tests), `GEN` (generated code), `TOOL` (tool configuration), `VER` (verification results), `DOC` (documents). The first rows are given:

| CI ID | Configuration item | Repository path | Type |
|---|---|---|---|
| `CC-REQ-001` | Cruise Control requirements (REQ-01, 02, 04, 07, 08) | `requirements/requirements.md` | Source |
| `CC-MDL-001` | Scade One project file | `CruiseControl/CruiseControl.sproj` | Source |
| `CC-MDL-002` | Cruise control design (state machine, regulator, limiter) | `CruiseControl/assets/CC_design.swan` | Source |
| … | *you complete the rest in the template* | | |

**Your task (template sections 2 and 8.1):** finish the CI table. Walk through your Lab 4 `CruiseControl/` folder file by file and classify every item:

- **Source CI** — hand-written, changes behavior or verification (`*.swan`, `*.sproj`, scenario CSVs, evaluation script, `requirements.txt`).
- **Generated CI** — produced by a tool from other CIs (`cc_wrapper/`). It *is* controlled (it is what actually runs), but it is **never edited by hand**; it is regenerated from the tagged model.
- **Record** — evidence of a controlled run (`results/summary.csv`, plots). Kept for the baseline it supports.
- **Not a CI** — user-specific or throw-away: `*.sproj.user`, `*.sproj.editor`, `jobs/` (code-generation job folders), `pyscadeone.log`, `__pycache__/`. These go in `.gitignore`.

## Activity 1B — Branching strategy

The goal: several lines of work coexist, but **`main` always holds an approved configuration**.

| Branch | Holds | Created from → merges into | Rule |
|---|---|---|---|
| `main` | Approved / released configuration only | — | No direct push. Merged only through a reviewed pull request. |
| `develop` | Integrated, reviewed work | `main` → `release/x.y` | Merged through pull requests. |
| `feature/REQ-<id>-<short-name>` | One change request at a time, e.g. `feature/REQ-07-regulator-gain` | `develop` → `develop` | Deleted after merge. |
| `release/<major>.<minor>` | Stabilisation before delivery — fixes only, no new features | `develop` → `main` (then tagged) | Merged through pull requests. |

**Your task (template section 8.2):** complete the branch table, and decide whether your project really needs `release/*` branches for a single-person project (both answers are acceptable if justified in the plan).

## Activity 1C — Versioning

IEEE 828 (Annex K) describes sequence-based build names `<major>.<minor>.<revision>` where the first number changes only for significant functional changes and later numbers for changes of decreasing significance, plus discriminators for development / alpha / beta / release-candidate builds. We use the widespread semantic form:

**`vMAJOR.MINOR.PATCH[-rcN]`**

| Change to the Cruise Control project | From | To |
|---|---|---|
| A limiter bound was wrong; fixed, interface unchanged | `v1.0.0` | `v1.0.1` |
| A new requirement implemented (e.g. a new REQ-09 behavior), interface unchanged | `v1.0.1` | `v1.1.0` |
| A new input added to the `cruise_control` node — every caller and the wrapper change | `v1.1.0` | `v2.0.0` |
| First candidate submitted for final verification of 2.0.0 | — | `v2.0.0-rc1` |
| A defect found in rc1, fixed | `v2.0.0-rc1` | `v2.0.0-rc2` |
| rc2 passes; released **without any further change** | `v2.0.0-rc2` | `v2.0.0` |

The last row is the important discipline: the released artifact must be *exactly* the last candidate that was verified.

**Your task (template section 8.3):** write the rules for MINOR and PATCH, and the release-candidate rule, in your own words.

## Activity 1D — Baselining

A baseline is a **set** of CI versions, approved together. IEEE 828 asks you to define, for each baseline: **the event that establishes it, the items it controls, the procedure to establish/change it, and the authority that approves changes**. After a baseline exists, its items change *only* through change control.

| Baseline | Established when | Contains | Git tag |
|---|---|---|---|
| Requirements | requirements reviewed and accepted | `CC-REQ-*` | `baseline/req-v1.0` |
| Design | model builds and simulates; design review passed | `CC-REQ-*`, `CC-MDL-*` | `baseline/des-v1.0` |
| Verification | all scenarios pass on the candidate | + `CC-TST-*`, `CC-TOOL-*`, `CC-VER-*` | `baseline/ver-v1.0` |
| Release | verification baseline approved, wrapper regenerated from the tagged model | all CIs | `v1.0.0` + GitHub Release |

A release can then be written as a **manifest**, exactly like the slides' "Release v1.2 = Requirements v3 + SCADE Model v7 + Tests v5 + Tool configuration + Generated code":

```text
v1.0.0 = baseline/req-v1.0 + baseline/des-v1.1 + baseline/ver-v1.0
         + Scade One Student v261 (as in generate_python_wrapper.bat) + requirements.txt (ansys-scadeone-core, matplotlib)
         + CruiseControl/cc_wrapper regenerated from the tagged model
```

**Your task (template section 8.4):** complete the baseline table (events, contents, approval authority) and write the manifest of *your* first release.

## Activity 1E — Complete and enrich the plan

Finish every remaining **TODO** in the template (sections 1.2–1.4, 3, 5–7, 8.5–8.9 and 9). *Enrich* means: where the template already gives an answer, check it against your own project and improve it — for example, if your Lab 4 folder also contains `root_wrapper/`, it has to appear in your CI table too. Fill in the **Document history** table at the top — the plan is itself a CI (`CC-DOC-001`).

Save it as **`CMP_CruiseControl.docx`**. Keep it: in [Lab 2](../lab2/) you commit it to your repository and implement it.

### Send your plan to the mentor

Upload the completed `.docx` below. It is emailed to your mentor together with your name and contact details, so they can reply to you directly. Only `.docx` files up to 5 MB are accepted.

<div id="cmp-submit"><p class="loading">Loading upload form…</p></div>

> **Send to mentor** goes through [FormSubmit](https://formsubmit.co), an external form-to-email service, because this site has no server of its own; after sending you are brought back here with a confirmation. If that service is unavailable, **Email it instead** opens your own mail app with the recipient, subject and details filled in — you only attach the `.docx`.

## Activity 1F — Quiz

<style>
  #cm-quiz { margin-top: 1rem; }
  .quiz-q { margin-bottom: 1.1rem; padding: 1.15rem 1.25rem; background: var(--white); border: 1px solid var(--border); border-radius: 8px; }
  .quiz-q strong { display: block; margin-bottom: .7rem; color: var(--navy); font-size: .97rem; }
  .quiz-option { display: flex; align-items: flex-start; gap: .55rem; padding: .42rem .55rem; border-radius: 5px; cursor: pointer; transition: background .13s; user-select: none; font-size: .92rem; }
  .quiz-option:hover { background: var(--ice); }
  .quiz-option input { margin-top: .22rem; flex-shrink: 0; accent-color: var(--blue); }
  .quiz-option.correct { background: #E8F5E9; color: #1B5E20; font-weight: 600; border-radius: 5px; }
  .quiz-option.wrong   { background: #FFEBEE; color: #B71C1C; text-decoration: line-through; border-radius: 5px; }
  .quiz-option.reveal  { background: #FFF8E1; color: #BF360C; font-weight: 600; border-radius: 5px; }
  #quiz-submit { margin-top: .75rem; padding: .55rem 1.5rem; background: var(--blue); color: var(--white); border: none; border-radius: 6px; font-size: .9rem; font-weight: 600; cursor: pointer; transition: background .15s; }
  #quiz-submit:hover:not(:disabled) { background: var(--sky); }
  #quiz-submit:disabled { opacity: .45; cursor: default; }
  #quiz-score { display: inline-block; margin-left: 1rem; font-size: 1rem; font-weight: 700; vertical-align: middle; }
  #quiz-reset { display: none; margin-left: .75rem; padding: .55rem 1.1rem; background: transparent; color: var(--muted); border: 1px solid var(--border); border-radius: 6px; font-size: .88rem; cursor: pointer; transition: color .15s, border-color .15s; vertical-align: middle; }
  #quiz-reset:hover { color: var(--blue); border-color: var(--sky); }
</style>

<div id="cm-quiz">
  <div class="quiz-q" data-correct="a">
    <strong>Q1 — Cruise Control v1.2.0 is released. A wrong limiter bound is fixed; no interface changes. What is the next version?</strong>
    <label class="quiz-option"><input type="radio" name="q1" value="a"><span>v1.2.1</span></label>
    <label class="quiz-option"><input type="radio" name="q1" value="b"><span>v1.3.0</span></label>
    <label class="quiz-option"><input type="radio" name="q1" value="c"><span>v2.0.0</span></label>
    <label class="quiz-option"><input type="radio" name="q1" value="d"><span>v1.2.0-fix</span></label>
  </div>
  <div class="quiz-q" data-correct="b">
    <strong>Q2 — The current release is v1.2.1. A new requirement is implemented without changing the model interface. What is the next version?</strong>
    <label class="quiz-option"><input type="radio" name="q2" value="a"><span>v1.2.2</span></label>
    <label class="quiz-option"><input type="radio" name="q2" value="b"><span>v1.3.0</span></label>
    <label class="quiz-option"><input type="radio" name="q2" value="c"><span>v2.0.0</span></label>
    <label class="quiz-option"><input type="radio" name="q2" value="d"><span>v1.2.1.1</span></label>
  </div>
  <div class="quiz-q" data-correct="c">
    <strong>Q3 — Starting from v1.3.0, a new input is added to the <code>cruise_control</code> node, so the generated wrapper and every caller change. What is the next version?</strong>
    <label class="quiz-option"><input type="radio" name="q3" value="a"><span>v1.3.1</span></label>
    <label class="quiz-option"><input type="radio" name="q3" value="b"><span>v1.4.0</span></label>
    <label class="quiz-option"><input type="radio" name="q3" value="c"><span>v2.0.0</span></label>
    <label class="quiz-option"><input type="radio" name="q3" value="d"><span>v1.3.0-rc1</span></label>
  </div>
  <div class="quiz-q" data-correct="a">
    <strong>Q4 — Release candidate 1 of version 2.0.0 had a defect, which has been fixed. How is the next candidate named?</strong>
    <label class="quiz-option"><input type="radio" name="q4" value="a"><span>v2.0.0-rc2</span></label>
    <label class="quiz-option"><input type="radio" name="q4" value="b"><span>v2.0.1</span></label>
    <label class="quiz-option"><input type="radio" name="q4" value="c"><span>v2.0.0 (overwrite the existing tag)</span></label>
    <label class="quiz-option"><input type="radio" name="q4" value="d"><span>rc2-final</span></label>
  </div>
  <div class="quiz-q" data-correct="c">
    <strong>Q5 — You start working on change request #3, which modifies REQ-07. According to the branching strategy in this lab, which branch do you work in?</strong>
    <label class="quiz-option"><input type="radio" name="q5" value="a"><span>main</span></label>
    <label class="quiz-option"><input type="radio" name="q5" value="b"><span>REQ-07</span></label>
    <label class="quiz-option"><input type="radio" name="q5" value="c"><span>feature/REQ-07-regulator-gain, created from develop</span></label>
    <label class="quiz-option"><input type="radio" name="q5" value="d"><span>release/1.1</span></label>
  </div>
  <div class="quiz-q" data-correct="b">
    <strong>Q6 — Which branch must contain only an approved configuration and never receive direct commits?</strong>
    <label class="quiz-option"><input type="radio" name="q6" value="a"><span>develop</span></label>
    <label class="quiz-option"><input type="radio" name="q6" value="b"><span>main</span></label>
    <label class="quiz-option"><input type="radio" name="q6" value="c"><span>feature/*</span></label>
    <label class="quiz-option"><input type="radio" name="q6" value="d"><span>Any branch, as long as it has a tag</span></label>
  </div>
  <div class="quiz-q" data-correct="b">
    <strong>Q7 — The Cruise Control requirements have been reviewed and accepted for the first time. Which tag identifies this?</strong>
    <label class="quiz-option"><input type="radio" name="q7" value="a"><span>v1.0.0</span></label>
    <label class="quiz-option"><input type="radio" name="q7" value="b"><span>baseline/req-v1.0</span></label>
    <label class="quiz-option"><input type="radio" name="q7" value="c"><span>feature/requirements</span></label>
    <label class="quiz-option"><input type="radio" name="q7" value="d"><span>No tag is needed; the commit hash is enough</span></label>
  </div>
  <div class="quiz-q" data-correct="c">
    <strong>Q8 — Which file from the Lab 4 project is <em>not</em> a configuration item?</strong>
    <label class="quiz-option"><input type="radio" name="q8" value="a"><span>assets/CC_design.swan</span></label>
    <label class="quiz-option"><input type="radio" name="q8" value="b"><span>scenarios/tc03_brake_suspends.csv</span></label>
    <label class="quiz-option"><input type="radio" name="q8" value="c"><span>CruiseControl.sproj.user</span></label>
    <label class="quiz-option"><input type="radio" name="q8" value="d"><span>requirements.txt</span></label>
  </div>
  <div class="quiz-q" data-correct="d">
    <strong>Q9 — How should the generated <code>cc_wrapper/</code> be handled?</strong>
    <label class="quiz-option"><input type="radio" name="q9" value="a"><span>It is not a CI, so it is never stored</span></label>
    <label class="quiz-option"><input type="radio" name="q9" value="b"><span>It is a CI, and you fix bugs directly in the generated C file</span></label>
    <label class="quiz-option"><input type="radio" name="q9" value="c"><span>It is stored only on feature branches</span></label>
    <label class="quiz-option"><input type="radio" name="q9" value="d"><span>It is a CI marked as generated, never edited by hand, and regenerated from the tagged model</span></label>
  </div>
  <div class="quiz-q" data-correct="c">
    <strong>Q10 — All test scenarios pass on the candidate configuration and the results are recorded. Which baseline does this establish?</strong>
    <label class="quiz-option"><input type="radio" name="q10" value="a"><span>Requirements baseline</span></label>
    <label class="quiz-option"><input type="radio" name="q10" value="b"><span>Design baseline</span></label>
    <label class="quiz-option"><input type="radio" name="q10" value="c"><span>Verification baseline</span></label>
    <label class="quiz-option"><input type="radio" name="q10" value="d"><span>No baseline; only releases are baselines</span></label>
  </div>
  <div>
    <button id="quiz-submit" type="button">Check Answers</button>
    <button id="quiz-reset" type="button">Try Again</button>
    <span id="quiz-score"></span>
  </div>
</div>

---

# Summary

- A configuration is a **consistent set of CI versions**, not "the latest files". Requirements, Scade One models, tests, generated code, tool configuration, results and the plan itself are all CIs.
- The **CMP** (IEEE 828 Annex D) makes the CM decisions explicit before any tool is touched: identification, branching, versioning, baselines, change control, status accounting, audits.
- **Branches** keep the approved configuration stable, **versions** tell you how much changed, and **baselines** freeze an approved set of CI versions that later changes only through change control.

**Hand in:** your completed `CMP_CruiseControl.docx` through the upload form in Activity 1E.

**Next:** [Module 2 · Lab 2](../lab2/) — put the Cruise Control project under configuration on GitHub, exactly as your plan says.
