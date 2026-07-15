"""
Compressor Node

Responsibilities
----------------
1. Remove empty lines
2. Remove duplicate lines
3. Normalize whitespace
4. Reduce token usage
5. Keep metadata intact
"""

from __future__ import annotations

from copy import deepcopy

from state import AgentState, Document
from config import settings
from common import get_logger
from common.token_counter import count_tokens

logger = get_logger(__name__)


class CompressorNode:
    """
    Compress retrieved documents before Prompt Builder.
    """

    def __init__(self):

        self.max_tokens = settings.MAX_DOCUMENT_TOKENS

        logger.info(
            f"Compressor initialized "
            f"(max_tokens={self.max_tokens})"
        )

    def __call__(self, state: AgentState) -> AgentState:

        logger.info("Compressing documents...")

        compressed_docs = []

        before_tokens = 0
        after_tokens = 0

        for document in state.reranked_docs:

            before_tokens += count_tokens(document.content)

            compressed = self.compress(document)

            after_tokens += count_tokens(compressed.content)

            compressed_docs.append(compressed)

        state.compressed_docs = compressed_docs

        state.token_usage["compressor"] = {

            "before_tokens": before_tokens,

            "after_tokens": after_tokens,

            "saved_tokens": before_tokens - after_tokens,

            "documents": len(compressed_docs)

        }

        logger.info(

            f"Compression Finished | "

            f"{before_tokens} -> {after_tokens}"

        )

        return state

    # ----------------------------------------------------

    def compress(

        self,

        document: Document

    ) -> Document:

        doc = deepcopy(document)

        text = doc.content

        text = self.remove_empty_lines(text)

        text = self.remove_duplicate_lines(text)

        text = self.normalize_spaces(text)

        text = self.truncate(text)

        doc.content = text

        return doc

    # ----------------------------------------------------

    @staticmethod
    def remove_empty_lines(text: str) -> str:

        lines = [

            line.strip()

            for line in text.splitlines()

            if line.strip()

        ]

        return "\n".join(lines)

    # ----------------------------------------------------

    @staticmethod
    def remove_duplicate_lines(text: str) -> str:

        seen = set()

        output = []

        for line in text.splitlines():

            line = line.strip()

            if line in seen:

                continue

            seen.add(line)

            output.append(line)

        return "\n".join(output)

    # ----------------------------------------------------

    @staticmethod
    def normalize_spaces(text: str) -> str:

        return " ".join(text.split())

    # ----------------------------------------------------

    def truncate(

        self,

        text: str

    ) -> str:

        if count_tokens(text) <= self.max_tokens:

            return text

        words = text.split()

        result = []

        for word in words:

            result.append(word)

            candidate = " ".join(result)

            if count_tokens(candidate) >= self.max_tokens:

                break

        return " ".join(result)