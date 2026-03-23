# Lab 2 – Cruise Control Safety System
# Student name: _______________________________________________________________
#
# Work through Parts 1-5 in the README, then fill in this file.
# Run the file when done — all 7 tests must print PASS.

# ------------------------------------------------------------------------------
# System states — do not change
OFF       = "OFF"
ACTIVE    = "ACTIVE"
SUSPENDED = "SUSPENDED"


# ------------------------------------------------------------------------------
# PART 1 — Requirements Analysis
# ------------------------------------------------------------------------------

# Answer 1A — what is wrong with the poorly written requirements?
answer_1a = """
[your answer here]
"""

# Answer 1B — REQ-02 vs REQ-04: when speed > 130, does the system go to
# SUSPENDED or OFF? Do the requirements say clearly?
answer_1b = """
[your answer here]
"""


# ------------------------------------------------------------------------------
# PART 2 — System Design
# ------------------------------------------------------------------------------

# Activity 2B — fill in the REQ covered column
traceability_design = {
    "State SUSPENDED (distinct from OFF)":                    "",  # e.g. "REQ-04"
    "Transition ACTIVE -> SUSPENDED on brake":                "",
    "Block activation if speed < 30":                         "",
    "Transition ACTIVE -> SUSPENDED on speed > 130":          "",
    "Transition SUSPENDED -> ACTIVE only on explicit action": "",
}

# Answer 2C — design decision: what should happen before implementing it?
# What could go wrong if two developers resolved the ambiguity differently?
answer_2c = """
[your answer here]
"""


# ------------------------------------------------------------------------------
# PART 3 — Implementation
# ------------------------------------------------------------------------------

def update_cruise_control(current_state, speed, brake_pressed,
                          driver_activates, driver_reactivates):
    """
    Update the cruise control state based on current inputs.

    Args:
        current_state      (str):  "OFF", "ACTIVE", or "SUSPENDED"
        speed              (int):  vehicle speed in km/h
        brake_pressed      (bool): True if brake pedal is pressed
        driver_activates   (bool): True if driver presses activate button
        driver_reactivates (bool): True if driver explicitly reactivates
                                   after a SUSPENDED state
    Returns:
        str: new state
    """

    # Step 1 — Safety conditions (from ACTIVE)
    #          brake OR speed > 130  ->  SUSPENDED   [REQ-01, REQ-02, REQ-04]


    # Step 2 — SUSPENDED state
    #          driver_reactivates    ->  ACTIVE       [REQ-04]
    #          driver_activates only ->  SUSPENDED    [REQ-04]  ← KEY TRAP


    # Step 3 — OFF state
    #          activates + speed >= 30  ->  ACTIVE    [REQ-03]
    #          activates + speed < 30   ->  OFF       [REQ-03]


    # Step 4 — Default
    return current_state


# ------------------------------------------------------------------------------
# PART 4 — Verification & Validation
# ------------------------------------------------------------------------------

def run_tests():
    test_cases = [
        # (state,     speed, brake, activates, reactivates, expected,   id,       req)
        (ACTIVE,    80,  True,  False, False, SUSPENDED, "TC-01", "REQ-01"),
        (ACTIVE,   140,  False, False, False, SUSPENDED, "TC-02", "REQ-02"),
        (OFF,       20,  False, True,  False, OFF,       "TC-03", "REQ-03"),
        (OFF,       80,  False, True,  False, ACTIVE,    "TC-04", "REQ-03"),
        (SUSPENDED, 80,  False, True,  False, SUSPENDED, "TC-05", "REQ-04"),  # key trap
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
    return all_passed


# Activity 4B — TC-05 analysis
answer_4b_1 = """Did TC-05 pass or fail on your first attempt?
[your answer here]
"""

answer_4b_2 = """Root cause — was it in the requirement, the design, or the code?
[your answer here]
"""

answer_4b_3 = """What would happen if this bug reached a deployed real vehicle?
[your answer here]
"""

# Activity 4C — fill in the Status column
traceability_matrix = {
    "REQ-01": {"design": "ACTIVE->SUSPENDED on brake",           "code": "brake_pressed and ACTIVE",  "tests": "TC-01,TC-07", "status": ""},
    "REQ-02": {"design": "ACTIVE->SUSPENDED on speed>130",       "code": "speed>130 and ACTIVE",      "tests": "TC-02,TC-07", "status": ""},
    "REQ-03": {"design": "Block activation below 30 km/h",       "code": "speed<30: stay OFF",        "tests": "TC-03,TC-04", "status": ""},
    "REQ-04": {"design": "SUSPENDED->ACTIVE only if reactivates","code": "if driver_reactivates",     "tests": "TC-05,TC-06", "status": ""},
    "REQ-05": {"design": "Single-pass, no delay",                "code": "returns immediately",       "tests": "All TCs",     "status": ""},
    "REQ-06": {"design": "Simulatable inputs",                   "code": "bool/int parameters",       "tests": "All TCs",     "status": ""},
}


# ------------------------------------------------------------------------------
# PART 5 — Reflection
# ------------------------------------------------------------------------------

answer_q1 = """Value of design: how did the State Machine help resolve the REQ-04
ambiguity before writing code? What would have happened without it?
[your answer here]
"""

answer_q2 = """Waterfall: if you discovered the REQ-04 ambiguity only during testing
in a pure Waterfall project, what would the impact be?
[your answer here]
"""

answer_q3 = """Agile in safety-critical systems: why is skipping REQ-05 for
a later sprint dangerous here, compared to a regular web app?
[your answer here]
"""

answer_q4 = """Scade One: with 400 requirements instead of 6, what would
happen to the matrix manually? What would Scade One automate?
[your answer here]
"""


# ------------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    print("Quick checks:")
    print(update_cruise_control(ACTIVE, 80, True, False, False))   # SUSPENDED
    print(update_cruise_control(SUSPENDED, 80, False, True, False)) # SUSPENDED (not ACTIVE!)
    print()
    run_tests()
