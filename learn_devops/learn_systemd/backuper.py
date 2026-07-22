from pathlib import Path
import dotenv, os, logging, sys

dotenv.load_dotenv()
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

class Backuper:
    def __init__(self):
        try:
            self.destination = Path(os.getenv("DESTINATION"))
            self.target = Path(os.getenv("TARGET"))
            self.backup_name = str(os.getenv("BACKUP_NAME"))
            if self.backup_name.strip():
                self.backup_name = self.destination.name
        except (NotADirectoryError, TypeError) as e:
            logger.error(str(e))

if __name__ == "__main__":
    backup = Backuper()
