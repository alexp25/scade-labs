# -*- coding: utf-8 -*-
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
import types
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Optional, Type, Union, cast

import numpy as np
import tensorflow as tf  # type: ignore
from ansys.scadeone.core import swan  # type: ignore
from ansys.scadeone.core.common.storage import SwanString  # type: ignore
from ansys.scadeone.core.svc.swan_creator.operator_creator import OperatorFactory
from keras import KerasTensor, Variable, layers  # type: ignore

from ..graph.graph_nodes import LayerNode

from ..utils.s1_api_utils import (
    LiteralNumeric,
    SWAN_PARSER,
    add_block_from_id,
    add_constant_without_value,
    get_valid_id,
    get_valid_swan_name,
    op2map,
)
from .constants import ConstDecl4Swan, ConstDeclFromVar, ConstDeclValue

LOGGER = logging.getLogger("keras_importer.converters")

FACTORY = OperatorFactory()

# pylint: disable=invalid-name  # for parameters using capital letters

COMMON_LAYER_ATTRIBUTES = [
    "kernel_size",
    "padding",
    "data_format",
    "strides",
    "filters",
    "groups",
    "dilation_rate",
    "use_bias",
    "bias",
    "kernel",
    # For Batch Normalization
    "gamma",
    "beta",
    "moving_mean",
    "moving_variance",
]

InputsShape = Union[list[int], tuple[list[int], ...]]


@dataclass
class LayerInfo(LayerNode):
    """Information for layer"""

    input: Union[KerasTensor, list[KerasTensor]] = field(repr=False)
    output: KerasTensor = field(repr=False)
    activation_name: Optional[str] = field(init=False)
    activation: Optional[types.FunctionType] = field(init=False, repr=False)

    def __post_init__(self):
        self.name = get_valid_swan_name(self.layer.name)
        self.activation = getattr(self.layer, "activation", None)
        self.activation_name = self.activation.__name__ if self.activation else None

    def __getattr__(self, __name: str) -> Any:
        if __name in COMMON_LAYER_ATTRIBUTES:
            return getattr(self.layer, __name, None)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{__name}'"
        )

    @property
    def has_activation(self) -> bool:
        """Whether the layer has an activation layer"""
        return bool(self.activation_name and self.activation_name != "linear")

    @property
    def _is_activation_from_keras(self) -> bool:
        """Whether the activation is a keras activation"""
        if not self.activation:
            return False
        return self.activation.__module__.startswith("keras.")

    def is_keras_activation(self, name: str) -> bool:
        """Whether the activation is a keras activation and matches a given name"""
        return self._is_activation_from_keras and self.activation_name == name

    def get_activation_operator(self) -> Optional[swan.Block]:
        """Get activation block if an activation shall be performed"""
        if not self.has_activation or self.activation_name is None:
            return None

        if self._is_activation_from_keras:
            module = "activations"
            if self.activation_name == "softmax":
                return add_block_from_id(
                    f"{module}::softmax",
                    sizes=[s for s in self.layer.output.shape if s],
                )
        else:
            module = self.activation.__module__.replace(".", "::")

        block = add_block_from_id(
            f"{module}::{self.activation_name}",
        )
        block._instance = op2map(
            block.instance, sizes=[s for s in self.output.shape[::-1] if s]
        )
        return block

    @property
    def has_parameters(self) -> bool:
        """Whether the layer has parameters (kernel, bias, ...)"""
        return any(hasattr(self.layer, p) for p in ["kernel", "bias"])

    @property
    def identifier(self) -> swan.Identifier:
        """Get valid identifier in Swan for layer"""
        return get_valid_id(self.name)

    def name_cst(self, base_name: str) -> swan.Identifier:
        """Give a name to constants using layer name as prefix"""
        layer_name = self.identifier.value
        return get_valid_id(f"{layer_name}_{base_name}")


class LayerConverter(ABC):
    """Base class for converting layers"""

    def __init__(
        self,
        layer: layers.Layer,
        module: swan.Module,
        constants: list[ConstDeclFromVar],
    ) -> None:
        self.layer = layer
        self.module = module
        self.info = LayerInfo.from_layer(layer)
        self.constants = constants
        self.input_shape = self._get_input_shape()

    @property
    def layer_type(self) -> str:
        """Return name of layer type"""
        return self.layer.__class__.__name__

    def _get_input_shape(self) -> InputsShape:
        """Input shape as a list, with a filter of None"""
        inp = self.layer.input
        if isinstance(inp, list):
            return tuple([s for s in i.shape if s] for i in inp)
        return [s for s in inp.shape if s]

    def _get_pass_through_operator(self, name: str) -> swan.Block:
        """Get Pass-through operator with a given name (using lambda function)"""
        return swan.Block(SWAN_PARSER.op_expr(SwanString(f"function {name} => {name}")))

    def convert_2_block(self) -> swan.Block:
        """Conversion of Layer to block for main operator"""
        LOGGER.debug(
            f"Translation of {self.layer_type} layer: {self.layer.name} (id: {id(self.layer)})"
        )
        try:
            return self._convert()
        except NotImplementedError:
            return self._get_pass_through_operator(f"{self.layer_type}_not_implemented")

    def _convert(self) -> swan.Block:
        """Real implementation: to be replaced in sub-classes"""
        raise NotImplementedError

    @property
    def operator_block(self) -> swan.Block:
        """Method to get the call for operator to implement the layer"""
        raise NotImplementedError("Method to get operator call shall be implemented")


class _ParamLayerConverter(LayerConverter, ABC):
    """Base class for layers with parameters and potentially an activation function"""

    MANDATORY_CONSTANTS = ["kernel", "bias"]
    # As operators for a layer implementation have a given shape for the input,
    # we will have to apply a map if the input has more dimensions.
    # For more convenience, we can set a class property to this number of dimensions
    # in the operator (if the attribute is None, nothing is done)
    # For example, if this attribute value is `2` and the input has shape 5^6^7^8
    # then we will apply a map 6^5 (i.e. removing the last two values and reversing the order)
    OPERATOR_SHAPE_DIM: Optional[int] = None

    def _create_call_to_operator(self, operator: swan.Block) -> Optional[swan.Block]:
        """Create an external operator if needed, and returns the operator name"""
        constants = self.get_constants()
        if not (self.info.has_parameters or self.info.has_activation):
            return None  # ? Is it always the case?

        operator_id = self.info.identifier
        # NOTE: self.module.add_constant(c.name, c.type_as_str) is not usable in our case
        # because it does not (yet) support imported constants
        constants_expr = [
            add_constant_without_value(self.module, c.name, c.type_as_str)
            for c in constants
        ]

        operator_activation = self.module.add_operator(operator_id.value, is_node=False)
        inputs = [
            operator_activation.add_input(i.name, i.var_type)
            for i in self.info.inputs_info
        ]
        outputs = [
            operator_activation.add_output(o.name, o.var_type)
            for o in self.info.outputs_info
        ]
        diag = operator_activation.add_diagram()

        input_blocks = [diag.add_expr_block(i) for i in inputs]
        cst_blocks = [diag.add_expr_block(i) for i in constants_expr]
        def_blocks = [diag.add_def_block(o) for o in outputs]

        diag._diagram_adder.add_block(operator)

        activation_block = self.info.get_activation_operator()
        if activation_block:
            diag._diagram_adder.add_block(activation_block)

        # Inputs -> Operator
        for i, input_ in enumerate(input_blocks):
            diag.connect(input_, (operator, i + 1))

        # Constants -> Operator
        for cst, block in zip(constants, cst_blocks):
            diag.connect(block, (operator, cst.param_name))

        # Operator -> Activation (if any)
        if activation_block:
            diag.connect((operator, 1), activation_block)

        # Activation / Operator -> Output
        last_block = activation_block or operator
        for i, output in enumerate(def_blocks):
            diag.connect((last_block, 1), output)

        self.constants.extend(c for c in constants if isinstance(c, ConstDeclFromVar))
        return swan.Block(operator_activation.id)

    def _get_map_size(self) -> list[int]:
        """Get sizes for applying map on operator OR replication on kernel/bias"""
        if self.OPERATOR_SHAPE_DIM:
            return self.input_shape[: -1 * self.OPERATOR_SHAPE_DIM][::-1]

        return []

    def _get_kernel(self) -> ConstDeclFromVar:
        """Get constant for Kernel"""
        return ConstDeclFromVar.from_variable(
            self.layer.kernel, sizes=self._get_map_size()
        )

    def _get_bias(self) -> ConstDecl4Swan:
        """Get constant for Bias"""
        if getattr(self.layer, "bias", None) is not None:
            return ConstDeclFromVar.from_variable(
                self.layer.bias, sizes=self._get_map_size()
            )
        else:
            return ConstDeclValue(swan.Identifier("bias"), expr=self._get_bias_default())

    def _get_bias_default(self) -> swan.Expression:
        """Get default value of bias"""
        return LiteralNumeric(0).repeat(self.info.output.shape[::-1])

    def get_constants(self) -> list[ConstDecl4Swan]:
        """Get the list of constants"""
        constants: list[ConstDecl4Swan] = []
        for p in self.MANDATORY_CONSTANTS:
            get_func = getattr(self, f"_get_{p}")
            constants.append(get_func())

        return constants

    def _convert(self) -> swan.Block:
        operator_keras = self.operator_block
        map_sizes = self._get_map_size()
        if map_sizes:
            operator_keras._instance = op2map(operator_keras.instance, sizes=map_sizes)

        operator_called = self._create_call_to_operator(operator_keras)
        return operator_called or operator_keras


class _NoParamLayerConverter(LayerConverter):
    """Base class for layers that don't have parameters"""

    def _convert(self) -> swan.Block:
        return self.operator_block


class DummyConverter(LayerConverter):
    """Default converter"""

    def convert_2_block(self) -> swan.Block:
        return self._get_pass_through_operator(f"{self.layer_type}_not_supported")


class DropoutConverter(_NoParamLayerConverter):
    """Class for converting Dropout Layers"""

    @property
    def operator_block(self) -> swan.Block:
        # As Dropout is a pass-through layer during inference,
        # we can just use a lambda function
        return self._get_pass_through_operator("Dropout")


class ActivationConverter(_NoParamLayerConverter):
    """Class for converting Activation Layers"""

    @property
    def operator_block(self) -> swan.Block:
        return self.info.get_activation_operator()


class AddConverter(_NoParamLayerConverter):
    """Class for converting Add Layers"""

    @property
    def operator_block(self) -> swan.Block:
        sizes = list(self.layer.input[0].shape[1:])
        block = swan.Block(SWAN_PARSER.operator_block(SwanString("(+)")))
        block._instance = op2map(block.instance, sizes=sizes[::-1])
        return block


class DenseConverter(_ParamLayerConverter):
    """Class for converting Dense Layers"""

    OPERATOR_SHAPE_DIM = 1  # Input: 'T^N

    @property
    def operator_block(self) -> swan.Block:
        N = next(iter(self.layer.kernel.shape))
        M = self.layer.units
        return add_block_from_id("layers::Dense", sizes=[N, M])


class ZeroPadding2DConverter(_NoParamLayerConverter):
    """Class for converting ZeroPadding2D Layers"""

    # TODO: implement here... and the related Swan Operator
    # see link: https://keras.io/api/layers/reshaping_layers/zero_padding2d/

    # Arguments:
    # * padding: Integer, or tuple of 2 integers, or tuple of 2 tuples of 2 integers.
    #       If int: the same symmetric padding is applied to height and width.
    #       If tuple of 2 ints: interpreted as two different symmetric padding values for height and width:
    #           (symmetric_height_pad, symmetric_width_pad).
    #       If tuple of 2 tuples of 2 ints: interpreted as
    #           ((top_pad, bottom_pad), (left_pad, right_pad)).
    # * data_format: A string, one of channels_last (default) or channels_first.

    @property
    def operator_block(self) -> swan.Block:
        layer = cast(layers.ZeroPadding2D, self.layer)
        if layer.data_format == "channels_first":
            _, C, H, W = layer.input.shape
        else:
            _, H, W, C = layer.input.shape
        ((Pht, Phb), (Pwl, Pwr)) = layer.padding
        choice_operator = {
            "channels_last": "TZeroPadding2D",
            "channels_first": "ZeroPadding2D",
        }
        op_name = choice_operator[layer.data_format]
        return add_block_from_id(f"layers::{op_name}", sizes=[C, H, W, Pht, Phb, Pwl, Pwr])


class MaxPool2DConverter(_NoParamLayerConverter):  #
    """Class for converting MaxPool2D Layers"""

    @property
    def operator_block(self) -> swan.Block:
        layer = cast(layers.MaxPooling2D, self.layer)
        W, H, C = self.input_shape
        Ph, Pw = layer.pool_size
        Sh, Sw = layer.strides
        choice_operator = {
            "channels_last": "TMaxPool2D",
            "channels_first": "MaxPool2D",
        }
        try:
            op_name = choice_operator.get(layer.data_format)
            return add_block_from_id(
                f"layers::{op_name}", sizes=[C, H, W, Ph, Pw, Sh, Sw]
            )

        except KeyError:
            return self._get_pass_through_operator("maxpool_config_not_supported")


class FlattenConverter(_NoParamLayerConverter):
    """Class for converting Flatten Layers"""

    @property
    def operator_block(self) -> swan.Block:
        layer = cast(layers.Flatten, self.layer)
        input_shape = self.input_shape
        if len(input_shape) == 1:
            return self._get_pass_through_operator("Flatten_1D")
        if len(input_shape) > 2:
            choice_operator: dict[tuple[int, str], str] = {
                (2, "channels_last"): "Flatten2D",
                (3, "channels_last"): "Flatten3D",
                (2, "channels_first"): "TFlatten2D",
                (3, "channels_first"): "TFlatten3D",
            }
            try:
                op_name = choice_operator.get((len(input_shape), layer.data_format))
                return add_block_from_id(f"layers::{op_name}", sizes=input_shape)
            except KeyError:
                pass

        return self._get_pass_through_operator("flatten_config_not_supported")


class Conv2DConverter(_ParamLayerConverter):
    """Class for converting Conv2D Layers"""

    @property
    def has_dilation(self) -> bool:
        """Whether the layer has some dilation (Dh, Dw) != (1, 1)"""
        return self.layer.dilation_rate != (1, 1)

    @property
    def operator_block(self) -> swan.Block:
        if len(self.input_shape) == 1:
            return self._get_pass_through_operator("Conv_1D")
        if len(self.input_shape) > 2:
            layer = cast(layers.Conv2D, self.layer)
            choice_operator: dict[tuple[str, str], str] = {
                ("valid", "channels_last"): "TConv2D",
                ("same", "channels_last"): "TPConv2D",
                ("valid", "channels_first"): "Conv2D",
                ("same", "channels_first"): "PConv2D",
            }
            try:
                op_name = choice_operator.get((layer.padding, layer.data_format))
                F = layer.filters
                # For the input shape, it could be either (None, a, b, c) or (1, a, b, c)
                # ... so we can just ignore the first value to work in both cases
                if layer.data_format == "channels_first":
                    _, C, H, W = layer.input.shape
                else:
                    _, H, W, C = layer.input.shape
                Kh, Kw = layer.kernel_size
                Sh, Sw = layer.strides

                # Apply Dilation Rate
                if self.has_dilation:
                    Dh, Dw = layer.dilation_rate
                    Kh, Kw = Kh * Dh - Dh + 1, Kw * Dw - Dw + 1

                # create sizes
                sizes = [F, C, H, W, Kh, Kw, Sh, Sw]

                if layer.padding == "same":
                    Ph, Pw = self._compute_paddings(H, W, Kh, Kw, Sh, Sw)
                    sizes.extend([Ph, Pw])

                return add_block_from_id(f"layers::{op_name}", sizes=sizes)
            except KeyError:
                pass

        return self._get_pass_through_operator("conv_config_not_supported")

    def _get_kernel(self) -> ConstDeclFromVar:
        """Get Swan constant for Kernel (dilated if needed)

        Note: Kernel is of shape `T^F^C^Kw^Kh`

        Args:
            kernel: Kernel of the layer
        Returns:
            * if there is a Dilation: a Swan constant of the dilated kernel
                of shape T^(Kw*Dw-Dw+1)^(Kh*Dh-Dh+1)^C^F
            * if there is no dilation: a Swan constant of the kernel (shape T^Kw^Kh^C^F)
        """
        kernel = self.layer.kernel

        Kh, Kw, C, F = list(kernel.shape)
        kernel_np = kernel.numpy()  # type: ignore

        if self.has_dilation:
            Dh, Dw = self.layer.dilation_rate
            dilated_kernel = np.zeros(
                (Kh * Dh - Dh + 1, Kw * Dw - Dw + 1, C, F),
                dtype=kernel_np.dtype,
            )
            for i, j, k, m in np.ndindex((Kh, Kw, C, F)):
                dilated_kernel[i * Dh][j * Dw][k][m] = kernel_np[i][j][k][m]
            transposed_kernel = np.transpose(dilated_kernel, (3, 2, 0, 1))
            shape = [F, C, Kh * Dh - Dh + 1, Kw * Dw - Dw + 1]
        else:
            # actually the code below is the same as above
            # when Dh = Dw = 1, but it's much simpler and faster (no computation)
            transposed_kernel = np.transpose(kernel_np, (3, 2, 0, 1))
            shape = [F, C, Kh, Kw]

        kernel_var = Variable(
            initializer=transposed_kernel,
            name=kernel.name,
            dtype=kernel.dtype,
            shape=tf.TensorShape(shape),
        )
        kernel_var._path = kernel.path
        return ConstDeclFromVar.from_variable(kernel_var)

    def _compute_paddings(
        self, h: int, w: int, kh: int, kw: int, sh: int, sw: int
    ) -> tuple[int, int]:
        """Compute Padding for Convolution"""
        h1 = int(np.ceil(h / sh))
        w1 = int(np.ceil(w / sw))

        ph = 0
        if h % sh == 0:
            ph = max(kh - sh, 0)
        else:
            ph = max(kh - (h % sh), 0)

        pw = 0
        if w % sw == 0:
            pw = max(kw - sw, 0)
        else:
            pw = max(kw - (w % sw), 0)

        return (ph, pw)


class BatchNormalizationConverter(_ParamLayerConverter):
    """Class for converting BatchNormalization Layers"""

    MANDATORY_CONSTANTS = ["gamma", "beta", "moving_mean", "moving_variance"]

    # Inference formula: gamma * (x - moving_mean) / sqrt(moving_variance + epsilon) + beta
    # Two paths:
    #   3D channels_last (axis == last) → layers::BatchNorm3D with separate epsilon constant
    #   All other cases → nested-map utils::normalize with epsilon baked into variance

    @property
    def operator_block(self) -> swan.Block:
        raise NotImplementedError("BatchNormalizationConverter uses _convert() directly")

    def _get_gamma(self) -> ConstDecl4Swan:
        if not self.layer.scale:
            return ConstDeclValue(
                get_valid_id("gamma"),
                expr=LiteralNumeric(1.0).repeat(list(self.layer.moving_mean.shape)),
            )
        return ConstDeclFromVar.from_variable(self.layer.gamma)

    def _get_beta(self) -> ConstDecl4Swan:
        if not self.layer.center:
            return ConstDeclValue(
                get_valid_id("beta"),
                expr=LiteralNumeric(0).repeat(list(self.layer.moving_mean.shape)),
            )
        return ConstDeclFromVar.from_variable(self.layer.beta)

    def _get_moving_mean(self) -> ConstDeclFromVar:
        return ConstDeclFromVar.from_variable(self.layer.moving_mean)

    def _get_moving_variance(self) -> ConstDeclFromVar:
        return ConstDeclFromVar.from_variable(self.layer.moving_variance)

    def _add_cst_to_diag(self, diag, const: ConstDecl4Swan):
        """Declare ConstDeclFromVar in module and add expr block; embed ConstDeclValue inline."""
        if isinstance(const, ConstDeclFromVar):
            decl = add_constant_without_value(self.module, const.name, const.type_as_str)
            return diag.add_expr_block(decl)
        block = const.as_swan_expr()
        diag._diagram_adder.add_block(block)
        return block

    def _convert(self) -> swan.Block:
        input_shape = list(self.layer.input.shape[1:])
        ndims = len(input_shape)
        axis = self.layer.axis
        if isinstance(axis, (list, tuple)):
            axis = axis[0] if axis else -1
        if axis < 0:
            axis = ndims + axis + 1  # e.g. -1 → ndims (1-indexed including batch)
        if ndims == 3 and axis == ndims:
            return self._convert_3d(input_shape)
        return self._convert_general(input_shape, axis, ndims)

    def _convert_3d(self, input_shape: list) -> swan.Block:
        """3D channels_last path: BatchNorm3D<<C,H,W>> with separate epsilon."""
        H, W, C = input_shape[0], input_shape[1], input_shape[2]
        all_constants = [
            self._get_gamma(),
            self._get_beta(),
            self._get_moving_mean(),
            self._get_moving_variance(),
        ]

        operator_id = self.info.identifier
        op = self.module.add_operator(operator_id.value, is_node=False)
        inputs = [op.add_input(i.name, i.var_type) for i in self.info.inputs_info]
        outputs = [op.add_output(o.name, o.var_type) for o in self.info.outputs_info]
        diag = op.add_diagram()

        inner_block = add_block_from_id("layers::BatchNorm3D", sizes=[C, H, W])
        diag._diagram_adder.add_block(inner_block)

        input_blocks = [diag.add_expr_block(i) for i in inputs]
        cst_blocks = [self._add_cst_to_diag(diag, c) for c in all_constants]

        # Epsilon is an inline scalar literal, not a module-level constant
        epsilon_block = ConstDeclValue(
            get_valid_id(f"{self.info.name}_epsilon"),
            expr=LiteralNumeric(self.layer.epsilon),
        ).as_swan_expr()
        diag._diagram_adder.add_block(epsilon_block)

        def_blocks = [diag.add_def_block(o) for o in outputs]

        for i, ib in enumerate(input_blocks):
            diag.connect(ib, (inner_block, i + 1))

        for cst_block, param_name in zip(cst_blocks, ["scale", "offset", "mean", "variance"]):
            diag.connect(cst_block, (inner_block, param_name))

        diag.connect(epsilon_block, (inner_block, "epsilon"))

        for def_block in def_blocks:
            diag.connect((inner_block, 1), def_block)

        self.constants.extend(c for c in all_constants if isinstance(c, ConstDeclFromVar))
        return swan.Block(op.id)

    def _convert_general(self, input_shape: list, axis: int, ndims: int) -> swan.Block:
        """General path: broadcast constants to full shape, bake epsilon, use map(normalize)."""

        def broadcast_var(var):
            b_shape = [1] * ndims
            b_shape[axis - 1] = var.shape[0]
            b_v = np.broadcast_to(np.reshape(var.numpy(), b_shape), input_shape)
            result = Variable(
                initializer=b_v,
                name=var.name,
                dtype=var.dtype,
                shape=tf.TensorShape(input_shape),
            )
            result._path = var.path
            return result

        # Bake epsilon into variance before broadcasting
        mv = self.layer.moving_variance
        variance_baked = Variable(
            initializer=mv.numpy() + self.layer.epsilon,
            name=mv.name,
            dtype=mv.dtype,
            shape=mv.shape,
        )
        variance_baked._path = mv.path

        if self.layer.scale:
            gamma_cst = ConstDeclFromVar.from_variable(broadcast_var(self.layer.gamma))
        else:
            gamma_cst = ConstDeclValue(
                get_valid_id("gamma"),
                expr=LiteralNumeric(1.0).repeat(input_shape[::-1]),
            )
        if self.layer.center:
            beta_cst = ConstDeclFromVar.from_variable(broadcast_var(self.layer.beta))
        else:
            beta_cst = ConstDeclValue(
                get_valid_id("beta"),
                expr=LiteralNumeric(0).repeat(input_shape[::-1]),
            )
        mean_cst = ConstDeclFromVar.from_variable(broadcast_var(self.layer.moving_mean))
        var_cst = ConstDeclFromVar.from_variable(broadcast_var(variance_baked))
        all_constants = [gamma_cst, beta_cst, mean_cst, var_cst]

        operator_id = self.info.identifier
        op = self.module.add_operator(operator_id.value, is_node=False)
        inputs = [op.add_input(i.name, i.var_type) for i in self.info.inputs_info]
        outputs = [op.add_output(o.name, o.var_type) for o in self.info.outputs_info]
        diag = op.add_diagram()

        normalize_block = add_block_from_id("utils::normalize")
        normalize_block._instance = op2map(normalize_block.instance, sizes=input_shape[::-1])
        diag._diagram_adder.add_block(normalize_block)

        input_blocks = [diag.add_expr_block(i) for i in inputs]
        cst_blocks = [self._add_cst_to_diag(diag, c) for c in all_constants]
        def_blocks = [diag.add_def_block(o) for o in outputs]

        for i, ib in enumerate(input_blocks):
            diag.connect(ib, (normalize_block, i + 1))

        for cst_block, param_name in zip(cst_blocks, ["scale", "offset", "mean", "variance"]):
            diag.connect(cst_block, (normalize_block, param_name))

        for def_block in def_blocks:
            diag.connect((normalize_block, 1), def_block)

        self.constants.extend(c for c in all_constants if isinstance(c, ConstDeclFromVar))
        return swan.Block(op.id)


def get_layer_converter(layer_type: layers.Layer) -> Type[LayerConverter]:
    """Get convertor of layer"""
    # Note: the dictionary below shall be updated with additional layer implementation
    # after these layers conversion classes have been created
    # ... or we could use a mapping based on name (e.g. Flatten => FlattenConverter)
    conversion_layers: dict[layers.Layer, Type[LayerConverter]] = {
        layers.Dense: DenseConverter,
        layers.Conv2D: Conv2DConverter,
        layers.MaxPool2D: MaxPool2DConverter,
        layers.Flatten: FlattenConverter,
        layers.Add: AddConverter,
        layers.Activation: ActivationConverter,
        layers.Dropout: DropoutConverter,
        layers.BatchNormalization: BatchNormalizationConverter,
        layers.ZeroPadding2D: ZeroPadding2DConverter,
    }

    return conversion_layers.get(layer_type, DummyConverter)
