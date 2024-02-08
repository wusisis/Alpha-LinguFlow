from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    StringPromptTemplate,
    SystemMessagePromptTemplate,
)

from observability import event, span
from resolver import pattern

from .embedding import Namespace


@pattern(name="Few_Shot_Prompt_Template")
class FewShotPromptTemplate(StringPromptTemplate):
    """
    Template for generating prompts for few-shot learning.
    """

    namespace: Namespace = None
    prefix: str = ""
    suffix: str = ""
    example_prompt: str = ""

    def __init__(
        self,
        namespace: