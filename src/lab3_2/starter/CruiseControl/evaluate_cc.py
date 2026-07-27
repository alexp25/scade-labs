# evaluate_cc.py
# Instructor reference for Lab 3.2 Part 6 (Activities 6C-6F).
# Runs every scenario in scenarios/*.csv against the generated cruise_control
# wrapper, logs the per-cycle trace to results/<tid>_trace.csv, checks any
# expected_throttle checkpoints, writes a traceability summary to
# results/summary.csv, and plots each scenario's dynamic behaviour to
# results/plots/<tid>.png.
#
# NOTE: the generated wrapper (cc_wrapper/cc_wrapper.py) exposes the
# cruise_control operator as a class named after the root operator and the
# design file it was generated from (cruise_control_CC_design here), with
# inputs/outputs grouped under .inputs / .outputs rather than as direct
# attributes. The exact class name and grouping depend on your Scade One
# version and the operator you target for code generation - check the
# generated wrapper file and adjust the import/instantiation below and
# run_cycle() accordingly, same caveat as lab.md's Activity 6D.
#
# The cruise_control node takes set_point as a plain input rather than
# computing it internally (see assets/CC_design.swan), so this script
# reproduces Activity 4E's "rising edge of on locks set_point = v_speed"
# rule in Python and feeds the held value in every cycle. The scenario
# CSVs' "set" column is not part of this model's interface (only "on" and
# "res" affect set_point/state) and is kept only for traceability/logging.
#
# Requires a local Scade One install + a regenerated wrapper; cannot be run
# in an environment without Scade One (see .agents/testing.md).

import csv
import glob
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt

from ansys.scadeone.core import ScadeOne
from ansys.scadeone.core.svc.pywrapper.python_wrapper import PythonWrapper

SCADE_INSTALL = r"C:\Program Files\Ansys Inc\v261\Scade One Student\Scade One"
PROJECT_DIR = r"CruiseControl.sproj"
WRAPPER_NAME = "cc_wrapper"

app = ScadeOne(install_dir=SCADE_INSTALL)
prj = app.load_project(PROJECT_DIR)
prj.load_jobs()
JOB_NAME = "CodeGenerationJob_CC"
gen = PythonWrapper(prj, JOB_NAME, output=WRAPPER_NAME)
gen.generate()

# Instantiate generated operator class - check cc_wrapper/cc_wrapper.py if
# the class name differs for your Scade One version/project (pattern is
# <operator>_<design>, same convention as Lab 3.1's wrapper classes).
sys.path.insert(0, str(Path(__file__).parent / WRAPPER_NAME))
from cc_wrapper import cruise_control_CC_design  # noqa: E402

cc = cruise_control_CC_design()

SCENARIOS_DIR, RESULTS_DIR, TOLERANCE = "scenarios", "results", 1e-3
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")

_prev_on, _held_set_point = False, 0.0


def run_cycle(on, _set_flag, v_speed, brake, accel, res):
    """Set inputs, run one cycle, return throttle output.

    _set_flag (the scenario CSV's "set" column) is not part of this model's
    interface - see the NOTE at the top of this file - and is accepted only
    to keep the call site in run_scenario() self-documenting.
    """
    global _prev_on, _held_set_point
    if on and not _prev_on:
        _held_set_point = v_speed
    _prev_on = on

    cc.inputs.on, cc.inputs.v_speed = on, v_speed
    cc.inputs.brake, cc.inputs.accel, cc.inputs.res = brake, accel, res
    cc.inputs.set_point = _held_set_point
    cc.cycle()
    return cc.outputs.throttle


def plot_scenario(tid, trace):
    cycles = [int(r["cycle"]) for r in trace]
    throttle = [float(r["throttle"]) for r in trace]
    v_speed = [float(r["v_speed"]) for r in trace]

    fig, ax1 = plt.subplots()
    ax1.plot(cycles, throttle, color="tab:blue", label="throttle")
    ax1.set_xlabel("cycle")
    ax1.set_ylabel("throttle", color="tab:blue")

    ax2 = ax1.twinx()
    ax2.plot(cycles, v_speed, color="tab:orange", label="v_speed")
    ax2.set_ylabel("v_speed", color="tab:orange")

    plt.title(tid)
    fig.tight_layout()
    fig.savefig(os.path.join(PLOTS_DIR, f"{tid}.png"))
    plt.close(fig)


def run_scenario(path):
    global _prev_on, _held_set_point
    tid = os.path.splitext(os.path.basename(path))[0]
    cc.reset()
    _prev_on, _held_set_point = False, 0.0
    trace, checks = [], []

    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            throttle = run_cycle(
                row["on"] == "True", row["set"] == "True", float(row["v_speed"]),
                float(row["brake"]), float(row["accel"]), row["res"] == "True",
            )
            trace.append({**row, "throttle": f"{throttle:.3f}"})
            if row["expected_throttle"]:
                expected = float(row["expected_throttle"])
                passed = abs(throttle - expected) <= TOLERANCE
                checks.append({
                    "tid": tid, "cycle": row["cycle"], "req": row["req"],
                    "note": row["note"], "expected": expected,
                    "actual": throttle, "status": "PASS" if passed else "FAIL",
                })

    with open(os.path.join(RESULTS_DIR, f"{tid}_trace.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=trace[0].keys())
        writer.writeheader()
        writer.writerows(trace)

    plot_scenario(tid, trace)
    return checks


if __name__ == "__main__":
    os.makedirs(PLOTS_DIR, exist_ok=True)
    all_checks = []

    for path in sorted(glob.glob(os.path.join(SCENARIOS_DIR, "*.csv"))):
        all_checks.extend(run_scenario(path))

    with open(os.path.join(RESULTS_DIR, "summary.csv"), "w", newline="") as f:
        fields = ["tid", "cycle", "req", "note", "expected", "actual", "status"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_checks)

    print("=" * 70)
    print("  VERIFICATION REPORT -- cruise_control (Scade One, scenario files)")
    print("=" * 70)
    for c in all_checks:
        print(f"  [{c['req']:8s}] {c['tid']:38s} | expected={c['expected']:.3f} "
              f"actual={c['actual']:.3f} | {c['status']}")
    n_fail = sum(1 for c in all_checks if c["status"] == "FAIL")
    print("=" * 70)
    print("VALIDATION: ALL REQUIREMENTS MET." if n_fail == 0
          else f"VALIDATION: ISSUES FOUND ({n_fail} failing).")
