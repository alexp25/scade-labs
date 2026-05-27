# Lab 2 – Applying the SDLC: Cruise Control Safety System

**Course:** Software Engineering  
**Lesson:** Software Development Life Cycle (SDLC)  
**Duration:** 2 hours  
**Language:** Python 3  
**Work mode:** Individual  

---

## Objectives

By the end of this lab you will be able to:

- Apply all SDLC phases on a concrete safety-critical problem
- Explain why requirements must be precise and unambiguous
- Build a state machine as a design artifact and trace it back to requirements
- Implement a function whose logic is fully driven by a design — not intuition
- Run a structured verification and validation test suite
- Explain how traceability connects requirements, design, code, and tests
- Reflect on the differences between Waterfall, Agile, and V-Cycle in a safety context

---

## Setup

Clone this repository and open the starter file:

```bash
git clone <repo-url>
cd lab2-sdlc-cruise-control
python starter/lab2_cruise_control_starter.py
```

You need Python 3.6 or later. No external libraries required.

---

## The Problem

You are a junior software engineer on a safety-critical automotive project.  
Your system controls **cruise control** on a vehicle.

The client sent this informal description:

> *"Cruise control must be safe. It should stop when needed, should not start
> in dangerous conditions, and if it stops for a safety reason the driver
> must be aware that they need to restart it manually."*

Your job is to take this informal description through all SDLC phases:
requirements → design → implementation → verification & validation.

---

## Structure

Work through the starter file **in order**, from Part 0 to Part 5.  
Every section is clearly marked. Do not skip ahead.

| Part | Topic | Time |
|------|-------|------|
| 0 | Python in 15 Minutes | 15 min |
| 1 | Requirements Analysis | 20 min |
| 2 | System Design | 20 min |
| 3 | Implementation | 25 min |
| 4 | Verification & Validation | 25 min |
| 5 | Reflection | 15 min |

---

## Part 0 — Python in 15 Minutes

You do **not** need to be a programmer for this lab.  
We use Python to make requirements and design **executable and testable** —
exactly what a tool like Scade One does, but manually.

Everything you need is in the starter file. Read Part 0 carefully before writing any code.

---

## Part 1 — Requirements Analysis

### Why requirements matter

Before any line of code is written, the team must agree on exactly **what** the system must do. Vague requirements lead to different implementations, untestable behavior, and expensive fixes discovered late.

### Activity 1A — Poorly written requirements

Another team received this version:

| Req. ID | Description |
|---------|-------------|
| REQ-A | The system must stop cruise control when it is dangerous. |
| REQ-B | Speed must be OK to start cruise control. |
| REQ-C | If it stops, the driver must do something. |

**Question:** What is wrong with these? Why can you NOT implement or test anything based on them?  
Write 2–3 sentences in the starter file.

### Activity 1B — Correct SRS

Well-written requirements follow the pattern:  
`"The system SHALL [action] WHEN/IF [condition]."`

Your **Software Requirements Specification (SRS)**:

| Req. ID | Description | Type |
|---------|-------------|------|
| REQ-01 | The system SHALL deactivate cruise control if the brake is pressed. | Functional |
| REQ-02 | The system SHALL deactivate cruise control if speed exceeds 130 km/h. | Functional |
| REQ-03 | The system SHALL refuse to activate if speed is below 30 km/h. | Functional |
| REQ-04 | The system SHALL enter state SUSPENDED (not OFF) when deactivated by a safety condition, so that reactivation must be explicit by the driver. | Functional |
| REQ-05 | The system SHALL respond to any input in less than 100 ms. | Non-functional |
| REQ-06 | The system SHALL be testable with simulated boolean inputs. | Non-functional |

**Critical question:** Read REQ-02 and REQ-04 together.  
When speed exceeds 130 km/h, does the system go to `SUSPENDED` or directly to `OFF`?  
Do the requirements state this clearly? Note your answer in the starter file — you will revisit it in Part 2.

---

## Part 2 — System Design

### Why design before code?

Try to implement REQ-01 through REQ-04 directly without a design. You will immediately not know:
- How many states does the system have?
- What happens if brake AND high speed occur simultaneously?
- Where is the current state stored?

Design answers all of these **before** you write a single line of code.

### Activity 2A — State Machine

The system has **three states**:

```
+----------+   driver activates (speed >= 30)   +-----------+
|   OFF    | ----------------------------------> |  ACTIVE   |
+----------+                                     +-----------+
     ^                                                 |
     |                                  brake OR speed > 130
     |                                                 |
     |      driver reactivates explicitly     +--------v--------+
     +----------------------------------------|   SUSPENDED    |
                                              +-----------------+
```

| State | Meaning |
|-------|---------|
| `OFF` | System is off; driver can activate if speed ≥ 30 |
| `ACTIVE` | Cruise control is running |
| `SUSPENDED` | Stopped by a safety condition; driver **must** reactivate explicitly |

**Transition table:**

| From | Event | To | REQ covered |
|------|-------|----|-------------|
| OFF | driver activates AND speed ≥ 30 | ACTIVE | REQ-03 |
| OFF | driver activates AND speed < 30 | OFF | REQ-03 |
| ACTIVE | brake pressed | SUSPENDED | REQ-01, REQ-04 |
| ACTIVE | speed > 130 | SUSPENDED | REQ-02, REQ-04 |
| SUSPENDED | driver reactivates explicitly | ACTIVE | REQ-04 |
| SUSPENDED | driver activates (no reactivation) | SUSPENDED | REQ-04 |

### Activity 2B — Traceability: Design → Requirements

Fill in the `REQ covered` column in the starter file:

| Design Element | REQ covered |
|----------------|-------------|
| State SUSPENDED (distinct from OFF) | |
| Transition ACTIVE → SUSPENDED on brake | |
| Block activation if speed < 30 | |
| Transition ACTIVE → SUSPENDED on speed > 130 | |
| Transition SUSPENDED → ACTIVE only on explicit reactivation | |

### Activity 2C — Design decision

The state machine resolves the REQ-02 / REQ-04 ambiguity:  
speed > 130 → `SUSPENDED` (not `OFF`), because REQ-04 covers all safety-condition deactivations.

This is a **design decision you made** — not something the client specified.  
Answer in the starter file: what should happen before implementing this? What could go wrong if two developers resolved it differently?

---

## Part 3 — Implementation

Open `starter/lab2_cruise_control_starter.py` and implement:

```python
def update_cruise_control(current_state, speed, brake_pressed,
                          driver_activates, driver_reactivates):
```

Follow the transition table from Part 2 exactly.  
**Do not guess** — every line of code should trace back to a REQ ID and a design element.

**Recommended order inside the function:**
1. Check safety conditions first (brake, speed > 130) — these trigger from `ACTIVE`
2. Handle `SUSPENDED`: reactivates → `ACTIVE`; activates only → stay `SUSPENDED`
3. Handle `OFF`: activates + speed ≥ 30 → `ACTIVE`; else stay `OFF`
4. Default: return `current_state` unchanged

---

## Part 4 — Verification & Validation

### Verification vs Validation

| | Question | Focus |
|-|----------|-------|
| **Verification** | Are we building the system *right*? | Code matches design |
| **Validation** | Are we building the *right* system? | All requirements are met |

### Activity 4A — Run the tests

The test suite is already written in the starter file. Run it:

```bash
python starter/lab2_cruise_control_starter.py
```

All 7 tests must print `PASS` before you move on.

**Test table:**

| Test ID | current_state | speed | brake | activates | reactivates | Expected | REQ |
|---------|--------------|-------|-------|-----------|-------------|----------|-----|
| TC-01 | ACTIVE | 80 | True | False | False | SUSPENDED | REQ-01 |
| TC-02 | ACTIVE | 140 | False | False | False | SUSPENDED | REQ-02 |
| TC-03 | OFF | 20 | False | True | False | OFF | REQ-03 |
| TC-04 | OFF | 80 | False | True | False | ACTIVE | REQ-03 |
| TC-05 ⚠️ | SUSPENDED | 80 | False | True | False | SUSPENDED | REQ-04 |
| TC-06 | SUSPENDED | 80 | False | False | True | ACTIVE | REQ-04 |
| TC-07 | ACTIVE | 80 | False | False | False | ACTIVE | REQ-01,02 |

> ⚠️ **TC-05 is the key test.** A student who skipped the design or misread REQ-04 will return `ACTIVE` instead of `SUSPENDED`. This is intentional — it shows exactly why the design phase matters.

### Activity 4B — TC-05 analysis

Answer in the starter file:
1. Did TC-05 pass or fail on your first attempt?
2. If it failed — where was the root cause: in the requirement, the design, or the code?
3. What would happen if this bug reached a deployed real vehicle system?

### Activity 4C — Full Traceability Matrix

Fill in the `Status` column in the starter file:

| Req. ID | Design Element | Code Element | Test ID(s) | Status |
|---------|---------------|-------------|-----------|--------|
| REQ-01 | ACTIVE → SUSPENDED on brake | `if brake_pressed and ACTIVE` | TC-01, TC-07 | |
| REQ-02 | ACTIVE → SUSPENDED on speed > 130 | `if speed > 130 and ACTIVE` | TC-02, TC-07 | |
| REQ-03 | Block activation below 30 km/h | `if speed < 30: stay OFF` | TC-03, TC-04 | |
| REQ-04 | SUSPENDED → ACTIVE only if reactivates | `if driver_reactivates` | TC-05, TC-06 | |
| REQ-05 | Single-pass, no delay | Function returns immediately | All TCs | |
| REQ-06 | Simulatable inputs | Bool/int parameters | All TCs | |

---

## Part 5 — Reflection

Answer each question in 3–5 sentences in the starter file.

**Q1 — Value of design**  
TC-05 exposed an ambiguity in the requirements. How did the State Machine from Part 2 help you resolve this ambiguity *before* writing code? What would have happened without it?

**Q2 — Waterfall**  
Imagine you discovered the REQ-04 ambiguity only during the testing phase in a pure Waterfall project. What would the impact be? How costly would it be to go back to the requirements phase?

**Q3 — Agile in safety-critical systems**  
A colleague suggests skipping REQ-05 (response < 100 ms) and adding it "in a later sprint". Why is this approach specifically dangerous in safety-critical systems, compared to a regular web application?

**Q4 — Scade One**  
Look at your traceability matrix. Now imagine the system has 400 requirements instead of 6. What would happen to the matrix if maintained manually? What parts of what you did by hand today would Scade One automate?

---

## Deliverables Checklist

Submit the completed starter file. Before submitting, verify:

- [ ] Answer 1A — what is wrong with poorly written requirements
- [ ] Answer 1B — REQ-02 vs REQ-04 ambiguity noted
- [ ] Activity 2B — traceability Design → Requirements filled in
- [ ] Answer 2C — design decision documented
- [ ] Part 3 — `update_cruise_control()` implemented
- [ ] Part 4 — all 7 tests print `PASS`
- [ ] Answer 4B — TC-05 analysis (3 questions)
- [ ] Activity 4C — traceability matrix `Status` column filled in
- [ ] Answers Q1–Q4 — reflection questions answered

---

## Expected Output

When your implementation is correct, running the file produces:

```
Quick manual checks:
SUSPENDED
SUSPENDED

======================================================================
  VERIFICATION REPORT -- Cruise Control Safety System
======================================================================
  TC-01 [REQ-01     ] | Expected=SUSPENDED  Got=SUSPENDED  | PASS
  TC-02 [REQ-02     ] | Expected=SUSPENDED  Got=SUSPENDED  | PASS
  TC-03 [REQ-03     ] | Expected=OFF        Got=OFF        | PASS
  TC-04 [REQ-03     ] | Expected=ACTIVE     Got=ACTIVE     | PASS
  TC-05 [REQ-04     ] | Expected=SUSPENDED  Got=SUSPENDED  | PASS
  TC-06 [REQ-04     ] | Expected=ACTIVE     Got=ACTIVE     | PASS
  TC-07 [REQ-01,02  ] | Expected=ACTIVE     Got=ACTIVE     | PASS
----------------------------------------------------------------------
  VALIDATION: ALL REQUIREMENTS MET.
======================================================================
```

---

## Connection to Lecture 2

| SDLC Phase | What you did today |
|------------|--------------------|
| Requirements Analysis | Wrote REQ-01 to REQ-06 with IDs, precise language, and types |
| System Design | Built a 3-state machine and mapped every transition to a requirement |
| Implementation | Coded logic driven entirely by the design — not intuition |
| Verification & Validation | Ran 7 structured tests, each linked to a requirement |
| Traceability | Maintained REQ → Design → Code → Test links throughout |

> **Key takeaway:** Traceability is not paperwork — it is what makes a safety-critical system auditable and certifiable. This is exactly what tools like **Scade One** automate at industrial scale.
