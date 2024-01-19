import json
from typing import Set


class NodeException(Exception):
    """
    Exceptions raised from a DAG node.

    Usage:

    ```
    try:
        node.run(...)
    except Exception as e:
        raise NodeException(node.id) from e
    ```
    """

    def __init__(self, node_id: str):
        self.node_id = node_id


class DuplicatedNameError(Exception):
    """
    DuplicatedNameError indicates that two different blocks have the same name.
    """

    def __init__(self, name: str):
        super(DuplicatedNameError, self).__init__(f"name {name} is duplicated")


class DuplicatedTypeError(Exception):
    """
    DuplicatedTypeError indicates that the same block class has been registered
    multiple times with different names.
    """

    def __init__(self, typ: type):
        super(DuplicatedTypeError, self).__init__(f"type {typ} is duplicated")


class UnregisteredError(Exception):
    """
    UnregisteredError indicates that a nam