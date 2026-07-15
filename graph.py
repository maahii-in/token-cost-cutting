"""
graph.py

LangGraph workflow for the Token Cost Agent.
"""

from __future__ import annotations

from langgraph.graph import StateGraph, START, END

from state import AgentState

from nodes import (
    ClassifierNode,
    MemoryNode,
    RetrieverNode,
    RerankerNode,
    CompressorNode,
    DeduplicatorNode,
    PromptBuilderNode,
    RouterNode,
    LLMNode,
    SummarizerNode,
)


# ==========================================================
# Initialize Nodes
# ==========================================================

classifier = ClassifierNode()

memory = MemoryNode()

retriever = RetrieverNode()

reranker = RerankerNode()

compressor = CompressorNode()

deduplicator = DeduplicatorNode()

prompt_builder = PromptBuilderNode()

router = RouterNode()

llm = LLMNode()

summarizer = SummarizerNode()


# ==========================================================
# Build Graph
# ==========================================================

builder = StateGraph(AgentState)


# ==========================================================
# Register Nodes
# ==========================================================

builder.add_node("classifier", classifier)

builder.add_node("memory", memory)

builder.add_node("retriever", retriever)

builder.add_node("reranker", reranker)

builder.add_node("compressor", compressor)

builder.add_node("deduplicator", deduplicator)

builder.add_node("prompt_builder", prompt_builder)

builder.add_node("router", router)

builder.add_node("llm", llm)

builder.add_node("summarizer", summarizer)


# ==========================================================
# Routing Function
# ==========================================================

def route_after_classifier(state: AgentState) -> str:
    """
    Decide which branch to execute.
    """

    query_type = state.query_type.lower()

    if query_type == "chat":
        return "router"

    if query_type in {
        "retrieval",
        "reasoning",
        "hybrid",
    }:
        return "memory"

    if query_type == "tool":
        return "router"

    return "router"


# ==========================================================
# Graph Edges
# ==========================================================

builder.add_edge(START, "classifier")


builder.add_conditional_edges(

    "classifier",

    route_after_classifier,

    {

        "memory": "memory",

        "router": "router",

    },

)


builder.add_edge("memory", "retriever")

builder.add_edge("retriever", "reranker")

builder.add_edge("reranker", "compressor")

builder.add_edge("compressor", "deduplicator")

builder.add_edge("deduplicator", "prompt_builder")

builder.add_edge("prompt_builder", "router")

builder.add_edge("router", "llm")

builder.add_edge("llm", "summarizer")

builder.add_edge("summarizer", END)


# ==========================================================
# Compile Graph
# ==========================================================

graph = builder.compile()