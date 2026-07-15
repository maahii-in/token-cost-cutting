"""
Reranker Node

Responsibilities
----------------
1. Re-score retrieved documents
2. Sort documents by relevance
3. Keep only Top-K documents
4. Update AgentState
"""

from __future__ import annotations

from state import AgentState, Document
from config import settings
from common import get_logger
from common.token_counter import count_tokens

logger = get_logger(__name__)


class RerankerNode:
    """
    Re-ranks retrieved documents.

    Current:
        Uses Milvus similarity score.

    Future:
        CrossEncoder (BAAI/bge-reranker-base)
    """

    def __init__(self):

        self.top_k = settings.RERANK_TOP_K

        logger.info(
            f"Reranker initialized (Top-K={self.top_k})"
        )

    def __call__(self, state: AgentState) -> AgentState:

        logger.info("Starting reranking...")

        if not state.retrieved_docs:

            logger.warning("No retrieved documents.")

            state.reranked_docs = []

            return state

        before_tokens = self.total_tokens(
            state.retrieved_docs
        )

        reranked = self.rerank_documents(
            state.question,
            state.retrieved_docs,
        )

        after_tokens = self.total_tokens(
            reranked
        )

        state.reranked_docs = reranked

        state.token_usage["reranker"] = {

            "documents_before": len(
                state.retrieved_docs
            ),

            "documents_after": len(
                reranked
            ),

            "before_tokens": before_tokens,

            "after_tokens": after_tokens,

            "saved_tokens": before_tokens - after_tokens,

        }

        logger.info(
            f"Selected {len(reranked)} documents."
        )

        return state

    # --------------------------------------------------

    def rerank_documents(

        self,

        question: str,

        documents: list[Document],

    ) -> list[Document]:
        """
        Placeholder reranker.

        Later this method will use
        CrossEncoder.
        """

        ranked = sorted(

            documents,

            key=lambda doc: doc.score,

            reverse=True,

        )

        return ranked[: self.top_k]

    # --------------------------------------------------

    @staticmethod
    def total_tokens(
        documents: list[Document],
    ) -> int:

        return sum(

            count_tokens(doc.content)

            for doc in documents

        )