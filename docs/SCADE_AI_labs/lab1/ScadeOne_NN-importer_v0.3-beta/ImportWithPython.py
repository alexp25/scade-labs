#!/usr/bin/env python3
"""Import a trained Keras model and create the SCADE One Code Generation Job."""

import os
import shutil
import sys
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from ansys.scadeone.core import ScadeOne
from ansys.scadeone.core.job import CodeGenerationJob
from ansys.scadeone.importers.nn import ModelCreator


# ============================================================
# Importer and model paths
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent

MODEL_FILE = ROOT_DIR / "lenet.keras"
OUTPUT_DIR = ROOT_DIR / "lenetS1"
PROJECT_FILE = OUTPUT_DIR / "lenet.sproj"
KERAS_LIB = ROOT_DIR / "keras"


# ============================================================
# SCADE One installation
# ============================================================

SCADE_ONE_INSTALL_VALUE = os.environ.get(
    "SCADE_ONE_INSTALL"
)

if not SCADE_ONE_INSTALL_VALUE:
    raise EnvironmentError(
        "SCADE_ONE_INSTALL is not defined. "
        "Run install_global_AnyVersion.bat first, "
        "then restart Visual Studio Code."
    )

SCADE_ONE_INSTALL = Path(
    SCADE_ONE_INSTALL_VALUE
)

SCADE_ONE_CODE_GENERATOR = (
    SCADE_ONE_INSTALL
    / "tools"
    / "swan_cg.exe"
)


# ============================================================
# Code Generation Job configuration
# ============================================================

CODE_GENERATION_JOB = "JobLenet1"
INPUT_SWAN_FILE = "assets/lenet.swan"
ROOT_OPERATOR = "lenet::lenet"


# ============================================================
# Start from the importer folder
# ============================================================

os.chdir(ROOT_DIR)


# ============================================================
# Display configuration
# ============================================================

print("\n" + "=" * 79)
print("IMPORT THE TRAINED KERAS MODEL INTO SCADE ONE")
print("=" * 79)
print("Python:", sys.executable)
print("Importer directory:", ROOT_DIR)
print("Keras model:", MODEL_FILE)
print("Keras library:", KERAS_LIB)
print("Output directory:", OUTPUT_DIR)
print("Output project:", PROJECT_FILE)
print("SCADE One installation:", SCADE_ONE_INSTALL)
print("Code Generation Job:", CODE_GENERATION_JOB)
print("Input SWAN file:", INPUT_SWAN_FILE)
print("Root operator:", ROOT_OPERATOR)


# ============================================================
# Validate input files and product installation
# ============================================================

if sys.version_info[:2] != (3, 12):
    raise RuntimeError(
        "This script must be executed with Python 3.12. "
        "Use: py -3.12 .\\ImportWithPython.py"
    )

if not MODEL_FILE.is_file():
    raise FileNotFoundError(
        f"Trained Keras model not found: {MODEL_FILE}"
    )

if not KERAS_LIB.is_dir():
    raise FileNotFoundError(
        f"Keras SWAN library not found: {KERAS_LIB}"
    )

if not SCADE_ONE_INSTALL.is_dir():
    raise FileNotFoundError(
        f"SCADE One installation not found: {SCADE_ONE_INSTALL}"
    )

if not SCADE_ONE_CODE_GENERATOR.is_file():
    raise FileNotFoundError(
        "SCADE One code generator not found: "
        f"{SCADE_ONE_CODE_GENERATOR}"
    )


# ============================================================
# Remove the previously generated project
# ============================================================

if OUTPUT_DIR.exists():
    print(
        "\nRemoving existing generated project:",
        OUTPUT_DIR,
    )

    shutil.rmtree(OUTPUT_DIR)


# ============================================================
# Import the Keras model
# ============================================================

print("\nImporting the trained Keras model...")

creator = ModelCreator(
    MODEL_FILE,
    sproj_or_outdir=PROJECT_FILE,
    keras_lib_path=KERAS_LIB,
    copy_keras_lib=True,
    exists_ok=True,
    importer_version="0.2.1",
)

creator.create_module()
creator.write(auto_layout=False)


# ============================================================
# Validate the generated SCADE One project
# ============================================================

CONSTANTS_FILE = (
    OUTPUT_DIR
    / "resources"
    / "constants.c"
)

MATH_IMPLEMENTATION_FILE = (
    OUTPUT_DIR
    / "keras_lib"
    / "resources"
    / "math_imported.c"
)

if not PROJECT_FILE.is_file():
    raise RuntimeError(
        "The SCADE One project was not generated."
    )

if not CONSTANTS_FILE.is_file():
    raise RuntimeError(
        "The neural-network constants file was not generated."
    )

if not MATH_IMPLEMENTATION_FILE.is_file():
    raise RuntimeError(
        "The imported mathematical implementation was not copied."
    )

print("Keras model imported successfully.")


# ============================================================
# Create the Code Generation Job
# ============================================================

print("\nCreating the Code Generation Job...")

with ScadeOne(
    install_dir=SCADE_ONE_INSTALL
) as application:

    project = application.load_project(
        PROJECT_FILE
    )

    if project is None:
        raise RuntimeError(
            "The SCADE One project could not be loaded: "
            f"{PROJECT_FILE}"
        )

    project.load_jobs()

    existing_job = project.get_job(
        CODE_GENERATION_JOB
    )

    if existing_job is not None:
        print(
            "Code Generation Job already exists:",
            existing_job.name,
        )

    else:
        job = CodeGenerationJob(
            name=CODE_GENERATION_JOB,
            sproj=project,
        )

        job.input_paths = [
            INPUT_SWAN_FILE
        ]

        job.root_declarations = [
            ROOT_OPERATOR
        ]

        job.custom_arguments = ""
        job.expansion = None
        job.expansion_exp = ""
        job.expansion_no_exp = ""
        job.name_length = 255
        job.keep_assume = False
        job.globals_prefix = ""
        job.use_macros = False
        job.static_locals = False
        job.max_function_parameters = None
        job.with_probes = False

        job.save()

        print(
            "Code Generation Job saved successfully."
        )


# ============================================================
# Display and verify the import result
# ============================================================

print("\n" + "=" * 79)
print("IMPORT RESULT")
print("=" * 79)
print(
    "Project file exists:",
    PROJECT_FILE.is_file(),
)
print(
    "Constants file exists:",
    CONSTANTS_FILE.is_file(),
)
print(
    "Keras library copied:",
    (OUTPUT_DIR / "keras_lib").is_dir(),
)
print(
    "Mathematical implementation exists:",
    MATH_IMPLEMENTATION_FILE.is_file(),
)


# ============================================================
# Reopen the project and verify the saved job
# ============================================================

with ScadeOne(
    install_dir=SCADE_ONE_INSTALL
) as application:

    project = application.load_project(
        PROJECT_FILE
    )

    if project is None:
        raise RuntimeError(
            "The generated project could not be reopened."
        )

    project.load_jobs()

    created_job = project.get_job(
        CODE_GENERATION_JOB
    )

    if created_job is None:
        raise RuntimeError(
            "The Code Generation Job was not created: "
            f"{CODE_GENERATION_JOB}"
        )

    print("Code Generation Job exists: True")
    print("Job name:", created_job.name)
    print("Job type:", created_job._kind)
    print("Input paths:", created_job.input_paths)
    print(
        "Root declarations:",
        created_job.root_declarations,
    )


print("\nImportation completed successfully.")