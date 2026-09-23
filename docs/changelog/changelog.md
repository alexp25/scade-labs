# Portfolio Changelog

A high-level, admin-facing summary of what changed in this portfolio and
when. This is a curated view, not the full maintainer history — it skips
validation notes, file lists, and session narration. Newest first.

> This page is intentionally short per entry. It exists so an admin can see
> "what changed recently" without digging through commit history.

---

## 2026-09-23 — Lab 6: Software Architecture (new lab)

Added a sixth lab on software architecture, built around the existing Lab 4
Cruise Control model. Students get a short recap of the lecture, then work
through three hands-on exercises using a new live, editable diagram tool
(finish the Cruise Control component diagram, sketch a whole-vehicle view,
and propose an emergency-braking extension). Fully registered across the
site (portfolio card, admin/account labels, quiz).

## 2026-09-23 — Lab 5: condensed to a recap

Reworked Lab 5 (Design Principles) so it no longer reproduces the lecture
slides in full — replaced with a short recap plus a link to the course
slides viewer. The reading, paper citation, and quiz are unchanged.

## 2026-09-23 — Lab 4: added a full-script reference

Students can now expand the two Cruise Control evaluation scripts in full
(collapsed by default) directly on the lab page, instead of only seeing
excerpts. Live in-browser execution isn't possible for these scripts since
they depend on a compiled model wrapper.

## 2026-09-23 — Lab 5: Design Principles (new lab)

Added a fifth lab on software design principles (top-down design,
modularity, strong typing, SOLID, DRY/KISS, model-based design), connecting
the lecture to a real automotive architecture research paper, with a quiz.

## 2026-08-18 — Lab 4: script renames for clarity

Renamed the two Cruise Control Python scripts to names that describe what
they do (`evaluate_cc_full_report.py`, `evaluate_cc_quick_tester.py`). No
behavior change.

## 2026-08-11 — Lab 1: Introduction to Software Engineering (new lab)

Added the first lab in the portfolio — a reading-plus-quiz introduction to
the software engineering lifecycle.

## 2026-08-10 — Lab 3 (Requirements Engineering) introduced; numbering reshuffled

Added a new Lab 3 on requirements engineering and traceability, including
an in-browser requirement-traceability checker and Scade One traceability
screenshots. The former Lab 3.1/3.2 became Lab 4.1, then Lab 4.1 was merged
into Lab 3 and Lab 4.2 became the current Lab 4.

## 2026-07-27 — Lab 4 (then Lab 3.2): evaluation moved to Python

Replaced the Scade One test-harness workflow for the Cruise Control lab
with a Python-driven evaluation script against the generated model wrapper,
fixed to match the real PyScadeOne API.

---

*Earlier platform features (login/registration, progress tracking, and this
admin panel) were added alongside the labs above; see the full maintainer
changelog for exact dates if needed.*
