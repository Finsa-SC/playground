# Menggunakan metode **LOOKAHEAD**, melihat value didepan untuk menentukan operasi

class Solution:
    def __init__(self):
        self.roman = {
            "I": 1, "V": 5, "X": 10,
            "L": 50, "C": 100, "D": 500,
            "M": 1000,
        }

    def romanToInt(self, roman: str) -> int:
        value = 0
        len_roman = len(roman)

        for i in range(len_roman):
            if i < len_roman - 1 and self.roman[roman[i]] < self.roman[roman[i + 1]]:
                value -= self.roman[roman[i]]
            else:
                value += self.roman[roman[i]]

        return value

if __name__ == "__main__":
    sol = Solution()
    integer = sol.romanToInt("MCMXCIV")
    print(integer)