# -*- coding: utf-8 -*-
"""Import of Keras Models (.h5 / .keras files or models) into Scade One

Example of command line:
-----------------------
python s1_keras_importer.py "../Examples/lenet/trained_lenet.h5" -o "app_model" --copy-keras

Note: option "--copy-keras" will copy the keras lib to create a standalone project

"""
# MIT License
#
# Copyright (c) 2024 ANSYS, Inc. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional, Union

# disable display of info and warning messages of tensorflow
# ... and because we have code in the middle of imports:
# pylint: disable=import-error, wrong-import-position
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
logging.getLogger("tensorflow").setLevel(logging.ERROR)

import numpy as np  # type: ignore  # noqa

from keras import Model  # type: ignore # noqa
from keras_importer import ModelCreator  # type: ignore # noqa
from keras_importer.utils import improve_array_pprint  # pylint: disable=unused-import # noqa

# Check version of Python (compatibility with TensorFlow: https://www.tensorflow.org/install)
assert (3, 9) <= sys.version_info < (3, 13), "Requires Python 3.9 to 3.12"

ModelOrPath = Union[Model, Path, str]
PathStr = Union[Path, str]


S1_IMPORTER_VERSION = "0.2-beta"

KERAS_LIB = Path(__file__).parent.parent / "keras"


def import_keras_in_s1(
    model: ModelOrPath,
    root: PathStr,
    clean_first: bool = True,
    copy_keras_lib: bool = True,
    tests_inputs: Optional[list[np.ndarray]] = None,
):
    """Import a Keras Model into a Scade One Project

    Args:
        model: Keras Model or path to a Keras Model (.h5 or .keras)
        root: Path to the Scade One project folder or .sproj file
        clean_first: If True, delete the project folder if it exists (default: True)
        copy_keras_lib: If True, copy the Keras library to the project (default: True)
        tests_inputs: List of inputs for the test harness (default: None)
    """
    creator = ModelCreator(
        model,
        sproj_or_outdir=root,
        keras_lib_path=KERAS_LIB,
        copy_keras_lib=copy_keras_lib,
        exists_ok=clean_first,
        importer_version=S1_IMPORTER_VERSION,
    )
    creator.create_module()
    if tests_inputs:
        creator.create_test_harness(tests_inputs)
    creator.write()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scade One Keras Importer.")
    parser.add_argument("h5", type=Path, help="h5 file")
    parser.add_argument(
        "-o",
        "--outdir",
        type=Path,
        default=None,
        help="Output folder for created Scade One project",
    )
    parser.add_argument(
        "-c",
        "--copy-keras-lib",
        action="store_true",
        help="Copy the keras library (default: False)",
    )
    parser.add_argument(
        "-a",
        "--append",
        action="store_true",
        help="Append data instead of creating project from scratch (default: False)",
    )

    args = parser.parse_args()

    outdir = args.outdir if args.outdir else Path(f"imported__{args.h5.name}")

    print("Start creation")
    import_keras_in_s1(
        args.h5,
        root=outdir,
        copy_keras_lib=args.copy_keras_lib,
    )
    print(f"End creation (in {outdir.absolute()})")
