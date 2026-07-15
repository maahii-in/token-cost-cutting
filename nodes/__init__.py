"""
Token Cost Agent - Processing Nodes

This package contains all LangGraph processing nodes used by the
Token Cost Agent workflow.

Workflow
--------

                User Question
                      │
                      ▼
              ClassifierNode
                      │
                      ▼
                MemoryNode
                      │
                      ▼
              RetrieverNode
                      │
                      ▼
              RerankerNode
                      │
                      ▼
             CompressorNode
                      │
                      ▼
            DeduplicatorNode
                      │
                      ▼
           PromptBuilderNode
                      │
                      ▼
                RouterNode
                      │
                      ▼
                  LLMNode
                      │
                      ▼
              SummarizerNode

Each node receives an AgentState object,
updates it, and returns the updated state.
"""

# ==========================================================
# Classification
# ==========================================================
from .classifier import ClassifierNode

# ==========================================================
# Memory
# ==========================================================
from .memory import MemoryNode

# ==========================================================
# Retrieval Pipeline
# ==========================================================
from .retriever import RetrieverNode
from .reranker import RerankerNode
from .compressor import CompressorNode
from .deduplicator import DeduplicatorNode

# ==========================================================
# Prompt Generation
# ==========================================================
from .prompt_builder import PromptBuilderNode

# ==========================================================
# Routing
# ==========================================================
from .router import RouterNode

# ==========================================================
# LLM
# ==========================================================
from .llm import LLMNode

# ==========================================================
# Response Processing
# ==========================================================
from .summarizer import SummarizerNode

# ==========================================================
# Public API
# ==========================================================
__all__ = (
    "ClassifierNode",
    "MemoryNode",
    "RetrieverNode",
    "RerankerNode",
    "CompressorNode",
    "DeduplicatorNode",
    "PromptBuilderNode",
    "RouterNode",
    "LLMNode",
    "SummarizerNode",
)