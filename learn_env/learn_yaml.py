from pathlib import Path
import yaml

config = Path("/home/silence-suzuka/Project/playground/learn_env/config.yaml")

with config.open('r') as f:
    data = yaml.safe_load(f)

print(data)