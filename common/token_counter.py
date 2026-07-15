"""
Token Counter Utilities
"""

from __future__ import annotations

import tiktoken

ENCODING = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """
    Count tokens in a string.
    """
    if not text:
        return 0

    return len(ENCODING.encode(text))


def count_documents_tokens(documents) -> int:
    """
    Count tokens across multiple documents.
    """

    total = 0

    for document in documents:

        if hasattr(document, "content"):

            total += count_tokens(document.content)

        elif isinstance(document, str):

            total += count_tokens(document)

    return total


def count_messages(messages: list[dict]) -> int:
    """
    Count tokens in chat messages.
    """

    total = 0

    for message in messages:

        total += count_tokens(
            message.get("content", "")
        )

    return total