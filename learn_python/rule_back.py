import fnmatch
from pathlib import Path
from enum import Enum, auto

class Rule(Enum):
    Exact = auto()
    Glob = auto()
    Directory = auto()

exact_list: set[str] = set()
glob_list: list[str] = []
directory_list: set[str] = set()

def load_ignore():
    with open("/home/silence-suzuka/.gitignore", 'r') as file:
        for line in file:
            if line.strip() and not line.startswith("#"):
                rule = set_rule(line)
                add_rule_and_grouping(rule, line.replace("\n", ""))

def add_rule_and_grouping(rule, word):
    match rule:
        case Rule.Exact:
            exact_list.add(word)
        case Rule.Glob:
            glob_list.append(word)
        case Rule.Directory:
            directory_list.add(word)

def match_exact(file: str) -> bool:
    for exact in exact_list:
        # print(f"{file} matching with {exact}")
        if fnmatch.fnmatch(file, exact):
            return True
    return False

def match_glob(file: str) -> bool:
    for glob in glob_list:
        if fnmatch.fnmatch(file, glob):
            return True
    return False

def match_directory(file: str) -> bool:
    for directory in directory_list:
        if fnmatch.fnmatch(file, directory):
            return True
    return False

def rule_matching(rule, file: str) -> bool:
    match rule:
        case Rule.Exact:
            return match_exact(file)
        case Rule.Glob:
            return match_glob(file)
        case Rule.Directory:
            return match_directory(file)
        case _:
            return False

def set_rule(word):
    if "*" in word:
        return Rule.Glob
    elif word.endswith("/"):
        return Rule.Directory
    elif word.startswith("."):
        return Rule.Exact
    else:
        ...
        # raise ValueError("Invalid format, waiting for fixing in backend")

load_ignore()

for file in Path("/home/silence-suzuka/test_1").iterdir():
    rule = set_rule(file.name)
    match = rule_matching(rule, file.name)
    print(f"{file.name} {rule} {match}")