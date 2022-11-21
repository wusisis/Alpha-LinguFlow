from typing import List

from resolver import block

from .base import InputBlock


@block(name="Text_Input", kind="input & output")
class TextInput(InputBlock):
    """
    A input block that accepts a text as the DAG input.
    """

    def input(self, text: str):
        self.text = text

    def __call__(self) -> str:
        return self.text


@block(name="List_Input", kind="input & output")
class ListInput(InputBlock):
    """
    A input block that accpets a list of t