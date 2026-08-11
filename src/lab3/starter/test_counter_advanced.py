# test_counter_advanced.py
# Same tests as test_counter.py, plus a custom traceability tool: Scade
# One Student Edition does not ship a requirement-coverage report or a
# pass/fail-colored model view, so this script builds both by reading
# blocks.swan as plain text (see parse_operator / print_requirement_report)
# and rendering a diagram with matplotlib.
#
# Output (under <project-dir>/results/): counter_traceability.csv and
# counter_diagram.png (skipped with a warning if matplotlib isn't
# installed).
#
# Run setup_wrapper.py first.
#
# By default this looks for blocks.swan / counter_wrapper/ next to this
# script (the solution/starter layout). To test your own generated project
# instead — e.g. after copying/uploading your own blocks.swan + generated
# wrapper into a different folder — pass --project-dir:
#   python test_counter_advanced.py --project-dir path\to\your\project

import argparse
import csv
import os
import re
import sys
from pathlib import Path

OPERATOR_NAME = "counter"
EXPECTED_REQS = ["REQ-CNT-01", "REQ-CNT-02"]

# (cycle, expected, req)
expected_sequence = [(0, 0, "REQ-CNT-01"), (1, 1, "REQ-CNT-02"),
                      (2, 2, "REQ-CNT-02"), (3, 3, "REQ-CNT-02")]


def find_swan_path(project_dir):
    candidates = [
        project_dir / "assets" / "blocks.swan",  # solution layout
        project_dir / "blocks.swan",              # starter layout
    ]
    return next((p for p in candidates if p.exists()), None)


def parse_operator(swan_path, operator_name):
    """Parse a function/node's diagram body out of blocks.swan.

    Returns (elements, owner, wires):
      elements: {id: {"id", "kind", "desc", "req", "xy"}} for each
        top-level (#N expr ...)/(#N def ...) diagram element.
      owner: {sub_id: top_level_id} — maps the anonymous "(#N group)" wire
        slots declared inside an element's "where" clause back to the
        element that owns them, so wires can be drawn element-to-element.
      wires: [(src_id, [dst_id, ...]), ...] from "(#N wire #S => #D, ...)".

    This is a small regex/brace-matching reader, not a full Swan parser —
    good enough to recover the diagram structure and the
    '#pragma requirement <ID> #end' annotations the Requirements panel
    writes (see Lab 3 Part 9), without needing the Scade One API.
    """
    text = swan_path.read_text(encoding="utf-8")
    m = re.search(rf"(?:function|node)\s+{re.escape(operator_name)}\s*\(", text)
    if not m:
        return {}, {}, []

    brace_start = text.index("{", m.end())
    depth, end = 0, brace_start
    for i in range(brace_start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    body = text[brace_start:end + 1]

    elem_re = re.compile(r"^\s*\(#(\d+)\s+(expr|def)\s+(.*)$")
    sub_re = re.compile(r"^\s*\(#(\d+)\s+group\)\s*$")
    req_re = re.compile(r"#pragma requirement (\S+) #end")
    xy_re = re.compile(r'"xy":"H(-?\d+);V(-?\d+)"')
    wire_re = re.compile(r"^\s*\(#(\d+)\s+wire\s+#(\d+)\s*=>\s*(.*?)(?:\n|$)", re.MULTILINE)

    elements, owner, current = {}, {}, None
    for line in body.splitlines():
        elem_match = elem_re.match(line)
        if elem_match:
            eid, kind, desc = elem_match.group(1), elem_match.group(2), elem_match.group(3).strip()
            current = eid
            elements[eid] = {"id": eid, "kind": kind, "desc": desc, "req": None, "xy": None}
            owner[eid] = eid
            continue
        sub_match = sub_re.match(line)
        if sub_match and current is not None:
            owner[sub_match.group(1)] = current
            continue
        if current is not None:
            req_match = req_re.search(line)
            if req_match:
                elements[current]["req"] = req_match.group(1)
            xy_match = xy_re.search(line)
            if xy_match:
                elements[current]["xy"] = (int(xy_match.group(1)), int(xy_match.group(2)))

    wires = []
    for wm in wire_re.finditer(body):
        _wid, src, rest = wm.group(1), wm.group(2), wm.group(3)
        dst_ids = re.findall(r"#(\d+)", rest)
        wires.append((src, dst_ids))

    return elements, owner, wires


def traces_from_elements(elements):
    """{req_id: [(node_id, node_desc), ...]} from parsed elements."""
    traces = {}
    for e in elements.values():
        if e["req"]:
            traces.setdefault(e["req"], []).append((e["id"], e["desc"]))
    return traces


def print_requirement_report(operator_name, expected_reqs, swan_path, elements):
    print("=" * 60)
    print(f"  REQUIREMENT TRACEABILITY — {operator_name} (blocks.swan)")
    print("=" * 60)

    if swan_path is None:
        print("  blocks.swan not found under --project-dir — skipping trace check.")
        print("=" * 60)
        return {}

    traces = traces_from_elements(elements)
    print(f"  Source: {swan_path}")
    if not traces:
        print(f"  No '#pragma requirement' links found for '{operator_name}'.")
        print("  (Expected if the Requirements panel links haven't been added yet"
              " — see Lab 3 Activity 4F.)")
    for req in expected_reqs:
        nodes = traces.get(req)
        if nodes:
            node_list = ", ".join(f"#{node_id} ({desc})" for node_id, desc in nodes)
            print(f"  {req:12s} -> {node_list}")
        else:
            print(f"  {req:12s} -> NOT TRACED (missing '#pragma requirement {req} #end')")

    untracked = sorted(set(traces) - set(expected_reqs))
    if untracked:
        print(f"  Untracked req IDs present in the model but not expected here: {untracked}")
        print("  (Check spelling against requirements.md — Lab 3 Part 9's reQ2/REQ-02")
        print("   example shows exactly this kind of silent mismatch.)")
    print("=" * 60)
    return traces


def write_traceability_csv(rows, out_path):
    """One row per test case: which REQ it exercises, which model node(s)
    that REQ traces to, the inputs, and the pass/fail outcome. Same shape
    as Lab 4's results/summary.csv (tid, req, ..., status)."""
    os.makedirs(out_path.parent, exist_ok=True)
    fields = ["tid", "req", "nodes", "inputs", "expected", "actual", "status"]
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return out_path


def render_diagram(operator_name, elements, owner, wires, req_status, out_path):
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch

    STATUS_COLOR = {"PASS": "#2e7d32", "FAIL": "#c62828", None: "#607d8b"}
    STATUS_FACE = {"PASS": "#c8e6c9", "FAIL": "#ffcdd2", None: "#eceff1"}

    xs = [e["xy"][0] for e in elements.values() if e["xy"]]
    ys = [e["xy"][1] for e in elements.values() if e["xy"]]
    fig_w = max(8, (max(xs) - min(xs)) / 6000) if xs else 8
    fig_h = max(6, (max(ys) - min(ys)) / 4000) if ys else 6

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    positions = {}
    for eid, e in elements.items():
        x, y = e["xy"] if e["xy"] else (0, 0)
        positions[eid] = (x, -y)  # flip V so "up" in Scade reads up on screen

    for src, dsts in wires:
        src_owner = owner.get(src)
        if src_owner not in positions:
            continue
        for d in dsts:
            dst_owner = owner.get(d)
            if dst_owner not in positions or dst_owner == src_owner:
                continue
            arrow = FancyArrowPatch(positions[src_owner], positions[dst_owner],
                                     arrowstyle="-|>", mutation_scale=12,
                                     color="#9e9e9e", linewidth=1, zorder=1,
                                     connectionstyle="arc3,rad=0.05")
            ax.add_patch(arrow)

    for eid, e in elements.items():
        x, y = positions[eid]
        req = e["req"]
        status = req_status.get(req) if req else None
        label = f"#{eid} {e['desc']}"
        if req:
            label += f"\n[{req}]"
        half_w = max(3800, max(len(line) for line in label.split("\n")) * 480)
        box = FancyBboxPatch((x - half_w, y - 1500), half_w * 2, 3000,
                              boxstyle="round,pad=200",
                              linewidth=1.5, edgecolor=STATUS_COLOR[status],
                              facecolor=STATUS_FACE[status], zorder=2)
        ax.add_patch(box)
        ax.text(x, y, label, ha="center", va="center", fontsize=7, zorder=3)

    ax.set_title(f"{operator_name} — model diagram (colored by requirement test status)")
    ax.set_xlim(min(x for x, _ in positions.values()) - 9000,
                max(x for x, _ in positions.values()) + 9000)
    ax.set_ylim(min(y for _, y in positions.values()) - 5000,
                max(y for _, y in positions.values()) + 5000)
    ax.set_aspect("equal")
    ax.axis("off")

    legend_items = [
        Patch(facecolor=STATUS_FACE["PASS"], edgecolor=STATUS_COLOR["PASS"], label="requirement PASS"),
        Patch(facecolor=STATUS_FACE["FAIL"], edgecolor=STATUS_COLOR["FAIL"], label="requirement FAIL"),
        Patch(facecolor=STATUS_FACE[None], edgecolor=STATUS_COLOR[None], label="not requirement-tagged"),
    ]
    ax.legend(handles=legend_items, loc="lower center", ncol=3, fontsize=8,
              bbox_to_anchor=(0.5, -0.05), frameon=False)

    os.makedirs(out_path.parent, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    return out_path


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--project-dir", "-d", type=Path, default=Path(__file__).parent,
                     help="Folder containing blocks.swan and counter_wrapper/"
                          " (default: this script's folder)")
args = parser.parse_args()
project_dir = args.project_dir
results_dir = project_dir / "results"

swan_path = find_swan_path(project_dir)
elements, owner, wires = (parse_operator(swan_path, OPERATOR_NAME) if swan_path
                           else ({}, {}, []))
traces = print_requirement_report(OPERATOR_NAME, EXPECTED_REQS, swan_path, elements)

sys.path.insert(0, str(project_dir / "counter_wrapper"))
from counter_wrapper import counter_blocks  # class is <module>_<operator>

cnt = counter_blocks()

print()
print("=" * 50)
print("  COUNTER TEST REPORT")
print("=" * 50)

cnt.reset()  # reset once — do NOT reset between cycles
all_passed = True
csv_rows = []
for cycle_n, expected, req in expected_sequence:
    cnt.inputs.init_value = 0  # inputs via .inputs.<name>
    cnt.inputs.step       = 1
    cnt.cycle()               # advance one clock cycle
    result = cnt.outputs.count  # outputs via .outputs.<name>
    status = "PASS" if result == expected else "FAIL"
    if status == "FAIL":
        all_passed = False
    print(f"  [{req:10s}] Cycle {cycle_n}  expected={expected}  got={result}  {status}")

    nodes = "; ".join(f"#{nid} ({desc})" for nid, desc in traces.get(req, []))
    csv_rows.append({
        "tid": f"TC-CNT-{cycle_n:02d}", "req": req, "nodes": nodes,
        "inputs": f"cycle={cycle_n}, init_value=0, step=1",
        "expected": expected, "actual": result, "status": status,
    })

print("-" * 50)
print("  ALL PASS" if all_passed else "  SOME TESTS FAILED")
print("=" * 50)

# Aggregate a PASS/FAIL status per requirement (FAIL if any of its test
# cases failed) to drive the CSV report and the diagram's node coloring.
req_status = {}
for row in csv_rows:
    req_status[row["req"]] = "FAIL" if (req_status.get(row["req"]) == "FAIL"
                                         or row["status"] == "FAIL") else "PASS"

generated_files = []
try:
    csv_path = write_traceability_csv(csv_rows, results_dir / "counter_traceability.csv")
    generated_files.append(csv_path)
except OSError as e:
    print(f"  WARNING: could not write traceability CSV: {e}")

if swan_path is not None:
    try:
        diagram_path = render_diagram(
            OPERATOR_NAME, elements, owner, wires, req_status,
            results_dir / "counter_diagram.png")
        generated_files.append(diagram_path)
    except ImportError:
        print("  NOTE: matplotlib not installed — skipping counter_diagram.png"
              " (pip install matplotlib).")
    except Exception as e:  # noqa: BLE001 - diagram is a nice-to-have, must not mask test results
        print(f"  WARNING: could not render counter_diagram.png: {e}")

if generated_files:
    print("  Generated:")
    for f in generated_files:
        print(f"    {f}")
    print("=" * 50)
