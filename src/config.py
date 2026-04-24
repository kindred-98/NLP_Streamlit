import logging
import sys

logger = logging.getLogger("nlp")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))
    logger.addHandler(handler)

__all__ = ["logger"]