class Solution:

    ## Error while meet "([])"
    # def isValid(self, s: str) -> bool:
    #     match_parentheses = {
    #         '(': ')',
    #         '[': ']',
    #         '{': '}',
    #     }
    #
    #     for i, delimiter in enumerate(s):
    #         if i % 2 == 0:
    #             print(f"{delimiter} == {match_parentheses[delimiter]}")
    #             if s[i+1] != match_parentheses[delimiter]:
    #                 return False
    #     return True

    # Not completed, still index error but i know this is would be error while meet "{}[]"
    # def isValid(self, s: str) -> bool:
    #     match_parentheses = {
    #         '(': ')',
    #         '[': ']',
    #         '{': '}',
    #     }
    #
    #     for i, delimiter in enumerate(s):
    #         clode_d = delimiter[-i]
    #         if match_parentheses[clode_d] == clode_d:
    #             return False
    #     return True

    # return true because not checking last open dentan recent close and possible index error
    # def isValid(self, s: str) -> bool:
    #     close_delimiter = {
    #         ']': '[',
    #         '}': '{',
    #         ')': '(',
    #     }
    #     founded_open = []
    #
    #     for d in s:
    #         if not close_delimiter.get(d, None):
    #             founded_open.append(d)
    #         else:
    #             founded_open.pop()
    #
    #     if not founded_open:
    #         return True
    #     return False

    def isValid(self, s: str) -> bool:
        close_delimiter = {
            ']': '[',
            '}': '{',
            ')': '(',
        }
        founded_open = []

        for d in s:
            if d not in close_delimiter:
                founded_open.append(d)
            else:
                if not founded_open or founded_open[-1] != close_delimiter[d]:
                    return False
                founded_open.pop()

        return len(founded_open) == 0

if __name__ == "__main__":
    sol = Solution()

    delimiters = "(){}({})"
    print(sol.isValid(delimiters))