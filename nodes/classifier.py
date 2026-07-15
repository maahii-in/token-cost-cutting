"""
Classifier Node

Responsible for identifying the type of user query.

Query Types
-----------
- chat
- retrieval
- reasoning
- tool
- hybrid
"""

from __future__ import annotations

from typing import Dict, List

from state import AgentState
from common import get_logger, count_tokens

logger = get_logger(__name__)


class ClassifierNode:
    """
    Determines the execution path for a user query.
    """

    CHAT_KEYWORDS = {
        "hi",
        "hello",
        "hey",
        "thanks",
        "thank you",
        "bye",
        "good morning",
        "good evening",
    }

    RETRIEVAL_KEYWORDS = {
        "invoice",
        "document",
        "pdf",
        "policy",
        "contract",
        "status",
        "payment",
        "report",
        "email",
        "customer",
        "ticket",
    }

    TOOL_KEYWORDS = {
        "create",
        "delete",
        "restart",
        "shutdown",
        "start",
        "stop",
        "deploy",
        "execute",
        "run",
        "install",
    }

    REASONING_KEYWORDS = {
        "why",
        "how",
        "explain",
        "difference",
        "compare",
        "analysis",
        "analyze",
        "design",
        "architecture",
        "optimize",
    }

    def __init__(self):

        logger.info("Classifier Node Initialized")

    def __call__(self, state: AgentState) -> AgentState:
        """
        Execute the classifier.
        """

        question = state.question.strip()

        logger.info(f"Question : {question}")

        query_type = self.classify(question)

        logger.info(f"Query Type : {query_type}")

        state.query_type = query_type

        state.token_usage["classifier"] = {
            "tokens": count_tokens(question),
            "query_type": query_type,
        }

        return state

    def classify(self, question: str) -> str:

        q = question.lower()

        if self._contains(q, self.CHAT_KEYWORDS):
            return "chat"

        retrieval = self._contains(
            q,
            self.RETRIEVAL_KEYWORDS,
        )

        reasoning = self._contains(
            q,
            self.REASONING_KEYWORDS,
        )

        tool = self._contains(
            q,
            self.TOOL_KEYWORDS,
        )

        if retrieval and reasoning:
            return "hybrid"

        if retrieval:
            return "retrieval"

        if tool:
            return "tool"

        return "reasoning"

    @staticmethod
    def _contains(
        question: str,
        keywords: set[str],
    ) -> bool:

        return any(
            keyword in question
            for keyword in keywords
        )