import enum
from dataclasses import dataclass
from typing import Any, Optional, TypeVar, Union, cast

from keras import KerasTensor  # type: ignore
from typing_extensions import Self

from keras import layers  # type: ignore

from ..utils.s1_api_utils import get_valid_swan_name

IOSizeSingleInput = tuple[Optional[int], ...]
IOSize = Union[IOSizeSingleInput, list[IOSizeSingleInput]]

T = TypeVar("T")


class NodeKind(enum.IntEnum):
    """Type of Node in the graph"""

    INPUT = enum.auto()
    LAYER = enum.auto()
    NESTED = enum.auto()
    OUTPUT = enum.auto()
    TERMINATOR = enum.auto()


NODE_COLORS = {
    NodeKind.INPUT: "gold",
    NodeKind.LAYER: "turquoise",
    NodeKind.NESTED: "purple",
    NodeKind.OUTPUT: "orange",
    NodeKind.TERMINATOR: "grey",
}


@dataclass
class Node:
    """Node for Graph representing the architecture"""

    name: str
    layer: layers.Layer
    dtype: str

    def __post_init__(self):
        if hasattr(self.dtype, "name"):
            self.dtype = self.dtype.name
            assert isinstance(self.dtype, str), (
                f"dtype should be a string but got {self.dtype}"
            )

    @property
    def swan_name(self) -> str:
        """Name valid for Scade One model"""
        return get_valid_swan_name(self.name)

    @staticmethod
    def get_as_list(elements: Union[T, list[T]]) -> list[T]:
        """Return elements as list, even if it's provided as a non-list"""
        return elements if isinstance(elements, list) else [elements]


@dataclass
class IOInfo:
    """Information on input / output"""

    name: str
    dtype: str
    shape: IOSizeSingleInput

    @classmethod
    def _get_dtype_name(cls, dtype: Any) -> str:
        """Get the name of the dtype"""
        if hasattr(dtype, "name"):
            return dtype.name
        return str(dtype)

    @classmethod
    def from_tensor(cls, io: KerasTensor) -> Self:
        """Create from a tensor"""
        return cls(io.name, cls._get_dtype_name(io.dtype), tuple(io.shape))

    @classmethod
    def get_var_type(cls, io: Any) -> str:
        """Get type of a variable (method callable from anywhere)

        Args:
            io: object with attributes "dtype" and "shape"
        Returns:
            string representation of type (e.g. float^32^3)
        """
        var_type = cls._get_dtype_name(io.dtype)
        size = "^".join(str(s) for s in io.shape[::-1] if s)

        if size:
            var_type += f"^{size}"

        return var_type

    @property
    def var_type(self) -> str:
        """Type for variable in swan"""
        return self.get_var_type(self)


@dataclass
class IONode(Node):
    """Node for input or output"""

    shape: IOSizeSingleInput

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.shape, (tuple, list)):
            self.shape = tuple(self.shape)

    @property
    def var_type(self) -> str:
        """Type for variable in swan"""
        return IOInfo.get_var_type(self)


@dataclass
class InputNode(IONode):
    """Node for Input"""

    @staticmethod
    def get_shape(node: Union[KerasTensor, layers.InputLayer]) -> IOSizeSingleInput:
        """Get input shape"""
        if isinstance(node, layers.InputLayer):
            # InputLayer has no .shape in Keras 3; use the output tensor's shape
            return node.output.shape
        try:
            shape: IOSizeSingleInput = node.shape
        except AttributeError:
            shape = getattr(node, "input_shape", tuple([None]))
            # It seems that `input_shape` might return a list
            # so we want to extract the first value
            if isinstance(shape, list) and shape and isinstance(shape[0], tuple):
                shape = shape[0]  # type: ignore

        return shape

    @classmethod
    def from_input(cls, input_: Union[KerasTensor, layers.InputLayer]) -> Self:
        """Create object from input"""
        name = cast(str, input_.name)
        shape = cls.get_shape(input_)
        dtype: str = input_.dtype  # type: ignore  # will be converted to string later
        return cls(name=name, layer=input_, dtype=dtype, shape=shape)


@dataclass
class OutputNode(IONode):
    """Node for Output"""

    @classmethod
    def from_output(cls, output: KerasTensor) -> Self:
        """Create object from output"""
        # pylint: disable=protected-access
        layer = output._keras_history.operation  # type: ignore
        name: str = output.name  # type: ignore
        # # ? Why do we need tensor index in old importer?
        # tensor_index = output._keras_history.tensor_index
        return cls(name=name, layer=layer, dtype=output.dtype, shape=output.shape)


@dataclass
class LayerNode(Node):
    """Layer as a graph node"""

    # Keras 3.x: layer.input is list for multi-input layers (Add, Concat), single tensor otherwise
    input: Union[KerasTensor, list[KerasTensor]]
    input_shape: IOSize
    # Keras 3.x: layer.output may become list for multi-output layers
    output: Union[KerasTensor, list[KerasTensor]]
    output_shape: Union[IOSizeSingleInput, list[IOSizeSingleInput]]
    inputs_info: list[IOInfo]
    outputs_info: list[IOInfo]

    @classmethod
    def from_layer(cls, layer: layers.Layer) -> Self:
        """Create object from a layer"""
        inp = layer.input
        out = layer.output
        inp_shape = (
            [i.shape for i in inp] if isinstance(inp, list) else inp.shape
        )
        out_shape = (
            [o.shape for o in out] if isinstance(out, list) else out.shape
        )
        return cls(
            name=layer.name,
            layer=layer,
            dtype=layer.dtype,  # type: ignore  # will be converted to string later
            input=inp,
            input_shape=inp_shape,
            output=out,
            output_shape=out_shape,
            inputs_info=cls.get_io_infos(inp),
            outputs_info=cls.get_io_infos(out),
        )

    @classmethod
    def get_io_infos(cls, io_tensor: Any) -> list[IOInfo]:
        """Get infos on inputs / layers as dictionaries"""
        return [IOInfo.from_tensor(io) for io in cls.get_as_list(io_tensor)]

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class NestedModelNode(LayerNode):
    """Nested Model in a node"""

    # TODO: Implement
