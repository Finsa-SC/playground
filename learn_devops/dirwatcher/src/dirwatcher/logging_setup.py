"""
Logging configuration for dirwatcher.

Keeps things simple: a single stream handler to stdout. Whatever process
supervisor runs this is expected to capture and redirect stdout to wherever
logs need to live.
"""

import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )
