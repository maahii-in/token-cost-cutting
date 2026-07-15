"""
db/postgres.py

PostgreSQL database client for the Token Cost Agent.

Features
--------
- Connection Pool
- Automatic Transaction Management
- Automatic Rollback
- Thread-safe Connection Pool
- Logging
- Context Manager Support
"""

from __future__ import annotations

from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

from config import settings
from common.logger import get_logger

logger = get_logger(__name__)


class PostgresDB:
    """
    PostgreSQL Database Client.

    Provides a reusable connection pool for executing SQL
    queries safely and efficiently.
    """

    def __init__(self) -> None:
        """Initialize the PostgreSQL connection pool."""

        self.pool = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD.get_secret_value(),
        )

        if self.pool is None:
            raise RuntimeError("Failed to create PostgreSQL connection pool.")

        logger.info("PostgreSQL connection pool initialized.")

    # ---------------------------------------------------------
    # Execute Query
    # ---------------------------------------------------------

    def execute(
        self,
        query: str,
        params: tuple | dict | None = None,
    ) -> list[dict[str, Any]] | None:
        """
        Execute a SQL query.

        Parameters
        ----------
        query : str
            SQL query.

        params : tuple | dict | None
            Query parameters.

        Returns
        -------
        list[dict] | None
        """

        conn = None

        try:
            conn = self.pool.getconn()

            with conn.cursor(
                cursor_factory=RealDictCursor
            ) as cursor:

                cursor.execute(query, params)

                result = None

                if cursor.description:
                    result = cursor.fetchall()

                conn.commit()

                logger.debug("SQL executed successfully.")

                return result

        except psycopg2.Error as exc:

            if conn:
                conn.rollback()

            logger.exception(
                "Database execution failed."
            )

            raise

        finally:

            if conn:
                self.pool.putconn(conn)

    # ---------------------------------------------------------
    # Execute Many
    # ---------------------------------------------------------

    def executemany(
        self,
        query: str,
        params: list[tuple],
    ) -> None:
        """
        Execute multiple SQL statements.
        """

        conn = None

        try:

            conn = self.pool.getconn()

            with conn.cursor() as cursor:

                cursor.executemany(
                    query,
                    params,
                )

                conn.commit()

                logger.debug(
                    "Batch query executed."
                )

        except psycopg2.Error:

            if conn:
                conn.rollback()

            logger.exception(
                "Batch execution failed."
            )

            raise

        finally:

            if conn:
                self.pool.putconn(conn)

    # ---------------------------------------------------------
    # Fetch One
    # ---------------------------------------------------------

    def fetch_one(
        self,
        query: str,
        params: tuple | dict | None = None,
    ) -> dict[str, Any] | None:
        """
        Fetch a single record.
        """

        result = self.execute(query, params)

        if result:

            return result[0]

        return None

    # ---------------------------------------------------------
    # Fetch All
    # ---------------------------------------------------------

    def fetch_all(
        self,
        query: str,
        params: tuple | dict | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch all records.
        """

        result = self.execute(query, params)

        return result or []

    # ---------------------------------------------------------
    # Health Check
    # ---------------------------------------------------------

    def health_check(self) -> bool:
        """
        Check database connectivity.
        """

        try:

            self.fetch_one("SELECT 1;")

            return True

        except Exception:

            return False

    # ---------------------------------------------------------
    # Close Pool
    # ---------------------------------------------------------

    def close(self) -> None:
        """
        Close all pooled connections.
        """

        if self.pool:

            self.pool.closeall()

            logger.info(
                "PostgreSQL connection pool closed."
            )

    # ---------------------------------------------------------
    # Context Manager
    # ---------------------------------------------------------

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):
        self.close()