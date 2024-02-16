import inspect
from collections import namedtuple
from typing import Any, Callable, Dict, List, Union

import networkx as nx

from blocks import BaseBlock
from exceptions import NodeException

from .rule import (
    EndpointExist,
    ExactlyOneInputAndOutput,
    GraphIsDAG,
    PortTypeMatch,
    RequiredInPortIsFit,
    Rule,
    TypeHasStrMethod,
)

Edge = namedtuple("Edge", ["source", "sink", "port", "case"])


class Graph:
    """
    The primary class of the scheduler module, which represents a DAG graph.

    When executed, it will run each node of the DAG until the last node (OutputBlock).
    """

    def __init__(
        self,
        nodes: Dict[str, BaseBlock],
        edges: List[Edge],
        skip_validation: bool = False,
    ):
        """
        Args:
            nodes (dict): the nodes of the DAG, composed of BaseBlock instances and their unique ids.
            edges (list): directed edges connecting the nodes, where their direction represents the flow of data.
            skip_validation (bool): whether the validity of the DAG graph needs to be checked.
        """
        super(Graph, self).__init__()
        self.g = nx.DiGraph()
        self.nodes = nodes
        for e in edges:
            self.g.add_edge(e.source, e.sink, port=e.port, case=e.case)

        if not skip_validation:
            self._validate(
                [
                    EndpointExist(),
                    GraphIsDAG(),
                    RequiredInPortIsFit(),
                    ExactlyOneInputAndOutput(),
                    PortTypeMatch(),
                    TypeHasStrMethod(),
                ]
            )

    def _validate(self, rules: List[Rule]):
        """
        Validates the DAG graph against a list of rules.

        Args:
            rules (list): List of rules to validate against.
        """
        for r in rules:
            r.check(self.g, self.nodes)

    def _reset(self):
        """
        Resets the data attribute of each node in the graph.
        """
        for n in self.g.nodes:
            if "data" in self.g.nodes[n]:
                del self.g.nodes[n]["data"]

    def run_node(
        self, node_id, node_callback: Callable[[str, Any], None] = None
    ) -> Any:
        """
        Runs a node in the graph and returns its output.

        Args:
            node_id (str): The id of the node to run.
            node_callback (callable): Optional callback function to be called after running the node.

        Returns:
            Any: The output of the node.
        """
        node = self.nodes[node_id]
        in_edges = self.g.in_edges(node_id, data=True)
        if len(in_edges) == 0:
            try:
                return node()
            except Exception as e:
                raise NodeException(node_id) from e

        signature = inspect.signature(node.__call__)
        node_params = {}

        # fill default values
        for k, p in signature.parameters.items():
            if p.default != inspect.Parameter.empty:
                node_params[k] = p.default

        # run upstreams and fill values
        for source_node, _, properties in in_edges:
            port = properties["port"]
            if "data" not in self.g.nodes[source_node]:
                self.g.nodes[source_node]["data"] = self.run_node(
                    source_node,
                    node_callback=node_callback,
                )
                if node_callback:
                    node_callback(source_node, self.g.nodes[source_node]["data"])

            if port is None or port not in signature.parameters:
                # the None port and unknown port is special, it's required
                if self.g.nodes[source_node]["data"] is None:
                    return None
                # if the edge has a filter, check if the value is match with the filter
                if (
                    properties["case"] is not None
                    and properties["case"] != self.g.nodes[source_node]["data"]
                ):
                    return None
                if port is not None:
                    node_params[port] = self.g.nodes[source_node]["data"]
            elif self.g.nodes[source_node]["data"] is not None:
                if (
                    properties["case"] is not None
                    and properties["case"] != self.g.nodes[source_node]["data"]
                ):
                    continue
                node_params[port] = self.g.nodes[source_node]["data"]

        # check if required params are filled
        leak_params = set(
            [k for k, p in signature.parameters.items() if p.kind != p.VAR_KEYWORD]
        )
        leak_params -= set(node_params.keys())
        if len(leak_params) > 0:
            # some params leaked
            return None

        try:
            return node(**node_params)
        except Exception as e:
            raise NodeException(node_id) from e

    def input_type(self) -> type:
        """
 