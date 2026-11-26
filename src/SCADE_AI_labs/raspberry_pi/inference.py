"""Small adapter for Lab 1's generated PyScadeOne proxy interface."""

import ctypes
import importlib
from pathlib import Path
import sys
import threading
from time import perf_counter

import numpy as np


def classify(score, threshold):
    """All selected Lab 2 models return one float32 sigmoid Murmur score."""
    if not np.isfinite(score) or not 0 <= score <= 1:
        raise ValueError(f"Expected a sigmoid score in [0, 1], got {score}.")
    return int(score >= threshold)


def run_inference(image, model_config):
    """Load, reset and cycle the generated operator in a larger-stack thread."""
    if image.shape != tuple(model_config["shape"]):
        raise ValueError(f"Expected {model_config['shape']}, got {image.shape}.")
    wrapper_dir = Path(model_config["wrapper_dir"])
    if not wrapper_dir.is_dir():
        raise FileNotFoundError(
            f"Generated wrapper folder is missing: {wrapper_dir}. "
            "Add the ARM64 wrapper/library and set its names in config.py."
        )
    result = {}

    def worker():
        try:
            started = perf_counter()
            sys.path.insert(0, str(wrapper_dir))
            try:
                module = importlib.import_module(model_config["wrapper_module"])
            finally:
                sys.path.pop(0)
            operator = getattr(module, model_config["operator_class"])()
            operator.reset()
            result["model_loading"] = perf_counter() - started

            started = perf_counter()
            height, width, channels = image.shape
            tensor_type = ctypes.c_float * channels * width * height
            tensor = tensor_type.from_buffer_copy(np.ascontiguousarray(image, dtype=np.float32))
            # A misspelled name must not silently leave the native input unset.
            getattr(operator.inputs, model_config["input_field"])
            setattr(operator.inputs, model_config["input_field"], tensor)
            operator.cycle()
            output = getattr(operator.outputs, model_config["output_field"])
            index = model_config["output_index"]
            result["score"] = float(output if index is None else output[index])
            result["inference"] = perf_counter() - started
        except Exception as error:
            result["error"] = error

    previous_size = threading.stack_size()
    try:
        threading.stack_size(model_config["stack_mb"] * 1024 * 1024)
        thread = threading.Thread(target=worker)
        thread.start()
    finally:
        threading.stack_size(previous_size)
    thread.join()
    if "error" in result:
        raise result["error"]
    return result
