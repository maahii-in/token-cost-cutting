"""
Application Logger
"""

from __future__ import annotations

import logging
from pathlib import Path

from config import settings

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "agent.log"


def get_logger(name: str) -> logging.Logger:
    """
    Create or return a configured logger.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    file = logging.FileHandler(LOG_FILE)
    file.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file)

    return logger