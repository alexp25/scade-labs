# Module 2 · Lab 2 — Putting a Scade One Project Under Configuration on GitHub

- **Course:** Advanced Critical Software Engineering (Module 2)
- **Lesson:** 1 — Configuration Management Tools
- **Duration:** 2 hours
- **Tools:** Git and a GitHub account (installation and setup are explained in this lab); Python and the Lab 4 environment to re-run `evaluate_cc_full_report.py`; Scade One only if you want to re-open the model
- **Work mode:** Individual
- **Prerequisites:** [Module 2 · Lab 1](../lab1/) (your completed `CMP_CruiseControl.docx`), [Lab 3](../../lab3/) (the Cruise Control requirements) and [Lab 4](../../lab4/) (the Cruise Control Scade One project folder). The Module 2 Lesson 1 slides are available from the **Course Slides** button above.

---

# Context

In [Lab 1](../lab1/) you *decided* how the Cruise Control project is to be configured: which artifacts are configuration items and how they are named, which branches exist, how versions are numbered, and which baselines are created when. A plan on paper does not control anything by itself, though.

In this lab you first install and learn **Git** (skip that part if you already use it), then carry the plan out with Git and **GitHub**: you create the repository, record the first baseline, take one change request all the way from an issue to a release, and write down the traceability chain of that change. At the end, the page **checks your public repository** against the plan.

---

# Learning Objectives

By the end of this lab you will be able to:

- Install and configure Git, connect it to GitHub, and use its everyday commands (status, add, commit, branch, merge, push, pull, tag).
- Lay out a repository so that every configuration item from your plan has a controlled place, and keep everything else out with `.gitignore`.
- Record a baseline as an annotated tag, and protect the branch that holds the approved configuration.
- Take a change through the GitHub control workflow: issue → feature branch → traced commits → pull request → merge → version tag → release.
- Trace a requirement through issue, commit, test case and release, using identifiers from your own repository.

---

# Recap — From the Plan to the Repository

**Git** gives versioning and history (repository → commit → branch → merge → tag); **GitHub** adds the control workflow around it (issues, pull requests, reviews, releases). Scade One stays the engineering environment. Each decision in your CMP becomes something concrete in the repository:

| CMP decision (Lab 1) | Implemented on GitHub as | Activity |
|---|---|---|
| Configuration identification (section 2, 8.1) | Repository layout, one place per CI category; `.gitignore` for everything that is *not* a CI | 2A |
| Branching strategy (section 8.2) | `main`, `develop`, `feature/REQ-…` branches; branch protection on `main` | 2B, 2C |
| Versioning (section 8.3) | `vMAJOR.MINOR.PATCH[-rcN]` tags | 2C |
| Baselining (section 8.4) | Annotated `baseline/…` tags; a GitHub Release with the release manifest | 2B, 2C |
| Change control and status accounting (section 8.5–8.6) | Issues as change requests, pull requests as reviews, traced commit messages | 2C, 2D |

---

# Getting Started with Git

If Git is already installed and configured on your computer and you have used it before, check Step 2 (especially `init.defaultBranch`) and Step 3, then skip ahead to [the activities](#put-the-cruise-control-project-under-configuration). Otherwise, work through all the steps — they take about 20 minutes.

> **Git or GitHub?** **Git** is a program on your computer that records versions of a folder. **GitHub** is a website that hosts Git repositories and adds the collaboration and control features (issues, pull requests, releases). You need both: Git does the versioning locally, and you *push* to GitHub to share it.

## Step 1 — Install Git

**Windows.** Download **Git for Windows** from [git-scm.com/download/win](https://git-scm.com/download/win) and run the installer. The default options are fine; it also installs **Git Bash** (a terminal where every command in this lab works as written) and **Git Credential Manager** (which handles signing in to GitHub, see Step 3). If you prefer the command line:

```powershell
winget install --id Git.Git -e --source winget
```

**macOS.** Open Terminal and run `git --version`. If Git is missing, macOS offers to install the *Command Line Developer Tools* — accept. (With [Homebrew](https://brew.sh): `brew install git`.)

**Linux.** Use your package manager, e.g. `sudo apt install git` (Debian/Ubuntu) or `sudo dnf install git` (Fedora).

Then open a **new** terminal (Git Bash, PowerShell or Terminal) and check:

```bash
git --version
# git version 2.4x.x  — any recent version is fine
```

## Step 2 — Tell Git who you are

Every commit records an author name and email — this is part of the CM record (*who* changed it). Set them once per computer:

```bash
git config --global user.name  "Ana Popescu"
git config --global user.email "ana.popescu@stud.upb.ro"   # use the email of your GitHub account
git config --global init.defaultBranch main                # new repositories start on "main", as in your CMP
git config --global core.editor "code --wait"              # optional: write commit messages in VS Code instead of Vim
git config --global --list                                 # check what you set
```

> If a command ever drops you into a screen full of `~` lines, that is the **Vim** editor. Type `:q!` and press Enter to leave it, then use `git commit -m "message"` to give the message directly.

## Step 3 — GitHub account and signing in from Git

1. Create a free account at [github.com](https://github.com) (or sign in). Pick a professional username — it appears in the URL of the repository you hand in.
2. GitHub **does not accept your account password** for `git push`. The simplest way to authenticate:
   - **Windows:** nothing to do now. The first time you push, Git Credential Manager opens a browser window; sign in to GitHub and authorise it. The login is remembered.
   - **macOS / Linux:** install the [GitHub CLI](https://cli.github.com) and run `gh auth login` once (choose *GitHub.com → HTTPS → Login with a web browser*). It configures Git to use your GitHub login.
3. Alternatives you may meet later: a **personal access token** typed in place of the password, or **SSH keys** (`git@github.com:…` URLs). Either works; this lab uses HTTPS URLs.

## Step 4 — How Git works: four places

Almost every Git command moves changes between four places:

```text
 working tree ──git add──▶ staging area ──git commit──▶ local repository ──git push──▶ remote (GitHub)
 (your files)              (next commit)                (.git folder,                  ("origin")
                                                          full history)
 working tree ◀──git switch / git restore── local repository ◀──git pull / git clone── remote (GitHub)
```

- **Working tree** — the files you see and edit.
- **Staging area** — the changes you have selected (`git add`) for the next commit. It lets you commit a model change and its matching test together, and leave unrelated edits out.
- **Commit** — a permanent snapshot of the staged files, with author, date, message and a unique ID (the *hash*, e.g. `a73f2c1`). Commits are never changed afterwards; new commits are added on top.
- **Branch** — a movable name pointing to the latest commit of a line of work (`main`, `develop`, `feature/REQ-07-…`).
- **Tag** — a fixed name for one specific commit (`baseline/req-v1.0`, `v1.0.0`). Unlike a branch, it never moves — which is why tags identify baselines and releases.
- **Remote** — the copy on GitHub, called `origin` by default.

## Step 5 — The everyday commands

| Command | What it does |
|---|---|
| `git clone <url>` | Copy a repository from GitHub to your computer (once) |
| `git status` | Show what changed, what is staged and which branch you are on — **run it often** |
| `git add <file or folder>` | Stage changes for the next commit (`git add .` = everything in the current folder) |
| `git commit -m "REQ-07: …"` | Record the staged changes as a commit |
| `git diff` / `git diff --staged` | Show unstaged / staged changes line by line |
| `git log --oneline --graph --all` | Show the history of all branches as a graph |
| `git switch <branch>` | Move to an existing branch |
| `git switch -c <new-branch>` | Create a branch at the current commit and move to it |
| `git branch -a` | List local and remote branches |
| `git merge <branch>` | Bring another branch's commits into the current branch |
| `git push` / `git push -u origin <branch>` | Send commits to GitHub (`-u` the first time, to link the branch) |
| `git pull` | Fetch new commits from GitHub and merge them into the current branch |
| `git tag -a <name> -m "…"` | Create an annotated tag on the current commit; `git push origin <name>` publishes it |
| `git restore <file>` | Throw away unstaged edits to a file (careful — they are lost) |
| `git restore --staged <file>` | Unstage a file, keeping your edits |

> **Graphical tools.** VS Code's *Source Control* panel and *GitHub Desktop* run the same commands behind buttons and are fine for everyday work. This lab writes the commands out because they show exactly what happens — and because a CM plan has to describe a procedure precisely.

## Step 6 — Practise in a scratch repository

Before touching the Cruise Control project, try the whole cycle in a throw-away folder (not inside another repository):

```bash
mkdir git-practice
cd git-practice
git init                               # creates the hidden .git folder; you are on branch "main"
echo "REQ-01: the system shall ..." > requirements.md
git status                             # requirements.md is "untracked"
git add requirements.md
git status                             # now listed under "Changes to be committed" (staged)
git commit -m "REQ-01: first requirement"

echo "REQ-02: the system shall ..." >> requirements.md
git diff                               # shows the added line
git commit -am "REQ-02: second requirement"   # -a stages files Git already tracks

git switch -c feature/REQ-03-limit     # a branch for one change
echo "REQ-03: the speed shall be limited ..." >> requirements.md
git commit -am "REQ-03: speed limit"
git switch main                        # REQ-03 is not here yet
git merge feature/REQ-03-limit         # now it is (a "fast-forward": main had no new commits, so it just moves up)
git tag -a v0.1.0 -m "Practice release"

git log --oneline --graph --all        # read the history: commits, branch, tag
```

Make sure you can explain every line of the final `git log` output. Then delete the `git-practice` folder — it was only practice.

## When something goes wrong

| Situation | What to do |
|---|---|
| Edited a file by mistake, not committed | `git restore <file>` |
| Staged a file that should not be in the commit | `git restore --staged <file>` |
| Typo in the last commit message, **not pushed yet** | `git commit --amend -m "correct message"` |
| A commit that is **already pushed** was wrong | `git revert <hash>` — creates a new commit that undoes it; the history stays intact |
| `git push` is rejected ("fetch first") | New commits exist on GitHub: `git pull`, then push again |
| Merge conflict | Open the files Git lists, keep the right lines, delete the `<<<<<<<`, `=======`, `>>>>>>>` markers, then `git add` the files and `git commit` |
| Committed a file that should be ignored | Add it to `.gitignore`, run `git rm --cached <file>`, and commit |

> **The CM rule behind this table:** once something is pushed — and especially once it is tagged as a baseline — you do not rewrite it. You add a new, traceable change on top. Never move or delete a `baseline/…` or `v…` tag, and never force-push (`git push --force`) to `main` or `develop`.

---

# Put the Cruise Control Project Under Configuration

Every step below leaves a trace on GitHub that the checker at the end of this lab can see.

## Activity 2A — Create the repository and its structure

1. On GitHub, click **New repository**, name it e.g. `cruise-control-cm`, choose **Public**, and leave *Add a README file* unticked (you add your own in 2B). Then clone it — GitHub shows the URL on the empty repository's page:

   ```bash
   git clone https://github.com/<your-username>/cruise-control-cm.git
   cd cruise-control-cm
   ```

   Git warns that you cloned an empty repository — that is expected.
2. Arrange it like this. **Keep the Lab 4 `CruiseControl/` folder exactly as it is** — `evaluate_cc_full_report.py` expects `cc_wrapper/` and `scenarios/` next to it:

```text
cruise-control-cm/
├── README.md                    project description, tool versions, how to rebuild & verify
├── .gitignore                   everything that is NOT a configuration item
├── requirements/
│   └── requirements.md          REQ-01, 02, 04, 07, 08 from Lab 3 Part 8
├── CruiseControl/               the Lab 4 Scade One project folder, unchanged
│   ├── CruiseControl.sproj
│   ├── assets/                  CC_design.swan, Car_design.swan, Simulation.swan
│   ├── scenarios/               tc01 … tc06 .csv
│   ├── cc_wrapper/              generated — never edited by hand
│   ├── evaluate_cc_full_report.py, requirements.txt, generate_python_wrapper.bat
│   └── …
├── verification/                summary.csv + plots of the run that supports the verification baseline
└── docs/
    └── CMP_CruiseControl.docx   your plan from Lab 1
```

3. A starting `.gitignore` for a Scade One project (adjust it to match section 2 of your CMP):

```text
# Scade One: code-generation jobs, user-specific project state, logs
jobs/
*.sproj.user
*.sproj.editor
pyscadeone.log

# Python
__pycache__/

# Working output — the run that supports a baseline is copied to verification/
CruiseControl/results/
```

## Activity 2B — First commit and the requirements baseline

Commit the requirements first, on their own, then baseline them. Then add the model and the rest.

```bash
git add README.md .gitignore requirements/
git commit -m "REQ-01 REQ-02 REQ-04 REQ-07 REQ-08: add Cruise Control requirements"
git tag -a baseline/req-v1.0 -m "Requirements baseline 1.0 (reviewed)"

git add CruiseControl/ docs/
git commit -m "Add Lab 4 Cruise Control model, scenarios and CMP (implements REQ-01..REQ-08)"
git push -u origin main --tags

git switch -c develop
git push -u origin develop
```

> **Annotated tags** (`-a`) record who created the tag, when, and why — that is exactly the information a baseline needs. A lightweight tag is just a name.

On GitHub, go to **Settings → Branches** and add a protection rule for `main` that requires a pull request before merging. This is the policy from section 7 of your CMP, now enforced by the tool.

## Activity 2C — One controlled change, end to end

Simulate a change request on REQ-07 (for example: retune the regulator, or add a missing scenario that verifies REQ-07):

1. **Issue (change request).** On GitHub, open an issue titled e.g. `REQ-07: add scenario covering regulator convergence`. Note its number (say `#1`).
2. **Branch.**
   ```bash
   git switch develop
   git switch -c feature/REQ-07-regulator-scenario
   ```
3. **Change model, tests and requirements together**, then commit with a traced message:
   ```bash
   git add CruiseControl/scenarios/tc07_regulator_converges.csv
   git commit -m "REQ-07: add regulator convergence scenario (#1)"
   git push -u origin feature/REQ-07-regulator-scenario
   ```
4. **Pull request** into `develop`. In the description write `Refs #1`. Review it (model + tests + requirements), re-run `evaluate_cc_full_report.py`, then merge.
5. **Release.** Open a pull request from `develop` into `main` with `Closes #1` in the description (GitHub closes an issue automatically only when the pull request is merged into the default branch). Merge it, then tag and publish:
   ```bash
   git switch main
   git pull
   git tag -a v1.0.0 -m "Release 1.0.0 — see release notes"
   git push origin v1.0.0
   ```
   On GitHub: **Releases → Draft a new release → choose tag `v1.0.0`**. Paste your release manifest (Lab 1, Activity 1D) into the release notes, and list the issues it closes.

## Activity 2D — Trace a requirement through your configuration

The lecture's example chain was:

`REQ-SAFE-021 → Issue #47 → Commit a73f… → TEST-021 → Release v2.1`

Write the same chain for your change, using real identifiers from your repository, and add it to your README:

```text
REQ-07 → Issue #1 → Commit <short hash> → TC-07 (tc07_regulator_converges.csv) → Release v1.0.0
```

This answers the certification question from the lecture: *can we demonstrate exactly how a safety requirement is implemented and verified in this released version?*

## Activity 2E — Check your repository

Paste the URL of your **public** repository below. The page asks GitHub's API for the current status of the repository — files, branches, tags, releases, commits, pull requests, issues — and checks it against the plan from Lab 1. Fix what fails and check again; it is meant to be run several times.

<div id="repo-checker"><p class="loading">Loading repository checker…</p></div>

| Check | Evidence the checker looks for |
|---|---|
| Public repository | the repository is readable without logging in |
| README / .gitignore | both files at the repository root |
| Requirements | at least one file under `requirements/` |
| Model | a `*.sproj` file and at least one `*.swan` file |
| Test cases | files under a `scenarios/` or `tests/` folder |
| CM Plan | a `.docx` whose name contains `CMP` or `configuration`, under `docs/` |
| Branches | `main` and `develop` |
| Feature work | a `feature/*` branch, or a merged pull request from one |
| Baseline | at least one `baseline/…` tag |
| Version | at least one `vX.Y.Z` (or `vX.Y.Z-rcN`) tag |
| Release | at least one published GitHub Release |
| Review & merge | at least one merged pull request |
| Change request | an issue that mentions a `REQ-…` ID |
| Traced commits | at least 3 commits on the default branch, and at least half of them mention a `REQ-…` ID or an issue `#n` |

> The checker verifies that the *evidence* of your CM process exists. It cannot judge whether your CI table, baselines or reviews are *good* — that is what the CMP document is graded on. A green checklist does not mean the project is compliant with any safety standard.

---

# Summary

- **Git** gives identity and history to every change; **GitHub** adds the control workflow — issues as change requests, pull requests as reviews, a protected `main`, tags as baselines, releases as delivered configurations.
- A configuration you can show is a **consistent set of tagged CI versions**, reachable from a release.
- Traceability + baselines + reproducibility = confidence: you can show exactly *what* was built, *from which* versions, *how* it was verified, and *what* was released.

**Hand in:** your repository URL — with all checks passing, or an explanation in the README for any that do not — with `docs/CMP_CruiseControl.docx` inside it.
