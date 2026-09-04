class Solution:
    def __init__(self):
        self.roman = {
            "I": 1, "V": 5, "X": 10,
            "L": 50, "C": 100, "D": 500,
            "M": 1000,
        }

    def romanToInt(self, roman: str) -> int:
        value = 0
        for r in roman:
            value += self.roman[roman]
        return value

if __name__ == "__main__":
    sol = Solution()
    sol.romanToInt("I")