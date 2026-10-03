class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:
        ### Use hashmap method
        # val_found = []
        # total = 0
        # for i, num in enumerate(nums):
        #     if num == val:
        #         val_found.append(i)
        #
        #     elif val_found:
        #         total += 1
        #         nums[val_found[0]], nums[i] = nums[i], nums[val_found[0]]
        #         val_found.pop(0)
        #         print(nums)
        #
        #     else:
        #         continue
        #
        # return total

        ### Use sweeping method
        k = 0
        for num in nums:
            if num != val:
                nums[k] = num
                k += 1

        return k

if __name__ == "__main__":
    sol = Solution()
    el = [0,1,2,2,3,0,4,2]
    el2 = [3, 2, 2, 3]
    print(sol.removeElement(el, 2))