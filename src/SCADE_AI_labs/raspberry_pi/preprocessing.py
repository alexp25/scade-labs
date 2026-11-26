"""Notebook-style audio and image preparation, without TensorFlow or librosa."""

import numpy as np
import soundfile as sf
from scipy import fft, signal
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter, MaxNLocator

N_FFT = 8192
HOP_LENGTH = 512


def load_recording(path):
    """Read the whole WAV as float32, keeping its sample rate; mix to mono."""
    samples, sample_rate = sf.read(path, dtype="float32", always_2d=True)
    samples = samples.mean(axis=1)
    if samples.size == 0 or not np.isfinite(samples).all():
        raise ValueError("The recording must contain finite audio samples.")
    return samples, sample_rate


def filter_recording(samples, sample_rate):
    """Lab 1's causal 11th-order, 600 Hz Butterworth low-pass filter."""
    if sample_rate <= 1200:
        raise ValueError("The 600 Hz filter needs a sample rate above 1200 Hz.")
    # Second-order sections keep the same filter stable at high sample rates.
    sections = signal.butter(11, 600, fs=sample_rate, btype="low", output="sos")
    return signal.sosfilt(sections, samples).astype(np.float32)


def spectrogram_db(samples):
    """Centered Hann STFT, relative amplitude dB, clipped to an 80 dB range."""
    padded = np.pad(samples, (N_FFT // 2, N_FFT // 2))
    frames = np.lib.stride_tricks.sliding_window_view(padded, N_FFT)[::HOP_LENGTH]
    window = signal.get_window("hann", N_FFT)
    spectrum = np.empty((N_FFT // 2 + 1, len(frames)), dtype=np.float32)
    # Small FFT batches avoid allocating a complex STFT for the entire WAV.
    for start in range(0, len(frames), 32):
        transformed = fft.rfft(frames[start:start + 32] * window, axis=1)
        spectrum[:, start:start + 32] = np.abs(transformed.astype(np.complex64)).T

    # amplitude_to_db computes 10*log10(amplitude**2), including this floor.
    reference = np.maximum(np.float32(1e-10), np.square(spectrum.max()))
    np.square(spectrum, out=spectrum)
    np.maximum(spectrum, 1e-10, out=spectrum)
    np.log10(spectrum, out=spectrum)
    spectrum *= 10
    spectrum -= 10 * np.log10(reference)
    np.maximum(spectrum, spectrum.max() - 80, out=spectrum)
    return spectrum


def render_spectrogram(spectrum, sample_rate):
    """Keep the training plot: 600x400 RGB pixels, axes, title and colorbar."""
    frequencies = fft.rfftfreq(N_FFT, d=1 / sample_rate)
    times = np.arange(spectrum.shape[1]) * HOP_LENGTH / sample_rate
    # Only visible frequencies enter Matplotlib's mesh, saving substantial RAM.
    rows = min(len(frequencies), np.searchsorted(frequencies, 1000) + 2)
    figure = Figure(figsize=(6, 4), dpi=100)
    canvas = FigureCanvasAgg(figure)
    axes = figure.add_subplot()
    mesh = axes.pcolormesh(
        times, frequencies[:rows], spectrum[:rows], cmap="magma",
        shading="auto", rasterized=True, edgecolors="None",
        vmin=float(spectrum.min()), vmax=float(spectrum.max()),
    )
    # Lab 1 calls tight_layout before restricting the visible frequency range.
    axes.set_ylim(-sample_rate / N_FFT / 2, sample_rate / 2 + sample_rate / N_FFT / 2)
    axes.set(xlabel="Time", ylabel="Hz", title="Spectrogram")
    axes.xaxis.set_major_locator(MaxNLocator(steps=[1, 1.5, 5, 6, 10]))

    def format_time(value, position):
        lower, upper = axes.get_xlim()
        duration = upper - lower
        if duration > 3600:
            return f"{int(value / 3600)}:{int(value / 60) % 60:02d}:{int(value) % 60:02d}"
        if duration > 60:
            return f"{int(value / 60)}:{int(value) % 60:02d}"
        return f"{value:.2g}" if duration >= 1 else f"{value:.3f}"

    axes.xaxis.set_major_formatter(FuncFormatter(format_time))
    figure.colorbar(mesh, ax=axes, format="%+2.0f dB")
    figure.tight_layout()
    axes.set_ylim(0, 1000)
    canvas.draw()
    image = np.asarray(canvas.buffer_rgba())[:, :, :3].copy()
    figure.clear()
    return image


def resize_bilinear(image, size):
    """TensorFlow-style bilinear resize: half-pixel centers, no antialiasing."""
    height, width = size
    y = (np.arange(height, dtype=np.float32) + 0.5) * (image.shape[0] / height) - 0.5
    x = (np.arange(width, dtype=np.float32) + 0.5) * (image.shape[1] / width) - 0.5
    y = np.clip(y, 0, image.shape[0] - 1)
    x = np.clip(x, 0, image.shape[1] - 1)
    y0, x0 = y.astype(int), x.astype(int)
    y1 = np.minimum(y0 + 1, image.shape[0] - 1)
    x1 = np.minimum(x0 + 1, image.shape[1] - 1)
    wy, wx = (y - y0).astype(np.float32)[:, None], (x - x0).astype(np.float32)[None, :]
    top = image[y0[:, None], x0].astype(np.float32)
    top += (image[y0[:, None], x1] - top) * wx
    bottom = image[y1[:, None], x0].astype(np.float32)
    bottom += (image[y1[:, None], x1] - bottom) * wx
    return top + (bottom - top) * wy


def prepare_model_input(rgb_image, model_config):
    """Match Lab 2's PNG grayscale decoding, resizing and model normalization."""
    # libpng's integer BT.601 conversion, as used by TensorFlow decode_png.
    rgb = rgb_image.astype(np.uint32)
    gray = ((rgb[..., 0] * 9797 + rgb[..., 1] * 19234 + rgb[..., 2] * 3737) >> 15)
    gray = resize_bilinear(gray, model_config["shape"][:2]) / np.float32(255)
    if model_config["preprocessing"] == "resnet":
        # prepare_resnet_input: grayscale [0,1] -> RGB [0,255] -> BGR means.
        image = np.repeat((gray * np.float32(255))[..., None], 3, axis=2)
        image -= np.array([103.939, 116.779, 123.68], dtype=np.float32)
    else:
        image = gray[..., None]
    return np.ascontiguousarray(image, dtype=np.float32)
