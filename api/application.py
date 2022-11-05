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
                    slot