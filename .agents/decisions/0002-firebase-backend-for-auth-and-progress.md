# ADR 0002: Firebase as the backend for login, progress tracking, and the admin panel

**Date:** this session.

## Context

Until now this repo had no database, API, authentication, or hosted backend
service — `.agents/architecture.md` and `.agents/integrations.md` stated this
explicitly, and it was true. The user asked for student login/registration,
per-student progress tracking (labs opened, quiz scores), and a secured
admin view of all students' progress. GitHub Pages (the site's only hosting)
cannot run server code, so any of this requires an external backend.

## Decision

Use Firebase (Firebase Authentication for email/password accounts, Firestore
for data) as the sole backend, added client-side only via the Firebase Web
SDK loaded from a CDN as ES modules. No bundler, no Firebase CLI, no build
step — `docs/` remains a plain static site served as-is by GitHub Pages.

## Why

- Managed auth + database avoids building and hosting a custom server for a
  small class (tens of students), which this repo's static-hosting setup
  cannot run anyway.
- Firebase's Web SDK works as plain `<script type="module">` imports from
  `gstatic.com`, matching the site's existing pattern of loading libraries
  (marked.js, highlight.js, CodeMirror, Skulpt) directly from a CDN with no
  build tooling.
- Firestore Security Rules enforce access control server-side (inside
  Firestore itself), so the "admin" check is never trusted to client code —
  see `firestore.rules` at the repo root and
  `project_docs/integrations/firebase.md` for the full model.
- Lab content stays fully public; login is only required to record progress
  and to view `/admin/` — this was an explicit choice to avoid turning a
  previously open site into a gated one.

## Consequences

- `.agents/architecture.md` and `.agents/integrations.md` are updated to
  describe this backend instead of stating none exists.
- `firestore.rules` (repo root) is the hand-authored source of truth for
  security rules; there is no CI/deploy pipeline for it — a maintainer must
  manually paste it into the Firebase console's Rules tab after any change.
- `docs/assets/js/firebase-config.js` ships with placeholder values; a real
  Firebase project must be provisioned by whoever runs the class (see
  `project_docs/integrations/firebase.md`), and only they can promote an
  account to `isAdmin: true` (a manual Firestore console edit — there is no
  code path that can do this, by design, so a client can never
  self-promote).
- New paths added to the repo: `docs/assets/js/firebase-*.js`,
  `docs/assets/js/auth-header.js`, `docs/account/`, `docs/admin/`,
  `firestore.rules`.
