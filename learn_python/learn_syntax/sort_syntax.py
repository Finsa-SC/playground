import re

from packaging.version import parse

# tags = [
#     "v1.0.0", "v1.2.0", "v1.6.0", "v1.7.0", "v1.3.0", "v1.4.0", "v1.5.0", "v1.8.0", "v1.9.0", "v1.10.0",
# ]
#
# tags_sorted = sorted(tags, key=parse)
#
# print(tags)

# files = [
#     "config.conf", "config(2).conf", "config(3).conf",
#     "config(4).conf", "config(5).conf", "config(5).conf",
#     "config(7).conf","config(8).conf", "config(9).conf",
#     "config(10).conf", "config(11).conf", "config(12).conf",
# ]
#
# def natural_keys(text) -> list:
#     return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', text)]
#
# files_sorted = sorted(files, key=natural_keys)
# print(files_sorted)

leaderboards = {
    "agus resing": {
        "score": 70,
        "time": 203
    },
    "ridwad kebab": {
        "score": 90,
        "time": 271
    },
    "crazy killer": {
        "score": 87,
        "time": 301
    },
    "abbas kehidupan": {
        "score": 42,
        "time": 311
    },
    "rahmat toilet": {
        "score": 82,
        "time": 461
    },
    "andi speaker": {
        "score": 79,
        "time": 241
    },
    "bayu digital": {
        "score": 90,
        "time": 93
    }
}

sorted_games = sorted(leaderboards, key=lambda x: leaderboards[x]['score'], reverse=True)
# print(sorted_games)