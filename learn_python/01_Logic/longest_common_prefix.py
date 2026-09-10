from typing import List

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        idx = 0
        word = ""
        w = ""
        while True:
            if w.strip():
                for st in strs:
                    w = strs[idx]
                idx += 1

if __name__ == "__main__":
    sol = Solution()
    val = sol.longestCommonPrefix(["hello", "hell", "hentai"])