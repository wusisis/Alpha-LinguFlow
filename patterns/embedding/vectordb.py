from abc import ABC, abstractmethod
from typing import List, TypeVar

from resolver import pattern

T = TypeVar("T")


@pattern(name="VectorDB")
class VectorDB(ABC):
    """
    Abstract base class for vector databases.
    """

    @abstractmethod
    def vec_id