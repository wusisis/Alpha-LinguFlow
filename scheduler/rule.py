
import builtins
import inspect
from abc import ABC, abstractmethod
from typing import Any, Dict

import networkx as nx

from blocks import BaseBlock
from exceptions import GraphCheckError


class NotDAGError(GraphCheckError):
    """
    NotDAGError indicates that the graph is not a DAG (has cycle, has orphaned node .etc.)
    """

    def __init__(self):
        super(NotDAGError, self).__init__("graph is not a valid DAG")


class PortMismatchError(GraphCheckError):
    """
    PortMismatchError indicates that the in port at the downstream node can not accept the data
    produced by the out port at the upstream node since the data types are incompatible.
    """

    def __init__(self, source: str, sink: str, port: str):
        super(PortMismatchError, self).__init__(
            f"port type mismatch on {sink}.{port} with {source}"
        )


class EndpointNotExistError(GraphCheckError):
    """
    EndpointNotExistError indicates that an edge connected to a node that is not in the graph.
    """

    def __init__(self, node: str, port: str = None):
        if port is not None:
            node += "." + port
        super(EndpointNotExistError, self).__init__(f"edge endpoint {node} not exist")


class PortNotConnectedError(GraphCheckError):
    """
    PortNotConnectedError indicates that the in port at the downstream node requires a
    value to fill, but no edges connect to that port.
    """

    def __init__(self, node: str, port: str):
        super(PortNotConnectedError, self).__init__(f"port {node}.{port} not connected")


class InputOutputCountError(GraphCheckError):
    """
    InputOutputCountError indicates that the graph breaks the rule that there should
    be exactly one input and output node in the DAG.
    """

    def __init__(self, input_count: int, output_count: int):
        super(InputOutputCountError, self).__init__(
            "expect exactly one input and output block, "
            f"got {input_count} input blocks and {output_count} output blocks",
        )


class PatternNoStrMethodError(GraphCheckError):
    """
    PatternNoStrMethodError indicates that a Pattern type does not have a __str__ method
    but has been passed between nodes.

    The __str__ method is required if a type is to be passed between nodes.
    """

    def __init__(self, _type: type) -> None:
        super(PatternNoStrMethodError, self).__init__(
            f'{_type} does not have a "__str__" method'
        )


class Rule(ABC):
    """
    An abstract class for graph checking rules.

    Rules are used for checking the validity of a graph.