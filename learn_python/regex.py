import re


with open("/home/silence-suzuka/Project/playground/learn_setfactl/silence-suzuka.txt", 'r') as file:
    text = file.read()

# Find first word that match with pattern
print("Search")
match = re.search(r"silence.suzuka", text, re.IGNORECASE)
if match:
    print(match.group(0))


# Find pattern in the first word
print("Match")
match = re.match(r"silence.suzuka", text, re.IGNORECASE)
if match:
    print(match.group(0))

# Only capture until find pattern
print("Split")
match = re.split(r"silence.suzuka", text, flags=re.IGNORECASE, maxsplit=10)
if match:
    for i in match:
        print(i)
        print("="*100)

# Find all matched pattern
print("Findall")
match = re.findall(r"silence.suzuka", text, re.IGNORECASE)
if match:
    print(match)