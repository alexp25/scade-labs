# Firebase backend: login, progress tracking, and the admin panel

See `.agents/decisions/0002-firebase-backend-for-auth-and-progress.md` for
why this was introduced. This page is the canonical, longer write-up of the
setup and operational procedure (per ADR 0001, canonical documentation lives
here, not under `docs/`).

## What this is

A client-side-only integration: no server, no build step, no Firebase CLI.
Every page that needs it loads the Firebase Web SDK directly from
`gstatic.com` as ES modules (`<script type="module">`). It adds:

- Optional email/password login (`docs/account/index.html`).
- Progress tracking: which labs a student opened and how many times, and
  every quiz/code-run attempt with its score — recorded automatically once a
  student is logged in, via `window.recordLabOpen(labId)` and
  `window.recordQuizAttempt(labId, quizId, score, total)` (defined in
  `docs/assets/js/auth-header.js`).
- A secured admin view (`docs/admin/index.html`) listing every student's
  progress.

Lab content itself is never gated — anonymous visitors can still read every
lab and take every quiz; only the recording of that activity requires login.

## One-time setup (must be done by whoever runs the class — not automatable from this repo)

1. Create a free project at https://console.firebase.google.com.
2. **Authentication** → Sign-in method → enable **Email/Password**.
3. **Firestore Database** → Create database (production mode; the rules
   below apply regardless of this toggle).
4. **Project settings** → "Your apps" → Add app → Web (`</>`). Copy the
   resulting `firebaseConfig` object.
5. Paste that object into `docs/assets/js/firebase-config.js`, replacing the
   placeholder values. These values are not secret — they identify the
   project, not grant access to it; Firestore Security Rules are the actual
   access boundary (see below).
6. Paste the contents of `firestore.rules` (repo root) into Firestore
   Database → Rules tab in the console, then click Publish. There is no
   CLI/deploy pipeline — the console is where these rules actually take
   effect; the repo file is the source of truth to copy from and diff
   against on future changes.
7. Sign up once through the live `/account/` page. Then, in Firestore
   Database → Data, open the new `profiles/{yourUid}` document and manually
   change `isAdmin` to `true`. This is intentionally the only way to become
   an admin — no code path in this repo can do it, so a compromised or
   malicious client can never self-promote.

## Data model

| Collection | Doc ID | Fields | Written by |
|---|---|---|---|
| `profiles` | Firebase Auth UID | `email`, `displayName`, `isAdmin`, `createdAt` | Client, on first login (`isAdmin` always created `false`; only editable via the Firebase console) |
| `labOpens` | `{uid}_{labId}` | `userId`, `labId`, `firstOpenedAt`, `lastOpenedAt`, `openCount` | Client, via `window.recordLabOpen(labId)`, called once per page load once a session exists |
| `quizAttempts` | auto-ID | `userId`, `labId`, `quizId`, `score`, `total`, `submittedAt` | Client, via `window.recordQuizAttempt(...)`, called from Lab 3.1/3.2's quiz submit handler and from Lab 2's `runCode()` (using `quizId: 'code-run'`, `score`/`total` = pass/fail line counts from the test output) |

## Security model

`firestore.rules` (repo root) is the actual access boundary. Every rule
checks `request.auth.uid` (verified server-side by Firebase from the
caller's ID token — never anything the client can forge) against either the
document's own `userId`/doc-ID, or an `isAdmin()` helper that looks up the
caller's *own* `profiles.isAdmin` field. This means:

- A student can only ever read/write their own `profiles`, `labOpens`, and
  `quizAttempts` documents.
- `profiles` create/update rules explicitly forbid ever setting `isAdmin` to
  anything but its existing value — a student account cannot self-promote by
  crafting a client-side write.
- `docs/admin/index.html`'s own "is this user an admin" check and its
  redirect-if-logged-out behavior are UX conveniences only. The real
  enforcement is that Firestore itself returns zero rows / a
  permission-denied error to any non-admin caller, regardless of what the
  page's JavaScript does or whether the redirect is bypassed.

## Maintenance notes

- If `firestore.rules` changes in this repo, a maintainer must manually
  re-paste it into the Firebase console — nothing in this repo deploys it
  automatically.
- `docs/assets/js/firebase-client.js` pins the SDK version in its `import`
  URLs (currently `10.14.1`); bump it there if a newer SDK version is
  needed, matching the pattern the rest of this repo already uses for
  CDN-pinned dependencies (see `.agents/integrations.md`).
- There is no automated test coverage for any of this (no CI, no test
  runner in this repo) — verify changes manually against a real Firebase
  project by signing up, opening a lab, taking a quiz, and checking the
  Firestore console / `/account/` / `/admin/` pages.
