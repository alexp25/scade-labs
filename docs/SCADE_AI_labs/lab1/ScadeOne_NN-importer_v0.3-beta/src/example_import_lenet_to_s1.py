# -*- coding: utf-8 -*-
"""Example of import of a trained Lenet with an test input from MNIST into Scade One

Unlike the main file, we use a Python function to perform the import.
This could be replicated for example on a Jupyter Notebook
"""
# MIT License
#
# Copyright (c) 2021 ANSYS, Inc. All rights reserved.
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

import logging
import os
from pathlib import Path

# disable display of info and warning messages of tensorflow
# ... and because we have code in the middle of imports:
# pylint: disable=import-error, wrong-import-position
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
logging.getLogger("tensorflow").setLevel(logging.ERROR)

# 1. We import Keras
from keras.datasets import mnist  # type: ignore  # noqa

from s1_keras_importer import import_keras_in_s1  # type: ignore  # noqa

# 2. We load the .h5 file corresponding to Lenet Model
LENET_H5 = Path(__file__).parent.parent / "Examples" / "lenet" / "trained_lenet.h5"
LENET_ABS = LENET_H5.parent.absolute()
assert LENET_H5.is_file(), f"File {LENET_H5.name} not found in '{LENET_ABS}'"

# 3. We load the data from MNIST (it will be automatically downloaded the first time)
_, (x_test, y_test) = mnist.load_data()


# 4. We get the FIRST input of MNIST (index=0) => this is a digit "7"
# Note: we need an input of size 28^28^1 for Lenet
# ... but MNIST is of size 28^28 so we need to reshape
# If you want to load other numbers, change the index: e.g. `x_test[0]` => `x_test[10]`
INPUT_MNIST = x_test[0].reshape(28, 28, 1)

# 5. We convert into a Scade One Model (in folder "lenet_s1")
print(f"...Importing Lenet model to Scade One ({LENET_H5})")
OUTPUT_DIR = "lenet_s1"
import_keras_in_s1(LENET_H5, OUTPUT_DIR, tests_inputs=[INPUT_MNIST])
print(f"=> Finished converting to Scade One (in folder {OUTPUT_DIR})")
