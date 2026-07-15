"""
Prompt Builder Node

Responsibilities
----------------
1. Load system prompt
2. Add memory
3. Add retrieved context
4. Add user question
5. Respect token budget
"""

from __future__ import annotations

from common import (
    get_logger,
    count_tokens,
)

from config import settings
from prompts import SYSTEM_PROMPT
from state import AgentState

logger = get_logger(__name__)


class PromptBuilderNode:
    """
    Builds the final prompt sent to the LLM.
    """

    def __init__(self) -> None:

        self.max_tokens = settings.MAX_PROMPT_TOKENS

        logger.info(
            "Prompt Builder Initialized "
            "(budget=%s tokens)",
            self.max_tokens,
        )

    # =====================================================
    # Main Entry
    # =====================================================

    def __call__(
        self,
        state: AgentState,
    ) -> AgentState:

        logger.info("Building prompt...")

        try:

            prompt = self.build_prompt(state)

            state.prompt = prompt

            total_tokens = count_tokens(prompt)

            state.token_usage["prompt_builder"] = {

                "tokens": total_tokens,

                "max_tokens": self.max_tokens,

            }

            logger.info(
                "Prompt built (%s tokens)",
                total_tokens,
            )

        except Exception:

            logger.exception(
                "Prompt Builder failed."
            )

            raise

        return state

    # =====================================================
    # Build Prompt
    # =====================================================

    def build_prompt(
        self,
        state: AgentState,
    ) -> str:

        sections = [

            self.system_section(),

            self.memory_section(state),

            self.context_section(state),

            self.question_section(state),

        ]

        prompt = "\n\n".join(

            section

            for section in sections

            if section

        )

        return self.fit_budget(prompt)

    # =====================================================
    # Sections
    # =====================================================

    def system_section(self) -> str:

        return f"# SYSTEM\n{SYSTEM_PROMPT}"

    def memory_section(
        self,
        state: AgentState,
    ) -> str:

        if not state.memories:

            return ""

        memories = "\n".join(

            f"- {memory}"

            for memory in state.memories

        )

        return f"# MEMORY\n{memories}"

    def context_section(
        self,
        state: AgentState,
    ) -> str:

        if not state.compressed_docs:

            return ""

        parts: list[str] = []

        for document in state.compressed_docs:

            parts.append(
                f"[{document.source}]"
            )

            parts.append(
                document.content
            )

            parts.append("")

        return "# CONTEXT\n" + "\n".join(parts)

    def question_section(
        self,
        state: AgentState,
    ) -> str:

        return (
            "# QUESTION\n"
            f"{state.question}"
        )

    # =====================================================
    # Token Budget
    # =====================================================

    def fit_budget(
        self,
        prompt: str,
    ) -> str:

        if count_tokens(prompt) <= self.max_tokens:

            return prompt

        logger.warning(
            "Prompt exceeds token budget."
        )

        words = prompt.split()

        output: list[str] = []

        for word in words:

            output.append(word)

            candidate = " ".join(output)

            if (
                count_tokens(candidate)
                >= self.max_tokens
            ):
                break

        logger.info(
            "Prompt truncated."
        )

        return " ".join(output)