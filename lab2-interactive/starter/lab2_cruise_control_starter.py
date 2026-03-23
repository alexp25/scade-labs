# Lab 2 – Cruise Control Safety System
# Run the file when done — all 7 tests must print PASS.

# ------------------------------------------------------------------------------
# System states — do not change
OFF       = "OFF"
ACTIVE    = "ACTIVE"
SUSPENDED = "SUSPENDED"

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

# ------------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    print("Quick checks:")
    print(update_cruise_control(ACTIVE, 80, True, False, False))   # SUSPENDED
    print(update_cruise_control(SUSPENDED, 80, False, True, False)) # SUSPENDED (not ACTIVE!)
    print()
    run_tests()
