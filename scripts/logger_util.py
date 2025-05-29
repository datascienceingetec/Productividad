import logging
import os
from pathlib import Path

def setup_logger(log_path: str) -> logging.Logger:
    """Configure and return a logger that writes to log_path."""
    logger = logging.getLogger("productivity")
    logger.setLevel(logging.INFO)

    # Create log directory if not exists
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(log_path)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)
    return logger


def close_logger(logger: logging.Logger) -> None:
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)