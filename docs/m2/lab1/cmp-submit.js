// CMP submission form for Module 2 · Lab 1.
//
// The site is static (GitHub Pages), so it cannot send email itself. The form
// is posted to FormSubmit (https://formsubmit.co), a third-party form-to-email
// service that forwards the fields and the attached .docx to MENTOR_EMAIL.
//
// A plain (non-AJAX) multipart POST is used because file attachments are only
// forwarded for regular form submissions. After sending, FormSubmit redirects
// back to this page (`_next`) with #cmp-submitted, which shows a confirmation.
//
// Operational notes:
// - FormSubmit sends an activation email to MENTOR_EMAIL on the very first
//   submission; nothing is forwarded until the mentor confirms it once.
// - MENTOR_EMAIL is a placeholder until the real mentor address is set.

(function () {
  const MENTOR_EMAIL = "xxxx@upb.ro";
  const MAX_BYTES = 5 * 1024 * 1024;

  function initCmpSubmit() {
    const box = document.getElementById("cmp-submit");
    if (!box) return;

    const back = location.href.split("#")[0] + "#cmp-submitted";
    box.innerHTML = `
      <form id="cmp-form" action="https://formsubmit.co/${MENTOR_EMAIL}" method="POST" enctype="multipart/form-data">
        <input type="hidden" name="_subject" value="[M2 Lab 1] CMP submission" />
        <input type="hidden" name="_template" value="table" />
        <input type="hidden" name="_next" value="${back}" />
        <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" />
        <div class="cs-grid">
          <label>Full name<input type="text" name="name" required /></label>
          <label>Your email<input type="email" name="email" required placeholder="you@stud.upb.ro" /></label>
          <label>Group<input type="text" name="group" placeholder="e.g. 1241EA" /></label>
          <label>GitHub repository URL (optional)<input type="url" name="repository" placeholder="https://github.com/…" /></label>
        </div>
        <label>Configuration Management Plan (.docx)
          <input type="file" name="attachment" id="cs-file" accept=".docx,application/vnd.openxmlformats-officedocument.wordprocessingml.document" required />
        </label>
        <label>Message to the mentor (optional)<textarea name="message" rows="3"></textarea></label>
        <div class="cs-actions">
          <button type="submit" id="cs-send">Send to mentor</button>
          <button type="button" id="cs-mail">&#9993; Email it instead</button>
          <span class="cs-to">Recipient: <code>${MENTOR_EMAIL}</code></span>
        </div>
        <p class="cs-note">If <strong>Send to mentor</strong> shows an error page (the upload service is external and
          occasionally down), come back and use <strong>Email it instead</strong>: it opens your own mail app with
          the message filled in — attach your <code>.docx</code> there before sending.</p>
        <div id="cs-status" class="cs-status"></div>
      </form>`;

    const form = document.getElementById("cmp-form");
    const fileEl = document.getElementById("cs-file");
    const statusEl = document.getElementById("cs-status");

    // Fallback that needs no third party: a mailto: link cannot carry the
    // attachment, so the student attaches the file in their own mail client.
    document.getElementById("cs-mail").addEventListener("click", () => {
      const f = name => (form.elements[name].value || "").trim();
      const file = fileEl.files[0];
      const body = [
        `Name: ${f("name") || "-"}`,
        `Group: ${f("group") || "-"}`,
        `GitHub repository: ${f("repository") || "-"}`,
        "",
        f("message"),
        "",
        `Attached: ${file ? file.name : "CMP_CruiseControl.docx"}  <-- remember to attach the file before sending`,
      ].join("\n");
      const subject = `[M2 Lab 1] CMP submission - ${f("name") || "student"}`;
      location.href = `mailto:${MENTOR_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      statusEl.className = "cs-status";
      statusEl.textContent = "Your mail app should open now. Attach your .docx there and send it.";
    });

    form.addEventListener("submit", e => {
      const file = fileEl.files[0];
      let error = "";
      if (!file) error = "Choose your CMP .docx file.";
      else if (!/\.docx$/i.test(file.name)) error = "The plan must be a Word .docx file.";
      else if (file.size > MAX_BYTES) error = "The file is larger than 5 MB.";
      if (error) {
        e.preventDefault();
        statusEl.className = "cs-status cs-bad";
        statusEl.textContent = error;
        return;
      }
      statusEl.className = "cs-status";
      statusEl.textContent = "Sending…";
      document.getElementById("cs-send").disabled = true;
    });

    if (location.hash === "#cmp-submitted") {
      statusEl.className = "cs-status cs-good";
      statusEl.textContent = "✓ Your plan was sent to the mentor.";
      box.scrollIntoView({ block: "center" });
    }
  }

  window.initCmpSubmit = initCmpSubmit;
})();
