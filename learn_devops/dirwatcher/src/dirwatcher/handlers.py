"""
Handlers responsible for what happens to a file once it's been judged
"stable" (i.e. finished being written) by the watcher.
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

from dirwatcher.config import WatchTarget

logger = logging.getLogger(__name__)


def dispatch(target: WatchTarget, file_path: str) -> bool:
    """
    Perform the configured action for a stable file.
    Returns True if the file was handled successfully.
    """
    src = Path(file_path)

    if target.action == "log_only":
        logger.info("[%s] observed stable file: %s", target.name, file_path)
        return True

    if target.action in ("move", "copy"):
        if not target.destination:
            logger.error(
                "[%s] action '%s' requires a destination, but none is configured",
                target.name,
                target.action,
            )
            return False

        dest_dir = Path(target.destination)
        dest_path = dest_dir / src.name

        try:
            if target.action == "move":
                shutil.move(str(src), str(dest_path))
            else:
                shutil.copy2(str(src), str(dest_path))
            logger.info(
                "[%s] %s -> %s (%s)", target.name, src, dest_path, target.action
            )
            return True
        except OSError as exc:
            logger.error("[%s] failed to %s %s: %s", target.name, target.action, src, exc)
            return False

    logger.warning("[%s] unknown action '%s', skipping", target.name, target.action)
    return False
