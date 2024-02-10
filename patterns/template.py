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
        namespace: Namespace,
        prefix: str,
        suffix: str,
        example_prompt: str,
    ):
        """
        Initialize the FewShotPromptTemplate with the provided namespace, prefix, suffix, and example prompt.

        Args:
            namespace (Namespace): The namespace for retrieving examples.
            prefix (str): The prefix for the prompt.
            suffix (str): The suffix for the prompt.
            example_prompt (str): The example prompt format.
        """
        super(FewShotPromptTemplate, self).__init__(
            input_variables=list(
                set(
                    PromptTemplate.from_template(prefix).input_variables
                    + PromptTemplate.from_template(suffix).input_variables
                )
            ),
        )
        self.namespace = namespace
        self.prefix = prefix
        self.suffix = suffix
        self.example_prompt = example_prompt

    @span(name="few shot prompt format")
    def format(self, text: str, **kwargs) -> str:
        """
        Format the text with examples retrieved from the namespace.

        Args:
            text (str): The text to format.
            **kwargs