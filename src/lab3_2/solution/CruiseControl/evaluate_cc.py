# evaluate_cc.py
# Instructor reference for Lab 3.2 Part 6 (Activities 6C-6F).
# Runs every scenario in scenarios/*.csv against the generated cruise_control
# wrapper, logs the per-cycle trace to results/<tid>_trace.csv, checks any
# expected_throttle checkpoints, writes a traceability summary to
# results/summary.csv, and plots each scenario's dynamic behaviour to
# results/plots/<tid>.png.
#
# NOTE: this mirrors the hypothetical single-operator wrapper API taught in
# docs/lab3_2/lab.md (cc.on, cc.brake, cc.cycle(), cc.throttle, root
# declarations = the cruise_control operator). The exact attribute names
# depend on your Scade One version and the operator you target for code
# generation - check the generated wrapper file and adjust run_cycle()
# accordingly, same caveat as lab.md's Activity 6D.
#
# Requires a local Scade One install + a regenerated wrapper; cannot be run
# in an environment without Scade One (see .agents/testing.md).

import csv
import glob
import os

import matplotlib.pyplot as plt

from ansys.scadeone.core import ScadeOne
from ansys.scadeone.core.svc.pywrapper.python_wrapper import PythonWrapper

SCADE_INSTALL = r"C:\Program Files\ANSYS Inc\v251\SCADE"
PROJECT_DIR = r"path\to\your\CruiseControl.sproj"

app = ScadeOne(install_dir=SCADE_INSTALL)
prj = app.load_project(PROJECT_DIR)
prj.load_jobs()
job = prj.get_job("CodeGenerationJob_CC")
gen = PythonWrapper(prj, job)
gen.generate()

# Instantiate generated operator class - check generated file for exact name.
cc = gen.get_operator_instance()

SCENARIOS_DIR, RESULTS_DIR, TOLERANCE = "scenarios", "results", 1e-3
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")


def run_cycle(on, set_flag, v_speed, brake, accel, res):
    """Set inputs, run one cycle, return throttle output."""
    cc.on, cc.set, cc.v_speed = on, set_flag, v_speed
    cc.brake, cc.accel, cc.res = brake, accel, res
    cc.cycle()
    return cc.throttle


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
    tid = os.path.splitext(os.path.basename(path))[0]
    cc.reset()
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
