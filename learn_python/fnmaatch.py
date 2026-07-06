import fnmatch
import re
from pathlib import Path

# Find match word using incasesensitive (Except linux)
print("==============Regular fnmatch===================")
print(fnmatch.fnmatch("playground", "*yground"))
print(fnmatch.fnmatch("pliyground", "pl?yground"))
print(fnmatch.fnmatch("pli53hyground", "pl*yground"))

file = [
    "notes.txt", "traffic.log", "shop.txt",
    "password.txt", "my_directory", "recovery.txt.bak",
    "main.py", "engine.py", "filter.py",
    "main.rs", "database.rs", "logic.rs",
]

# Find match pattern and return list of matched word
print("==============Filter===================")
print(fnmatch.filter(file, "*.txt*"))

#It's the same as regular fnmatch because i use arch linux
print("==============Casesensitive fnmatch===================")
print(fnmatch.fnmatchcase("playground", "play*"))
print(fnmatch.fnmatchcase("playground", "playground"))

# Inverted from reguler fnmatch filter
print("==============Inverted Filter===================")
print(fnmatch.filterfalse(file, "*.txt*"))

# Translate from shell's like to regex pattern format
print("==============Translate into regex pattern===================")
pattern = fnmatch.translate("*.txt")
print(pattern)
found = []
for i in file:
    match = re.search(pattern, i)
    if match:
        found.append(match.group(0))
print(found)


print("==============Use sequence pattern===================")
# Use [!seq] to get inverted return
# for i in file:
#     pattern = "[*.py]"
#     if fnmatch.fnmatch(i, pattern):
#         print(i)

# text = "log_2.log"
text = "log_two.log"
pattern = "log_[a-z][a-z][a-z].log"
# pattern = "log_[0-9].log"
match = fnmatch.fnmatch(text, pattern)
print(f"{text} {match}")