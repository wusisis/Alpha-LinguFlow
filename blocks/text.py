from resolver import block

from .base import BaseBlock


@block(name="Text_Join_to_Dict", kind="data process")
class ComposeDict(BaseBlock):
    """
    ComposeDict compose multiple str into a dict.

    Example:

    ```
    node = ComposeDict()
    result = node(name="foo", value="bar", comment="barz")
    ```

    The result: `{"name": "foo", "value": "bar", "comment": "barz"}`
    """

    def __call__(self, **kwargs) -> dict:
        return kwargs


@block(name="Text_split_to_List", kind="data process")
class ListParser(