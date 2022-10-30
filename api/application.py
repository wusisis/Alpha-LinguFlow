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
    VersionMetadat