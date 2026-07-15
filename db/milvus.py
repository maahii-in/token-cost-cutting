"""
Milvus Client
"""

from __future__ import annotations

from pymilvus import MilvusClient

from config import settings
from common import get_logger

logger = get_logger(__name__)


class MilvusDB:

    def __init__(self):

        self.client = MilvusClient(

            uri=f"http://{settings.MILVUS_HOST}:{settings.MILVUS_PORT}"

        )

        logger.info("Milvus Connected")

    def search(

        self,

        collection_name: str,

        vector: list[float],

        limit: int = 5,

    ):

        return self.client.search(

            collection_name=collection_name,

            data=[vector],

            limit=limit,

        )

    def insert(

        self,

        collection_name: str,

        data,

    ):

        return self.client.insert(

            collection_name=collection_name,

            data=data,

        )

    def delete(

        self,

        collection_name: str,

        ids,

    ):

        return self.client.delete(

            collection_name=collection_name,

            ids=ids,

        )