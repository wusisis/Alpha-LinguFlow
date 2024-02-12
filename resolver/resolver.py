import functools
import inspect
from typing import Dict, List, Optional, Union

from exceptions import DuplicatedNameError, DuplicatedTypeError, UnregisteredError


class Resolver:
    """
    The name resolver, used to register/resolve blocks and patterns.

    Example:

    ```
    @block(name='test_block')
    class TestBlock(BaseBlock):
        ...

    r = Resolver()

    assert type(r.lookup('test_block')) == type(TestBlock)
    ```
    """

    _block_list = []
    _pattern_list = []

    def __init__(self):
        # check _block_list and _pattern_list
        self.consistent_assert()

    def consistent_assert(self):
        """
        Checks if block and pattern definitions are valid.
        Raises errors any definition is not valid.
        """
        nameset = set()
        typeset = set()

        for i, n in enumerate(self._block_list + self._pattern_list):
            name = n["name"]
            if name in nameset:
                raise DuplicatedNameError(name)
            if n["class"] in typeset:
                raise DuplicatedTypeError(n["class"])
            nameset.add(name)
            typeset.add(n["class"])

            if n["category"] == "builtin":
                continue

            types = set()

            if not self.is_abstract(self.lookup(name)):
                # add slots for check
                slots = self.slots(name)
                for s in slots.values():
                    types.add(s.annotation)

            if i < len(