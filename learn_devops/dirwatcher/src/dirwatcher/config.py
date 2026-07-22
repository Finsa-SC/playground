"""
Configuration loading for dirwatcher.

Two layers of config:
  1. Environment variables (.env) - process-level settings (paths, timing, logging).
  2. watch_config.yaml - the actual list of directories to watch and what to do
     with files that show up in them.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

import yaml
from dotenv import load_dotenv

load_dotenv()


@dataclass
class WatchTarget:
    name: str
    path: str
    pattern: str
    action: str
    destination: str | None = None


@dataclass
class Settings:
    watch_config_path: str
    state_file_path: str
    poll_interval_seconds: int
    stability_checks: int
    log_level: str
    watches: list[WatchTarget] = field(default_factory=list)


def _load_watch_targets(watch_config_path: str) -> list[WatchTarget]:
    with open(watch_config_path, "r") as f:
        raw = yaml.safe_load(f) or {}

    targets = []
    for entry in raw.get("watches", []):
        targets.append(
            WatchTarget(
                name=entry["name"],
                path=entry["path"],
                pattern=entry.get("pattern", "*"),
                action=entry.get("action", "log_only"),
                destination=entry.get("destination"),
            )
        )
    return targets


def load_settings() -> Settings:
    # WATCH_CONFIG_PATH is the one setting the process genuinely can't run
    # without, so it's read directly rather than via .get(default=...).
    watch_config_path = os.environ["WATCH_CONFIG_PATH"]

    state_file_path = os.environ.get("STATE_FILE_PATH", "data/state.json")
    poll_interval_seconds = int(os.environ.get("POLL_INTERVAL_SECONDS", "5"))
    stability_checks = int(os.environ.get("STABILITY_CHECKS", "2"))
    log_level = os.environ.get("LOG_LEVEL", "INFO")

    watches = _load_watch_targets(watch_config_path)

    return Settings(
        watch_config_path=watch_config_path,
        state_file_path=state_file_path,
        poll_interval_seconds=poll_interval_seconds,
        stability_checks=stability_checks,
        log_level=log_level,
        watches=watches,
    )
