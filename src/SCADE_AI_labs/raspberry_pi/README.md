# Raspberry Pi heart-sound classifier

Loads one WAV from the SD card, filters it, makes the training-style
spectrogram, resizes it for a Lab 2 model, and runs its generated C code
through a PyScadeOne proxy. The result is **Normal (0)** or **Murmur (1)**.

The generated model files have not been supplied yet. Audio preprocessing
and the proxy adapter are implemented; real inference and the Raspberry Pi
60-second target remain to be tested. No TensorFlow, Keras, librosa, training,
or laptop benchmark runs on the Pi.

## Files

| File | Purpose |
| --- | --- |
| `config.py` | Hardcoded WAV path, selected model, threshold, proxy settings |
| `preprocessing.py` | WAV loading, filtering, STFT, plot, resize, normalization |
| `inference.py` | Generated proxy loading, reset/cycle, score classification |
| `run.py` | Runs one recording and reports result, timings and peak RAM |
| `check_pipeline.py` | Local smoke checks using synthetic audio and a stub proxy |

## Install on 64-bit Raspberry Pi OS

The OS packages provide ARM64 builds without compiling scientific libraries
on the 1 GB Pi:

```sh
sudo apt update
sudo apt install python3-venv python3-numpy python3-scipy python3-matplotlib python3-soundfile time
cd /path/to/scade-labs/src/SCADE_AI_labs/raspberry_pi
python3 -m venv --system-site-packages .venv
. .venv/bin/activate
```

For another environment with suitable binary wheels, use
`python -m pip install -r requirements.txt` in its virtual environment.
Package versions and OS installation commands have not been tested on a Pi.

## Configure the recording and model

Edit `config.py`:

```python
RECORDING_PATH = Path("/home/pi/heart_sounds/recording.wav")
MODEL_NAME = "70_10_20_cnn_2_blocks"
THRESHOLD = 0.5
```

`MODEL_NAMES` lists all 16 `.keras` model names currently in `../lab2/`.
Select one by name; the appropriate grayscale or ResNet input preparation
is selected with it. All currently use 64×64 inputs. Each `MODELS` entry
has its own shape and generated-proxy settings, which you can override
using the example at the end of `config.py`.

The WAV is read in full, kept at its original sample rate, converted to
float32, and mixed to mono when needed. Nothing is trimmed, segmented, or
resampled. The 600 Hz cutoff requires a sample rate **above 1200 Hz**.

## Add the generated C model later

For the selected model, place the complete generated proxy and its native
library together under:

```text
generated/
  70_10_20_cnn_2_blocks/
    <actual_proxy_module>.py
    <native ARM64 Linux library and any required companion files>
```

Set `wrapper_module`, `operator_class`, `input_field`, and `output_field`
using the **actual generated proxy**, rather than guessing layer names.
`output_index=0` selects the notebook's one-element score array; set it to
`None` for a scalar output. These settings are currently placeholders.

The adapter follows the [Lab 1 tutorial](https://alexp25.github.io/scade-labs/SCADE_AI_labs/lab1/):
construct the root operator, call `reset()`, copy a contiguous float32 HWC
image into a `ctypes.c_float * channels * width * height` tensor, assign
`inputs.<field>`, call `cycle()`, and read `outputs.<field>[0]`.
The [PyScadeOne proxy documentation](https://scadeone.docs.pyansys.com/version/stable/api/svc/pywrapper.html)
describes this interface.

The library and its loader must work on **Linux ARM64**. A Windows DLL or
an x86 library cannot execute on this Pi. Build/loader adjustments depend
on the generated files and are intentionally left until those files arrive;
no platform compatibility is assumed. Keep generated files unchanged here.
The Pi executes the already-built model; wrapper generation happens on the
development machine. The supplied adapter itself needs no Ansys Python
package at runtime; additional needs of the actual proxy must be checked.

Inference runs in a worker thread with a configurable 64 MiB stack, since
the Lab 1 example needs a larger native stack. This is an initial setting,
not a measured requirement. Tune `stack_mb` for the generated model; the
entire process, native work buffers, and OS must fit within the Pi's RAM.
The INT8 model's input is still float32. A profile for it does not establish
that Scade One supports all operations in its rewritten/quantized graph.

## Preprocessing follows the notebooks

1. Causal 11th-order Butterworth low-pass at 600 Hz. Second-order sections
   implement the same filter more stably at high sample rates than the
   notebook's direct polynomial coefficients.
2. Hann STFT: FFT/window 8192, hop 512, centered zero padding; relative
   amplitude in dB with an 80 dB range.
3. The 600×400 spectrogram plot retains the magma colors, time/frequency
   axes, title, colorbar, and 0–1000 Hz visible range from Lab 1. Its invalid
   `figsize=(600, 400, "px")` expression is implemented as 6×4 inches at
   100 dpi. The image stays in memory; intermediate WAVs/PNGs are not
   written to the SD card. Plot styling assumes Matplotlib defaults.
4. PNG-style grayscale conversion precedes bilinear resize. A small NumPy
   implementation matches the [TensorFlow resize](https://www.tensorflow.org/api_docs/python/tf/image/resize)
   used by Lab 2 without importing TensorFlow. Its integer grayscale
   conversion follows [TensorFlow's PNG decoder](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/core/lib/png/png_io.cc).
5. CNNs receive `(64, 64, 1)` float32 pixels divided by 255. ResNet variants
   receive `(64, 64, 3)` float32, using replicated grayscale pixels at the
   0–255 scale and subtracting BGR means `[103.939, 116.779, 123.68]`.
   There is no manual INT8 input casting.
6. A sigmoid score **>= threshold** means Murmur (1); otherwise Normal (0).

FFT batches limit temporary allocations, and only visible frequency bins
enter Matplotlib's mesh. The whole WAV and dB matrix still occupy memory
proportional to recording length/sample rate; there is no fixed RAM or
latency guarantee for arbitrarily large recordings. Plot/fonts/library
versions can affect pixels; compare against the actual training images
when moving to a different software environment.

## Run and measure

```sh
python3 run.py
/usr/bin/time -v python3 run.py
```

The script prints the class, raw Murmur score, selected model, audio
duration, time for each stage, total elapsed time, a 60-second PASS/FAIL,
and peak process RAM in MiB. Each invocation loads the model once and makes
one prediction. Run a fresh process for each model/recording.

The internal total begins before scientific-library imports and includes
WAV loading, filtering, STFT/rendering, resizing/normalization, proxy/native
library loading, reset, thread setup, tensor copying, and C inference.
It ends when the class has been determined. It measures the target without
aborting a slow inference. It excludes interpreter startup and final output/
shutdown; `/usr/bin/time -v` provides the **complete process wall time** and
independent peak-RAM measurement. Use that wall time for the full one-minute
decision. Run it on the actual Pi with the actual SD card and library.

The first run can also create Matplotlib's font cache. Record it and repeat
fresh-process runs to see variation, rather than discarding the slower run.
No timing measured on a laptop establishes Pi performance.

## Local checks

```sh
python3 check_pipeline.py
```

These check audio formats, mono conversion, filter agreement, spectrogram
and tensor shapes, normalization, labels/threshold, HWC proxy transfer,
thread error propagation, and runner reporting. A temporary **stub** stands
in for the missing proxy. It does not validate generated C inference,
classification accuracy, ARM64 deployment, or the Pi performance target.
