"""
LLM Node

Responsibilities
----------------
1. Send prompt to Groq
2. Receive response
3. Store response
4. Track token usage
5. Handle API failures gracefully
"""

from __future__ import annotations

from groq import Groq

from common import (
    count_tokens,
    get_logger,
)
from config import settings
from state import AgentState

logger = get_logger(__name__)


class LLMNode:
    """
    Executes the final LLM request.
    """

    def __init__(self) -> None:

        self.client = Groq(
            api_key=settings.GROQ_API_KEY.get_secret_value(),
        )

        self.model = settings.GROQ_MODEL

        logger.info(
            "LLM initialized (%s)",
            self.model,
        )

    # =====================================================
    # Main Entry
    # =====================================================

    def __call__(
        self,
        state: AgentState,
    ) -> AgentState:

        if not state.prompt:

            raise ValueError(
                "Prompt is empty."
            )

        logger.info("Calling Groq...")

        try:

            response = self.generate_response(
                state.prompt
            )

            state.response = response

            input_tokens = count_tokens(
                state.prompt
            )

            output_tokens = count_tokens(
                response
            )

            state.token_usage["llm"] = {

                "model": self.model,

                "input_tokens": input_tokens,

                "output_tokens": output_tokens,

                "total_tokens": (
                    input_tokens
                    + output_tokens
                ),

            }

            logger.info(
                "LLM response generated."
            )

        except Exception:

            logger.exception(
                "Groq request failed."
            )

            raise

        return state

    # =====================================================
    # Generate Response
    # =====================================================

    def generate_response(
        self,
        prompt: str,
    ) -> str:

        completion = self.client.chat.completions.create(

            model=self.model,

            temperature=0.2,

            max_tokens=1024,

            messages=[

                {
                    "role": "system",
                    "content": (
                        "You are an expert AI assistant."
                    ),
                },

                {
                    "role": "user",
                    "content": prompt,
                },

            ],

        )

        if not completion.choices:

            raise RuntimeError(
                "Groq returned no response."
            )

        message = completion.choices[0].message.content

        if not message:

            raise RuntimeError(
                "Empty response from Groq."
            )

        return message.strip()