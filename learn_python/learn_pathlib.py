from pathlib import Path

target = Path("/home/silence-suzuka/test_1")

# Get spesific file with glob rule
print("=========================Glob=============================")
this_path = target.glob("*.log")
for path in this_path:
    print(path)

# Get spesific recursive file with glob rule
print("=========================Recursive Glob=============================")
this_path = target.rglob("*.log")
for path in this_path:
    print(path)