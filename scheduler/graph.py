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
        node = sel