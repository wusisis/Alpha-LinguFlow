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
            skip_validation (bool, optional): Whether to skip validation of the graph. Defaults to False.

        Returns:
            Graph: The initialized graph.
        """
        edges = []
        for edge in configuration["edges"]:
            edges.append(
                Edge(
                    source=edge.get("src_block"),
                    sink=edge.get("dst_block"),
                    port=edge.get("dst_port"),
                    case=edge.get("case"),
                )
            )
        nodes = {}
        for node in configuration["nodes"]:
            nodes[node.get("id")] = self.construct_graph_node(node)
        return Graph(nodes, edges, skip_validation)

    def invoke(
        self,
        user: str,
        app_id: str,
        input: Union[str, dict, list],
        version_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> str:
        """
        Invoke the specified application with the given input.

        Args:
            input (Union[str, dict, list]): The input data for the application,
                which can be a string, dictionary, or list.
            app_id (str): The ID of the application to invoke.
            version_id (str): The version to invoke, by default the active_version of
                the application will be used.

        Returns:
            str: The ID of the interaction created for this invocation.
        """
        app = self.database.get_application(app_id)
        if not app:
            raise ApplicationNotFound(app_id)
        if not version_id:
            if not app.active_version:
                raise NoActiveVersion(app_id)
            version_id = app.active_version
        version = self.database.get_version(version_id)
        if not version:
            raise VersionnNotFound(version_id)
        graph = self.initialize_graph(version.configuration)
        if type(input) != graph.input_type():
            raise ApplicationInputTypeMismatch(graph.input_type(), type(input))

        _id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        self.database.create_interaction(
            Interaction(
                id=_id,
                user=user,
                app_id=app_id,
                version_id=version_id,
                created_at=created_at,
                updated_at=created_at,
                output=None,
                data=None,
                error=None,
            )
        )

        @trace(id=_id, name=app.name, user_id=user, session_id=session_id)
        def async_task(input: Union[str, dict, list]) -> str:
            h = AsyncExceptionHandler()
            register_exception_handlers(h)
            try:
                output = graph.run(
                    input,
                    context={
                        "app_id": app_id,
                        "version_id": version_id,
                        "interaction_id": _id,
                        "user": user,
                        "session_id": session_id,
                    },
                    node_callback=lambda *args: self.database.update_interaction(
                        _id,
                        {
                            "data": graph.data,
                        },
                    ),
                )
                self.database.update_interaction(_id, {"output": output})
                return output
            except Exception as e:
                r = h.render(e)
                self.database.update_interaction(
              