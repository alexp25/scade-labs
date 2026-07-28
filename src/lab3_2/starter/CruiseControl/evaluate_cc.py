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
# computing it internally (see assets/CC_design.swan). Each scenario CSV's
# "set_point" column already encodes Activity 4E's "rising edge of on locks
# set_point = v_speed" rule (worked out once when the scenario was authored),
# so this script just feeds that column straight into cc.inputs.set_point
# every cycle - no derivation logic needed here. The CSVs' "set" column is
# a separate thing: it is not part of this model's interface (only "on" and
# "res" affect set_point/state) and is kept only for traceability/logging.
#
# The wrapper only exposes "throttle" as an output - the automaton's actual
# state (cc_disabled/cc_active/cc_standby) is internal to the generated
# model and not observable through cc.outputs. The "state" column in the
# trace/plot is therefore NOT read from the model: it is a Python-side
# re-derivation of the state, driven off the same on/brake/accel/res guards
# as the Activity 7A transition table, kept only so the chart can show
# roughly where the automaton should be. Treat it as a plotting aid, not a
# verified model output - it can drift from the model's real state if the
# guards above are ever changed in CC_design.swan without updating this file.
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

_prev_on, _cc_state = False, "active"


def run_cycle(on, _set_flag, v_speed, brake, accel, res, set_point):
    """Set inputs, run one cycle, return (throttle, state).

    _set_flag (the scenario CSV's "set" column) is not part of this model's
    interface - see the NOTE at the top of this file - and is accepted only
    to keep the call site in run_scenario() self-documenting.

    state is re-derived in Python from the same guards as the Activity 7A
    transition table (on; brake > 10.0 or accel > 10.0; res and brake <
    10.0) - see the NOTE at the top of this file for why this is a display
    aid, not a value read from the model.
    """
    global _prev_on, _cc_state
    if on and not _prev_on:
        _cc_state = "active"  # entering cc_enabled resets the inner state
    _prev_on = on

    if on:
        if brake > 10.0 or accel > 10.0:
            _cc_state = "standby"
        elif res and brake < 10.0:
            _cc_state = "active"
        state = _cc_state
    else:
        state = "disabled"

    cc.inputs.on, cc.inputs.v_speed = on, v_speed
    cc.inputs.brake, cc.inputs.accel, cc.inputs.res = brake, accel, res
    cc.inputs.set_point = set_point
    cc.cycle()
    return cc.outputs.throttle, state


_STATE_LEVELS = ["disabled", "standby", "active"]


def plot_scenario(tid, trace):
    cycles = [int(r["cycle"]) for r in trace]
    throttle = [float(r["throttle"]) for r in trace]
    v_speed = [float(r["v_speed"]) for r in trace]
    set_point = [float(r["set_point"]) for r in trace]
    brake = [float(r["brake"]) for r in trace]
    on = [1 if r["on"] == "True" else 0 for r in trace]
    set_flag = [1 if r["set"] == "True" else 0 for r in trace]
    res = [1 if r["res"] == "True" else 0 for r in trace]
    state = [_STATE_LEVELS.index(r["state"]) for r in trace]

    fig, (ax1, ax3) = plt.subplots(2, 1, sharex=True, figsize=(7, 6))

    # Top: throttle, v_speed / set_point (same units, same axis), and brake.
    ax1.plot(cycles, throttle, color="tab:blue", label="throttle")
    ax1.set_ylabel("throttle", color="tab:blue")
    ax1.set_title(tid)

    ax2 = ax1.twinx()
    ax2.plot(cycles, v_speed, color="tab:orange", label="v_speed")
    ax2.plot(cycles, set_point, color="tab:orange", linestyle="--", label="set_point")
    ax2.set_ylabel("v_speed / set_point", color="tab:orange")
    ax2.legend(loc="upper left", fontsize=8)

    ax6 = ax1.twinx()
    ax6.spines["right"].set_position(("outward", 60))
    ax6.plot(cycles, brake, color="tab:brown", label="brake")
    ax6.set_ylabel("brake", color="tab:brown")

    # Bottom: boolean inputs (on/set/res) plus the derived cc state.
    ax3.step(cycles, on, where="post", color="tab:green", label="on")
    ax3.step(cycles, set_flag, where="post", color="tab:purple", label="set")
    ax3.step(cycles, res, where="post", color="tab:red", label="res")
    ax3.set_ylim(-0.2, 1.2)
    ax3.set_yticks([0, 1])
    ax3.set_ylabel("inputs (bool)")
    ax3.set_xlabel("cycle")
    ax3.legend(loc="upper left", fontsize=8)

    ax4 = ax3.twinx()
    ax4.step(cycles, state, where="post", color="tab:gray",
              linestyle="--", label="cc state")
    ax4.set_ylim(-0.2, len(_STATE_LEVELS) - 0.8)
    ax4.set_yticks(range(len(_STATE_LEVELS)))
    ax4.set_yticklabels(_STATE_LEVELS)
    ax4.set_ylabel("cc state (derived)")

    fig.tight_layout()
    plot_path = os.path.join(PLOTS_DIR, f"{tid}.png")
    fig.savefig(plot_path)
    plt.close(fig)
    return plot_path


def run_scenario(path, index=None, total=None):
    global _prev_on, _cc_state
    tid = os.path.splitext(os.path.basename(path))[0]
    prefix = f"[{index}/{total}] " if index else ""
    print(f"{prefix}Running {tid} ...")

    cc.reset()
    _prev_on, _cc_state = False, "active"
    trace, checks = [], []

    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            throttle, state = run_cycle(
                row["on"] == "True", row["set"] == "True", float(row["v_speed"]),
                float(row["brake"]), float(row["accel"]), row["res"] == "True",
                float(row["set_point"]),
            )
            trace.append({**row, "throttle": f"{throttle:.3f}", "state": state})
            if row["expected_throttle"]:
                expected = float(row["expected_throttle"])
                passed = abs(throttle - expected) <= TOLERANCE
                checks.append({
                    "tid": tid, "cycle": row["cycle"], "req": row["req"],
                    "note": row["note"], "expected": expected,
                    "actual": throttle, "status": "PASS" if passed else "FAIL",
                })

    trace_path = os.path.join(RESULTS_DIR, f"{tid}_trace.csv")
    with open(trace_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=trace[0].keys())
        writer.writeheader()
        writer.writerows(trace)

    plot_path = plot_scenario(tid, trace)

    if checks:
        n_fail = sum(1 for c in checks if c["status"] == "FAIL")
        print(f"    {len(trace)} cycles, {len(checks)} checkpoint(s): "
              f"{len(checks) - n_fail} passed, {n_fail} failed")
    else:
        print(f"    {len(trace)} cycles, no checkpoints - see chart for regulator behaviour")

    return checks, [trace_path, plot_path]


if __name__ == "__main__":
    os.makedirs(PLOTS_DIR, exist_ok=True)
    all_checks = []
    generated_files = []

    scenario_paths = sorted(glob.glob(os.path.join(SCENARIOS_DIR, "*.csv")))
    for i, path in enumerate(scenario_paths, start=1):
        checks, files = run_scenario(path, i, len(scenario_paths))
        all_checks.extend(checks)
        generated_files.extend(files)

    summary_path = os.path.join(RESULTS_DIR, "summary.csv")
    with open(summary_path, "w", newline="") as f:
        fields = ["tid", "cycle", "req", "note", "expected", "actual", "status"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_checks)
    generated_files.append(summary_path)

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

    print("=" * 70)
    print("  GENERATED FILES -- inspect these for details")
    print("=" * 70)
    for f in generated_files:
        print(f"  {f}")
