"""
Persists the "seen files" state between restarts so that a restart of the
watcher doesn't re-process files it already handled.

State shape on disk:

{
    "<watch_name>": {
        "<absolute_file_path>": {
            "size": 1234,
            "stable_count": 2,
            "processed": true
        }
    }
}
"""

from __future__ import annotations

import json
import logging
import os

logger = logging.getLogger(__name__)


class StateStore:
    def __init__(self, path: str):
        self.path = path
        self._data: dict[str, dict[str, dict]] = {}

    def load(self) -> None:
        if not os.path.exists(self.path):
            logger.info("No existing state file at %s, starting fresh", self.path)
            self._data = {}
            return

        with open(self.path, "r") as f:
            self._data = json.load(f)

    def save(self) -> None:
        # NOTE: state file directory is assumed to already exist relative to
        # wherever the process was launched from.
        with open(self.path, "w") as f:
            json.dump(self._data, f, indent=2)

    def get_watch_state(self, watch_name: str) -> dict[str, dict]:
        return self._data.setdefault(watch_name, {})

    def update_file_state(self, watch_name: str, file_path: str, entry: dict) -> None:
        self._data.setdefault(watch_name, {})[file_path] = entry

    def remove_file_state(self, watch_name: str, file_path: str) -> None:
        self._data.get(watch_name, {}).pop(file_path, None)
