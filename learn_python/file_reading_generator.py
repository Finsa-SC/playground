from pathlib import Path

ignore_path = Path("/home/silence-suzuka/Project/playground/.gitignore")

def ignore_gen():
    with open(ignore_path, 'r') as file:
        print(file.readline())

ignore_gen()