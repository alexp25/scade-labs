// Single Firebase app/auth/Firestore bootstrap, shared by every page that
// needs auth or progress tracking. Loaded as an ES module
// (<script type="module">) so it can use CDN `import`s directly — no
// bundler, consistent with the rest of this static site.

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-firestore.js";
import { firebaseConfig } from "./firebase-config.js";

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);
