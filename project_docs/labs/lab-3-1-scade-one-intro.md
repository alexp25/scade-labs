# Lab 3.1 — Introduction to Scade One: Modeling Combinatorial and Sequential Logic

**Published:** `https://alexp25.github.io/scade-labs/lab3_1/` (`docs/lab3_1/index.html` + `docs/lab3_1/lab.md`)
**Source:** `src/lab3_1/solution/`

## Purpose

Teach Scade One fundamentals: typed operator interfaces, combinatorial logic
(a `limiter`), sequential logic (a `counter` using `pre`), the
Definition/Expression/Instance-block distinction, simulation, test harnesses,
and Python-wrapper testing of generated code.

## Prerequisites (quoted, `docs/lab3_1/lab.md`)

1. Install Scade One Student Edition. **The student edition does not require
   any registration or license activation** — corrected this session (the
   lab previously incorrectly stated a free license had to be registered).
2. Complete the official Scade One QuickStart YouTube tutorial.

This is the first Scade One lab — no prior lab is a prerequisite.

## Learning outcomes (quoted)

- Create Scade One projects and modules
- Create operators with typed interfaces
- Implement combinatorial logic
- Implement sequential logic using delays (`pre`)
- Simulate models
- Create and configure test harnesses
- Run automated simulations

## Repository files

| File | Role |
|---|---|
| `docs/lab3_1/lab.md` | Published lesson (Parts 1–7: module creation, limiter, counter, harnesses, Python wrapper, common errors, reflection quiz) |
| `docs/lab3_1/index.html` | Page shell + reflection-quiz widget |
| `docs/lab3_1/img/` | 14 screenshots (1 unreferenced: `scade_generate_python_wrapper.png`) |
| `src/lab3_1/solution/demo.sproj` | Project manifest (plain JSON) |
| `src/lab3_1/solution/assets/blocks.swan` | Hand-authored model: `function limiter(...)`, `node counter(...)`, `const init` |
| `src/lab3_1/solution/assets/test.swant` | Hand-authored, populated test harness (2 harnesses) |
| `src/lab3_1/solution/{setup_wrapper.py, requirements.txt}` | Wrapper-generation driver (requires local Scade One) |
| `src/lab3_1/solution/{test_counter.py, test_limiter.py}` | Manual PASS/FAIL Python test scripts |
| `src/lab3_1/solution/{counter_wrapper/, limiter_wrapper/}` | **Generated** ctypes wrappers — do not hand-edit |

There is **no `src/lab3_1/starter/`** — this lab is GUI-modeling, not a code
stub exercise.

## Student workflow

1. Install Scade One, watch the QuickStart video.
2. Create a project + `blocks` Swan module.
3. Build `limiter` (combinatorial): comparison blocks, clamp logic; simulate
   and check documented expected output (e.g. `value_in=120 → value_out=100`
   when `max=100`).
4. Build a populated test harness (`harness_limiter`) and run it — expected
   `value_out = 100.0`.
5. Build `counter` (sequential): `pre` + `+`; simulate over several cycles
   (expected sequence `0,1,2,3,4,5`).
6. Build `harness_counter` and run it.
7. Generate a Python wrapper for both operators and run `test_limiter.py` /
   `test_counter.py` locally.

## Model architecture

See `project_docs/architecture/scade-projects.md`. Summary: a
`function limiter` (stateless, combinatorial) and a `node counter`
(stateful, uses `pre`) inside a single `blocks.swan` module, exercised by a
populated `test.swant` harness file and, later, by generated Python wrappers.

## Requirements / traceability

**None.** This lab defines no REQ-xx identifiers anywhere — it teaches tool
mechanics, not requirements engineering. Test harnesses and Python tests
check hardcoded expected values with no formal requirement behind them. Do
not invent a traceability framing for this lab.

## Test/simulation procedure and expected results

- **Manual simulation** (documented in `lab.md`, not independently
  re-verified this session — requires Scade One):
  limiter: `(5,0,10)→5`, `(20,0,10)→10`, `(-5,0,10)→0`; counter: cycles
  0→0,1→1,2→2,3→3.
- **Test harness run** (in-tool, requires Scade One): expected
  `value_out = 100.0` for the shipped harness constants.
- **Python wrapper tests** (requires local Scade One install +
  `ansys-scadeone-core==0.8.2` + regenerated wrappers — **not runnable in
  this documentation-pass environment**, verified via
  `ModuleNotFoundError: No module named 'ansys'`): `test_counter.py` expects
  sequence `[0,1,2,3,4,5]`; `test_limiter.py` expects the same 3 cases as the
  manual simulation, tolerance `1e-9`. Both scripts were syntax-checked
  (`python -m py_compile`, passed) but not executed.

## Traceability

Not applicable — see "Requirements / traceability" above.

## Known limitations

- No starter/code-stub path — entirely GUI-driven, cannot be exercised
  without a Scade One install.
- One screenshot (`scade_generate_python_wrapper.png`) is unreferenced.
- Simulation/harness expected values above are the repository's own stated
  expectations, not independently re-run in this environment.

## Publishing route

`/lab3_1/` — see `project_docs/architecture/site-and-publishing.md`.
