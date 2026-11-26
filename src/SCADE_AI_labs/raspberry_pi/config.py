"""Edit this file to choose the recording and generated Lab 2 model."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RECORDING_PATH = Path("/home/pi/heart_sounds/recording.wav")
MODEL_NAME = "70_10_20_cnn_2_blocks"
THRESHOLD = 0.5  # Score >= threshold means Murmur (1); otherwise Normal (0).
TIME_LIMIT_SECONDS = 60.0

# These are the actual .keras model names in ../lab2/. No .keras file is
# loaded on the Pi. Each name identifies its separately generated C model.
MODEL_NAMES = (
    "70_10_20_cnn_2_blocks",
    "70_10_20_cnn_3_blocks",
    "70_10_20_cnn_4_blocks",
    "85_5_10_cnn_2_blocks",
    "85_5_10_cnn_3_blocks",
    "85_5_10_cnn_4_blocks",
    "90_5_5_cnn_2_blocks",
    "90_5_5_cnn_3_blocks",
    "90_5_5_cnn_4_blocks",
    "70_10_20_KT_cnn_5_convs",
    "70_10_20_KT_cnn_6_convs",
    "70_10_20_KT_cnn_7_convs",
    "resnet50_murmur_detection",
    "resnet50_murmur_detection_copy",
    "resnet50_murmur_detection_copy_pruned",
    "resnet50_murmur_detection_copy_int8",
)

MODELS = {}
for name in MODEL_NAMES:
    is_resnet = name.startswith("resnet50_")
    MODELS[name] = {
        "shape": (64, 64, 3 if is_resnet else 1),  # height, width, channels
        "preprocessing": "resnet" if is_resnet else "grayscale",
        "wrapper_dir": BASE_DIR / "generated" / name,
        "wrapper_module": "model_wrapper",  # module filename without .py
        "operator_class": "ROOT_OPERATOR",  # replace using the generated proxy
        "input_field": "INPUT_FIELD",       # model.inputs.<name>
        "output_field": "OUTPUT_FIELD",     # model.outputs.<name>
        "output_index": 0,  # use None if the wrapper returns a scalar
        "stack_mb": 64,  # native CNN stack; tune after inspecting generated C
    }

# Set the actual wrapper names for each model here once files are available:
# MODELS["70_10_20_cnn_2_blocks"].update({
#     "wrapper_module": "cnn_wrapper",
#     "operator_class": "cnn_Model",
#     "input_field": "image",
#     "output_field": "score",
# })
