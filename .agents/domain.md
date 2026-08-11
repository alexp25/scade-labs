# Domain vocabulary

Only concepts actually present in this repo, and the concrete role each plays here.

- **Laboratory (lab)** — one self-contained exercise, published as `docs/labN/`
  (instructions + interactive page) with matching source in `src/labN/`.
  Three exist: Lab 2 (Python/SDLC), Lab 3 (requirements engineering + Scade
  One/Swan basics + Limiter/Counter modeling + traceability mechanics), Lab 4
  (the Scade One cruise-control system: design, implementation, traceability).

- **EARS (Easy Approach to Requirements Syntax)** — a fixed set of five
  requirement sentence templates (ubiquitous / event-driven / state-driven /
  unwanted-behavior / optional-feature) plus a complex/combined form, taught
  in Lab 3 Part 1 (`docs/lab3/lab.md`) as a more rigorous alternative to
  Lab 2's free-form "SHALL" prose.

- **Requirement (REQ-xx)** — a numbered "SHALL"-style statement. Lab 2 defines
  the original full set: REQ-01..REQ-04 (functional, e.g. "deactivate cruise
  control if the brake is pressed") and REQ-05/06 (non-functional: response
  time, testability) in `docs/lab2/lab.md`. Lab 3 has students write two new
  small ID sets Lab 2 never needed (REQ-LIM-01..03 for the Limiter,
  REQ-CNT-01..02 for the Counter — both modeled within Lab 3 itself), then
  rewrite Lab 2's REQ-01/02/04 in EARS syntax and add two more new IDs,
  REQ-07/REQ-08 (regulator behavior and throttle clamping — model elements
  that only exist once Lab 4's Scade One model separates the
  regulator/limiter out). Lab 4 reuses REQ-01/02/04(/07/08) on its
  state-transition table (`docs/lab4/lab.md`, transition table near
  "Activity 4B") and traces them via `#pragma requirement` (Activity 7A).
  Lab 2's REQ-03 (refuse to activate below 30 km/h) is never carried into
  Lab 3 or Lab 4 — the Scade One model doesn't implement that guard.

- **Safety requirement** — in this repo, a requirement whose violation would
  be a hazard (e.g. REQ-01/02: cruise control must not stay active under
  brake or overspeed). Framed only at the requirement-statement level; there
  is no separate hazard-analysis artifact.

- **Decision table** — a markdown table mapping (state, condition) → new
  state, used as the design artifact between requirements and code in Lab 2
  (`docs/lab2/lab.md`, "Activity 2A — Decision Table"), and echoed as a
  smaller state-transition table in Lab 4.

- **Cruise-control controller** — implemented twice, independently: as a
  Python function `update_cruise_control(...)` (Lab 2,
  `src/lab2/*/lab2_cruise_control_*.py`) and as a Swan node
  `cruise_control` with a nested automaton (Lab 4, `CC_design.swan`). Lab
  4's `lab.md` and test comments explicitly state the Python wrapper test is
  meant to "mirror" Lab 2's test cases — see `.agents/verification.md` for how
  literal that correspondence is.

- **Limiter** — a saturation/clamp block: `if x > max then max elif x < min
  then min else x`. Taught standalone in Lab 3 (`function limiter(...)` in
  `blocks.swan`, Parts 2–3) and reused inside Lab 4's `regulator` node
  (`CC_design.swan`) to clamp the integral term and the final throttle.

- **Counter** — the first sequential (stateful) operator students build:
  `node counter(init_value, step) returns (count)` in `blocks.swan` (Lab 3,
  Parts 4–5), using `pre` to remember the previous cycle's value.

- **State machine** — in Lab 2, plain Python `if`/`elif` branches over string
  states (`OFF`/`ACTIVE`/`SUSPENDED`). In Lab 4, a real Scade One graphical
  automaton with two nesting levels: outer `cc_disabled`/`cc_enabled`, inner
  `cc_active`/`cc_standby` (`CC_design.swan`).

- **Synchronous operator / instance block** — a Swan `function`/`node`
  declaration is the operator; placing `+`, `-`, `>`, `<`, or `pre` on a
  diagram creates an **instance block** of that built-in operator, which
  processes a flow over time — distinct from an **Expression**, which is a
  literal constant (`0_i32`, `0.0_f64`). This distinction is documented in
  `docs/lab3/lab.md` ("Understanding Definition vs Expression" /
  "Instance blocks" subsections, inside Part 2's Limiter design activity).

- **Test harness** — a Swan `.swant` file that instantiates an operator
  under test with fixed input constants and a `_stop_condition`. Lab 3's
  `test.swant` is populated (two harnesses: counter, limiter); Lab 4 ships no
  `.swant` harness at all — its Part 5 only briefly mentions Scade One test
  harnesses before Part 6's Python evaluation script (`evaluate_cc.py` +
  `scenarios/*.csv`) takes over as the actual verification mechanism.

- **Simulation scenario** — either a hand-run sequence in the Scade One
  simulator (documented as expected-value tables in lab.md) or a saved
  `SimulationData` resource (`resources/main_inputs.sd`, binary, referenced by
  `CruiseControl.sproj`).

- **Traceability** — in Lab 2, an explicit REQ↔TC mapping carried both in
  prose (lab.md states "This test case verifies that REQ-X is met") and as a
  literal `req` field in each test tuple. In Lab 3 (Part 9, new this
  session), the mechanism is taught explicitly: linking a requirement via
  Scade One's Requirements panel writes a `#pragma requirement <ID> #end`
  annotation directly into the `.swan` source; students practice this on
  their own Limiter/Counter (Activities 2G, 4F) before Lab 4 Activity 7A asks
  them to do the same for `cruise_control`. The shipped `CC_design.swan`
  demonstrates the mechanism on exactly one node (`#pragma requirement reQ2`)
  — with a casing mismatch against the canonical `REQ-02` spelling, now used
  explicitly (in both Lab 3 Part 9 and Lab 4 Activity 7A) as a worked lesson
  on why Scade One doesn't validate pragma text. See
  `.agents/verification.md` for the full explicit/inferred breakdown — don't
  assume every REQ mention is a real trace link.

- **Verification** — running a test/simulation and checking it against a
  documented expected value (e.g. "Expected output: `value_out = 100.0`").

- **Validation** — checking the overall behavior against the informal client
  description in Lab 2 ("Cruise control must be safe...").

- **Generated code** — C/Python output of Scade One's code generator and
  Python-wrapper generator, always carrying a `generated by PyScadeOne
  Wrapper 1.0` banner or matching the generator's own manifest file. See
  `.agents/scade-models.md`.
