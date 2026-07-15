"""
config.py

Centralized application configuration for the
Token Cost Agent.

Loads all configuration from the .env file using
Pydantic Settings.
"""

from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings
    """

    # ==========================================================
    # Application
    # ==========================================================

    APP_NAME: str = "Token Cost Agent"

    APP_ENV: Literal[
        "development",
        "testing",
        "production",
    ] = "development"

    APP_DEBUG: bool = True

    # ==========================================================
    # Groq
    # ==========================================================

    GROQ_API_KEY: SecretStr

    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # ==========================================================
    # PostgreSQL
    # ==========================================================

    POSTGRES_HOST: str = "localhost"

    POSTGRES_PORT: int = 5432

    POSTGRES_DB: str = "token_cost_agent"

    POSTGRES_USER: str = "postgres"

    POSTGRES_PASSWORD: SecretStr

    # ==========================================================
    # Milvus
    # ==========================================================

    MILVUS_HOST: str = "localhost"

    MILVUS_PORT: int = 19530

    MILVUS_COLLECTION: str = "documents"

    # ==========================================================
    # Redis
    # ==========================================================

    REDIS_HOST: str = "localhost"

    REDIS_PORT: int = 6379

    REDIS_DB: int = 0

    # ==========================================================
    # Embedding
    # ==========================================================

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    # ==========================================================
    # Reranker
    # ==========================================================

    RERANKER_MODEL: str = "BAAI/bge-reranker-base"

    # ==========================================================
    # Retrieval
    # ==========================================================

    TOP_K: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    RERANK_TOP_K: int = Field(
        default=5,
        ge=1,
        le=20,
    )

    SIMILARITY_THRESHOLD: float = Field(
        default=0.75,
        ge=0.0,
        le=1.0,
    )

    # ==========================================================
    # Compression
    # ==========================================================

    MAX_DOCUMENT_TOKENS: int = Field(
        default=300,
        ge=50,
    )

    MAX_PROMPT_TOKENS: int = Field(
        default=4000,
        ge=100,
    )

    # ==========================================================
    # Logging
    # ==========================================================

    LOG_LEVEL: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    LOG_FILE: str = "logs/agent.log"

    # ==========================================================
    # Token Cost Tracking
    # ==========================================================

    ENABLE_TOKEN_LOGGING: bool = True

    ENABLE_COST_TRACKING: bool = True

    # ==========================================================
    # LangGraph
    # ==========================================================

    CHECKPOINT_PATH: str = "checkpoints/"

    # ==========================================================
    # Cache
    # ==========================================================

    CACHE_TTL: int = 3600

    # ==========================================================
    # API
    # ==========================================================

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    # ==========================================================
    # Pydantic Settings
    # ==========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()