# Lab 5 — Software Design Principles in Safety-Critical Software Engineering

**Course:** Software Engineering
**Lesson:** Software Design Principles in Safety-Critical Software Engineering and Best Practices
**Duration:** 1 hour
**Tool:** None — a short recap, then a reading + quiz
**Work mode:** Individual
**Recommended prerequisite:** the Lesson 5 lecture/slides on Software Design Principles (this lab assumes you've already seen that material — open it any time with the **Course Slides** button above) and [Lab 1](../lab1/) for the foundational software-engineering vocabulary

---

# Context

The Recap below briefly revisits the vocabulary from Lesson 5 — Top-Down
Design, Modularity, Traceability, Strong Typing, SOLID, DRY, KISS,
Model-Based Design. For the full explanations and worked examples, use the
**Course Slides** button in the header.

This lab's real work is applying those principles somewhere they were
**not** designed for a classroom: a real, recent research paper on
automotive software architecture. You will read the paper, then map each
studied principle onto a specific thing the paper's authors actually did,
and finish with a quiz that checks both the recap and the reading.

---

# Learning Objectives

By the end of this lab you will be able to:

- Recall, in your own words, the eight core design principles for
  safety-critical software and why standards such as DO-178C, ISO 26262,
  EN 50716, IEC 62304, and IEC 61508 require them
- Read a real systems-engineering paper and identify Top-Down Design,
  Modularity, Information Hiding, Traceability, SOLID (Single
  Responsibility, Interface Segregation), and Model-Based Design in a
  concrete, non-classroom example
- Explain how the paper's semantic interface characterization (direction,
  temporal coupling, criticality, binding) relates to the lecture's
  Strong Typing / Deterministic Design and Traceability material
- Apply SOLID, DRY, and KISS to a small automotive brake-controller scenario

---

# Recap — Design Principles Essentials

> Quick reminder of the lecture, not a replacement for it. Open the
> **Course Slides** button above for the full explanations, worked
> examples (Emergency Braking, the Ariane 5 failure, the Brake Controller),
> and the Best Practices / Common Mistakes list.

- **Why design matters more here:** safety-critical software is optimized
  for safety and determinism, not just features — failures must be
  *prevented*, not fixed after release, and verification/documentation are
  mandatory, not optional.
- **Standards drive architecture:** DO-178C (aerospace), ISO 26262
  (automotive), EN 50716 (railway), IEC 62304 (medical), IEC 61508
  (industrial) all require requirements-based design, traceability,
  independent verification, coding guidelines, deterministic behavior, and
  configuration management — the architecture must support certification
  from day one.
- **Top-Down Design:** decompose from mission → system → subsystems →
  components → functions → implementation, for easier verification and
  requirement allocation.
- **Modularity & Information Hiding:** independent modules that expose only
  necessary interfaces — a defect stays localized instead of propagating.
- **Traceability by Design:** requirement → architecture → model → code →
  test, kept linked for compliance, impact analysis, and audits.
- **Strong Typing & Deterministic Design:** explicit types, no hidden side
  effects, identical outputs for identical inputs — the canonical
  cautionary tale is Ariane 5 (1996), lost to an unguarded 64-bit-to-16-bit
  conversion overflow.
- **SOLID:** Single Responsibility, Open/Closed, Liskov Substitution,
  Interface Segregation, Dependency Inversion — improves maintainability,
  extensibility, testability, and certification effort.
- **DRY / KISS:** eliminate duplicated logic; favor the simplest solution
  that is still easy to verify — but don't let over-abstraction hide safety
  behavior.
- **Model-Based Design:** executable models (e.g. in Ansys Scade One)
  replace hand-written code as the thing that gets simulated, verified, and
  traced, supporting certified code generation.

---

# Part 1 — Reading: Applying the Principles to a Real Automotive Architecture

Read the following article carefully before continuing:

> **"Semantic Interface Modeling for Automotive Architectures Using a
> Domain-Driven Approach"**
> Christian Hackenbeck, Alexander Walz, Pascal Hirmer, Stefan Wagner,
> Michael Weyrich — *IFAC-PapersOnLine*, Volume 59, Issue 25 (2025),
> pp. 125–130.
> DOI: [10.1016/j.ifacol.2025.11.936](https://doi.org/10.1016/j.ifacol.2025.11.936)
> https://www.sciencedirect.com/science/article/pii/S2405896325026576

The article proposes a Domain-Driven Design (DDD)-inspired methodology for
modeling semantically meaningful interfaces in Software-Defined Vehicle
architectures, demonstrated on a safety-critical **Life Presence Detection
(LPD)** use case (preventing children or pets left in a parked vehicle from
being harmed by extreme temperatures). It identifies **bounded contexts**
(Body, Infotainment, Connection, Powertrain, Backend), maps them onto
**domain / application / infrastructure** layers that mirror the automotive
**logical / software / technical** layers, and characterizes every
interface between them by direction, temporal coupling, data-interaction
type, **criticality**, implementation binding, and change tolerance.

## How the studied principles show up in the paper

| Studied Principle | Connection to the paper |
|---|---|
| Top-Down Design | Architecture is developed across abstraction levels (logical → software → technical / domain → application → infrastructure) |
| Modularity | System is decomposed into bounded contexts and components (Body, Connection, Backend, …) |
| Information Hiding | Clear separation of responsibilities and layers between domain, application, and infrastructure |
| Explicit Interfaces | One of the central subjects of the paper — the semantic interface characterization table |
| Traceability | Supports cross-domain traceability between functional model, architecture, and interfaces |
| Deterministic / Safety thinking | Interfaces are explicitly characterized by timing (temporal coupling) and criticality (safety-critical / mission-critical / comfort) |
| SOLID — Single Responsibility | Conceptually related to separation into bounded contexts, each with one functional responsibility |
| SOLID — Interface Segregation | Strong conceptual connection with small, semantic, well-defined interfaces per bounded context |
| Model-Based Design | The methodology is explicitly positioned within Model-Based Systems Engineering (UML/SysML artifacts) |
| Safety-critical design | Demonstrated through a real automotive safety-critical use case (Life Presence Detection) |

---

# Summary

- This lab did not repeat the lecture — it applied it. The eight design
  principles from Lesson 5 are not classroom abstractions: Hackenbeck et
  al. (2025) uses Top-Down Design, Modularity, Information Hiding,
  Traceability, and SOLID-style separation of responsibility to structure a
  real, safety-critical automotive Software-Defined Vehicle architecture.
- The paper's **semantic interface characterization** (direction, temporal
  coupling, criticality, binding, change tolerance) is a concrete,
  research-grade instance of the lecture's Traceability-by-Design and
  Deterministic-Design ideas, applied one level up at the architecture
  stage rather than inside a single component.
- If any of the Recap's vocabulary was unfamiliar while reading the paper,
  revisit the **Course Slides** for the full explanations and worked
  examples before taking the quiz below.

---

# Quiz

Answer the ten questions below (based on the lecture and the assigned
reading) to check your understanding.

<style>
  #design-quiz { margin-top: 1rem; }
  .quiz-q { margin-bottom: 1.1rem; padding: 1.15rem 1.25rem; background: var(--white); border: 1px solid var(--border); border-radius: 8px; }
  .quiz-q strong { display: block; margin-bottom: .7rem; color: var(--navy); font-size: .97rem; }
  .quiz-option { display: flex; align-items: flex-start; gap: .55rem; padding: .42rem .55rem; border-radius: 5px; cursor: pointer; transition: background .13s; user-select: none; font-size: .92rem; }
  .quiz-option:hover { background: var(--ice); }
  .quiz-option input { margin-top: .22rem; flex-shrink: 0; accent-color: var(--blue); }
  .quiz-option.correct { background: #E8F5E9; color: #1B5E20; font-weight: 600; border-radius: 5px; }
  .quiz-option.wrong   { background: #FFEBEE; color: #B71C1C; text-decoration: line-through; border-radius: 5px; }
  .quiz-option.reveal  { background: #FFF8E1; color: #BF360C; font-weight: 600; border-radius: 5px; }
  #quiz-submit { margin-top: .75rem; padding: .55rem 1.5rem; background: var(--blue); color: var(--white); border: none; border-radius: 6px; font-size: .9rem; font-weight: 600; cursor: pointer; transition: background .15s; }
  #quiz-submit:hover:not(:disabled) { background: var(--sky); }
  #quiz-submit:disabled { opacity: .45; cursor: default; }
  #quiz-score { display: inline-block; margin-left: 1rem; font-size: 1rem; font-weight: 700; vertical-align: middle; }
  #quiz-reset { display: none; margin-left: .75rem; padding: .55rem 1.1rem; background: transparent; color: var(--muted); border: 1px solid var(--border); border-radius: 6px; font-size: .88rem; cursor: pointer; transition: color .15s, border-color .15s; vertical-align: middle; }
  #quiz-reset:hover { color: var(--blue); border-color: var(--sky); }
</style>

<div id="design-quiz">
  <div class="quiz-q" data-correct="a">
    <strong>Q1 — What is the main purpose of Top-Down Design in safety-critical software?</strong>
    <label class="quiz-option"><input type="radio" name="q1" value="a"><span>To progressively decompose system objectives into smaller, manageable elements</span></label>
    <label class="quiz-option"><input type="radio" name="q1" value="b"><span>To begin implementation with low-level hardware drivers</span></label>
    <label class="quiz-option"><input type="radio" name="q1" value="c"><span>To eliminate the need for software requirements</span></label>
    <label class="quiz-option"><input type="radio" name="q1" value="d"><span>To postpone architectural decisions until testing</span></label>
  </div>
  <div class="quiz-q" data-correct="c">
    <strong>Q2 — In safety-critical software, what is the main role of information hiding?</strong>
    <label class="quiz-option"><input type="radio" name="q2" value="a"><span>To prevent developers from accessing software documentation</span></label>
    <label class="quiz-option"><input type="radio" name="q2" value="b"><span>To hide all communication between software components</span></label>
    <label class="quiz-option"><input type="radio" name="q2" value="c"><span>To expose necessary interfaces while hiding internal implementation details</span></label>
    <label class="quiz-option"><input type="radio" name="q2" value="d"><span>To combine several modules into one monolithic component</span></label>
  </div>
  <div class="quiz-q" data-correct="b">
    <strong>Q3 — A requirement is changed late in a safety-critical project. Which design practice most directly helps identify the affected architecture, implementation, and test cases?</strong>
    <label class="quiz-option"><input type="radio" name="q3" value="a"><span>Dynamic interpretation</span></label>
    <label class="quiz-option"><input type="radio" name="q3" value="b"><span>Traceability</span></label>
    <label class="quiz-option"><input type="radio" name="q3" value="c"><span>Code duplication</span></label>
    <label class="quiz-option"><input type="radio" name="q3" value="d"><span>Interface enlargement</span></label>
  </div>
  <div class="quiz-q" data-correct="c">
    <strong>Q4 — Which situation best illustrates the Single Responsibility Principle in an automotive brake-control architecture?</strong>
    <label class="quiz-option"><input type="radio" name="q4" value="a"><span>The Brake Controller performs braking, diagnostics, display management, and communication</span></label>
    <label class="quiz-option"><input type="radio" name="q4" value="b"><span>Every component implements its own copy of the braking algorithm</span></label>
    <label class="quiz-option"><input type="radio" name="q4" value="c"><span>The Brake Controller calculates braking commands while diagnostics are handled by another component</span></label>
    <label class="quiz-option"><input type="radio" name="q4" value="d"><span>The Brake Controller directly manages every hardware device in the vehicle</span></label>
  </div>
  <div class="quiz-q" data-correct="a">
    <strong>Q5 — A validated Brake Controller must support a new compatible distance sensor without changing its validated control logic. Which SOLID principle is illustrated most directly?</strong>
    <label class="quiz-option"><input type="radio" name="q5" value="a"><span>Open/Closed Principle</span></label>
    <label class="quiz-option"><input type="radio" name="q5" value="b"><span>Single Responsibility Principle</span></label>
    <label class="quiz-option"><input type="radio" name="q5" value="c"><span>Interface Segregation Principle</span></label>
    <label class="quiz-option"><input type="radio" name="q5" value="d"><span>DRY Principle</span></label>
  </div>
  <div class="quiz-q" data-correct="c">
    <strong>Q6 — The same obstacle-distance validation logic appears separately in BrakeControl, WarningSystem, and Diagnostics. Which change best follows the DRY principle?</strong>
    <label class="quiz-option"><input type="radio" name="q6" value="a"><span>Create additional copies of the validation logic for reliability</span></label>
    <label class="quiz-option"><input type="radio" name="q6" value="b"><span>Remove distance validation from all components</span></label>
    <label class="quiz-option"><input type="radio" name="q6" value="c"><span>Implement one validated distance-check function and reuse it</span></label>
    <label class="quiz-option"><input type="radio" name="q6" value="d"><span>Replace the validation with a more complex multi-layer algorithm</span></label>
  </div>
  <div class="quiz-q" data-correct="a">
    <strong>Q7 — Which emergency-braking decision flow best illustrates the KISS principle while retaining the required safety behavior?</strong>
    <label class="quiz-option"><input type="radio" name="q7" value="a"><span>Obstacle detected &rarr; risk threshold exceeded &rarr; apply brake</span></label>
    <label class="quiz-option"><input type="radio" name="q7" value="b"><span>Obstacle detected &rarr; add several unnecessary abstraction layers &rarr; evaluate risk &rarr; apply brake</span></label>
    <label class="quiz-option"><input type="radio" name="q7" value="c"><span>Obstacle detected &rarr; dynamically select an undocumented algorithm &rarr; apply brake</span></label>
    <label class="quiz-option"><input type="radio" name="q7" value="d"><span>Obstacle detected &rarr; duplicate the decision logic across several modules &rarr; apply brake</span></label>
  </div>
  <div class="quiz-q" data-correct="b">
    <strong>Q8 — What distinguishes Model-Based Design from the traditional development workflow presented in the lesson?</strong>
    <label class="quiz-option"><input type="radio" name="q8" value="a"><span>It removes the need for requirements and verification</span></label>
    <label class="quiz-option"><input type="radio" name="q8" value="b"><span>It uses an executable model that can support simulation, verification, and automatic code generation</span></label>
    <label class="quiz-option"><input type="radio" name="q8" value="c"><span>It requires all production code to be written manually before modeling</span></label>
    <label class="quiz-option"><input type="radio" name="q8" value="d"><span>It performs modeling only after final system testing</span></label>
  </div>
  <div class="quiz-q" data-correct="a">
    <strong>Q9 — In Hackenbeck et al. (2025), which combination describes key elements of the proposed automotive interface-modeling methodology?</strong>
    <label class="quiz-option"><input type="radio" name="q9" value="a"><span>Bounded contexts, separation of architectural layers, and semantic interface characterization</span></label>
    <label class="quiz-option"><input type="radio" name="q9" value="b"><span>Monolithic components, hidden interfaces, and removal of abstraction levels</span></label>
    <label class="quiz-option"><input type="radio" name="q9" value="c"><span>Manual code duplication, dynamic interpretation, and unrestricted platform dependence</span></label>
    <label class="quiz-option"><input type="radio" name="q9" value="d"><span>Elimination of interfaces, architectural layers, and component boundaries</span></label>
  </div>
  <div class="quiz-q" data-correct="c">
    <strong>Q10 — What does the characterization model in Hackenbeck et al. (2025) enable architects to reason about when defining automotive interfaces?</strong>
    <label class="quiz-option"><input type="radio" name="q10" value="a"><span>Only source-code formatting and naming conventions</span></label>
    <label class="quiz-option"><input type="radio" name="q10" value="b"><span>Only user-interface appearance and driver preferences</span></label>
    <label class="quiz-option"><input type="radio" name="q10" value="c"><span>Timing, criticality, and platform binding</span></label>
    <label class="quiz-option"><input type="radio" name="q10" value="d"><span>Only database normalization and storage capacity</span></label>
  </div>
  <div>
    <button id="quiz-submit" type="button">Check Answers</button>
    <button id="quiz-reset" type="button">Try Again</button>
    <span id="quiz-score"></span>
  </div>
</div>
