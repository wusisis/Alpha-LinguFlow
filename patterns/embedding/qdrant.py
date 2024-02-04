import hashlib
from typing import List

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointIdsList, PointStruct, VectorParams

from resolver import pattern

from ..secret import Secret
from .vectordb import VectorDB


@pattern(name="Qdrant")
class Qdrant(VectorDB):
    """
    VectorDB implementation using Qdrant.
    """

    def __init__(self, url: str, api_key: Secret = None):
        """
        Initialize a Qdrant instance.

        Args:
            url (str): The URL of the Qdrant server.
            api_key (Secret, optional): The API key for accessing Qdrant services. Defaults to None.
        """
        self.client = QdrantClient(url=url, api_key=api_key)

    def create_ns(self, ns: str, size: int):
        """
        Create a new namespace in Qdrant.

        Args:
            ns (str): The name of the namespace to create.
            size (int): The size of the vectors in the namespace.
        """
        self.client.recreate_collection(
            collection_name=ns,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )

    def delete_ns(self, ns: str):
        """
        Delete a namespace from Qdrant.

        Args:
            ns (str): The name of the namespace to delete.
        """
        self.client.delete_collection(collection_name=ns)

    def vec_id(s