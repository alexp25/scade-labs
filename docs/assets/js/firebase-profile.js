// Shared "ensure a profiles/{uid} document exists" logic, used by every
// page that establishes a session (auth-header.js's widget, and
// docs/account/index.html which doesn't load that widget but is where most
// users actually register). Keeping this in one place avoids the bug where
// only some pages created the profile doc on first login.

import { db } from "./firebase-client.js";
import {
  doc,
  getDoc,
  setDoc,
  serverTimestamp,
} from "https://www.gstatic.com/firebasejs/10.14.1/firebase-firestore.js";

export async function ensureProfile(user) {
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
