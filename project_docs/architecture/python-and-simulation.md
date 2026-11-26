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

## Lab 3 / 3.2 — Scade One Python wrapper testing (requires local install)

Both labs follow the same pattern: a Scade One code-generation job produces
C code; a `PythonWrapper` (from `ansys.scadeone.core.svc.pywrapper
.python_wrapper`) generates a ctypes-based `.py` wrapper around a compiled
`.dll`; a hand-written test/demo script drives it.

- **Lab 3**: `test_counter.py` ("Mirrors the multi-cycle simulation from
  Activity 4D") drives `counter_wrapper` through `expected_sequence =
  [0,1,2,3,4,5]`. `test_limiter.py` ("Mirrors the 3 manual simulation steps
  from Activity 2D") checks 3 cases (pass-through, clamp-max, clamp-min,
  tolerance `1e-9`). Both print manual PASS/FAIL text — no assertion
  framework.
- **Lab 4**: `evaluate_cc_quick_tester.py` is a **live console demo, not an automated
  test** — a 1000-cycle loop toggling `accel`/`on`/`res`/`set_point`
  (cruise control engages at cycle 200, `set_point=50.0`), printing
  speed/gear/rpm/state each cycle with `time.sleep(0.05)`. There are no
  assertions and no PASS/FAIL output; a human reads the trace. Kept as-is —
  not part of the Part 6 lesson flow.
- `docs/lab4/lab.md` Part 6 (Activities 6C–6F, rewritten in this session to
  replace Scade One test-harness building with a Python-driven evaluation
  workflow) now teaches `evaluate_cc_full_report.py`: test scenarios are stored as CSV
  files under `scenarios/` (one row per simulation cycle, optional
  `expected_throttle`/`req`/`note` checkpoint columns), the script drives the
  generated wrapper cycle-by-cycle, writes a per-scenario trace CSV plus a
  `results/summary.csv` traceability report, and plots
  `results/plots/<tid>.png` (throttle + `v_speed` vs. cycle on twin axes) via
  `matplotlib`. A matching reference copy —
  `src/lab4/starter/CruiseControl/evaluate_cc_full_report.py` plus six scenario CSVs
  under `src/lab4/starter/CruiseControl/scenarios/` — **does exist in the
  repository** (unlike the lab.md's prior `test_cc_main.py` snippet, which
  had no backing file). It still illustrates the same simplified hypothetical
  wrapper API (`cc.on`, `cc.brake`, `cc.cycle()`, `cc.throttle`) as before —
  not the real generated `cc_wrapper.py`'s `.inputs.<name>`/`.outputs.<name>`
  pattern (that wrapper is generated for the closed-loop `main` node, not a
  standalone `cruise_control` operator) — both `evaluate_cc_full_report.py` and lab.md
  carry the same "check the generated wrapper file" caveat as before; this
  session did not change which operator the wrapper is generated for.

**Verified this session:** `ansys.scadeone.core` is not installed in this
environment (`ModuleNotFoundError`), so none of these scripts could be
executed. `python -m py_compile` on every `.py` file in both labs' solution
trees (including the generated wrappers) succeeded — syntactically valid,
but this does not prove runtime correctness (which additionally requires the
sibling `.dll`, produced only by Scade One's code generator).

## Correspondence between the Python reference and the Scade models

Explicitly stated by the repo (not inferred):
- Lab 3's `test_limiter.py`/`test_counter.py` docstrings state they mirror
  specific Lab 3 manual-simulation activities.
- `docs/lab4/lab.md` states its wrapper test "mirrors the test cases from
  Lab 2" and asks students to "compare the output to Lab 2's verification
  report."

**There is no automated cross-check** between Lab 2's Python state machine
and Lab 4's Swan `cruise_control` node — correspondence is manual: a human
runs both and compares printed output. No script in the repo runs both and
diffs the results.

## Simulation controls / timing

Lab 4's `evaluate_cc_quick_tester.py` uses `time.sleep(0.05)` between
printed cycles, purely for human-readable pacing of the console trace — not
a real-time simulation constraint of the model itself. The separate SCADE
AI Raspberry Pi runtime described below measures execution time with
`perf_counter()` and reports a 60-second target.

## SCADE AI · Lab 2 — Transfer Learning summary export

`src/SCADE_AI_labs/lab2/lab2.ipynb` selects the best transfer-learning model
by validation PR-AUC. After selection, it displays `best_model.summary()` and
writes the same summary to `{best_model.name}.txt` with a `print_fn` callback.
The UTF-8 file is created in the kernel's working directory and replaced on
rerun; the current model name yields `resnet50_murmur_detection.txt`.
The separate model export uses `{best_model.name}.keras`.

## SCADE AI · Lab 2 — INT8 quantization

The notebook's `Quantization example` loads
`resnet50_murmur_detection_copy.keras` and creates a genuine
`resnet50_murmur_detection_copy_int8.keras` archive with `model.save()`.
The file is replaced on rerun in the kernel's working directory. The source
model remains unchanged. The saved model loads
with `keras.models.load_model` / `tf.keras.models.load_model`,
`compile=False`, without custom objects, and accepts the original float32
ResNet-preprocessed inputs. The `Test the saved models`
cell now loads this artifact into `int8_resnet50_model` and aliases it as
`model`, preserving the original prediction and reporting loop. The prior
pruned-model selection and generic loading statements remain commented.

Keras's native INT8 support covers Dense, but not Conv2D. With the default
`QUANTIZE_CONVOLUTIONS = True`, each convolution becomes a nested Functional
model: extract patches with the original kernel size, stride, dilation and
padding, then apply a Dense projection with its reshaped kernel, bias and
activation. Unit-stride 1x1 convolutions apply Dense directly to each pixel.
Other layers retain their original configuration and weights. This is an
algebraically equivalent float32 graph before quantization; the notebook
checks its outputs before calling `model.quantize("int8", filters=...)`.
The rewrite is for the ordinary channels-last convolutions in this model;
grouped convolutions, other data formats, or unequal dilation rates raise.

All six convolution kernels and both original Dense kernels are stored as
INT8. Setting `QUANTIZE_CONVOLUTIONS = False` instead preserves Conv2D layers
and quantizes just the original Dense kernels. Biases, scales, batch
normalization, residual additions, and model I/O remain float32. Keras
quantizes Dense inputs dynamically: no representative calibration set is
required. This is a mixed-precision Keras artifact, not a full integer-only
graph. The old TFLite example has been replaced entirely; renaming a TFLite
file never creates a Keras model.

The two code cells check eight validation images using `load_images(val_70,
shuffle=False).map(prepare_resnet_input)`, assert rewrite equivalence,
inspect actual kernel dtypes, and verify output equality after saving and
reloading. This is a smoke check, not a held-out accuracy/recall assessment.
Patch extraction can increase runtime memory and latency. Built-in Keras
serialization avoids custom Python layer dependencies, but downstream tools
must support the new graph operations and quantized Dense layers; Scade One
import/deployment is not validated by this example.

The testing dataset uses the original `load_images(test_70, shuffle=False)`
and `prepare_resnet_input` mapping: float32 grayscale normalized to [0, 1],
restored to the pixel range, replicated to RGB, then ResNet-preprocessed.
There is no manual INT8 input conversion or score dequantization for this
Keras model. Run the helper definitions and path/options first; if the saved
artifact exists, quantization need not be rerun. Testing uses threshold 0.5,
overwrites `resnet50_murmur_detection_copy_int8_test_predictions.txt`, and
appends the classification report/confusion matrix to
`resnet50_murmur_detection_copy_int8.txt` (created if missing). Other models'
reports are unaffected.

The adapted testing cell was executed on 2026-11-23 against all 1,279 real
test images: 1,047 Normal and 232 Murmur. The confusion matrix was
`[[970, 77], [110, 122]]` (rows true, columns predicted), accuracy about
85.4%, Murmur precision 61.3%, and Murmur recall 52.6% at threshold 0.5.
The score/report files were generated in the notebook directory; the saved
model was unchanged. This is a quantized-model evaluation, not a comparison
against the original float32 model.

## SCADE AI — Raspberry Pi WAV classification runtime

`src/SCADE_AI_labs/raspberry_pi/` contains a small configurable pipeline
for the 1 GB Pi 3 B on 64-bit Raspberry Pi OS. It selects only Lab 2 models
and executes their generated C through a PyScadeOne-style proxy. The 16
model profiles were checked against the actual `.keras` archive metadata:
all expect float32 64x64 HWC input and one sigmoid output, with one channel
for ordinary CNNs and three for the ResNet variants. The runtime does not
load these archives or benchmark Keras.

The modules are `config.py` (hardcoded WAV path, selected model, threshold,
shape/preprocessing/proxy settings), `preprocessing.py` (soundfile float32
WAV decode/native sample rate/mono mix, 11th-order 600 Hz causal Butterworth,
STFT, training-style plot and model tensor), `inference.py` (proxy import,
construction/reset, HWC ctypes transfer, one cycle and score), and `run.py`
(sequencing, classification, stage timing, total timing and peak RSS).
`check_pipeline.py` is a plain local smoke-check script using synthetic
audio and a temporary Python proxy stub. The README documents installation,
configuration, pending generated artifacts and measurement commands.

SciPy second-order sections implement the same Butterworth transfer
function while avoiding the direct polynomial form's high-sample-rate
numerical instability. The 600 Hz cutoff requires sample rate >1200 Hz;
there is no resampling, segmentation or truncation. The centered Hann STFT
uses 8192 FFT/window and hop 512, and amplitude dB relative to the recording
maximum with an 80 dB range. Small FFT batches reduce complex temporary
allocations; Matplotlib only constructs a mesh for visible frequency bins.
The complete audio and dB matrix still scale with recording length/rate.

Training-image appearance matters: preserve the 600x400 magma plot,
time/frequency axes, title, colorbar, tight layout and 0–1000 Hz range. The
notebook's invalid three-item `figsize` is expressed as 6x4 inches at 100
dpi. Rendering stays in memory. Integer PNG-style grayscale conversion
and half-pixel bilinear resizing reproduce Lab 2's input preparation
without TensorFlow/librosa. Ordinary CNNs receive grayscale/255; ResNet
variants receive replicated grayscale*255 with BGR means subtracted. The
native Keras INT8 variant also has float32 input/output. Pixel agreement
can depend on the Matplotlib/fonts/software environment.

The adapter mirrors the Lab 1 tutorial's `reset()`/`cycle()` API. It copies
one contiguous float32 HWC tensor into a ctypes array with no batch
dimension. A worker thread has a per-profile initial 64 MiB stack; this is
configurable and not a measured native-stack requirement. Model scores
must be finite in [0,1]; scores >= configurable threshold (default 0.5)
produce Murmur=1, lower scores Normal=0.

Later artifacts go under `generated/<model-name>/`. Exact proxy module,
operator and input/output names are intentionally placeholders until the
files arrive. Native libraries/loaders must support Linux ARM64; Windows
DLLs and x86 binaries cannot simply be copied to the Pi. Generated code
and loaders were neither authored nor modified. Importer support for the
quantized graph is not assumed. The Ansys generator package is not imported
by this runtime; actual proxy dependencies remain to be inspected.

`run.py` starts its timer before scientific-library imports and includes
file read, filter, STFT/render, resizing/normalization, wrapper/library load,
operator reset, thread setup, input copy and inference. It ends after label
calculation, before reporting and shutdown. Its target is a measurement,
not an enforced timeout. Use `/usr/bin/time -v python3 run.py` for complete
process wall time, including interpreter startup, printing and shutdown,
and independent peak RSS. Run fresh processes on the actual Pi and SD
card, recording first-run font-cache costs and subsequent variation. No
local laptop measurements establish the Pi target or RAM fit. Real model
inference, ARM64 deployment and the 60-second target remain pending.
