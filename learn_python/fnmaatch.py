import fnmatch
from pathlib import Path

for file in Path("/home/silence-suzuka/test_1").iterdir():
    print(file.name)
    print(file.is_dir())
    print(fnmatch.fnmatch(file.name, "*.log"))