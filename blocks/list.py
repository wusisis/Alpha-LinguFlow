from resolver import block

from .base import BaseBlock


@block(name="List_Jion_to_Text", kind="data process")
class JoinList(BaseBlock):
    """
    JoinList join a str list to a single str.

    Example:

    ```
    node = JoinList(template="--{input}--", delimiter='\n')

    print(node(["test 1", "text 2", "text 3"]))
    ```

    Will output:

    ```
    --text 1--
    --text 2--
    --text 3--
    ```
    """

    def __init__(self, template: str, delimiter: str = "\n"):
        super(JoinList, self).__init__()
        self.template = template
        self.delimiter = delimiter

    def __call__(self, **kwargs)