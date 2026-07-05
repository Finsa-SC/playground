from pathlib import Path

ignore_path = Path("/home/silence-suzuka/Project/playground/.gitignore")

def ignore_gen():
    with open(ignore_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith("#"):
                yield line.strip()

for ign in ignore_gen():
    print(ign)