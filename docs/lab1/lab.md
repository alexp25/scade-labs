# Lab 1 — Introduction to Software Engineering

**Course:** Software Engineering  
**Lesson:** Software Engineering as an Engineering Discipline  
**Duration:** 1 hour  
**Tool:** None — reading + quiz only  
**Work mode:** Individual  
**Recommended prerequisite:** None — this is the first lab in the portfolio

---

# Context

Software has become one of the most complex artifacts humans build, yet it is often produced without the discipline applied to other engineering fields. This lab introduces **software engineering** as an engineering discipline in its own right: a systematic, disciplined, and quantifiable approach to building software — not just writing code.

You will see why that distinction matters most in **safety-critical systems**, where a software failure can cause injury, major financial loss, or environmental damage — and you will get a first look at **Model-Based Design (MBD)** and **Ansys Scade One**, the modeling tool used throughout the rest of this course (Labs 3 and 4).

---

# Learning Objectives

By the end of this lab you will be able to:

- State the IEEE definition of software engineering and explain each of its three qualifiers — systematic, disciplined, quantifiable
- Describe the phases of the software development lifecycle that software engineering spans
- Explain the difference between programming and software engineering
- List the characteristics of high-quality software, and explain why determinism and traceability matter especially in safety-critical systems
- Describe what Model-Based Design is and how it differs from writing code by hand
- Explain, at a high level, how Ansys Scade One supports software engineering principles

---

# Part 1 — What Is Software Engineering?

## Theory

According to **IEEE**, software engineering is defined as:

> *"The application of a systematic, disciplined, and quantifiable approach to the development, operation, and maintenance of software."*

Each word in that definition is doing real work:

### Systematic

A systematic approach means software is built following an organized sequence of steps, typically:

- requirements analysis
- architectural and detailed design
- implementation
- verification and validation
- deployment and maintenance

### Disciplined

Being disciplined means adhering to:

- coding standards
- modeling guidelines
- safety and certification standards
- review and approval processes

### Quantifiable

A quantifiable approach lets engineers answer questions such as:

- How much of the system has been tested?
- How many requirements are fully verified?
- What is the execution time or worst-case response?

Without measurable data, it is impossible to objectively claim that software is safe, reliable, or ready for certification.

> **Key idea:** software engineering spans the **entire lifecycle** — capturing and managing requirements, designing system behavior, implementing logic, verifying correctness, and maintaining the system after deployment. It does not stop once the code compiles.

---

# Part 2 — Why Projects Fail

## Theory

> *"A complex system that works is invariably found to have evolved from a simple system that worked."* — John Gall

Despite that, the history of IT projects is full of failures: **30–40% of system projects fail before completion.**

The secret to avoiding this does not reside only in programming, but also in **how the project is organized and developed**, and in **communication between team members**. A famous cartoon captures this well: the customer explains one thing, the project leader understands another, the analyst designs a third, the programmer builds a fourth — and what the customer actually needed was something else entirely. Every step of miscommunication compounds into a failed project, regardless of how skilled the programmer is.

This is precisely why software engineering treats requirements, design, and verification as first-class activities, not paperwork to get through before the "real" work of coding begins.

---

# Part 3 — Software Engineering vs. Programming

## Theory

- **Programming** focuses on **how** to implement a solution.
- **Software engineering** focuses on **whether** the solution is correct, safe, maintainable, and verifiable.

Programming is one activity inside software engineering — necessary, but not sufficient. A program can compile, run, and produce the right answer on the demo input, and still be bad software engineering if nobody can prove it is safe, nobody can trace it back to a requirement, and nobody can maintain it six months later.

---

# Part 4 — Characteristics of High-Quality Software

## Theory

High-quality software is not accidental; it is **engineered**. Key characteristics include:

| Characteristic | Meaning |
|---|---|
| **Reliability** | Consistent correct behavior over time |
| **Determinism** | Predictable outputs for given inputs |
| **Safety** | Avoidance of hazardous behavior |
| **Verifiability** | Ability to demonstrate correctness with evidence |
| **Traceability** | Links between requirements, models, and implementation |
| **Maintainability** | Ease of updates without introducing errors |

---

# Part 5 — Software Engineering in Safety-Critical Systems

## Theory

**Safety-critical systems** are systems where a failure can result in:

- injury or loss of life
- major financial loss
- environmental damage

Examples include flight control systems, braking systems, and railway signaling.

Such systems require:

- **predictability** — no unexpected behavior; the same input must always produce the same output
- **traceability** — every function must be justified against a requirement
- **verification evidence** — proof that the system meets its requirements

This is why determinism and traceability, which might sound like abstract engineering virtues elsewhere, become hard, non-negotiable requirements once a software failure can hurt someone.

---

# Part 6 — Model-Based Design

## Theory

**Model-Based Design (MBD)** is a development methodology where system behavior is first described using **executable models** instead of manually written code. Key ideas:

- **Graphical system modeling** — engineers describe system logic and behavior using formal models
- **Early simulation and validation** — system behavior can be tested before implementation
- **Automatic code generation** — production code can be generated directly from verified models
- **Improved traceability and reliability** — requirements, models, and code remain connected throughout the development process

This approach helps detect errors earlier, reduces development risk, and improves the overall quality of safety-critical software — because the model itself is what gets simulated, verified, and traced, rather than a separate hand-written implementation of it.

---

# Part 7 — Introduction to Ansys Scade One

## Theory

**Ansys Scade One** is a model-based development environment designed specifically for safety-critical software. Instead of writing large amounts of manual code, engineers describe system behavior using formal, executable models. These models are:

- deterministic
- analyzable
- traceable to requirements

### How Scade One supports software engineering principles

Scade One reinforces the software engineering practices from Parts 1–5 directly:

- **Deterministic models** — the behavior of the system is precisely defined and predictable
- **Automatic certified code generation** — code is generated automatically from models, reducing human error and supporting certification
- **Strong traceability** — requirements can be linked directly to model elements and generated code
- **Early verification and validation** — errors can be detected at the model level, long before deployment

### Where is it used?

Scade One is widely adopted in industries where software correctness is mandatory:

- **Aerospace** — flight control and avionics
- **Automotive** — ADAS and electronic control units
- **Railway** — signaling and train control
- **Industrial systems** — automation and safety controllers

> You will use Scade One hands-on starting in [Lab 3](../lab3/), where you build and trace a Limiter and a Counter, and in [Lab 4](../lab4/), where you model a full Cruise Control system.

---

# Part 8 — Reading

Before taking the quiz below, read the following article carefully to reinforce the concepts covered in this lab:

> **"Software Engineering: Foundations, Practices, and Future Directions"**
> V.J. Pugazhenthi, A. Murugan, B. Jeyarajan, G. Pandy — *Journal of Software Engineering (JSE)*, Volume 2, Issue 2, July–December 2024, pp. 43–54.
> DOI: [10.5281/zenodo.14472069](https://doi.org/10.5281/zenodo.14472069)

The article explores the foundations of software engineering, key methodologies and industry-standard practices, persistent challenges (scalability, security, rapid technological change), and the role of software engineering in safety and certification contexts.

---

# Summary

- Software engineering is a **disciplined, structured approach** to building software that must be correct, safe, and maintainable — not just "writing code that works."
- It spans the **entire lifecycle**: requirements, design, implementation, verification, deployment, and maintenance.
- In **safety-critical systems**, predictability, traceability, and verification evidence are non-negotiable.
- **Ansys Scade One** provides a practical way to apply these principles through **Model-Based Design** — automatic code generation and strong verification support.

---

# Quiz

Answer the ten questions below (based on the assigned reading) to check your understanding.

<style>
  #intro-quiz { margin-top: 1rem; }
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

<div id="intro-quiz">
  <div class="quiz-q" data-correct="b">
    <strong>Q1 — According to the IEEE definition, software engineering is best described as:</strong>
    <label class="quiz-option"><input type="radio" name="q1" value="a"><span>Writing efficient code using any available method</span></label>
    <label class="quiz-option"><input type="radio" name="q1" value="b"><span>Applying a systematic, disciplined, and quantifiable approach to software</span></label>
    <label class="quiz-option"><input type="radio" name="q1" value="c"><span>Debugging software after deployment</span></label>
    <label class="quiz-option"><input type="radio" name="q1" value="d"><span>Using programming languages to build applications</span></label>
  </div>
  <div class="quiz-q" data-correct="b">
    <strong>Q2 — Which of the following best explains the term "systematic" in software engineering?</strong>
    <label class="quiz-option"><input type="radio" name="q2" value="a"><span>Writing code quickly to meet deadlines</span></label>
    <label class="quiz-option"><input type="radio" name="q2" value="b"><span>Following clearly defined development processes and steps</span></label>
    <label class="quiz-option"><input type="radio" name="q2" value="c"><span>Allowing developers to choose any method they prefer</span></label>
    <label class="quiz-option"><input type="radio" name="q2" value="d"><span>Focusing only on implementation</span></label>
  </div>
  <div class="quiz-q" data-correct="b">
    <strong>Q3 — What does "quantifiable" mean in the context of software engineering?</strong>
    <label class="quiz-option"><input type="radio" name="q3" value="a"><span>Software quality cannot be measured</span></label>
    <label class="quiz-option"><input type="radio" name="q3" value="b"><span>Progress and quality can be measured using metrics</span></label>
    <label class="quiz-option"><input type="radio" name="q3" value="c"><span>Only code size is measured</span></label>
    <label class="quiz-option"><input type="radio" name="q3" value="d"><span>Measurements are optional</span></label>
  </div>
  <div class="quiz-q" data-correct="d">
    <strong>Q4 — Which activity is NOT part of the software engineering lifecycle?</strong>
    <label class="quiz-option"><input type="radio" name="q4" value="a"><span>Requirements definition</span></label>
    <label class="quiz-option"><input type="radio" name="q4" value="b"><span>Software design</span></label>
    <label class="quiz-option"><input type="radio" name="q4" value="c"><span>Long-term maintenance</span></label>
    <label class="quiz-option"><input type="radio" name="q4" value="d"><span>Writing code without documentation</span></label>
  </div>
  <div class="quiz-q" data-correct="c">
    <strong>Q5 — What is the main difference between software engineering and programming?</strong>
    <label class="quiz-option"><input type="radio" name="q5" value="a"><span>Programming is more complex than software engineering</span></label>
    <label class="quiz-option"><input type="radio" name="q5" value="b"><span>Software engineering focuses only on testing</span></label>
    <label class="quiz-option"><input type="radio" name="q5" value="c"><span>Programming is only one part of software engineering</span></label>
    <label class="quiz-option"><input type="radio" name="q5" value="d"><span>They are exactly the same thing</span></label>
  </div>
  <div class="quiz-q" data-correct="b">
    <strong>Q6 — Which of the following is a key characteristic of high-quality software?</strong>
    <label class="quiz-option"><input type="radio" name="q6" value="a"><span>Works only in ideal conditions</span></label>
    <label class="quiz-option"><input type="radio" name="q6" value="b"><span>Predictable and deterministic behavior</span></label>
    <label class="quiz-option"><input type="radio" name="q6" value="c"><span>Difficult to maintain</span></label>
    <label class="quiz-option"><input type="radio" name="q6" value="d"><span>No documentation required</span></label>
  </div>
  <div class="quiz-q" data-correct="c">
    <strong>Q7 — Why is predictability especially important in safety-critical systems?</strong>
    <label class="quiz-option"><input type="radio" name="q7" value="a"><span>It improves code readability</span></label>
    <label class="quiz-option"><input type="radio" name="q7" value="b"><span>It reduces the need for testing</span></label>
    <label class="quiz-option"><input type="radio" name="q7" value="c"><span>The same input must always produce the same output</span></label>
    <label class="quiz-option"><input type="radio" name="q7" value="d"><span>It allows faster execution on any hardware</span></label>
  </div>
  <div class="quiz-q" data-correct="b">
    <strong>Q8 — What is a major requirement for safety-critical software?</strong>
    <label class="quiz-option"><input type="radio" name="q8" value="a"><span>Minimal documentation</span></label>
    <label class="quiz-option"><input type="radio" name="q8" value="b"><span>Full traceability from requirements to code</span></label>
    <label class="quiz-option"><input type="radio" name="q8" value="c"><span>Manual code generation only</span></label>
    <label class="quiz-option"><input type="radio" name="q8" value="d"><span>Informal testing</span></label>
  </div>
  <div class="quiz-q" data-correct="b">
    <strong>Q9 — Which of the following is an example of a safety-critical system?</strong>
    <label class="quiz-option"><input type="radio" name="q9" value="a"><span>Social media platform</span></label>
    <label class="quiz-option"><input type="radio" name="q9" value="b"><span>Flight control systems</span></label>
    <label class="quiz-option"><input type="radio" name="q9" value="c"><span>Online shopping website</span></label>
    <label class="quiz-option"><input type="radio" name="q9" value="d"><span>Music streaming service</span></label>
  </div>
  <div class="quiz-q" data-correct="a">
    <strong>Q10 — What are the main benefits of Model-Based Design?</strong>
    <label class="quiz-option"><input type="radio" name="q10" value="a"><span>Early validation through simulation, automatic code generation, and strong traceability between requirements and implementation</span></label>
    <label class="quiz-option"><input type="radio" name="q10" value="b"><span>Manual coding first, reduced documentation, and minimal verification</span></label>
    <label class="quiz-option"><input type="radio" name="q10" value="c"><span>Late testing after deployment, hardware-first development, and reduced modeling effort</span></label>
    <label class="quiz-option"><input type="radio" name="q10" value="d"><span>Elimination of requirements management, no need for verification, and direct hardware programming</span></label>
  </div>
  <div>
    <button id="quiz-submit" type="button">Check Answers</button>
    <button id="quiz-reset" type="button">Try Again</button>
    <span id="quiz-score"></span>
  </div>
</div>
