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