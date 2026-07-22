"""
Core polling loop: scans each configured watch directory, tracks file sizes
across polls to detect when a file has stopped growing ("stable"), and hands
stable files off to the handlers module for processing.
"""

from __future__ import annotations

import fnmatch
import logging
import os

from dirwatcher import handlers
from dirwatcher.config import Settings, WatchTarget
from dirwatcher.state import StateStore

logger = logging.getLogger(__name__)


class DirectoryWatcher:
    def __init__(self, settings: Settings, state_store: StateStore):
        self.settings = settings
        self.state_store = state_store

    def scan_all(self) -> None:
        for target in self.settings.watches:
            self._scan_target(target)

    def _scan_target(self, target: WatchTarget) -> None:
        if not os.path.isdir(target.path):
            logger.warning("[%s] watch path does not exist: %s", target.name, target.path)
            return

        watch_state = self.state_store.get_watch_state(target.name)

        current_files = set()
        for fname in os.listdir(target.path):
            if not fnmatch.fnmatch(fname, target.pattern):
                continue

            full_path = os.path.join(target.path, fname)
            if not os.path.isfile(full_path):
                continue

            current_files.add(full_path)
            self._check_file(target, watch_state, full_path)

        # Drop state for files that have disappeared (processed/removed
        # externally) so the state file doesn't grow indefinitely.
        for known_path in list(watch_state.keys()):
            if known_path not in current_files:
                watch_state.pop(known_path, None)

    def _check_file(self, target: WatchTarget, watch_state: dict, full_path: str) -> None:
        size = os.path.getsize(full_path)
        entry = watch_state.get(full_path)

        if entry is None:
            watch_state[full_path] = {"size": size, "stable_count": 0, "processed": False}
            logger.debug("[%s] new file detected: %s", target.name, full_path)
            return

        if entry.get("processed"):
            return

        if entry["size"] == size:
            entry["stable_count"] += 1
        else:
            entry["size"] = size
            entry["stable_count"] = 0

        if entry["stable_count"] >= self.settings.stability_checks:
            success = handlers.dispatch(target, full_path)
            if success:
                entry["processed"] = True
            else:
                # Leave processed=False so it gets retried on the next scan.
                logger.info("[%s] will retry %s next cycle", target.name, full_path)
