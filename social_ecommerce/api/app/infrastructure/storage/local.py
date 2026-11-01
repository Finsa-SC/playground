from pathlib import Path
from app.core.config import get_settings


class LocalStorage:
    """Development-only storage adapter. Never expose its root as a public static mount."""

    def __init__(self):
        self.root = Path(get_settings().local_storage_root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def resolve(self, key: str) -> Path:
        candidate = (self.root / key).resolve()
        if self.root not in candidate.parents:
            raise ValueError("Invalid storage key")
        return candidate
