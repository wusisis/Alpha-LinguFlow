import inspect
from collections import namedtuple
from typing import Any, Callable, Dict, List, Union

import networkx as nx

from blocks import BaseBlock
from exceptions import NodeException

from .rule import (
    EndpointExist,
    ExactlyOneInputAndOutp