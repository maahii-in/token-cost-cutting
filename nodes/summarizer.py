"""
Summarizer Node

Responsibilities
----------------
1. Summarize long responses
2. Generate conversation memory
3. Store summary in AgentState
4. Track token reduction
"""

from __future__ import annotations

from state import AgentState
from common import get_logger
from common.token_counter import count_tokens

logger = get_logger(__name__)


class SummarizerNode:
    """
    Summarize long responses and prepare memory.
    """

    def __init__(self):

        logger.info("Summarizer Node Initialized")

    def __call__(self, state: AgentState) -> AgentState:

        logger.info("Summarizing response...")

        if not state.response:

            logger.warning("No response to summarize.")

            return state

        original = state.response

        summary = self.create_summary(original)

        state.metadata["summary"] = summary

        state.token_usage["summarizer"] = {

            "before_tokens": count_tokens(original),

            "after_tokens": count_tokens(summary),

            "saved_tokens": (

                count_tokens(original)

                - count_tokens(summary)

            )

        }

        logger.info("Summary generated.")

        return state

    # -----------------------------------------------------

    def create_summary(
        self,
        text: str,
        max_sentences: int = 3,
    ) -> str:
        """
        Simple extractive summarization.

        Later this will become
        an LLM-based summarizer.
        """

        sentences = [

            sentence.strip()

            for sentence in text.split(".")

            if sentence.strip()

        ]

        if len(sentences) <= max_sentences:

            return text

        summary = ". ".join(

            sentences[:max_sentences]

        )

        return summary + "."