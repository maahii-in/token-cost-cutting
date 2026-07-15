"""
Deduplicator Node

Responsibilities
----------------
1. Remove duplicate documents
2. Remove near-duplicate documents
3. Preserve metadata
4. Reduce token cost
"""

from __future__ import annotations

from copy import deepcopy

from rapidfuzz import fuzz

from common import (
    count_documents_tokens,
    get_logger,
)
from state import AgentState, Document

logger = get_logger(__name__)


class DeduplicatorNode:
    """
    Remove duplicate and near-duplicate documents.
    """

    def __init__(
        self,
        similarity_threshold: int = 90,
    ) -> None:

        self.threshold = similarity_threshold

        logger.info(
            "Deduplicator initialized "
            "(threshold=%s)",
            self.threshold,
        )

    # =====================================================
    # Main Entry
    # =====================================================

    def __call__(
        self,
        state: AgentState,
    ) -> AgentState:

        logger.info(
            "Removing duplicate documents..."
        )

        if not state.compressed_docs:

            logger.info(
                "No documents to deduplicate."
            )

            state.token_usage["deduplicator"] = {
                "documents_before": 0,
                "documents_after": 0,
                "before_tokens": 0,
                "after_tokens": 0,
                "saved_tokens": 0,
            }

            return state

        try:

            before_count = len(
                state.compressed_docs
            )

            before_tokens = (
                count_documents_tokens(
                    state.compressed_docs
                )
            )

            unique_docs = self.remove_duplicates(
                state.compressed_docs
            )

            after_count = len(unique_docs)

            after_tokens = (
                count_documents_tokens(
                    unique_docs
                )
            )

            state.compressed_docs = unique_docs

            state.token_usage["deduplicator"] = {

                "documents_before": before_count,

                "documents_after": after_count,

                "before_tokens": before_tokens,

                "after_tokens": after_tokens,

                "saved_tokens":
                    before_tokens - after_tokens,

            }

            logger.info(

                "Deduplication complete: "
                "%s → %s documents",

                before_count,

                after_count,

            )

        except Exception:

            logger.exception(
                "Deduplication failed."
            )

        return state

    # =====================================================
    # Remove Duplicates
    # =====================================================

    def remove_duplicates(
        self,
        documents: list[Document],
    ) -> list[Document]:

        unique: list[Document] = []

        for document in documents:

            if self.is_duplicate(
                document,
                unique,
            ):
                continue

            unique.append(
                deepcopy(document)
            )

        return unique

    # =====================================================
    # Similarity Check
    # =====================================================

    def is_duplicate(
        self,
        document: Document,
        existing_docs: list[Document],
    ) -> bool:

        for existing in existing_docs:

            similarity = fuzz.ratio(

                document.content,

                existing.content,

            )

            if similarity >= self.threshold:

                return True

        return False