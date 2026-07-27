// Shared auth-state widget + progress-tracking helpers.
//
// Each page that wants login/tracking loads this as an ES module and adds
// `<div id="auth-slot" data-base="...">` in its header, where `data-base`
// is the relative path prefix to reach `account/`/`admin/` from that page
// (e.g. "./" from docs/index.html, "../" from docs/lab2/index.html).
//
// Exposes window.recordLabOpen(labId) and
// window.recordQuizAttempt(labId, quizId, score, total) for lab pages to
// call; both are no-ops when nobody is signed in, since lab content stays
// open to everyone and tracking is purely additive.

import { auth, db } from "./firebase-client.js";
import {
  onAuthStateChanged,
  signOut,
} from "https://www.gstatic.com/firebasejs/10.14.1/firebase-auth.js";
import {
  doc,
  getDoc,
  setDoc,
  addDoc,
  collection,
  serverTimestamp,
  increment,
} from "https://www.gstatic.com/firebasejs/10.14.1/firebase-firestore.js";

const slot = document.getElementById("auth-slot");
const base = slot ? slot.dataset.base || "./" : "./";

let currentUser = null;
let currentProfile = null;

function escapeHtml(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function render() {
  if (!slot) return;

  if (!currentUser) {
    slot.innerHTML = `<a class="auth-link" href="${base}account/">Log in / Register</a>`;
    return;
  }

  const adminLink = currentProfile && currentProfile.isAdmin
    ? ` · <a class="auth-link" href="${base}admin/">Admin</a>`
    : "";

  slot.innerHTML = `
    <span class="auth-status">Signed in as ${escapeHtml(currentUser.email)}</span>
    <a class="auth-link" href="${base}account/">My Progress</a>${adminLink}
    <button type="button" class="auth-link auth-logout" id="auth-logout-btn">Log out</button>
  `;
  const logoutBtn = document.getElementById("auth-logout-btn");
  if (logoutBtn) logoutBtn.addEventListener("click", () => signOut(auth));
}

async function ensureProfile(user) {
  const ref = doc(db, "profiles", user.uid);
  const snap = await getDoc(ref);
  if (snap.exists()) return snap.data();

  const profile = {
    email: user.email || "",
    displayName: user.displayName || "",
    isAdmin: false,
    createdAt: serverTimestamp(),
  };
  await setDoc(ref, profile);
  return profile;
}

onAuthStateChanged(auth, async (user) => {
  currentUser = user;
  currentProfile = user ? await ensureProfile(user) : null;
  render();
  // Pages set window.CURRENT_LAB_ID before loading this module so the
  // "lab opened" event can be recorded automatically once a session is
  // known, without every lab page needing its own auth-ready polling logic.
  if (user && window.CURRENT_LAB_ID) {
    window.recordLabOpen(window.CURRENT_LAB_ID);
  }
});

// Minimal styling reusing whatever CSS variables the host page already
// defines in its own `:root` — no shared stylesheet needed.
const style = document.createElement("style");
style.textContent = `
  #auth-slot { display: flex; align-items: center; gap: .75rem; flex-wrap: wrap; font-size: .82rem; }
  #auth-slot .auth-link { color: var(--sky, #1E88E5); text-decoration: none; font-weight: 600; background: none; border: none; cursor: pointer; font: inherit; padding: 0; }
  #auth-slot .auth-link:hover { text-decoration: underline; }
  #auth-slot .auth-status { color: #90A4AE; }
`;
document.head.appendChild(style);

// ── Progress-tracking helpers, called from lab pages ───────────────────────
window.recordLabOpen = async function recordLabOpen(labId) {
  if (!currentUser) return;
  try {
    const ref = doc(db, "labOpens", `${currentUser.uid}_${labId}`);
    const snap = await getDoc(ref);
    if (snap.exists()) {
      await setDoc(
        ref,
        { userId: currentUser.uid, labId, lastOpenedAt: serverTimestamp(), openCount: increment(1) },
        { merge: true }
      );
    } else {
      await setDoc(ref, {
        userId: currentUser.uid,
        labId,
        firstOpenedAt: serverTimestamp(),
        lastOpenedAt: serverTimestamp(),
        openCount: 1,
      });
    }
  } catch (err) {
    console.warn("recordLabOpen failed:", err);
  }
};

window.recordQuizAttempt = async function recordQuizAttempt(labId, quizId, score, total) {
  if (!currentUser) return;
  try {
    await addDoc(collection(db, "quizAttempts"), {
      userId: currentUser.uid,
      labId,
      quizId,
      score,
      total,
      submittedAt: serverTimestamp(),
    });
  } catch (err) {
    console.warn("recordQuizAttempt failed:", err);
  }
};
