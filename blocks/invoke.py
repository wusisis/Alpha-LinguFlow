import functools
import json
import threading
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

from environs import Env
from sqlalchemy import create_engine

from database import Database
from exceptions import (
    ApplicationInputTypeMismatch,
    ApplicationNotFound,
    AsyncExceptionHandler,
    InteractionError,
    InteractionNotFound,
    NoActiveVersion,
    NodeConstructError,
    VersionnNotFound,
    register_exception_handlers,
)
from model import Interaction
from observability import langfuse, span, trace
from resolver import Resolver, block
from scheduler import Edge, Graph

from .base import BaseBlock


class AsyncInvoker:
    """
    AsyncInvoker invokes an application with specified input, and returns an
    interaction id, which can be used for polling the result later.

    Example:

    ```
    invoker = AsyncInvoker(Database(...))
    interaction_id = invoker.invoke(user="...", app_id="...", input=...)

    result = None
    while not result:
        # Poll the interaction until the result is available
        interaction = invoker.poll(interaction_id)
        result = interaction.output
        # sleep some time here
    ```
    """

    def __init__(self, database: Database):
        self.resolver = Resolver()
        self.database = database

    def construct_graph_node(self, config: dict) -> BaseBlock:
        """
        Construct a graph node based on the given configuration.

        Args:
            config (dict): The configuration dictionary containing information about the node.

        Returns:
            BaseBlock: An instance of the constructed graph node.

        Raises:
            NodeConstructError: If there is an error during node construction.
        """
        name = config["name"]
        cls = self.resolver.lookup(name)
        if cls is None:
            raise NodeConstructError(f"name {name} not found")
        elif self.resolver.is_abstract(cls):
            raise NodeConstructError(
                f"{name} is an abstract type and can NOT be constructed"
            )
        properties = {}
        if not isinstance(config, dict):
            slots = config.slots
            if slots is None:
                slots = {}
        else:
            slots = config.get("slots") or {}
        for p, v in slots.items():
            if isinstance(v, dict):
                properties[p] = self.construct_graph_node(v)
            elif isinstance(v, list):
                properties[p] = [
                    self.construct_graph_node(x) if isinstance(x, dict) else x
                    for x in v
                ]
            else:
                properties[p] = v

        try:
            return cls(**properties)
        except Exception as e:
            raise NodeConstructError(f"construct {name} failed: {str(e)}") from e

    def initialize_graph(
        self, configuration: dict, skip_validation: bool = False
    ) -> Graph:
        """
        Initialize a graph based on the given configuration.

        Args:
            configuration (dict): The configuration for the graph, including nodes and edges.
            skip_validation (bo