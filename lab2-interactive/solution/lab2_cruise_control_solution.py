# Lab 2 – Cruise Control Safety System
# SOLUTION FILE — instructor use only

OFF       = "OFF"
ACTIVE    = "ACTIVE"
SUSPENDED = "SUSPENDED"


# ------------------------------------------------------------------------------
# Reference implementation
# ------------------------------------------------------------------------------

def update_cruise_control(current_state, speed, brake_pressed,
                          driver_activates, driver_reactivates):
    # Step 1 — Safety conditions from ACTIVE  [REQ-01, REQ-02, REQ-04]
    if current_state == ACTIVE:
        if brake_pressed or speed > 130:
            return SUSPENDED

    # Step 2 — SUSPENDED state  [REQ-04]
    if current_state == SUSPENDED:
        if driver_reactivates:
            return ACTIVE
        return SUSPENDED   # driver_activates alone is NOT enough

    # Step 3 — OFF state  [REQ-03]
    if current_state == OFF:
        if driver_activates:
            if speed >= 30:
                return ACTIVE
            return OFF

    # Step 4 — Default
    return current_state


# ------------------------------------------------------------------------------
# Test suite
# ------------------------------------------------------------------------------

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


# ------------------------------------------------------------------------------
# Sample answers — for grading reference
# ------------------------------------------------------------------------------

# Answer 1A:
#   The requirements are too vague to implement or test. "When dangerous" and
#   "must be OK" are undefined — different engineers would interpret them
#   differently. REQ-C ("the driver must do something") specifies neither the
#   action nor the resulting system state.

# Answer 1B:
#   The requirements do not state this clearly. REQ-02 says "deactivate" on
#   speed > 130, but REQ-04 says safety deactivations must go to SUSPENDED.
#   Whether speed > 130 counts as a "safety condition" requires a design
#   decision not present in the SRS.

# Answer 2B traceability:
#   State SUSPENDED (distinct from OFF)                    -> REQ-04
#   Transition ACTIVE -> SUSPENDED on brake                -> REQ-01, REQ-04
#   Block activation if speed < 30                         -> REQ-03
#   Transition ACTIVE -> SUSPENDED on speed > 130          -> REQ-02, REQ-04
#   Transition SUSPENDED -> ACTIVE only on explicit action -> REQ-04

# Answer 2C:
#   The decision must be validated with the client before implementation and
#   written back into the SRS to eliminate ambiguity. If two developers
#   resolved it differently (one returning SUSPENDED, one returning OFF),
#   the system would behave inconsistently depending on which module ran —
#   a safety hazard that could go undetected until integration testing or
#   field deployment.

# Answer 4B — TC-05:
#   Most students fail TC-05 on first attempt. The root cause is in the
#   requirements — REQ-04's wording about "explicit reactivation" is not
#   obviously distinct from "pressing activate". In a deployed vehicle, this
#   bug means the driver could re-engage cruise control after an emergency
#   brake without knowing the system was suspended for safety reasons,
#   potentially causing loss of control at highway speed.

# Reflection Q1:
#   The state machine forced the ambiguity to surface explicitly: row 6 in
#   the transition table — SUSPENDED + driver_activates -> stay SUSPENDED —
#   had to be written down and justified before coding. Without the design,
#   the intuitive (wrong) implementation would have been written directly.

# Reflection Q2:
#   In Waterfall, all downstream phases (design, implementation, test suite)
#   were built on the flawed foundation. Rolling back requires revisiting
#   requirements, updating design, re-implementing, and re-testing — extremely
#   costly in time, budget, and re-certification in a regulated domain.

# Reflection Q3:
#   In a web app, a slow response is a UX issue fixable in a later sprint.
#   In a safety-critical system, REQ-05 is part of the safety specification —
#   the car must react within 100 ms to prevent an accident. Safety standards
#   (DO-178C, ISO 26262) require every safety requirement to be verified before
#   certification; deferred safety properties are not permitted.

# Reflection Q4:
#   With 400 requirements, manual traceability is unmanageable — every change
#   requires finding all affected design elements, code lines, and tests by
#   hand, and omissions are inevitable. Scade One automates the full chain:
#   requirements link to behavioral models, code is generated from models
#   (making REQ->model->code traceability automatic), and a change to one
#   requirement immediately flags all affected downstream elements.


# ------------------------------------------------------------------------------
# Grading rubric
# ------------------------------------------------------------------------------
# Part 1 written answers          10 pts  (5 each)
# Part 2 traceability table       10 pts  (2 per row)
# Part 2 design decision          10 pts
# Part 3 implementation           25 pts
#   TC-01 to TC-04, TC-06, TC-07  15 pts  (2.5 each)
#   TC-05 (key trap)              10 pts
# Part 4 TC-05 analysis           15 pts  (5 per sub-question)
# Part 4 traceability matrix      10 pts
# Part 5 reflection Q1-Q4         20 pts  (5 each)


if __name__ == "__main__":
    print("Quick checks:")
    print(update_cruise_control(ACTIVE, 80, True, False, False))    # SUSPENDED
    print(update_cruise_control(SUSPENDED, 80, False, True, False)) # SUSPENDED
    print()
    run_tests()
