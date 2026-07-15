"""
router.py

Execution Router Node
"""

from __future__ import annotations

from state import AgentState
from common import get_logger

logger = get_logger(__name__)


class RouterNode:
    """
    Creates an execution plan for the workflow.

    The graph decides the execution path.

    The router prepares metadata describing
    which resources are required.
    """

    def __init__(self):

        logger.info("Router Node Initialized")

    def __call__(
        self,
        state: AgentState,
    ) -> AgentState:

        query_type = (

            state.query_type or "reasoning"

        ).lower()

        plan = self.build_execution_plan(
            query_type
        )

        state.metadata["execution_plan"] = plan

        logger.info(
            f"Execution Plan : {plan}"
        )

        return state

    # -----------------------------------------------------

    def build_execution_plan(
        self,
        query_type: str,
    ) -> dict:

        plan = {

            "route": query_type,

            "requires_memory": False,

            "requires_retrieval": False,

            "requires_llm": True,

            "requires_tools": False,

        }

        if query_type == "retrieval":

            plan["requires_memory"] = True

            plan["requires_retrieval"] = True

        elif query_type == "hybrid":

            plan["requires_memory"] = True

            plan["requires_retrieval"] = True

        elif query_type == "tool":

            plan["requires_tools"] = True

        elif query_type == "chat":

            pass

        elif query_type == "reasoning":

            pass

        return plan