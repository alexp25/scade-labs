# ==============================================================================
# Lab 2 – Applying the SDLC: Cruise Control Safety System
# ==============================================================================
# Student name: ________________________________________________________________
# Date: ________________________________________________________________________
#
# INSTRUCTIONS:
#   Work through each PART in order. Fill in every TODO block and every
#   question marked with [YOUR ANSWER]. Do NOT change function signatures
#   or test IDs. Run the file when done — all 7 tests must print PASS.
#   Submit this single file as your lab deliverable.
#
#   Run:  python lab2_cruise_control_starter.py
# ==============================================================================


# ==============================================================================
# PART 0 — Python in 15 Minutes
# ==============================================================================
#
# You do NOT need to be a programmer for this lab.
# We use Python to make requirements and design EXECUTABLE and TESTABLE —
# exactly what a tool like Scade One does, but manually.
#
# --- Variables ----------------------------------------------------------------
#   speed = 85            # integer
#   brake_pressed = True  # boolean: True or False
#   state = "ACTIVE"      # string
#
# --- Conditions ---------------------------------------------------------------
#   if brake_pressed:
#       print("Brake is pressed")
#   elif speed < 30:
#       print("Speed too low")
#   else:
#       print("All good")
#
# --- Functions ----------------------------------------------------------------
#   def check_system(speed, brake):
#       if brake:
#           return False
#       return True
#
#   result = check_system(80, False)
#   print(result)   # True
#
# --- Self-test (run this mentally — make sure you understand the output) ------
#   def greet(name):
#       return "Hello, " + name + "!"
#
#   print(greet("Alice"))    # Hello, Alice!
#   print(greet("Student"))  # Hello, Student!
# ==============================================================================


# ==============================================================================
# PART 1 — Requirements Analysis  (~20 min)
# ==============================================================================
#
# CONTEXT
# -------
# You are a junior software engineer on a safety-critical automotive project.
# The client sent this informal description:
#
#   "Cruise control must be safe. It should stop when needed, should not start
#    in dangerous conditions, and if it stops for a safety reason the driver
#    must be aware that they need to restart it manually."
#
# ------------------------------------------------------------------------------
# ACTIVITY 1A — Poorly written requirements (reference only — do NOT implement)
# ------------------------------------------------------------------------------
#   REQ-A  The system must stop cruise control when it is dangerous.
#   REQ-B  Speed must be OK to start cruise control.
#   REQ-C  If it stops, the driver must do something.
#
# [YOUR ANSWER 1A]
# What is wrong with these requirements? Why can you NOT implement or test
# anything based on them? (2-3 sentences)
#
#   Answer:
#
#
# ------------------------------------------------------------------------------
# ACTIVITY 1B — Software Requirements Specification (SRS)
# ------------------------------------------------------------------------------
#
# | Req. ID | Description                                                           | Type           |
# |---------|-----------------------------------------------------------------------|----------------|
# | REQ-01  | The system SHALL deactivate cruise control if the brake is pressed.   | Functional     |
# | REQ-02  | The system SHALL deactivate cruise control if speed exceeds 130 km/h. | Functional     |
# | REQ-03  | The system SHALL refuse to activate if speed is below 30 km/h.        | Functional     |
# | REQ-04  | The system SHALL enter state SUSPENDED (not OFF) when deactivated by  | Functional     |
# |         | a safety condition, so reactivation must be explicit by the driver.  |                |
# | REQ-05  | The system SHALL respond to any input in less than 100 ms.            | Non-functional |
# | REQ-06  | The system SHALL be testable with simulated boolean inputs.           | Non-functional |
#
# [YOUR ANSWER 1B — Critical question]
# Read REQ-02 and REQ-04 together. When speed exceeds 130 km/h, does the
# system go to SUSPENDED or directly to OFF? Do the requirements say clearly?
# Note your answer — you will revisit this in Part 2.
#
#   Answer:
#
#
# ==============================================================================


# ==============================================================================
# PART 2 — System Design  (~20 min)
# ==============================================================================
#
# WITHOUT a design you do not know:
#   - How many states does the system have?
#   - What happens if brake AND high speed occur simultaneously?
#   - Where is current state stored? Who remembers it?
#
# ------------------------------------------------------------------------------
# ACTIVITY 2A — State Machine  (read carefully before writing any code)
# ------------------------------------------------------------------------------
#
#   +----------+   driver activates (speed >= 30)   +-----------+
#   |   OFF    | ----------------------------------> |  ACTIVE   |
#   +----------+                                     +-----------+
#        ^                                                 |
#        |                                  brake OR speed > 130
#        |                                                 |
#        |      driver reactivates explicitly     +--------v--------+
#        +----------------------------------------|   SUSPENDED    |
#                                                 +-----------------+
#
# States:
#   OFF       -- off; driver can activate if speed >= 30
#   ACTIVE    -- cruise control is running
#   SUSPENDED -- stopped by safety condition; driver MUST reactivate explicitly
#
# Transition table:
# | From      | Event                               | To        | REQ covered    |
# |-----------|-------------------------------------|-----------|----------------|
# | OFF       | driver activates AND speed >= 30    | ACTIVE    | REQ-03         |
# | OFF       | driver activates AND speed < 30     | OFF       | REQ-03         |
# | ACTIVE    | brake pressed                       | SUSPENDED | REQ-01, REQ-04 |
# | ACTIVE    | speed > 130                         | SUSPENDED | REQ-02, REQ-04 |
# | SUSPENDED | driver reactivates explicitly       | ACTIVE    | REQ-04         |
# | SUSPENDED | driver activates (no reactivation)  | SUSPENDED | REQ-04         |
#
# ------------------------------------------------------------------------------
# ACTIVITY 2B — Traceability: Design -> Requirements
# ------------------------------------------------------------------------------
# Fill in the REQ covered column.
#
# | Design Element                                         | REQ covered |
# |--------------------------------------------------------|-------------|
# | State SUSPENDED (distinct from OFF)                    |             |
# | Transition ACTIVE -> SUSPENDED on brake                |             |
# | Block activation if speed < 30                         |             |
# | Transition ACTIVE -> SUSPENDED on speed > 130          |             |
# | Transition SUSPENDED -> ACTIVE only on explicit action |             |
#
# ------------------------------------------------------------------------------
# ACTIVITY 2C — Design decision
# ------------------------------------------------------------------------------
# Revisit Activity 1B. The state machine resolves the ambiguity:
# speed > 130 -> SUSPENDED (not OFF), because REQ-04 covers ALL safety
# condition deactivations and speed > 130 is a safety condition.
#
# [YOUR ANSWER 2C]
# This is a design decision you made — not something the client specified.
# What should happen before implementing it in a real project?
# What could go wrong if two developers resolved it differently?
#
#   Answer:
#
#
# ==============================================================================


# ==============================================================================
# PART 3 — Implementation  (~25 min)
# ==============================================================================

# System states — do NOT change these
OFF       = "OFF"
ACTIVE    = "ACTIVE"
SUSPENDED = "SUSPENDED"


def update_cruise_control(current_state, speed, brake_pressed,
                          driver_activates, driver_reactivates):
    """
    Update the cruise control state based on current inputs.

    Traceability:
        REQ-01 -- deactivate on brake pressed      -> SUSPENDED
        REQ-02 -- deactivate on speed > 130 km/h  -> SUSPENDED
        REQ-03 -- block activation below 30 km/h  -> stay OFF
        REQ-04 -- SUSPENDED requires explicit reactivation
        REQ-05 -- single-pass function, no delay
        REQ-06 -- all inputs are simulatable (bool / int)

    Args:
        current_state     (str):  current state -- "OFF", "ACTIVE", or "SUSPENDED"
        speed             (int):  current vehicle speed in km/h
        brake_pressed     (bool): True if brake pedal is pressed
        driver_activates  (bool): True if driver presses the activate button
        driver_reactivates(bool): True if driver explicitly reactivates
                                  after a SUSPENDED state

    Returns:
        str: new state after applying safety logic
    """

    # TODO: Implement the state machine logic here.
    #
    # Follow the transition table from Activity 2A exactly.
    # Recommended order:
    #
    #   Step 1 -- Safety conditions (from ACTIVE only)
    #             if brake_pressed OR speed > 130 -> SUSPENDED
    #
    #   Step 2 -- SUSPENDED state
    #             if driver_reactivates           -> ACTIVE
    #             if driver_activates only        -> stay SUSPENDED  (REQ-04!)
    #
    #   Step 3 -- OFF state
    #             if driver_activates AND speed >= 30 -> ACTIVE
    #             if driver_activates AND speed < 30  -> stay OFF    (REQ-03!)
    #
    #   Step 4 -- Default: return current_state unchanged
    #
    # KEY TRAP:
    #   When current_state == SUSPENDED and driver_activates == True but
    #   driver_reactivates == False -> must return SUSPENDED (see TC-05 / REQ-04).
    #   This is the most common mistake. If you got TC-05 wrong, reread REQ-04
    #   and look at row 6 in the transition table above.

    pass  # remove this line when you add your implementation


# ==============================================================================
# PART 4 — Verification & Validation  (~25 min)
# ==============================================================================
#
# Verification: "Are we building the system RIGHT?"  -> code matches design
# Validation:   "Are we building the RIGHT system?"  -> all requirements are met
#
# Test table:
# | TC    | state     | speed | brake | activates | reactivates | Expected  | REQ         |
# |-------|-----------|-------|-------|-----------|-------------|-----------|-------------|
# | TC-01 | ACTIVE    | 80    | True  | False     | False       | SUSPENDED | REQ-01      |
# | TC-02 | ACTIVE    | 140   | False | False     | False       | SUSPENDED | REQ-02      |
# | TC-03 | OFF       | 20    | False | True      | False       | OFF       | REQ-03      |
# | TC-04 | OFF       | 80    | False | True      | False       | ACTIVE    | REQ-03      |
# | TC-05 | SUSPENDED | 80    | False | True      | False       | SUSPENDED | REQ-04  *** |
# | TC-06 | SUSPENDED | 80    | False | False     | True        | ACTIVE    | REQ-04      |
# | TC-07 | ACTIVE    | 80    | False | False     | False       | ACTIVE    | REQ-01,02   |
#
# *** TC-05 is the KEY test. If it fails, you misread REQ-04 or skipped the
#     design. Reread the transition table row: SUSPENDED + activates only
#     -> stays SUSPENDED. Reactivation must be explicit.


def run_tests():
    """Full verification and validation test suite."""

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


# ------------------------------------------------------------------------------
# ACTIVITY 4B — TC-05 analysis
# ------------------------------------------------------------------------------

# [YOUR ANSWER 4B-1]
# Did TC-05 pass or fail on your first implementation attempt?
#
#   Answer:

# [YOUR ANSWER 4B-2]
# If it failed -- where was the root cause: in the requirement, in your
# design, or in your code? Explain.
#
#   Answer:

# [YOUR ANSWER 4B-3]
# What would happen if this bug reached a deployed real vehicle system?
#
#   Answer:


# ------------------------------------------------------------------------------
# ACTIVITY 4C — Full Traceability Matrix
# ------------------------------------------------------------------------------
# Fill in the Status column after all tests pass.
#
# | Req. ID | Design Element                          | Code Element                    | Test ID(s)   | Status |
# |---------|-----------------------------------------|---------------------------------|--------------|--------|
# | REQ-01  | ACTIVE -> SUSPENDED on brake            | if brake_pressed and ACTIVE     | TC-01, TC-07 |        |
# | REQ-02  | ACTIVE -> SUSPENDED on speed > 130      | if speed > 130 and ACTIVE       | TC-02, TC-07 |        |
# | REQ-03  | Block activation below 30 km/h          | if speed < 30: stay OFF         | TC-03, TC-04 |        |
# | REQ-04  | SUSPENDED -> ACTIVE only if reactivates | if driver_reactivates -> ACTIVE | TC-05, TC-06 |        |
# | REQ-05  | Single-pass, no delay                   | Function returns immediately    | All TCs      |        |
# | REQ-06  | Simulatable inputs                      | Bool/int parameters             | All TCs      |        |


# ==============================================================================
# PART 5 — Reflection  (~15 min)
# ==============================================================================
# Answer each question in 3-5 sentences.

# [YOUR ANSWER Q1 -- Value of design]
# TC-05 exposed an ambiguity in the requirements. How did the State Machine
# from Part 2 help you resolve this ambiguity BEFORE writing code?
# What would have happened without it?
#
#   Answer:


# [YOUR ANSWER Q2 -- Waterfall]
# Imagine you discovered the REQ-04 ambiguity only during the testing phase
# in a pure Waterfall project. What would the impact be? How costly would
# it be to go back to the requirements phase?
#
#   Answer:


# [YOUR ANSWER Q3 -- Agile in safety-critical systems]
# A colleague suggests skipping REQ-05 (response < 100 ms) and adding it
# "in a later sprint". Why is this specifically dangerous in safety-critical
# systems, compared to a regular web application?
#
#   Answer:


# [YOUR ANSWER Q4 -- Scade One]
# Look at your traceability matrix. Now imagine the system has 400 requirements
# instead of 6. What would happen to the matrix if maintained manually?
# What parts of what you did by hand today would Scade One automate?
#
#   Answer:


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    print("Quick manual checks:")
    print(update_cruise_control(ACTIVE, 80, True, False, False))
    # Expected: SUSPENDED

    print(update_cruise_control(SUSPENDED, 80, False, True, False))
    # Expected: SUSPENDED  <-- REQ-04, NOT ACTIVE or OFF

    print()
    run_tests()
