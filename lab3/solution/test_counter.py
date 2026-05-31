# test_counter.py
# Tests the generated counter operator.
# Mirrors the multi-cycle simulation from Activity 4D.
# Run setup_wrapper.py first.

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "counter_wrapper"))
from counter_wrapper import counter_blocks  # class is <module>_<operator>

cnt = counter_blocks()

expected_sequence = [0, 1, 2, 3, 4, 5]

print("=" * 40)
print("  COUNTER TEST REPORT")
print("=" * 40)

cnt.reset()  # reset once — do NOT reset between cycles
all_passed = True
for cycle_n, expected in enumerate(expected_sequence):
    cnt.inputs.init_value = 0  # inputs via .inputs.<name>
    cnt.inputs.step       = 1
    cnt.cycle()               # advance one clock cycle
    result = cnt.outputs.count  # outputs via .outputs.<name>
    status = "PASS" if result == expected else "FAIL"
    if status == "FAIL":
        all_passed = False
    print(f"  Cycle {cycle_n}  expected={expected}  got={result}  {status}")

print("-" * 40)
print("  ALL PASS" if all_passed else "  SOME TESTS FAILED")
print("=" * 40)