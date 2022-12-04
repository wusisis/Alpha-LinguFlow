import langchain.chains
from langchain.prompts.chat import BaseChatPromptTemplate
from langchain_core.language_models import BaseChatModel, BaseLanguageModel
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import StringPromptTemplate

from observability import span
from resolver import block

from .base import BaseBlock


@block(name="LLM", kind="llm")
class LLMChain(BaseBlock):
    """
    LLMChain render template with given text and pass the result to llm model.
    """

    def __init__(
        self, model: BaseLanguageModel, prompt_template_type: S