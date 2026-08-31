from pathlib import Path

class CacheCleanup:
    def __init__(self, target_path: Path, exclude: list[str]|None=None):
        self.target = target_path

    def resolve_file(self):
        found_file = list(self.target.rglob("*"))

        return found_file

    def run_cleanup(self):
        result = self.resolve_file()

        return result


if __name__ == "__init__":
    cleaner = CacheCleanup()

    print(cleaner.run_cleanup())
