"""
Redis Client
"""

from __future__ import annotations

import redis

from config import settings
from common import get_logger

logger = get_logger(__name__)


class RedisDB:

    def __init__(self):

        self.client = redis.Redis(

            host=settings.REDIS_HOST,

            port=settings.REDIS_PORT,

            db=settings.REDIS_DB,

            decode_responses=True,

        )

        logger.info("Redis Connected")

    def set(

        self,

        key: str,

        value,

        ex: int | None = None,

    ):

        self.client.set(

            key,

            value,

            ex=ex,

        )

    def get(

        self,

        key: str,

    ):

        return self.client.get(key)

    def delete(

        self,

        key: str,

    ):

        self.client.delete(key)

    def exists(

        self,

        key: str,

    ):

        return self.client.exists(key)