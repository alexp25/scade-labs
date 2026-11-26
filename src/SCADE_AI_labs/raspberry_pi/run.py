"""Run once: python3 run.py. Edit config.py first."""

from time import perf_counter

STARTED = perf_counter()  # Before importing NumPy, SciPy, Matplotlib or the proxy.


def main():
    import resource
    import sys

    import config
    from inference import classify, run_inference
    from preprocessing import (
        filter_recording, load_recording, prepare_model_input,
        render_spectrogram, spectrogram_db,
    )

    timings = {"Imports/configuration": perf_counter() - STARTED}
    model_config = config.MODELS[config.MODEL_NAME]

    started = perf_counter()
    samples, sample_rate = load_recording(config.RECORDING_PATH)
    duration = len(samples) / sample_rate
    timings["WAV loading"] = perf_counter() - started

    started = perf_counter()
    samples = filter_recording(samples, sample_rate)
    timings["Filtering"] = perf_counter() - started

    started = perf_counter()
    spectrum = spectrogram_db(samples)
    del samples
    rgb_image = render_spectrogram(spectrum, sample_rate)
    del spectrum
    timings["Spectrogram/plot"] = perf_counter() - started

    started = perf_counter()
    image = prepare_model_input(rgb_image, model_config)
    del rgb_image
    timings["Resize/normalization"] = perf_counter() - started

    started = perf_counter()
    prediction = run_inference(image, model_config)
    timings["Wrapper load/reset"] = prediction["model_loading"]
    timings["Input transfer/C inference"] = prediction["inference"]
    timings["Thread overhead"] = max(
        0, perf_counter() - started - prediction["model_loading"] - prediction["inference"]
    )
    label = classify(prediction["score"], config.THRESHOLD)
    total = perf_counter() - STARTED
    peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_mb = peak_rss / (1024 * 1024 if sys.platform == "darwin" else 1024)

    print(f"Result: {('Normal', 'Murmur')[label]} ({label})")
    print(f"Murmur score: {prediction['score']:.6f}; threshold: {config.THRESHOLD}")
    print(f"Model: {config.MODEL_NAME}")
    print(f"Recording: {duration:.2f} s, {sample_rate} Hz")
    for stage, seconds in timings.items():
        print(f"  {stage:<26} {seconds:8.3f} s")
    print(f"Total (imports through result): {total:.3f} s")
    print(f"{config.TIME_LIMIT_SECONDS:g}-second target: "
          f"{'PASS' if total <= config.TIME_LIMIT_SECONDS else 'FAIL'} "
          f"(limit {config.TIME_LIMIT_SECONDS:g} s)")
    print(f"Peak process RAM: {peak_mb:.1f} MiB")
    return label


if __name__ == "__main__":
    main()
