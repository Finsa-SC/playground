from time import struct_time
from typing import Literal

string_1 = "hello"
string_2 = "gagagaga"

def two_string(string1, string2) -> str:
    set_1 = set(string1)
    set_2 = set(string2)
    have = set_1 & set_2

    return "YES" if have else "NO"

print(two_string(string_1, string_2))