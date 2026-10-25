"""Transform a Keras Model into a Networkx Graph"""

import logging
from pathlib import Path
from typing import Generator, Optional, Union, cast

import networkx as nx  # type: ignore
from keras import KerasTensor, Model, layers  # type: ignore
from keras.models import load_model  # type: ignore

try:
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
except ImportError:
    pass  # matplotlib used for displaying graph of the networkx graph


from .graph_nodes import (
    NODE_COLORS,
    InputNode,
    LayerNode,
    NestedModelNode,
    Node,
    NodeKind,
    OutputNode,
)


LOGGER = logging.getLogger("keras_importer.graph")

ModelOrLayer = Union[Model, layers.Layer]


class ModelParser:
    """Parse Keras model for transforming to Swan Project"""

    def __init__(self, model: Union[str, Path, Model]) -> None:
        if isinstance(model, (str, Path)):
            path = Path(model)
            if not path.is_file():
                raise FileNotFoundError(f"Path '{path}' is not a model (not a file)")
            if path.suffix not in (".h5", ".keras"):
                raise AttributeError(f"Path '{path}' is not a model (wrong extension)")

            self.model = cast(Model, load_model(model))
            LOGGER.info(f"Loaded model from '{path}' successfully")
        elif isinstance(model, Model):
            self.model = model
        else:
            raise AttributeError(
                f"Wrong type of model (keras Model or path accepted but got {model}"
            )

        self.inputs: dict[str, InputNode] = {}
        self.outputs: dict[str, OutputNode] = {}
        self.nested_graphs: dict[str, nx.DiGraph] = {}
        self.graph = self._get_graph(self.model)
        self.data: dict[str, Node] = nx.get_node_attributes(self.graph, "data")

    @staticmethod
    def get_inputs(node: ModelOrLayer) -> list[KerasTensor]:
        """Get inputs of a layer or model in Keras"""
        if hasattr(node, "inputs"):
            return node.inputs
        inputs = getattr(node, "input", [])
        return inputs if isinstance(inputs, list) else [inputs]

    @staticmethod
    def get_outputs(node: ModelOrLayer) -> list[KerasTensor]:
        """Get outputs of a layer or model in Keras"""
        if hasattr(node, "outputs"):
            return node.outputs
        outputs = getattr(node, "output", [])
        return outputs if isinstance(outputs, list) else [outputs]

    def _process_input(
        self,
        node: KerasTensor,
        graph: nx.DiGraph,
        depths: dict[str, int],
        store_io: bool,
    ) -> None:
        """Process an input layer"""
        # We need a dedicated function because an input might be retrieved
        # by either "input" from model, or layers (and check that layer is an InputLayer)
        name = str(node.name)
        data = InputNode.from_input(node)
        graph.add_node(name, kind=NodeKind.INPUT, data=data)
        depths[name] = 0
        if store_io:
            self.inputs[name] = data

    # For each input, we have to store several information
    # to help creating the diagram, including the nb of input of layer
    @staticmethod
    def _enumerate_inbound_operations(
        layer: layers.Layer,
    ) -> Generator[tuple[int, layers.Layer], None, None]:
        for inbound in layer._inbound_nodes:
            for i, n in enumerate(inbound.parent_nodes, start=1):
                yield i, n.operation

        # layer.inbound_nodes / node.iterate_inbound() have been removed in Keras 3.0
        # an equivalent is to search in the `_keras_history`
        # ... see https://github.com/keras-team/keras/issues/21205#issuecomment-2828427677
        # tensors = layer.input if isinstance(layer.input, (list, tuple)) else [layer.input]
        # for tensor in tensors:
        #     if hasattr(tensor, '_keras_history'):
        #         inbound_layer, _, tensor_index = tensor._keras_history
        #         yield tensor_index, inbound_layer

                # ibl_eq_ge = inbound_layer.to_scade(owner_model, root_operator, graph)
                # ibl_eq = ibl_eq_ge.presentable
                # ibl_output = ibl_eq.lefts[tensor_index]
                # inputs.append((ibl_output, ibl_eq_ge, tensor_index))


    def _get_graph(self, model: Model, store_io: bool = True) -> nx.DiGraph:
        """Create a Directed Acyclic Graph from a Keras Model"""
        # ? TODO: Improve the way we store Inputs/Outputs ...
        # ... maybe it could be removed and replaced by parsing nodes to get IONodes
        graph = nx.DiGraph()
        # We will update the depth starting of 0 for inputs and increasing to 1 for each successor
        # (in case of branching, we will take the maximum depth of predecessors + 1)
        # One goal of the depth is to be able to show a nice graph

        depths: dict[str, int] = {}

        for input_ in self.get_inputs(model):
            self._process_input(input_, graph, depths, store_io)

        for layer in model.layers:
            if isinstance(layer, layers.InputLayer):
                self._process_input(layer, graph, depths, store_io)
                continue

            name = str(layer.name)
            if isinstance(layer, Model):
                graph.add_node(
                    name, kind=NodeKind.NESTED, data=NestedModelNode.from_layer(layer)
                )
                self.nested_graphs[name] = self._get_graph(layer, store_io=False)
            else:
                graph.add_node(
                    name, kind=NodeKind.LAYER, data=LayerNode.from_layer(layer)
                )

            inbounds = {
                op.name: (i, op.name, op.output.shape, op.dtype)
                for i, op in self._enumerate_inbound_operations(layer)
            }
            graph.add_edges_from(
                (il, name, {"shape": s, "dtype": d, "target": t, "target_idx": i})
                for il, (i, t, s, d) in inbounds.items()
            )

            try:
                depths[name] = 1 + max(depths.get(i, 0) for i in inbounds)
            except ValueError:
                depths[name] = 0  # defensive code

        for output in self.get_outputs(model):
            data = OutputNode.from_output(output)
            name = str(data.name)
            graph.add_node(name, kind=NodeKind.OUTPUT, data=data)
            graph.add_edge(data.layer.name, name, shape=data.shape, dtype=data.dtype)
            depths[name] = 1 + depths.get(data.layer.name, 100)
            if store_io:
                self.outputs[name] = data

        nx.set_node_attributes(graph, depths, "depth")

        return graph

    # Note: "Figure" used as string, in case Matplotlib not installed
    def get_graph(self, graph: Optional[nx.DiGraph] = None) -> "Figure":
        """Get Networkx Graph"""
        if graph is None:
            graph = self.graph
        fig, _ = plt.subplots()
        colors = [NODE_COLORS[data["kind"]] for _, data in graph.nodes(data=True)]
        pos = nx.multipartite_layout(graph, "depth", align="horizontal", scale=-1)
        nx.draw(
            graph,
            with_labels=True,
            pos=pos,
            node_color=colors,
            font_size=8,
            node_size=80,
            edge_color="grey",
        )
        edge_labels = {
            (s, e): f'{d["dtype"]} ^ {d["shape"]}' for s, e, d in graph.edges(data=True)
        }
        nx.draw_networkx_edge_labels(
            graph, pos, edge_labels=edge_labels, font_size=3, rotate=False
        )
        return fig
