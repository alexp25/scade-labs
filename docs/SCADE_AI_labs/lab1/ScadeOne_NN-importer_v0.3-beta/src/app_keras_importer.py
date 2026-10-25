"""Streamlit app to visualize/experiment Keras Importer"""

# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2025 ANSYS, Inc. All rights reserved.
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

# pylint: disable=import-error

import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, Optional, Union, cast

import numpy as np  # type: ignore
import pygments
import streamlit as st
from ansys.scadeone.core import swan
from ansys.scadeone.core.svc.swan_printer import swan_to_str
from keras import Model  # type: ignore
from keras.models import load_model, model_from_json  # type: ignore
from keras.utils import model_to_dot  # type: ignore

from ansys.scadeone.importers.nn import ModelCreator, scan_for_auto_layout  # type: ignore
from ansys.scadeone.importers.nn.utils import improve_array_pprint # pylint: disable=unused-import # noqa: F401

assert sys.version_info >= (3, 8), "Requires Python 3.8 or above"

st.set_page_config("Keras Importer", page_icon="🦢", layout="wide")
st.title("Keras Importer")


ModelFunc = Callable[[], str]
ModelStrPath = Union[Model, str, Path]


def get_model_from_file(placeholder) -> Model:
    """Custom h5 provided by the user"""
    file = placeholder.file_uploader(
        "Upload a custom .h5/.keras/.json file", type=("h5", "keras", "json")
    )
    if file is None:
        st.warning(
            "Drag & Drop a **.h5/.keras/.json** file to the side bar to load a model"
        )
        st.stop()

    model_path = Path(file.name)
    if model_path.suffix == ".json":
        return cast(Model, model_from_json(model_path.read_text(encoding="utf-8")))

    with TemporaryDirectory() as tmp:
        model_path = Path(tmp) / model_path
        model_path.write_bytes(file.getbuffer().tobytes())  # type: ignore
        model_from_file = cast(Model, load_model(model_path, compile=False))

    return model_from_file


st.sidebar.write("***Configuration***")
COPY_KERAS_LIB = st.sidebar.checkbox("Copy Keras Lib in project", value=True)
DEBUG_MODE = st.sidebar.checkbox("Debug Mode", value=False)
SHOW_GRAPH_SIDEBAR = st.sidebar.checkbox("Show Keras Graph in Sidebar", value=False)


@st.cache_data(show_spinner="Searching for all AutoLayout exe in your disk")
def get_auto_layout() -> Optional[Path]:
    """Get AutoLayout exe, if any found among S1 Installations"""
    return scan_for_auto_layout()


auto_layout_exe = get_auto_layout()
auto_layout = st.sidebar.checkbox("AutoLayout", value=True)
if auto_layout:
    if not auto_layout_exe:
        st.sidebar.warning("No AutoLayout exe found!")
    else:
        st.sidebar.caption(f"**Path to AutoLayout**: {auto_layout_exe.as_posix()}")

st.sidebar.write("***Model***")
USE_LENET_EXAMPLE = st.sidebar.checkbox(
    "Example of Trained Lenet for MNIST🔢", value=False
)


@st.cache_data(show_spinner="Load MNIST Data")
def _get_mnist_test() -> tuple[list[np.ndarray], list[np.ndarray]]:
    """Get input array from MNIST"""
    # pylint: disable=import-outside-toplevel
    from keras.datasets import mnist  # type: ignore

    _, (x_test, y_test) = mnist.load_data()
    return x_test, y_test


@st.cache_data
def get_mnist_input(idx: int) -> tuple[np.ndarray, int]:
    """Get input from MNIST at a given index"""
    x_test, y_test = _get_mnist_test()
    return x_test[idx].reshape(28, 28, 1), y_test[idx]  # type: ignore


model_placeholder = st.sidebar.empty()
OUTPUT_DIR = st.sidebar.text_input("output folder", value="app_model")

MODEL: ModelStrPath
INPUT_TEST: Optional[list[np.ndarray]] = None
if USE_LENET_EXAMPLE:
    MODEL = Path(__file__).parent.parent / "Examples/lenet/trained_lenet.h5"
    with model_placeholder.container():
        st.caption(f"**Loaded model**: {Path(MODEL).resolve().absolute().as_posix()}")
        if st.checkbox("Use Test data from MNIST"):
            idx_mnist = st.number_input(
                "Index of MNIST Test Input", min_value=0, max_value=9999, value=0
            )
            _mnist_input, _mnist_output = get_mnist_input(int(idx_mnist))
            INPUT_TEST = [_mnist_input]
            st.caption(f"Expecting digit: {_mnist_output}")
else:
    MODEL = get_model_from_file(model_placeholder)

CREATOR = ModelCreator(
    MODEL,
    sproj_or_outdir=Path(OUTPUT_DIR) / f"{MODEL.name}.sproj",
    keras_lib_path=Path(__file__).resolve().parent.parent / "keras",
    copy_keras_lib=COPY_KERAS_LIB,
    exists_ok=True,
)


st.header("Graph of Model (Keras🧠)")
dot = model_to_dot(
    CREATOR.model,
    show_shapes=True,
    show_layer_names=True,
    show_layer_activations=True,
    show_dtype=True,
    dpi=72,
)

if SHOW_GRAPH_SIDEBAR:
    st.sidebar.graphviz_chart(str(dot), use_container_width=True)
st.graphviz_chart(str(dot), use_container_width=True)

st.header("Graph of Transformed Model (Networkx🕸️)")
st.pyplot(CREATOR.get_graph())
for nested_model, nested_graph in CREATOR.nested_graphs.items():
    st.subheader(f"... graph of nested model '{nested_model}' (Networkx🕸️)")
    st.pyplot(CREATOR.get_graph(nested_graph))

if DEBUG_MODE:
    st.header("Detailed Data of nodes (Python🐍)")
    with st.expander(
        "Click to switch between expanded and collapsed...", expanded=False
    ):
        for n, d in CREATOR.graph.nodes(data=True):
            st.subheader(n)
            data = d["data"]
            st.write(data)


def show_swan_code(swan_obj: Optional[swan.SwanItem]) -> None:
    """Display Swan code with syntax highlighting"""
    code = swan_to_str(swan_obj)
    try:

        lexer = pygments.lexers.get_lexer_by_name("swan")
        formatter = pygments.formatters.HtmlFormatter(
            linenos=True, cssclass="highlight"
        )
        highlighted_code = (
            "<html>\n<style>\n"
            f"{formatter.get_style_defs('.highlight')}"
            "\n</style>\n<body>\n"
            f"{pygments.highlight(code, lexer, formatter)}"
            "\n</body>\n</html>"
        )
        st.html(highlighted_code)
    except pygments.util.ClassNotFound:
        st.warning(
            "Python package `scade-one-pygments-plugin` not installed =>"
            " Using syntax highlight from Streamlit instead"
        )
        st.code(code)


st.sidebar.write("***Generation of S1 Models***")
st.header("Imported Model (Scade One🦢)")
CREATOR.create_module()
CREATOR.create_test_harness(INPUT_TEST)
show_swan_code(CREATOR.module_body)
st.subheader("... and Test Harness (Scade One🦢)")
show_swan_code(CREATOR.module_test)


if st.button("Generate Model🦢") or st.sidebar.button(
    "Generate Model🦢", key="gen_sidebar"
):
    generated_dir = CREATOR.write(auto_layout=auto_layout)
    st.balloons()
    st.info(f"Model generated in: ***{generated_dir.absolute().as_posix()}***")
    st.sidebar.info(f"Model generated in: ***{generated_dir.absolute().as_posix()}***")
