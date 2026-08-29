import tomllib, logging, sys
from pathlib import Path

import sys

logging.basicConfig(
    format="[%(levelname)s] %(asctime)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

logger.info(config)