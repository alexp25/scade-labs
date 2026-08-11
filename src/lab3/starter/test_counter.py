# test_counter.py
# Tests the generated counter operator against REQ-CNT-01..02.
# Mirrors the multi-cycle simulation from Activity 4E.
#
# Run setup_wrapper.py first.
#
# By default this looks for counter_wrapper/ next to this script (the
# solution/starter layout). To test your own generated project instead —
# e.g. after copying/uploading your own blocks.swan + generated wrapper
# into a different folder — pass --project-dir:
#   python test_counter.py --project-dir path\to\your\project
#
# This is the simple version: cycle the operator, print PASS/FAIL. For a
# requirement-traceability report plus a CSV/diagram of which requirements
# pass or fail on the model, see test_counter_advanced.py.

import argparse
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--project-dir", "-d", type=Path, default=Path(__file__).parent,
                     help="Folder containing counter_wrapper/ (default: this script's folder)")
args = parser.parse_args()

sys.path.insert(0, str(args.project_dir / "counter_wrapper"))
from counter_wrapper import counter_blocks  # class is <module>_<operator>

cnt = counter_blocks()

# (cycle, expected, req)
expected_sequence = [(0, 0, "REQ-CNT-01"), (1, 1, "REQ-CNT-02"),
                      (2, 2, "REQ-CNT-02"), (3, 3, "REQ-CNT-02")]

print("=" * 50)
print("  COUNTER TEST REPORT")
print("=" * 50)

cnt.reset()  # reset once — do NOT reset between cycles
all_passed = True
for cycle_n, expected, req in expected_sequence:
    cnt.inputs.init_value = 0  # inputs via .inputs.<name>
    cnt.inputs.step       = 1
    cnt.cycle()               # advance one clock cycle
    result = cnt.outputs.count  # outputs via .outputs.<name>
    status = "PASS" if result == expected else "FAIL"
    if status == "FAIL":
        all_passed = False
    print(f"  [{req:10s}] Cycle {cycle_n}  expected={expected}  got={result}  {status}")

print("-" * 50)
print("  ALL PASS" if all_passed else "  SOME TESTS FAILED")
print("=" * 50)
