# ==============================================================================
# Lab 2 – Applying the SDLC: Cruise Control Safety System
# SOLUTION FILE — for instructor use only
# ==============================================================================
#
# This file contains:
#   - The reference implementation of update_cruise_control()
#   - Sample answers for all written questions
#   - Notes on common mistakes to watch for when grading
#
# Do NOT share with students before the lab is complete.
# ==============================================================================


# ==============================================================================
# PART 1 — Sample answers
# ==============================================================================
#
# ANSWER 1A — What is wrong with the poorly written requirements?
#
#   The requirements are too vague to implement or test. "When it is dangerous"
#   (REQ-A) and "must be OK" (REQ-B) are undefined — different engineers would
#   interpret them differently, leading to inconsistent implementations. REQ-C
#   ("the driver must do something") does not specify what action or what state
#   the system should be in, making it impossible to write a test that verifies
#   whether it is satisfied.
#
# ANSWER 1B — Critical question: REQ-02 vs REQ-04
#
#   The requirements do not state this clearly. REQ-02 says to "deactivate"
#   if speed exceeds 130 km/h, but REQ-04 says deactivation due to a safety
#   condition must go to SUSPENDED, not OFF. There is a tension: does speed
#   > 130 count as a "safety condition"? A design decision is needed.
#
# ==============================================================================


# ==============================================================================
# PART 2 — Sample answers
# ==============================================================================
#
# ANSWER 2B — Traceability: Design -> Requirements
#
# | Design Element                                         | REQ covered    |
# |--------------------------------------------------------|----------------|
# | State SUSPENDED (distinct from OFF)                    | REQ-04         |
# | Transition ACTIVE -> SUSPENDED on brake                | REQ-01, REQ-04 |
# | Block activation if speed < 30                         | REQ-03         |
# | Transition ACTIVE -> SUSPENDED on speed > 130          | REQ-02, REQ-04 |
# | Transition SUSPENDED -> ACTIVE only on explicit action | REQ-04         |
#
# ANSWER 2C — Design decision
#
#   Before implementing this decision, it should be validated with the client
#   (or product owner) in a requirements review meeting, and the updated
#   interpretation should be written back into REQ-02 or REQ-04 to eliminate
#   the ambiguity. If two developers resolved it differently — one going to
#   SUSPENDED and one to OFF — the system would behave inconsistently depending
#   on which module was active, creating a safety hazard that might not be
#   caught until integration testing or, worse, field deployment.
#
# ==============================================================================


# ==============================================================================
# PART 3 — Reference implementation
# ==============================================================================

OFF       = "OFF"
ACTIVE    = "ACTIVE"
SUSPENDED = "SUSPENDED"


def update_cruise_control(current_state, speed, brake_pressed,
                          driver_activates, driver_reactivates):
    """
    Reference implementation — follows the transition table exactly.

    Traceability:
        REQ-01 -- deactivate on brake pressed      -> SUSPENDED
        REQ-02 -- deactivate on speed > 130 km/h  -> SUSPENDED
        REQ-03 -- block activation below 30 km/h  -> stay OFF
        REQ-04 -- SUSPENDED requires explicit reactivation
        REQ-05 -- single-pass function, no delay
        REQ-06 -- all inputs are simulatable (bool / int)
    """

    # Step 1 — Safety conditions: trigger from ACTIVE only
    # REQ-01, REQ-02, REQ-04
    if current_state == ACTIVE:
        if brake_pressed or speed > 130:
            return SUSPENDED

    # Step 2 — SUSPENDED state
    # REQ-04: driver_reactivates=True -> ACTIVE
    #         driver_activates=True but no reactivation -> stay SUSPENDED
    if current_state == SUSPENDED:
        if driver_reactivates:
            return ACTIVE
        return SUSPENDED   # covers both: activates-only and idle

    # Step 3 — OFF state
    # REQ-03: cannot activate below 30 km/h
    if current_state == OFF:
        if driver_activates:
            if speed >= 30:
                return ACTIVE
            return OFF     # REQ-03: refuse activation

    # Step 4 — Default: no change
    return current_state


# ==============================================================================
# PART 4 — Test suite (identical to starter)
# ==============================================================================

def run_tests():
    test_cases = [
        (ACTIVE,    80,  True,  False, False, SUSPENDED, "TC-01", "REQ-01"),
        (ACTIVE,   140,  False, False, False, SUSPENDED, "TC-02", "REQ-02"),
        (OFF,       20,  False, True,  False, OFF,       "TC-03", "REQ-03"),
        (OFF,       80,  False, True,  False, ACTIVE,    "TC-04", "REQ-03"),
        (SUSPENDED, 80,  False, True,  False, SUSPENDED, "TC-05", "REQ-04"),
        (SUSPENDED, 80,  False, False, True,  ACTIVE,    "TC-06", "REQ-04"),
        (ACTIVE,    80,  False, False, False, ACTIVE,    "TC-07", "REQ-01,02"),
    ]

    print("=" * 70)
    print("  VERIFICATION REPORT -- Cruise Control Safety System")
    print("=" * 70)

    all_passed = True
    for state, speed, brake, act, react, expected, tid, req in test_cases:
        result = update_cruise_control(state, speed, brake, act, react)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"  {tid} [{req:12s}] | "
              f"Expected={expected:9s}  Got={str(result):9s} | {status}")

    print("-" * 70)
    if all_passed:
        print("  VALIDATION: ALL REQUIREMENTS MET.")
    else:
        print("  VALIDATION: ISSUES FOUND -- review your implementation.")
    print("=" * 70)


# ==============================================================================
# PART 4 — Sample answers
# ==============================================================================
#
# ANSWER 4B-1 — Did TC-05 pass or fail on first attempt?
#
#   Most students fail TC-05 on first attempt. The expected answer is that it
#   failed, because the natural instinct is: "driver activates -> go to ACTIVE".
#   The student who passes it immediately likely did the design carefully first.
#
# ANSWER 4B-2 — Root cause
#
#   The root cause is in the REQUIREMENTS — specifically the ambiguity between
#   REQ-04 and intuitive behavior. The design (state machine) resolved it, but
#   a student who skipped the design or misread REQ-04 would implement the
#   intuitive (wrong) behavior. This demonstrates that ambiguous requirements
#   propagate directly into implementation bugs.
#
# ANSWER 4B-3 — Real-world impact
#
#   In a real vehicle, this bug would mean the driver could re-engage cruise
#   control after an emergency brake without being aware that the system had
#   been suspended for safety reasons. At highway speeds this could lead to
#   loss of control. In a certified system (DO-178C, ISO 26262), this would
#   be caught by mandatory traceability and formal review — which is exactly
#   what the lab simulates manually.
#
# GRADING NOTE on TC-05:
#   Award partial credit if the student:
#     - Correctly identifies the bug was in requirements ambiguity (not just "code error")
#     - Explains the connection between REQ-04 and the SUSPENDED state
#   Do not award credit if the student says "I just fixed the if statement"
#   without explaining WHY the design mandates SUSPENDED behavior.
#
# ==============================================================================


# ==============================================================================
# PART 5 — Sample answers
# ==============================================================================
#
# Q1 — Value of design
#
#   Without the state machine, the ambiguity in REQ-04 would have been resolved
#   implicitly and differently by each developer during coding. The state machine
#   forced the question to surface: "does SUSPENDED mean the driver must
#   reactivate, or can they just press activate again?" By making the transition
#   table explicit — row 6: SUSPENDED + activates -> stay SUSPENDED — the design
#   locked in a single interpretation before any code was written. Without it,
#   the bug would likely only surface during integration testing or field use.
#
# Q2 — Waterfall
#
#   In Waterfall, the requirements phase is completed and signed off before
#   design begins, and design before implementation, and so on. Discovering the
#   REQ-04 ambiguity during testing means all downstream phases — design,
#   implementation, and the test suite itself — were built on a flawed
#   foundation. Rolling back to fix the requirement, updating the design, and
#   re-implementing and re-testing the affected components is extremely costly,
#   both in time and budget, and may require re-certification in a regulated
#   domain.
#
# Q3 — Agile in safety-critical systems
#
#   In a web application, a slow response (> 100 ms) is a performance issue that
#   can be detected and fixed in a later sprint with no safety consequences.
#   In a safety-critical system, the response time is part of the safety
#   specification — the car must react to the brake in time to prevent an
#   accident. Adding REQ-05 "later" means the system was deployed and potentially
#   certified without a verified safety property. Safety standards like
#   DO-178C and ISO 26262 do not allow deferred safety requirements; every
#   requirement must be verified before certification.
#
# Q4 — Scade One
#
#   With 400 requirements, maintaining the traceability matrix manually becomes
#   unmanageable: every change to a requirement requires identifying which design
#   elements, code lines, and test cases are affected — and updating the matrix
#   by hand. Errors of omission (forgetting to update a link) are inevitable.
#   Scade One automates the entire traceability chain: requirements are linked
#   to behavioral models, code is generated from those models (so REQ -> model
#   -> code traceability is automatic), and test cases are generated from the
#   model's formal specification. A change to one requirement immediately flags
#   all affected elements.
#
# ==============================================================================


# ==============================================================================
# GRADING RUBRIC (suggested)
# ==============================================================================
#
# Part 1 — Written answers          10 pts  (5 per question)
# Part 2 — Traceability table       10 pts  (2 per row)
# Part 2 — Design decision answer   10 pts
# Part 3 — Implementation           25 pts
#   - TC-01 to TC-04, TC-06, TC-07  15 pts  (2.5 each)
#   - TC-05 (key trap)              10 pts
# Part 4 — TC-05 analysis            15 pts  (5 per sub-question)
# Part 4 — Traceability matrix       10 pts  (status + accuracy)
# Part 5 — Reflection Q1-Q4         20 pts  (5 each)
# ==============================================================================


if __name__ == "__main__":
    print("Quick manual checks:")
    print(update_cruise_control(ACTIVE, 80, True, False, False))   # SUSPENDED
    print(update_cruise_control(SUSPENDED, 80, False, True, False)) # SUSPENDED
    print()
    run_tests()
