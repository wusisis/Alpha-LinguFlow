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

        parameters = self.resolve_params(par