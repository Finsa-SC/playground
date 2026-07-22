import logging
from time import sleep
import sys

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("Main")

logger.info("Starting...")
sleep(1)
logger.info("Running...")
sleep(1)
logger.error("Error occured!")
logger.info("Stopping...")