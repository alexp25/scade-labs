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

if __name__ == "__main__":
    print("Quick checks:")
    print(update_cruise_control(ACTIVE, 80, True, False, False))    # SUSPENDED
    print(update_cruise_control(SUSPENDED, 80, False, True, False)) # SUSPENDED
    print()
    run_tests()
