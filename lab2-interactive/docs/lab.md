# Lab 2 — Applying the SDLC: Cruise Control Safety System

**Course:** Software Engineering &nbsp;·&nbsp; **Lesson:** SDLC &nbsp;·&nbsp; **Duration:** 2 hours &nbsp;·&nbsp; **Language:** Python 3 &nbsp;·&nbsp; **Work mode:** Individual

---

## Objectives

By the end of this lab you will be able to:

- Apply all SDLC phases on a concrete safety-critical problem
- Explain why requirements must be precise and unambiguous
- Build a decision table as a design artifact and trace it back to requirements
- Implement a function whose logic is fully driven by a design — not intuition
- Run a structured V&V test suite and interpret the results
- Explain how traceability connects requirements, design, code, and tests
- Reflect on Waterfall, Agile, and V-Cycle in a safety-critical context

---

## The Problem

You are a junior software engineer on a safety-critical automotive project. Your system controls **cruise control** on a vehicle.

> **Client description (informal):**
> *"Cruise control must be safe. It should stop when needed, should not start in dangerous conditions, and if it stops for a safety reason the driver must be aware that they need to restart it manually."*

Your job is to take this through all SDLC phases: requirements → design → implementation → verification & validation.

---

## Structure

Work through each Part in order. Do not skip ahead — each part builds on the previous one. Write your answers directly in the editor at the bottom of the page.

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

You do **not** need to be a programmer. Python is used here to make requirements and design **executable and testable** — exactly what Scade One does, but manually.

**Variables**

```python
speed         = 85       # integer
brake_pressed = True     # boolean: True or False
state         = "ACTIVE" # string
```

**Conditions**

```python
if brake_pressed:
    print("Brake is pressed")
elif speed < 30:
    print("Speed too low")
else:
    print("All good")
```

**Functions**

```python
def check_system(speed, brake):
    if brake:
        return False
    return True

result = check_system(80, False)
print(result)   # True
```

---

## Part 1 — Requirements Analysis

Before any line of code is written, the team must agree on exactly **what** the system must do. Vague requirements lead to different implementations, untestable behavior, and expensive fixes discovered late.

### Activity 1A — Poorly written requirements

Another team received this version. **Do not implement these.**

| Req. ID | Description |
|---------|-------------|
| REQ-A | The system must stop cruise control when it is dangerous. |
| REQ-B | Speed must be OK to start cruise control. |
| REQ-C | If it stops, the driver must do something. |

> **Question:** What is wrong with these requirements? Why can you NOT implement or test anything based on them?
> Write 2–3 sentences as `answer_1a` in the editor.

### Activity 1B — Software Requirements Specification (SRS)

Well-written requirements follow the pattern: `"The system SHALL [action] WHEN/IF [condition]."`

| Req. ID | Description | Type |
|---------|-------------|------|
| **REQ-01** | The system SHALL deactivate cruise control if the brake is pressed. | Functional |
| **REQ-02** | The system SHALL deactivate cruise control if speed exceeds 130 km/h. | Functional |
| **REQ-03** | The system SHALL refuse to activate if speed is below 30 km/h. | Functional |
| **REQ-04** | The system SHALL enter state `SUSPENDED` (not `OFF`) when deactivated by a safety condition, so that reactivation must be explicit by the driver. | Functional |
| **REQ-05** | The system SHALL respond to any input in less than 100 ms. | Non-functional |
| **REQ-06** | The system SHALL be testable with simulated boolean inputs. | Non-functional |

> **Critical question:** Read REQ-02 and REQ-04 together. When speed exceeds 130 km/h, does the system go to `SUSPENDED` or directly to `OFF`? Do the requirements state this clearly?
> Write your answer as `answer_1b` in the editor — you will revisit this in Part 2.

---

## Part 2 — System Design

Without a design you cannot answer: what happens when brake and high speed occur simultaneously? When can the driver reactivate? Design answers these **before** you write a single line of code.

### Activity 2A — Decision Table

A decision table lists every combination of conditions and the action the system must take. Each row is one decision rule. Read it **top to bottom** — the first rule that matches wins.

| Current state | brake\_pressed | speed > 130 | driver\_activates | driver\_reactivates | New state | REQ |
|---------------|:-----------:|:-----------:|:---------------:|:-----------------:|-----------|-----|
| `ACTIVE` | **True** | — | — | — | → `SUSPENDED` | REQ-01, REQ-04 |
| `ACTIVE` | — | **True** | — | — | → `SUSPENDED` | REQ-02, REQ-04 |
| `SUSPENDED` | — | — | — | **True** | → `ACTIVE` | REQ-04 |
| `SUSPENDED` ⚠️ | — | — | **True** | False | → `SUSPENDED` | REQ-04 |
| `OFF` | — | — | **True** | — | → `ACTIVE` if speed ≥ 30 / `OFF` if speed < 30 | REQ-03 |
| *any other* | | | | | *no change* | |

**—** means *don't care* — the condition is irrelevant for that rule.

> **⚠️ Key rule (row 4):** when the system is `SUSPENDED`, pressing *activate* alone is **not** enough — the driver must use *reactivate*. This is the most common implementation mistake.

### Activity 2B — Traceability: Design → Requirements

The REQ column in the decision table already gives you the links. Fill in the `traceability_design` dictionary in the editor — confirm you understand *why* each rule maps to its REQ.

### Activity 2C — Design decision

The decision table makes the REQ-02 / REQ-04 ambiguity from Part 1 explicit: row 2 sends `ACTIVE + speed > 130` to `SUSPENDED` (not `OFF`), because REQ-04 covers *all* safety-condition deactivations.

> **Question:** This is a design decision you made — not something the client specified. What should happen before implementing it in a real project? What could go wrong if two developers resolved it differently?
> Write your answer as `answer_2c` in the editor.

---

## Part 3 — Implementation

Implement `update_cruise_control()` in the editor. Each `if` branch you write corresponds directly to one row in the decision table — use the REQ column as your reference.

---

## Part 4 — Verification & Validation

| | Question | Focus |
|-|----------|-------|
| **Verification** | Are we building the system *right*? | Code matches design |
| **Validation** | Are we building the *right* system? | All requirements are met |

### Activity 4A — Run the tests

The test suite is already written in the editor. Click **▶ Run** below. All 7 tests must print `PASS`.

| Test ID | state | speed | brake | activates | reactivates | Expected | REQ |
|---------|-------|-------|-------|-----------|-------------|----------|-----|
| TC-01 | ACTIVE | 80 | True | False | False | SUSPENDED | REQ-01 |
| TC-02 | ACTIVE | 140 | False | False | False | SUSPENDED | REQ-02 |
| TC-03 | OFF | 20 | False | True | False | OFF | REQ-03 |
| TC-04 | OFF | 80 | False | True | False | ACTIVE | REQ-03 |
| **TC-05 ⚠️** | SUSPENDED | 80 | False | True | False | **SUSPENDED** | REQ-04 |
| TC-06 | SUSPENDED | 80 | False | False | True | ACTIVE | REQ-04 |
| TC-07 | ACTIVE | 80 | False | False | False | ACTIVE | REQ-01, REQ-02 |

> **⚠️ TC-05 is the key test.** A student who skipped the design or misread REQ-04 will return `ACTIVE` instead of `SUSPENDED`. This is intentional — it shows exactly why the design phase matters. If TC-05 fails, re-read REQ-04 and the ⚠️ key rule in the decision table.

### Activity 4B — TC-05 analysis

Answer in the editor as `answer_4b_1`, `answer_4b_2`, `answer_4b_3`:

1. Did TC-05 pass or fail on your first implementation attempt?
2. If it failed — where was the root cause: in the requirement, the design, or the code?
3. What would happen if this bug reached a deployed real vehicle system?

### Activity 4C — Full Traceability Matrix

Fill in the `status` field in the `traceability_matrix` dictionary in the editor after all tests pass.

| Req. ID | Design element | Code element | Test ID(s) | Status |
|---------|---------------|-------------|-----------|--------|
| REQ-01 | Row 1 of decision table | `if brake_pressed and ACTIVE` | TC-01, TC-07 | |
| REQ-02 | Row 2 of decision table | `if speed > 130 and ACTIVE` | TC-02, TC-07 | |
| REQ-03 | Row 5 of decision table | `if speed < 30: stay OFF` | TC-03, TC-04 | |
| REQ-04 | Rows 3 & 4 of decision table | `if driver_reactivates` | TC-05, TC-06 | |
| REQ-05 | Single-pass function | returns immediately | All TCs | |
| REQ-06 | Simulatable inputs | bool/int parameters | All TCs | |

---

## Part 5 — Reflection

Answer each question in 3–5 sentences in the editor (`answer_q1` through `answer_q4`).

**Q1 — Value of design**
TC-05 exposed an ambiguity in the requirements. How did the decision table from Part 2 help you resolve this ambiguity *before* writing code? What would have happened without it?

**Q2 — Waterfall**
Imagine you discovered the REQ-04 ambiguity only during testing in a pure Waterfall project. What would the impact be? How costly would it be to go back to the requirements phase?

**Q3 — Agile in safety-critical systems**
A colleague suggests skipping REQ-05 (< 100 ms) and adding it "in a later sprint". Why is this specifically dangerous in safety-critical systems, compared to a regular web application?

**Q4 — Scade One**
With 400 requirements instead of 6, what would happen to the traceability matrix if maintained manually? What parts of what you did by hand today would Scade One automate?

---

## Expected Output

When your implementation is correct, running the file produces:

```
Quick checks:
SUSPENDED
SUSPENDED

======================================================================
  VERIFICATION REPORT -- Cruise Control Safety System
======================================================================
  TC-01 [REQ-01      ] | Expected=SUSPENDED  Got=SUSPENDED  | PASS
  TC-02 [REQ-02      ] | Expected=SUSPENDED  Got=SUSPENDED  | PASS
  TC-03 [REQ-03      ] | Expected=OFF        Got=OFF        | PASS
  TC-04 [REQ-03      ] | Expected=ACTIVE     Got=ACTIVE     | PASS
  TC-05 [REQ-04      ] | Expected=SUSPENDED  Got=SUSPENDED  | PASS
  TC-06 [REQ-04      ] | Expected=ACTIVE     Got=ACTIVE     | PASS
  TC-07 [REQ-01,02   ] | Expected=ACTIVE     Got=ACTIVE     | PASS
----------------------------------------------------------------------
  VALIDATION: ALL REQUIREMENTS MET.
======================================================================
```

---

## Connection to Lecture 2

| SDLC Phase | What you did today |
|------------|--------------------|
| Requirements Analysis | Wrote REQ-01 to REQ-06 with IDs, precise language, and types |
| System Design | Built a decision table and mapped every row to a requirement |
| Implementation | Coded logic driven entirely by the design — not intuition |
| Verification & Validation | Ran 7 structured tests, each linked to a requirement |
| Traceability | Maintained REQ → Design → Code → Test links throughout |

> **Key takeaway:** Traceability is not paperwork — it is what makes a safety-critical system auditable and certifiable. This is exactly what tools like **Scade One** automate at industrial scale.
