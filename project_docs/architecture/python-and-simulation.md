# Python and simulation architecture

## Lab 2 — self-contained, dependency-free, dual execution path

`src/lab2/starter/lab2_cruise_control_starter.py`:
- Constants: `OFF`, `ACTIVE`, `SUSPENDED` (strings, "do not change").
- Stub: `update_cruise_control(current_state, speed, brake_pressed,
  driver_activates, driver_reactivates)` — docstring fully specifies the
  contract; body is 4 commented steps with no logic, falls through to
  `return current_state`.
- `run_tests()` — 7 hardcoded cases (`TC-01`…`TC-07`, each tagged with a REQ
  ID), prints a formatted PASS/FAIL table and an aggregate
  `"VALIDATION: ALL REQUIREMENTS MET."` / `"...ISSUES FOUND"` banner.

`src/lab2/solution/lab2_cruise_control_solution.py` — instructor-only,
same structure, with the stub replaced by:
```python
if current_state == ACTIVE:
    if brake_pressed or speed > 130:
        return SUSPENDED
if current_state == SUSPENDED:
    if driver_reactivates:
        return ACTIVE
    return SUSPENDED   # driver_activates alone is NOT enough
if current_state == OFF:
    if driver_activates:
        if speed >= 30:
            return ACTIVE
        return OFF
return current_state
```

**Verified this session** (Python 3.11.3, stdlib only, no install needed):
```
$ python src/lab2/solution/lab2_cruise_control_solution.py
...
  VALIDATION: ALL REQUIREMENTS MET.
```
All 7 PASS. Running the **starter** (unimplemented stub) as a control check:
3/7 PASS (TC-03, TC-05, TC-07 — the cases where "no state change" happens to
be the correct fallback), 4/7 FAIL (TC-01, TC-02, TC-04, TC-06),
`"VALIDATION: ISSUES FOUND"`. This confirms the harness correctly
discriminates a working implementation from a stub.

### Browser execution path

`docs/lab2/index.html` embeds the **identical** starter file (verified
byte-for-byte, aside from CRLF/LF line endings) as a JS `STARTER_CODE`
template literal, executed via **Skulpt** — a JavaScript Python interpreter
loaded from `skulpt.org` (CDN, not vendored). `runCode()`:
```js
Sk.configure({ output: ..., read: ..., __future__: Sk.python3 });
Sk.misceval.asyncToPromise(() =>
  Sk.importMainWithBody('<stdin>', false, editor.getValue(), true));
```
Output lines are pattern-matched (`| PASS`, `| FAIL`, `===`, `---`) for
color-coding and to drive a validation banner. Because Lab 2 imports nothing
beyond the stdlib, it runs unmodified under Skulpt — this is why Lab 2, and
only Lab 2, can offer a fully in-browser exercise.

## Lab 3.1 / 3.2 — Scade One Python wrapper testing (requires local install)

Both labs follow the same pattern: a Scade One code-generation job produces
C code; a `PythonWrapper` (from `ansys.scadeone.core.svc.pywrapper
.python_wrapper`) generates a ctypes-based `.py` wrapper around a compiled
`.dll`; a hand-written test/demo script drives it.

- **Lab 3.1**: `test_counter.py` ("Mirrors the multi-cycle simulation from
  Activity 4D") drives `counter_wrapper` through `expected_sequence =
  [0,1,2,3,4,5]`. `test_limiter.py` ("Mirrors the 3 manual simulation steps
  from Activity 2D") checks 3 cases (pass-through, clamp-max, clamp-min,
  tolerance `1e-9`). Both print manual PASS/FAIL text — no assertion
  framework.
- **Lab 3.2**: `tester.py` is a **live console demo, not an automated
  test** — a 1000-cycle loop toggling `accel`/`on`/`res`/`set_point`
  (cruise control engages at cycle 200, `set_point=50.0`), printing
  speed/gear/rpm/state each cycle with `time.sleep(0.05)`. There are no
  assertions and no PASS/FAIL output; a human reads the trace.
- `docs/lab3_2/lab.md`'s "Activity 6C" shows an **instructional-only**
  `test_cc_main.py` code block — **no such file exists in the repository**
  (confirmed by glob). It illustrates a different, simplified hypothetical
  wrapper API (`cc.on`, `cc.brake`, `cc.cycle()`) than the real generated
  `cc_wrapper.py` (`.inputs.<name>`/`.outputs.<name>`); the lab.md text
  itself flags this gap ("the exact class name and instantiation method
  depend on your Scade One version — check the generated wrapper file").

**Verified this session:** `ansys.scadeone.core` is not installed in this
environment (`ModuleNotFoundError`), so none of these scripts could be
executed. `python -m py_compile` on every `.py` file in both labs' solution
trees (including the generated wrappers) succeeded — syntactically valid,
but this does not prove runtime correctness (which additionally requires the
sibling `.dll`, produced only by Scade One's code generator).

## Correspondence between the Python reference and the Scade models

Explicitly stated by the repo (not inferred):
- Lab 3.1's `test_limiter.py`/`test_counter.py` docstrings state they mirror
  specific Lab 3.1 manual-simulation activities.
- `docs/lab3_2/lab.md` states its wrapper test "mirrors the test cases from
  Lab 2" and asks students to "compare the output to Lab 2's verification
  report."

**There is no automated cross-check** between Lab 2's Python state machine
and Lab 3.2's Swan `cruise_control` node — correspondence is manual: a human
runs both and compares printed output. No script in the repo runs both and
diffs the results.

## Simulation controls / timing

Only Lab 3.2's `tester.py` has a timing element: `time.sleep(0.05)` between
printed cycles, purely for human-readable pacing of the console trace — not
a real-time simulation constraint of the model itself.
