"""
Retriever Node

Responsibilities
----------------
1. Generate query embedding
2. Search Milvus
3. Convert search results into Document objects
4. Update AgentState
5. Track retrieval metrics
"""

from __future__ import annotations

from typing import Any

from common import (
    count_documents_tokens,
    get_logger,
)
from config import settings
from db import MilvusDB
from state import AgentState, Document

logger = get_logger(__name__)


class RetrieverNode:
    """
    Retrieve relevant documents from Milvus.
    """

    def __init__(self) -> None:

        self.milvus = MilvusDB()

        logger.info("Retriever Node Initialized")

    # =====================================================
    # Main Entry
    # =====================================================

    def __call__(
        self,
        state: AgentState,
    ) -> AgentState:

        logger.info("Retriever Started")

        try:

            embedding = self.generate_embedding(
                state.question
            )

            results = self.search(embedding)

            documents = self.parse_results(results)

            state.retrieved_docs = documents

            state.token_usage["retriever"] = {

                "documents": len(documents),

                "tokens": count_documents_tokens(
                    documents
                ),

            }

            logger.info(
                "Retrieved %s documents.",
                len(documents),
            )

        except Exception:

            logger.exception(
                "Retriever failed."
            )

            state.retrieved_docs = []

        return state

    # =====================================================
    # Embedding
    # =====================================================

    def generate_embedding(
        self,
        question: str,
    ) -> list[float]:
        """
        Generate embedding.

        Placeholder implementation.

        Later replace with SentenceTransformer
        or your vLLM embedding endpoint.
        """

        logger.info(
            "Generating embedding..."
        )

        return [0.1] * 768

    # =====================================================
    # Milvus Search
    # =====================================================

    def search(
        self,
        embedding: list[float],
    ) -> Any:

        logger.info(
            "Searching Milvus..."
        )

        return self.milvus.search(

            collection_name=settings.MILVUS_COLLECTION,

            vector=embedding,

            limit=settings.TOP_K,

        )

    # =====================================================
    # Result Parsing
    # =====================================================

    def parse_results(
        self,
        results: Any,
    ) -> list[Document]:

        documents: list[Document] = []

        if not results:

            logger.warning(
                "No documents returned."
            )

            return documents

        for hit in results[0]:

            entity = hit.get("entity", {})

            documents.append(

                Document(

                    id=str(
                        entity.get(
                            "id",
                            "",
                        )
                    ),

                    content=entity.get(
                        "content",
                        "",
                    ),

                    score=float(
                        hit.get(
                            "distance",
                            0.0,
                        )
                    ),

                    source=entity.get(
                        "source",
                        "",
                    ),

                    metadata=entity,

                )

            )

        return documents