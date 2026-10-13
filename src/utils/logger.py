"""
Logging utility for the Smart Jasmine Farming Assistant.
Configures timestamped console and file logs.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

_LOGGER_INSTANCE: Optional[logging.Logger] = None


def setup_logger(name: str = "JasmineAssistant", level: int = logging.INFO) -> logging.Logger:
    """Configures and returns a structured logger."""
    global _LOGGER_INSTANCE
    if _LOGGER_INSTANCE is not None:
        return _LOGGER_INSTANCE

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers if reloaded in Streamlit
    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    _LOGGER_INSTANCE = logger
    return logger


def get_logger() -> logging.Logger:
    """Returns the global logger instance."""
    return setup_logger()
