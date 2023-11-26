"""
https://leetcode.com/problems/remove-one-element-to-make-the-array-strictly-increasing/
"""
from typing import List


class Solution:
    def _canBeIncreasing(self, nums: List[int]) -> bool:
        misses = 0
        for i, el in enumerate(nums[1:]):
            if misses > 1:
                return False

            for ind_back in range(1, 3):
                prev_ind = i + 1 - ind_back
                if prev_ind < 0:
                    break
                prev = nums[prev_ind]
                if el > prev:
                    break
                misses += 1
            else:
                return False

        return True

    def canBeIncreasing(self, nums: List[int]) -> bool:
        o = nums
        if len(set(nums)) < len(nums) - 1:
            return False

        s = sorted(nums)
        if nums == s:
            return True

        for i, el in enumerate(nums):
            another = s[i]
            if el == another:
                continue

            f1 = list(nums)
            f1.pop(i)

            f2 = list(s)
            f2.remove(el)

            if f1 == f2:
                if len(set(f1)) == len(f1):
                    return True
                else:
                    z = 0

            f1 = list(nums)
            f1.remove(another)

            f2 = list(s)
            f2.pop(i)

            if f1 == f2:
                if len(set(f1)) == len(f1):
                    return True
                else:
                    z = 0

        return False


if __name__ == '__main__':
    assert Solution().canBeIncreasing([2,3,4,5,1,5]) == False
    assert Solution().canBeIncreasing([42,50,54,74,84,86,88,93,104,127,143,160,164,169,170,181,209,223,225,231,247,257,262,274,282,306,307,320,346,357,378,381,387,392,394,404,423,437,444,456,476,491,507,524,527,528,537,558,566,574,169,584,585,609,621,626,632,644,653,661,662,670,676,698,704,710,718,719,730,735,737,746,748,755,776,782,785,795,802,812,822,828,863,866,870,872,877,899,905,909,919,929,940,944,961,963,980,981]) == True
    assert Solution().canBeIncreasing([1,1,1]) == False
    assert Solution().canBeIncreasing([1,1]) == True
    assert Solution().canBeIncreasing([2,3,1,2]) == False
    assert Solution().canBeIncreasing([1,2,10,5,7]) == True
    assert Solution().canBeIncreasing([105,924,32,968]) == True
