from pathlib import Path

my_path = Path.cwd().parent

def iterasi_dir(iter_dir):
    for path in iter_dir:
        print(path)
        if path.is_dir():
            iterasi_dir(path.iterdir())

iterasi_dir(my_path.iterdir())