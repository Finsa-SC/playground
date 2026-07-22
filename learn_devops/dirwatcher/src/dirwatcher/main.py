"""
Entry point for the directory watcher daemon.

Usage:
    python -m dirwatcher.main
"""

from __future__ import annotations

import logging
import time

from dirwatcher.config import load_settings
from dirwatcher.logging_setup import configure_logging
from dirwatcher.state import StateStore
from dirwatcher.watcher import DirectoryWatcher

logger = logging.getLogger(__name__)


def run() -> None:
    settings = load_settings()
    configure_logging(settings.log_level)

    logger.info("Starting dirwatcher with %d watch target(s)", len(settings.watches))

    state_store = StateStore(settings.state_file_path)
    state_store.load()

    watcher = DirectoryWatcher(settings, state_store)

    try:
        while True:
            watcher.scan_all()
            state_store.save()
            time.sleep(settings.poll_interval_seconds)
    except KeyboardInterrupt:
        logger.info("Interrupted, saving state before exit")
        state_store.save()


def main() -> None:
    try:
        run()
    except Exception:
        logger.exception("dirwatcher crashed")


if __name__ == "__main__":
    main()
