import logging
import re
import textwrap
from abc import ABC
from typing import Optional, Union

import tensorflow as tf  # type: ignore
from ansys.scadeone.core import swan  # type: ignore
from ansys.scadeone.core.svc.swan_printer import PPrinter, swan_to_str
from typing_extensions import Self

from ..graph.graph_nodes import IOInfo
from ..utils.s1_api_utils import (
    get_valid_id,
    identifier2expr,
    repeat_expr,
    str2type,
    var2expr,
)

# pylint: disable=redefined-builtin

LOGGER = logging.getLogger("keras_importer.converters")


class ConstDecl4Swan(swan.ConstDecl, ABC):
    """Constant to be exported to Swan"""

    def as_swan_expr(self) -> swan.ExprBlock:
        """Return as a Swan Expression Block"""
        return swan.ExprBlock(identifier2expr(self.identifier))

    @property
    def name(self) -> str:
        """Name of the identifier"""
        return self.id.value

    @property
    def param_name(self) -> str:
        """Name of parameter for Operator"""
        raise NotImplementedError("should be implemented in sub-class")

    @property
    def type_as_str(self) -> str:
        """Type as a string"""
        return swan_to_str(self.type)


class ConstDeclFromVar(ConstDecl4Swan):
    """Constant to be stored in source C file"""
    UNIQUE_IDS: dict[str, int] = {}

    def __init__(
        self,
        id: swan.Identifier,
        type_expr: Optional[swan.TypeExpression],
        value: Optional[swan.Expression] = None,
        variable: Optional[tf.Variable] = None,
        imported: bool = True,
        sizes: Optional[list[int]] = None,
    ) -> None:
        super().__init__(id, type_expr, value)
        self.variable = variable
        self.imported = imported
        self.sizes = sizes or []

    @classmethod
    def _get_unique_id(cls, basename: str) -> str:
        """Get a unique ID for a constant"""
        baseid = cls.UNIQUE_IDS.get(basename)
        if baseid is not None:
            cls.UNIQUE_IDS[basename] += 1
            return f"{basename}__{baseid}"

        cls.UNIQUE_IDS[basename] = 1
        return basename

    @classmethod
    def from_variable(
        cls, var: tf.Variable, imported: bool = True, sizes: Optional[list[int]] = None
    ) -> Self:
        """Create a constant declaration from a variable"""
        var_type = IOInfo.get_var_type(var)

        var_id = var.name
        var_path = getattr(var, "path", None)
        if var_path:
            var_id += "__" + var_path.split("/")[0]
            if ":" in var_path:
                var_id += "__" + var_path.split(":")[-1]
        var_id = cls._get_unique_id(var_id)

        return cls(
            get_valid_id(var_id),
            type_expr=str2type(var_type),  # type: ignore
            value=None if imported else var2expr(var),
            variable=var,
            imported=imported,
            sizes=sizes,
        )

    def as_swan_expr(self) -> swan.ExprBlock:
        """Return as a Swan Expression Block"""
        expr = identifier2expr(self.identifier)
        if self.sizes:
            expr = repeat_expr(expr, self.sizes)

        return swan.ExprBlock(expr)

    @property
    def param_name(self) -> str:
        """Name of parameter for Operator

        Example: 'dense_1/bias:0' => 'bias'
        """
        if self.variable is None or "/" not in self.variable.path:
            return "??"

        return re.sub(r"(:\d+)+$", "", self.variable.path.split("/")[-1])

    @staticmethod
    def format_c(value: Union[int, float], as_hex: bool):
        """Format a value for representation in C"""
        # ? Can a value be something else? like a bool?
        # Note: the hexadecimal representation was used in first version of Scade NN
        # ... but it is not supported in 2024 R1 version of Scade One
        # (due to the choice of C compiler/builder for running simulation/debug)
        # ? TODO: Is it possible now??
        if not as_hex:
            return str(value)

        s = float.hex(float(value))
        return f"+{s}" if s[0] != "-" else s

    def get_c_code(self, module: str = "", as_hex: bool = False) -> str:
        """Get the C code for a constant in imported source C file"""
        if self.variable is None:
            return ""

        constant_name = self.id.value
        if module:
            constant_name += f"_{module}"

        scade_base_type = self.variable.dtype
        cst_type = f"swan_{scade_base_type}"
        size = "".join(f"[{d}]" for d in self.variable.shape)
        data = ", ".join(self.format_c(v, as_hex) for v in self.variable.numpy().flat)  # type: ignore
        data = textwrap.fill(data, width=100, subsequent_indent="  ")
        return f"\nconst {cst_type} {constant_name}{size} = {{\n  {data}\n}};\n"


PPrinter.visit_ConstDeclFromVar = PPrinter.visit_ConstDecl


class ConstDeclValue(ConstDecl4Swan):
    """Constant with a default value to replace a missing variable
    (e.g 0s for missing bias)
    """

    def __init__(
        self,
        id: swan.Identifier,
        type_expr: Optional[swan.TypeExpression] = None,
        expr: Optional[swan.Expression] = None,
    ) -> None:
        super().__init__(id, type_expr, expr)

    @property
    def param_name(self) -> str:
        return self.name

    def as_swan_expr(self) -> swan.ExprBlock:
        assert self.value is not None, f"Value for param '{self.name}' shall be defined"
        return swan.ExprBlock(self.value)
