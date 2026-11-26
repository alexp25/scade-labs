"""Local smoke checks, using synthetic audio and a stub proxy, not a real CNN."""

import contextlib
import io
from pathlib import Path
import sys
import tempfile

import numpy as np
import soundfile as sf
from scipy import signal

import config
from inference import classify, run_inference
from preprocessing import (
    filter_recording, load_recording, prepare_model_input,
    render_spectrogram, spectrogram_db,
)


def main():
    sample_rate = 4000
    time = np.arange(sample_rate * 2) / sample_rate
    samples = (0.2 * np.sin(2 * np.pi * 100 * time)
               + 0.1 * np.sin(2 * np.pi * 1400 * time)).astype(np.float32)
    with tempfile.TemporaryDirectory() as folder:
        folder = Path(folder)
        wav_path = folder / "recording.wav"
        for subtype in ("PCM_16", "PCM_24", "FLOAT"):
            sf.write(wav_path, np.column_stack([samples, samples / 2]), sample_rate, subtype=subtype)
            mono, rate = load_recording(wav_path)
            assert rate == sample_rate and mono.dtype == np.float32
            np.testing.assert_allclose(mono, samples * 0.75, atol=4e-5)
        print("PASS: WAV PCM16/PCM24/float, stereo-to-mono, original sample rate")

        filtered = filter_recording(mono, rate)
        b, a = signal.butter(11, 600 / (rate / 2), btype="low")
        notebook_filtered = signal.lfilter(b, a, mono).astype(np.float32)
        np.testing.assert_allclose(filtered, notebook_filtered, rtol=1e-5, atol=1e-7)
        for rate in (2000, 44100, 48000):
            assert np.isfinite(filter_recording(samples, rate)).all()
        print("PASS: notebook filter agreement at 4 kHz; stable at 2/44.1/48 kHz")

        spectrum = spectrogram_db(filtered)
        assert spectrum.shape == (4097, 1 + len(filtered) // 512)
        assert np.isfinite(spectrum).all() and spectrum.min() >= -80.001
        np.testing.assert_allclose(spectrogram_db(np.zeros(100, dtype=np.float32)), 0)
        rgb = render_spectrogram(spectrum, sample_rate)
        assert rgb.shape == (400, 600, 3) and rgb.dtype == np.uint8
        cnn = prepare_model_input(rgb, config.MODELS["70_10_20_cnn_2_blocks"])
        resnet = prepare_model_input(rgb, config.MODELS["resnet50_murmur_detection_copy_int8"])
        assert cnn.shape == (64, 64, 1) and cnn.dtype == np.float32
        assert cnn.flags.c_contiguous and 0 <= cnn.min() <= cnn.max() <= 1
        assert resnet.shape == (64, 64, 3) and resnet.dtype == np.float32
        np.testing.assert_allclose(resnet, cnn * 255 - [103.939, 116.779, 123.68], atol=1e-5)
        print("PASS: spectrogram, silence, plot size, CNN/ResNet float32 tensors")

        # This temporary proxy only checks the adapter API and HWC memory order.
        # It performs no native inference and says nothing about model accuracy.
        module_name = "pipeline_check_proxy"
        (folder / f"{module_name}.py").write_text(
            "from types import SimpleNamespace\n"
            "class Operator:\n"
            "    def __init__(self):\n"
            "        self.inputs = SimpleNamespace(image=None)\n"
            "        self.outputs = SimpleNamespace(score=[0.0])\n"
            "        self.ready = False\n"
            "    def reset(self):\n"
            "        self.ready = True\n"
            "    def cycle(self):\n"
            "        assert self.ready\n"
            "        image = self.inputs.image\n"
            "        assert image[1][2][0] == 0.75\n"
            "        assert image[1][2][1] == 0.25\n"
            "        assert image[1][2][2] == 0.5\n"
            "        self.outputs.score[0] = image[1][2][0]\n",
            encoding="utf-8",
        )
        profile = dict(config.MODELS["resnet50_murmur_detection"],
                       wrapper_dir=folder, wrapper_module=module_name,
                       operator_class="Operator", input_field="image", output_field="score")
        image = np.zeros(profile["shape"], dtype=np.float32)
        image[1, 2] = [0.75, 0.25, 0.5]
        result = run_inference(image, profile)
        assert result["score"] == 0.75
        assert classify(result["score"], 0.5) == 1
        assert [classify(score, 0.5) for score in (0, 0.499, 0.5, 1)] == [0, 0, 1, 1]
        for bad in (float("nan"), float("inf"), -0.1, 1.1):
            try:
                classify(bad, 0.5)
            except ValueError:
                pass
            else:
                raise AssertionError("Invalid sigmoid score accepted")
        try:
            run_inference(image, dict(profile, input_field="wrong_name"))
        except AttributeError:
            pass
        else:
            raise AssertionError("Worker error did not propagate")
        print("PASS: stub proxy reset/cycle, HWC transfer, labels, worker errors")

        # Exercise reporting with the real audio/image pipeline and a stub score.
        import run
        original_path = config.RECORDING_PATH
        original_profile = config.MODELS[config.MODEL_NAME]
        original_inference = sys.modules["inference"].run_inference
        try:
            config.RECORDING_PATH = wav_path
            config.MODELS[config.MODEL_NAME] = profile
            sys.modules["inference"].run_inference = lambda image, model: {
                "score": 0.75, "model_loading": 0.001, "inference": 0.001,
            }
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                assert run.main() == 1
            report = output.getvalue()
            for text in ("Result: Murmur (1)", "Total (imports through result):", "Peak process RAM:"):
                assert text in report
        finally:
            config.RECORDING_PATH = original_path
            config.MODELS[config.MODEL_NAME] = original_profile
            sys.modules["inference"].run_inference = original_inference
            sys.modules.pop(module_name, None)
        assert not any(name in sys.modules for name in ("tensorflow", "keras", "librosa", "numba"))
        print("PASS: integrated runner/report with stub inference; no training libraries imported")
    print("ALL CHECKS PASSED (synthetic audio/stub proxy; real C and Pi timing unverified)")


if __name__ == "__main__":
    main()
