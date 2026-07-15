"""
state.py

Shared state for the Token Cost Agent.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    """
    Represents a retrieved document.
    """

    id: str

    content: str

    score: float = 0.0

    source: str = ""

    metadata: dict[str, Any] = Field(default_factory=dict)

    embedding: list[float] | None = None


class AgentState(BaseModel):
    """
    Shared state passed between LangGraph nodes.
    """

    # =====================================================
    # User Input
    # =====================================================

    question: str = ""

    # =====================================================
    # Classification
    # =====================================================

    query_type: str = ""

    # =====================================================
    # Memory
    # =====================================================

    memories: list[str] = Field(default_factory=list)

    # =====================================================
    # Retrieval Pipeline
    # =====================================================

    retrieved_docs: list[Document] = Field(default_factory=list)

    reranked_docs: list[Document] = Field(default_factory=list)

    compressed_docs: list[Document] = Field(default_factory=list)

    # =====================================================
    # Prompt
    # =====================================================

    prompt: str = ""

    # =====================================================
    # LLM Response
    # =====================================================

    response: str = ""

    # =====================================================
    # Metrics
    # =====================================================

    token_usage: dict[str, Any] = Field(default_factory=dict)

    metadata: dict[str, Any] = Field(default_factory=dict)