"""
Memory Node

Responsibilities
----------------
1. Load recent conversation from Redis
2. Load long-term memory from PostgreSQL
3. Merge memories
4. Remove duplicates
5. Update AgentState
"""

from __future__ import annotations

from state import AgentState
from db import PostgresDB, RedisDB
from common import (
    get_logger,
    count_documents_tokens,
)

logger = get_logger(__name__)


class MemoryNode:
    """
    Loads conversational memory from Redis and PostgreSQL.
    """

    MEMORY_LIMIT = 5

    def __init__(self) -> None:

        self.postgres = PostgresDB()
        self.redis = RedisDB()

        logger.info("Memory Node Initialized")

    # ---------------------------------------------------------

    def __call__(
        self,
        state: AgentState,
    ) -> AgentState:

        logger.info("Loading memories...")

        recent = self.get_recent_memory()

        history = self.get_long_term_memory()

        memories = self.merge_memories(
            recent,
            history,
        )

        state.memories = memories

        state.token_usage["memory"] = {

            "documents": len(memories),

            "tokens": count_documents_tokens(memories),

        }

        logger.info(
            "Loaded %s memories",
            len(memories),
        )

        return state

    # =========================================================
    # Redis
    # =========================================================

    def get_recent_memory(self) -> list[str]:
        """
        Retrieve recent conversation from Redis.
        """

        try:

            memory = self.redis.get(
                "recent_memory"
            )

            if memory:

                return [str(memory)]

        except Exception:

            logger.exception(
                "Failed to load recent memory."
            )

        return []

    # =========================================================
    # PostgreSQL
    # =========================================================

    def get_long_term_memory(
        self,
    ) -> list[str]:
        """
        Retrieve long-term memory.
        """

        query = """
            SELECT memory
            FROM memories
            ORDER BY created_at DESC
            LIMIT %s;
        """

        try:

            rows = self.postgres.fetch_all(

                query,

                (self.MEMORY_LIMIT,),

            )

            return [

                row["memory"]

                for row in rows

                if row.get("memory")

            ]

        except Exception:

            logger.exception(
                "Failed to load long-term memory."
            )

            return []

    # =========================================================
    # Merge
    # =========================================================

    @staticmethod
    def merge_memories(

        recent: list[str],

        history: list[str],

    ) -> list[str]:
        """
        Merge recent and historical memories.
        """

        seen = set()

        merged: list[str] = []

        for memory in recent + history:

            clean = memory.strip()

            if not clean:

                continue

            if clean in seen:

                continue

            seen.add(clean)

            merged.append(clean)

        return merged