// Shared "Course Slides" widget: renders a header button that opens the
// associated lecture-slide PDF in an in-page viewer (iframe) with a
// download link, so students never have to leave the lab page.
//
// Each lab page loads this as a plain script (not a module, unlike
// auth-header.js) and adds `<div id="course-slides-slot" data-base="...">`
// in its header, mirroring the auth-slot pattern in auth-header.js:
// `data-base` is the relative path prefix to reach `courses/` from that
// page (e.g. "../" from docs/lab2/index.html). Pages set
// window.CURRENT_LAB_ID before loading this script so the slot knows which
// PDF to link to (`courses/<labId>.pdf`).

(function () {
  const slot = document.getElementById("course-slides-slot");
  if (!slot || !window.CURRENT_LAB_ID) return;

  const base = slot.dataset.base || "./";
  const pdfUrl = `${base}courses/${window.CURRENT_LAB_ID}.pdf`;
  const labLabel = document.querySelector(".page-header h1")
    ? document.querySelector(".page-header h1").textContent.replace(/^Lab\s*\d+\s*[—-]\s*/, "")
    : "this lab";

  slot.innerHTML = `<button type="button" class="slides-btn" id="slides-open-btn">&#128196; Course Slides</button>`;

  const modal = document.createElement("div");
  modal.className = "slides-modal";
  modal.id = "slides-modal";
  modal.innerHTML = `
    <div class="slides-modal-backdrop" id="slides-modal-backdrop"></div>
    <div class="slides-modal-panel" role="dialog" aria-modal="true" aria-label="Course slides">
      <div class="slides-modal-header">
        <span>Course Slides &mdash; ${labLabel}</span>
        <div class="slides-modal-actions">
          <a href="${pdfUrl}" download class="slides-download-btn">&#8681; Download</a>
          <button type="button" class="slides-close-btn" id="slides-close-btn" aria-label="Close">&times;</button>
        </div>
      </div>
      <iframe class="slides-modal-frame" id="slides-modal-frame" title="Course slides PDF" src=""></iframe>
    </div>
  `;
  document.body.appendChild(modal);

  const frame = document.getElementById("slides-modal-frame");
  let frameLoaded = false;

  function openModal() {
    if (!frameLoaded) {
      frame.src = pdfUrl;
      frameLoaded = true;
    }
    modal.classList.add("open");
    document.body.style.overflow = "hidden";
  }
  function closeModal() {
    modal.classList.remove("open");
    document.body.style.overflow = "";
  }

  document.getElementById("slides-open-btn").addEventListener("click", openModal);
  document.getElementById("slides-close-btn").addEventListener("click", closeModal);
  document.getElementById("slides-modal-backdrop").addEventListener("click", closeModal);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("open")) closeModal();
  });

  const style = document.createElement("style");
  style.textContent = `
    #course-slides-slot { display: inline-block; margin-left: .5rem; }
    .slides-btn {
      font-size: .8rem; font-weight: 600; color: #90A4AE;
      border: 1px solid #2A4A7F; border-radius: 5px;
      padding: .3rem .75rem; background: none; cursor: pointer;
      font-family: inherit; transition: color .15s, border-color .15s;
    }
    .slides-btn:hover { color: #FFFFFF; border-color: var(--sky, #1E88E5); }

    .slides-modal {
      display: none; position: fixed; inset: 0; z-index: 1000;
      align-items: center; justify-content: center;
    }
    .slides-modal.open { display: flex; }
    .slides-modal-backdrop {
      position: absolute; inset: 0; background: rgba(13, 27, 62, .65);
    }
    .slides-modal-panel {
      position: relative; z-index: 1; display: flex; flex-direction: column;
      width: min(920px, 94vw); height: min(88vh, 1100px);
      background: #FFFFFF; border-radius: 8px; overflow: hidden;
      box-shadow: 0 12px 40px rgba(0,0,0,.35);
    }
    .slides-modal-header {
      display: flex; align-items: center; justify-content: space-between;
      padding: .75rem 1rem; background: var(--navy, #0D1B3E); color: #FFFFFF;
      font-size: .95rem; font-weight: 600;
    }
    .slides-modal-actions { display: flex; align-items: center; gap: .6rem; }
    .slides-download-btn {
      font-size: .8rem; font-weight: 600; color: #FFFFFF;
      background: var(--sky, #1E88E5); border-radius: 5px;
      padding: .3rem .7rem; text-decoration: none;
    }
    .slides-download-btn:hover { background: var(--blue, #1565C0); }
    .slides-close-btn {
      font-size: 1.3rem; line-height: 1; color: #90A4AE; background: none;
      border: none; cursor: pointer; padding: 0 .2rem;
    }
    .slides-close-btn:hover { color: #FFFFFF; }
    .slides-modal-frame { flex: 1; border: none; width: 100%; }

    @media (max-width: 600px) {
      .slides-modal-panel { width: 100vw; height: 100vh; border-radius: 0; }
    }
  `;
  document.head.appendChild(style);
})();
