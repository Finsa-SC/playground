from pathlib import Path
import humanize

def collect_path_list(path: Path) -> list[Path]:
    return list(path.rglob("*.py"))

def get_total_size(path_list: list[Path]) -> float:
    total_size = 0.0
    for path in path_list:
        total_size += path.stat().st_size

    return total_size

def main():
    target_path = Path("/mnt/Home/Projects/playground")
    path_list = collect_path_list(target_path)

    total_size = get_total_size(path_list)
    total_size = humanize.naturalsize(total_size)

    print(total_size)

if __name__ == "__main__":
    main()