import fnmatch
import re
from pathlib import Path


print(fnmatch.fnmatch("playground", "*yground"))
print(fnmatch.fnmatch("pliyground", "pl?yground"))
print(fnmatch.fnmatch("pli53hyground", "pl*yground"))

file = ["notes.txt", "traffic.log", "shop.txt", "password.txt", "my_directory", "recovery.txt.bak"]
print(fnmatch.filter(file, "*.txt*"))

#It's the same as regular fnmatch because i use arch linux
print(fnmatch.fnmatchcase("playground", "play*"))
print(fnmatch.fnmatchcase("playground", "playground"))

print(fnmatch.filterfalse(file, "*.txt*"))

pattern = fnmatch.translate("*.txt")
found = []
for i in file:
    match = re.search(pattern, i)
    if match:
        found.append(match.group(0))

print(found)