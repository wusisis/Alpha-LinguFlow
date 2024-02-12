import functools
import inspect
from typing import Dict, List, Optional, Union

from exceptions import DuplicatedNameError, DuplicatedTypeError, UnregisteredError


class Resolver:
    """
    The name resolver, used to register/resolve blocks and patterns.

    Example:

    ```
    @block(name='