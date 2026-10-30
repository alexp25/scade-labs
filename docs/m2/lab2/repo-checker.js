// GitHub Configuration Management checker for Module 2 · Lab 2.
//
// A student pastes the URL of their public GitHub repository; the page asks
// the GitHub REST API for the repository's current status (file tree,
// branches, tags, releases, commits, pull requests, issues), and grades it
// against the CM plan from Lab 1, as implemented in lab.md (Lab 2).
//
// Split in two layers so the grading can be tested outside a browser:
//   fetchSnapshot()  - the only part that talks to api.github.com
//   evaluateRepo()   - pure: snapshot in, rule results out (no I/O)
//
// Unauthenticated GitHub API calls are limited to 60/hour per IP (a whole
// classroom behind one NAT shares that). One check costs 8 calls, so an
// optional personal access token can be supplied; it is kept only in
// sessionStorage and sent only to api.github.com.

(function (root) {
  const API = "https://api.github.com";
  const REQ_RE = /\bREQ-(?:[A-Z]+-)*\d+\b/i;
  const ISSUE_RE = /#\d+\b/;
  const RELEASE_TAG_RE = /^v\d+\.\d+\.\d+(-rc\d+)?$/;
  const TOKEN_KEY = "m2-lab2-gh-token";

  function parseRepoUrl(input) {
    const s = String(input || "").trim().replace(/\/+$/, "").replace(/\.git$/, "");
    let m = s.match(/^(?:https?:\/\/)?(?:www\.)?github\.com\/([\w.-]+)\/([\w.-]+)/i);
    if (!m) m = s.match(/^([\w.-]+)\/([\w.-]+)$/);
    return m ? { owner: m[1], repo: m[2] } : null;
  }

  class CheckError extends Error {
    constructor(kind, message, extra) {
      super(message);
      this.kind = kind;
      Object.assign(this, extra || {});
    }
  }

  async function fetchSnapshot(owner, repo, opts) {
    const token = opts && opts.token;
    const fetchImpl = (opts && opts.fetchImpl) || root.fetch.bind(root);
    const headers = { Accept: "application/vnd.github+json" };
    if (token) headers.Authorization = `Bearer ${token}`;

    async function gh(path, { emptyOn409 = false } = {}) {
      const res = await fetchImpl(`${API}${path}`, { headers });
      if (res.ok) return res.json();
      // 409 = "Git Repository is empty" for tree/commit endpoints
      if (res.status === 409 && emptyOn409) return null;
      const remaining = res.headers.get("x-ratelimit-remaining");
      if ((res.status === 403 || res.status === 429) && remaining === "0") {
        const reset = Number(res.headers.get("x-ratelimit-reset")) * 1000;
        throw new CheckError("ratelimit", "GitHub API rate limit reached.", { reset });
      }
      if (res.status === 404) {
        throw new CheckError("notfound", `Repository ${owner}/${repo} was not found, or it is private.`);
      }
      if (res.status === 401) throw new CheckError("auth", "The access token was rejected by GitHub.");
      throw new CheckError("http", `GitHub API error ${res.status} on ${path}`);
    }

    const base = `/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}`;
    const info = await gh(base);
    const branchRef = encodeURIComponent(info.default_branch);
    const [tree, branches, tags, releases, commits, pulls, issues] = await Promise.all([
      gh(`${base}/git/trees/${branchRef}?recursive=1`, { emptyOn409: true }),
      gh(`${base}/branches?per_page=100`),
      gh(`${base}/tags?per_page=100`),
      gh(`${base}/releases?per_page=100`),
      gh(`${base}/commits?per_page=100`, { emptyOn409: true }),
      gh(`${base}/pulls?state=closed&per_page=100`),
      gh(`${base}/issues?state=all&per_page=100`),
    ]);

    return {
      repo: { fullName: info.full_name, private: info.private, defaultBranch: info.default_branch, url: info.html_url },
      paths: tree ? tree.tree.filter(e => e.type === "blob").map(e => e.path) : [],
      branches: branches.map(b => b.name),
      tags: tags.map(t => t.name),
      releases: releases.map(r => ({ tag: r.tag_name, name: r.name || "" })),
      commits: (commits || []).map(c => c.commit.message),
      pulls: pulls.map(p => ({ number: p.number, title: p.title || "", head: p.head ? p.head.ref : "", merged: !!p.merged_at })),
      // the issues endpoint also returns pull requests - keep real issues only
      issues: issues.filter(i => !i.pull_request).map(i => ({ number: i.number, title: i.title || "", body: i.body || "" })),
    };
  }

  function evaluateRepo(snap) {
    const paths = snap.paths;
    const has = re => paths.filter(p => re.test(p));
    const list = (items, n = 4) => items.slice(0, n).join(", ") + (items.length > n ? `, … (+${items.length - n})` : "");
    const results = [];
    const rule = (id, label, ok, detail, hint) => results.push({ id, label, ok: !!ok, detail, hint });

    rule("public", "Repository is public", !snap.repo.private,
      snap.repo.fullName, "Make the repository public so it can be checked.");

    const readme = has(/^readme\.md$/i), gitignore = has(/^\.gitignore$/);
    rule("readme", "README.md and .gitignore at the repository root", readme.length && gitignore.length,
      `${readme.length ? "README.md ✓" : "README.md missing"} · ${gitignore.length ? ".gitignore ✓" : ".gitignore missing"}`,
      "Add a README describing the project and a .gitignore excluding non-CIs (jobs/, *.sproj.user, …).");

    const reqs = has(/^requirements\//i);
    rule("requirements", "Requirements are under configuration (requirements/)", reqs.length,
      reqs.length ? list(reqs) : "no files under requirements/", "Commit your requirements (Lab 3 Part 8) under requirements/.");

    const sproj = has(/\.sproj$/i), swan = has(/\.swan$/i);
    rule("model", "Scade One model is under configuration (*.sproj + *.swan)", sproj.length && swan.length,
      sproj.length || swan.length ? list(sproj.concat(swan)) : "no .sproj / .swan files found",
      "Commit the Scade One project file and its assets/*.swan model files.");

    const tests = has(/(^|\/)(tests?|scenarios)\/[^/]+$/i);
    rule("tests", "Test cases are under configuration (scenarios/ or tests/)", tests.length,
      tests.length ? list(tests) : "no files under a scenarios/ or tests/ folder",
      "Commit the scenario CSVs (CruiseControl/scenarios/) together with the model.");

    // filename must name the plan (CMP / configuration), not just be any .docx
    const cmp = has(/^(docs|documentation)\/(.*\/)?[^/]*(cmp|configuration)[^/]*\.docx$/i);
    rule("cmp", "Configuration Management Plan (.docx) under docs/", cmp.length,
      cmp.length ? list(cmp) : "no CMP*.docx under docs/ or documentation/", "Commit your completed CMP from Lab 1 as docs/CMP_CruiseControl.docx.");

    const hasMain = snap.branches.includes("main"), hasDev = snap.branches.some(b => /^dev(elop(ment)?)?$/.test(b));
    rule("branches", "Long-lived branches: main and develop", hasMain && hasDev,
      `branches: ${list(snap.branches, 6) || "none"}`, "Create a develop branch from main (git switch -c develop; git push -u origin develop).");

    const featureBranches = snap.branches.filter(b => b.startsWith("feature/"));
    const featurePulls = snap.pulls.filter(p => p.merged && p.head.startsWith("feature/"));
    rule("feature", "Changes are made in feature/* branches", featureBranches.length || featurePulls.length,
      featureBranches.length || featurePulls.length
        ? list(featureBranches.concat(featurePulls.map(p => `${p.head} (merged in #${p.number})`)))
        : "no feature/* branch found (open or merged)",
      "Work on each change request in its own branch, e.g. feature/REQ-07-regulator.");

    const baselines = snap.tags.filter(t => t.startsWith("baseline/"));
    rule("baseline", "At least one baseline tag (baseline/…)", baselines.length,
      baselines.length ? list(baselines) : `tags: ${list(snap.tags) || "none"}`,
      "Tag the approved requirements: git tag -a baseline/req-v1.0 -m \"…\"; git push origin --tags.");

    const releaseTags = snap.tags.filter(t => RELEASE_TAG_RE.test(t));
    rule("version", "At least one release version tag (vMAJOR.MINOR.PATCH)", releaseTags.length,
      releaseTags.length ? list(releaseTags) : "no tag matches vX.Y.Z or vX.Y.Z-rcN", "Tag the release on main, e.g. v1.0.0.");

    rule("release", "A GitHub Release is published", snap.releases.length,
      snap.releases.length ? list(snap.releases.map(r => r.tag)) : "no releases", "Create a GitHub Release from your v1.0.0 tag, with release notes.");

    const merged = snap.pulls.filter(p => p.merged);
    rule("pr", "Changes were integrated through a merged pull request", merged.length,
      merged.length ? list(merged.map(p => `#${p.number} ${p.title}`), 3) : "no merged pull requests",
      "Merge your feature branch through a pull request instead of a direct push.");

    const reqIssues = snap.issues.filter(i => REQ_RE.test(i.title) || REQ_RE.test(i.body));
    rule("issue", "A change request (issue) references a requirement ID", reqIssues.length,
      reqIssues.length ? list(reqIssues.map(i => `#${i.number} ${i.title}`), 3) : `${snap.issues.length} issue(s), none mentions a REQ-… ID`,
      "Open an issue describing the change and name the requirement, e.g. \"REQ-07: …\".");

    const traced = snap.commits.filter(m => REQ_RE.test(m) || ISSUE_RE.test(m));
    const ratio = snap.commits.length ? traced.length / snap.commits.length : 0;
    rule("commits", "At least half of the commits reference a REQ ID or an issue (#n)", snap.commits.length >= 3 && ratio >= 0.5,
      `${traced.length} of ${snap.commits.length} commit(s) on ${snap.repo.defaultBranch} (${Math.round(ratio * 100)}%)`,
      "Start commit messages with the requirement or issue, e.g. \"REQ-07: tune regulator gain (#1)\".");

    return results;
  }

  // ── Browser UI ────────────────────────────────────────────────────────
  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function storedToken() {
    try { return sessionStorage.getItem(TOKEN_KEY) || ""; } catch (e) { return ""; }
  }

  function initRepoChecker() {
    const box = document.getElementById("repo-checker");
    if (!box) return;
    box.innerHTML = `
      <div class="rc-row">
        <input type="text" id="rc-url" placeholder="https://github.com/your-user/cruise-control-cm" spellcheck="false" />
        <button type="button" id="rc-check">Check repository</button>
      </div>
      <details class="rc-token" id="rc-token-box">
        <summary>Optional: GitHub access token (only if you hit the rate limit)</summary>
        <p>Without a token GitHub allows 60 API requests per hour per network; one check uses 8.
          A <a href="https://github.com/settings/tokens?type=beta" target="_blank" rel="noopener">fine-grained token</a>
          with <em>public repositories (read-only)</em> access raises the limit. It is kept only in this browser tab
          (sessionStorage) and sent only to api.github.com.</p>
        <input type="password" id="rc-token" placeholder="github_pat_…" autocomplete="off" />
      </details>
      <div id="rc-status" class="rc-status"></div>
      <ul id="rc-results" class="rc-results"></ul>`;

    const urlEl = document.getElementById("rc-url");
    const tokenEl = document.getElementById("rc-token");
    const btn = document.getElementById("rc-check");
    const statusEl = document.getElementById("rc-status");
    const resultsEl = document.getElementById("rc-results");
    tokenEl.value = storedToken();

    async function run() {
      const target = parseRepoUrl(urlEl.value);
      resultsEl.innerHTML = "";
      if (!target) {
        statusEl.className = "rc-status rc-bad";
        statusEl.textContent = "Paste a repository URL like https://github.com/owner/repo.";
        return;
      }
      const token = tokenEl.value.trim();
      try { token ? sessionStorage.setItem(TOKEN_KEY, token) : sessionStorage.removeItem(TOKEN_KEY); } catch (e) { /* storage unavailable */ }

      btn.disabled = true;
      statusEl.className = "rc-status";
      statusEl.textContent = `Requesting status of ${target.owner}/${target.repo} from GitHub…`;
      try {
        const snap = await fetchSnapshot(target.owner, target.repo, { token });
        const results = evaluateRepo(snap);
        const passed = results.filter(r => r.ok).length;
        resultsEl.innerHTML = results.map(r => `
          <li class="${r.ok ? "rc-ok" : "rc-fail"}">
            <span class="rc-icon">${r.ok ? "✓" : "✗"}</span>
            <div><strong>${escapeHtml(r.label)}</strong>
              <div class="rc-detail">${escapeHtml(r.detail)}</div>
              ${r.ok ? "" : `<div class="rc-hint">${escapeHtml(r.hint)}</div>`}
            </div>
          </li>`).join("");
        statusEl.className = "rc-status " + (passed === results.length ? "rc-good" : "rc-bad");
        statusEl.innerHTML = `<strong>${passed} / ${results.length}</strong> checks passed for
          <a href="${escapeHtml(snap.repo.url)}" target="_blank" rel="noopener">${escapeHtml(snap.repo.fullName)}</a>`;
        if (window.recordQuizAttempt) window.recordQuizAttempt("m2-lab2", "repo-check", passed, results.length);
      } catch (err) {
        statusEl.className = "rc-status rc-bad";
        if (err.kind === "ratelimit") {
          const when = err.reset ? ` It resets at ${new Date(err.reset).toLocaleTimeString()}.` : "";
          statusEl.textContent = `GitHub's API rate limit for your network was reached.${when} You can add an access token below and try again.`;
          document.getElementById("rc-token-box").open = true;
        } else {
          statusEl.textContent = err.kind ? err.message : `Could not reach GitHub: ${err.message}`;
        }
      } finally {
        btn.disabled = false;
      }
    }

    btn.addEventListener("click", run);
    urlEl.addEventListener("keydown", e => { if (e.key === "Enter") run(); });
  }

  const api = { parseRepoUrl, fetchSnapshot, evaluateRepo };
  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  } else {
    root.RepoChecker = api;
    root.initRepoChecker = initRepoChecker;
  }
})(typeof window !== "undefined" ? window : globalThis);
