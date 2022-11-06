import inspect
import json
import uuid
from datetime import datetime
from typing import Dict, List

from environs import Env
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from langfuse import Langfuse
from sqlalchemy import create_engine

import patterns
import plugins
from api.api_schemas import (
    ApplicationBlocksResponse,
    ApplicationCreate,
    ApplicationCreateResponse,
    ApplicationInfo,
    ApplicationInfoResponse,
    ApplicationListResponse,
    ApplicationPatternsResponse,
    ApplicationRun,
    ApplicationRunResponse,
    ApplicationVersionCreate,
    ApplicationVersionInfo,
    AppMetadata,
    BlockInfo,
    InteractionInfo,
    InteractionInfoResponse,
    InteractionScore,
    ItemCreateResponse,
    ItemDeleteResponse,
    ItemUpdateResponse,
    Parameter,
    PatternInfo,
    User,
    VersionCreateResponse,
    VersionInfoResponse,
    VersionListResponse,
    VersionMetadata,
)
from blocks import AsyncInvoker
from database import Database
from exceptions import ApplicationNotFound, InteractionNotFound
from model import Application, ApplicationVersion
from resolver import Resolver

router = InferringRouter()


@cbv(router)
class ApplicationView:
    """
    The router class for LinguFlow. Any new api should be added here.
    """

    def __init__(self):
        env = Env()
        env.read_env()
        self.database = Database(create_engine(env.str("DATABASE_URL")))
        self.invoker = AsyncInvoker(self.database)
        self.resolver = Resolver()

    def resolve_params(self, params: Dict[str, inspect.Parameter]) -> List[Parameter]:
        """
        Resolves the parameters of a function.

        Args:
            params (Dict[str, inspect.Parameter]): A dictionary
                mapping parameter names to inspect.Parameter objects.

        Returns:
            List[Parameter]: A list of Parameter objects representing the resolved parameters.

        Example:
        ```
        def foo(x: int, y: bool) -> bool:
            ...

        signature = inspect.signature(foo)
        params = dict(signature.parameters)

        parameters = self.resolve_params(params)
        ```
        """
        ss = []
        for sname, param in params.items():
            p = Parameter(
                name=sname,
                class_name=self.resolver.relookup(param.annotation),
            )
            if param.default != inspect.Parameter.empty:
                p.default = param.default
            if param.kind == param.VAR_KEYWORD:
                p.is_variable_keyword = True
            ss.append(p)
        return ss

    @router.get("/patterns")
    def patterns(self) -> ApplicationPatternsResponse:
        """
        Retrieves application patterns based on resolver information.

        Returns:
            ApplicationPatternsResponse: A response containing a list of PatternInfo objects.
        """
        names = self.resolver.names()
        patterns = []
        for name in names:
            if (
                self.resolver.lookup(name, "category") == "type"
                or self.resolver.lookup(name, "category") == "builtin"
            ):
                pi = PatternInfo(
                    name=name,
                    alias=self.resolver.lookup(name, "alias"),
                    candidates=self.resolver.candidates(name),
                    slots=None,
                )
                if (not self.resolver.is_abstract(self.resolver.lookup(name))) and (
                    self.resolver.lookup(name, "category") == "type"
                ):
                    pi.slots = self.resolve_params(self.resolver.slots(name))
                patterns.append(pi)
        return ApplicationPatternsResponse(patterns=patterns)

    @router.get("/blocks")
    def blocks(self) -> ApplicationBlocksResponse:
        """
        Retrieves application blocks based on resolver information.

        Returns:
            ApplicationBlocksResponse: A response containing a list of BlockInfo objects.
        """
        names = self.resolver.names()
        blocks = []
        for name in names:
            if self.resolver.lookup(name, "category") == "block":
                blocks.append(
                    BlockInfo(
                        name=name,
                        alias=self.resolver.lookup(name, "alias"),
                        dir=self.resolver.lookup(name, "dir"),
                        slots=self.resolve_params(self.resolver.slots(name)),
                        inports=self.resolve_params(self.resolver.inports(name)),
                        outport=self.resolver.relookup(self.resolver.outport(name)),
                    )
                )

        return ApplicationBlocksResponse(blocks=blocks)

    @router.get("/applications/{application_id}")
    def get_app(self, application_id: str) -> ApplicationInfoResponse:
        """
        Get information about a specific application.

        Args:
            application_id (str): The ID of the application to retrieve.

        Returns:
            ApplicationInfoResponse: Information about the application, including its ID, name,
                active version, creation timestamp, and last update timestamp.
        """
        app = self.database.get_application(application_id)

        return ApplicationInfoResponse(
            application=(
                ApplicationInfo(
                    id=app.id,
                    name=app.name,
                    user=app.user,
                    langfuse_public_key=app.langfuse_public_key,
                    langfuse_secret_key=app.langfuse_secret_key,
                    active_version=app.active_version,
                    created_at=int(app.created_at.timestamp()),
                    updated_at=int(app.updated_at.timestamp()),
                )
                if app
                else None
            )
        )

    @router.get("/applications")
    def list_app(self) -> ApplicationListResponse:
        """
        Retrieve a list of applications.

        Returns:
            ApplicationListResponse: The response containing a list of applications.
        """
        apps = self.database.list_applications()
        return ApplicationListResponse(
            applications=[
                ApplicationInfo(
                    id=app.id,
                    name=app.name,
                    user=app.user,
                    langfuse_public_key=app.langfuse_public_key,
                    langfuse_secret_key=app.langfuse_secret_key,
                    active_version=app.active_version,
                    created_at=int(app.created_at.timestamp()),
                    updated_at=int(app.updated_at.timestamp()),
                )
                for app in apps
            ]
        )

    @router.post("/applications")
    def create_app(
        self, request: Request, application: ApplicationCreate
    ) -> ApplicationCreateResponse:
        """
        Endpoint to create a new application.

        Args:
            application (ApplicationCreate): The application data to create.

        Returns:
            ApplicationCreateResponse: The response containing the ID of the created application.
        """
        created_at = datetime.utcnow()
        _id = str(uuid.uuid4())
        self.database.create_application(
            Application(
                id=_id,
                name=application.name,
                user=request.state.user,
                langfuse_public_key=application.langfuse_public_key,
                langfuse_secret_key=application.langfuse_secret_key,
                created_at=created_at,
                updated_at=created_at,
            )
        )
        return ApplicationCreateResponse(id=_id)

    @router.post("/applications/{application_id}/async_run")
    def async_run_app(
        self, request: Request, application_id: str, config: ApplicationRun
    ) -> ApplicationRunResponse:
        """
        Asynchronously runs an application with the specified ID and configuration.

        Args:
            application_id (str): The ID of the application to run.
            config (ApplicationRun): The configuration for running the application.

        Returns:
            ApplicationRunResponse: The response containing the interaction ID which is
                used for polling running result latter.
        """
        return ApplicationRunResponse(
            id=self.invoker.invoke(
                user=request.state.user,
                app_id=application_id,
                input=config.input,
                session_id=config.session_id,
            )
        )

    @router.get("/interactions/{interaction_id}")
    def get_interaction(self, interaction_id: str) -> InteractionInfoResponse:
        """
        Retrieves information about a specific interaction by its ID.

        Args:
            interaction_id (str): The ID of the interaction to retrieve.

        Returns:
            InteractionInfoResponse: An object containing information about the interaction.
        """
        interaction = self.invoker.poll(interaction_id)
        if interaction is not None and interaction.error is not None:
            return JSONResponse(**interaction.error)
        return InteractionInfoResponse(
    