import logging
from typing import Optional, TypeVar, Union

import numpy as np  # type: ignore
from ansys.scadeone.core import swan  # type: ignore
from ansys.scadeone.core.svc.swan_creator.operator_creator import OperatorFactory


from keras import layers

from ..graph.graph_nodes import (
    InputNode,
    IOInfo,
    IONode,
    IOSizeSingleInput,
    LayerNode,
    Node,
    OutputNode,
)

from ..utils.s1_api_utils import (
    add_block_from_id,
    get_underscore_def_block,
    op2map,
    str2expr,
    var2expr,
)
from .constants import ConstDeclFromVar
from .layers import get_layer_converter

logger = logging.getLogger("keras_importer")

T = TypeVar("T")
L = TypeVar("L", layers.Layer, layers.Layer)

TestsInputsVar = Optional[list[np.ndarray]]

FACTORY = OperatorFactory()

# This was part of the old importer: we need to see if we really need it
# class memoize(object):  # pylint: disable=invalid-name
#     """Cache output of functions for memory/speed optimization"""
#
#     def __init__(self, func):
#         self.func = func
#         self.cache = {}
#
#     def __call__(self, *args):
#         if not isinstance(args, Hashable):
#             # un-cacheable. a list, for instance. Better to not cache than blow up.
#             return self.func(*args)
#
#         if args not in self.cache:
#             value = self.func(*args)
#             self.cache[args] = value
#
#         return self.cache[args]
#
#     def __repr__(self):
#         return self.func.__doc__
#
#     def __get__(self, obj: Any, obj_type: Any):
#         _ = obj_type


class OperatorCreator:
    """Class to create main operator for Neural Network"""

    def __init__(self, name: str, module: swan.Module) -> None:
        # We will use a class to be able to store extra operators
        # and constants that are added when converting the different nodes
        # of the layers
        self.module = module
        self.operator = module.add_operator(name, is_node=False)
        self._diag = self.operator.add_diagram()
        self.extra_operators: list[swan.Operator] = []
        self.constants: list[ConstDeclFromVar] = []
        self._blocks: dict[str, swan.Block] = {}

    def io2decl(self, io: Union[IONode, IOInfo]) -> swan.VarDecl:
        """Transform a graph Input/Output node to a declaration for operator I/O"""
        return FACTORY.create_variable(io.name, io.var_type)

    def node2diagram(self, node: Node) -> swan.DiagramObject:
        """Transform a graph node into an object for Swan Diagram"""
        if isinstance(node, InputNode):
            block = self.input2expr(node)
        elif isinstance(node, OutputNode):
            block = self.output2def(node)
        elif isinstance(node, LayerNode):
            block = self.layer2block(node)
        else:
            raise TypeError(f"Incorrect type: should be a node but is {node}")

        self._blocks[node.name] = block

    # ... SINGLE CONNECTION
    # def edge2wire(self, start: str, end: str, adapt: Optional[int]) -> None:
    #     """Create a wire for a given edge"""
    #     dest = self._blocks[end]
    #     if adapt is not None:
    #         dest = (dest, str(adapt))
    #     self._diag.connect(self._blocks[start], dest)

    def edges2wire(
        self, start: str, end_with_adaptation: dict[str, Optional[int]]
    ) -> None:
        """Create a wire for several edges with the same source"""
        targets = [
            self._blocks[e] if a is None else (self._blocks[e], str(a))
            for e, a in end_with_adaptation.items()
        ]
        self._diag.connect(self._blocks[start], targets)

    def input2expr(self, node: InputNode) -> swan.ExprBlock:
        """Convert an input node to an expression"""
        input_ = self.operator.add_input(node.name, node.var_type)
        return self._diag.add_expr_block(input_)

    def output2def(self, node: OutputNode) -> swan.DefBlock:
        """Convert an output node to a definition"""
        output = self.operator.add_output(node.name, node.var_type)
        return self._diag.add_def_block(output)

    def layer2block(self, node: LayerNode) -> swan.Block:
        """Convert a node of the graph to a block for Scade One Diagram"""
        converter_cls = get_layer_converter(node.layer.__class__)
        converter = converter_cls(
            layer=node.layer, module=self.module, constants=self.constants
        )
        block = converter.convert_2_block()
        block._luid = swan.Luid(node.name)
        self._diag._diagram_adder.add_block(block)
        return block

    def create_test_harness_body(
        self,
        test_harness: swan.TestHarness,
        module_body_name: str,
        inputs: list[IOSizeSingleInput],
        outputs: list[OutputNode],
        inputs_var: TestsInputsVar = None,
    ) -> None:
        """Create Test Harness body for testing main operator"""

        # We will create some input tests: by default, we set a 0
        # ... but we can specify manually some inputs
        def zeros(input_: IOSizeSingleInput) -> str:
            """Get swan tensors filled with zeros"""
            return "0" + " ".join(f"^{i}" for i in list(input_)[::-1] if i)

        inputs_test = [str2expr(zeros(i)) for i in inputs]
        for i, var in enumerate(inputs_var or []):
            # The utility `var2expr` will break the line returns
            # ... but the trick is to path the PPrinter for big arrays :)
            inputs_test[i] = var2expr(var)  # type: ignore

        diag = test_harness.add_diagram()

        operator_name = f"{module_body_name}::{module_body_name}"
        operator_call = add_block_from_id(operator_name, diag)
        # TODO: Add pragma `#pragma swt under_test #end`

        for i, input_ in enumerate(inputs_test, start=1):
            input_expr = swan.ExprBlock(input_)
            diag._diagram_adder.add_block(input_expr)
            diag.connect(input_expr, (operator_call, str(i)))

            for output in outputs:
                self._add_output_in_harness(output, operator_call, diag)

    def _add_output_in_harness(
        self,
        output: OutputNode,
        operator_call: swan.Block,
        diag: swan.Diagram,
    ) -> list[swan.DiagramObject]:
        """Add post-processing of model output in harness and return objects for diagram

        For example, for a "softmax", we want to get the index of higher value
        """
        output_name = output.swan_name

        if "softmax" in output_name.lower():
            shapes = [s for s in output.shape if s]
            max_idx = self.add_block_from_id("utils::max_index", sizes=[shapes[0]])
            max_idx._instance = op2map(max_idx.instance, sizes=shapes[1:])  # type: ignore

            for source, target, adapt in [
                (operator_call, max_idx, output_name),
                (max_idx, "_", "idx"),
                (max_idx, "_", "value"),
            ]:
                if target == "_":
                    target = get_underscore_def_block(diag)

                diag.connect((source, adapt), target)

        else:
            exit_def = get_underscore_def_block(diag)
            diag.connect(operator_call, exit_def)
