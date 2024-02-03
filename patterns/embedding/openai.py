from typing import List

import requests
from openai import OpenAI

from exceptions import EmbeddingError
from resolver import pattern

from ..secret import Secret
from .embedding import EmbeddingModel


@pattern(name="OpenAI_Embedding")
class OpenAIEmbedding(EmbeddingModel):
    """
    Embedding