"""
https://leetcode.com/explore/interview/card/top-interview-questions-medium/110/sorting-and-searching/798/

Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.

You must solve this problem without using the library's sort function.



Example 1:

Input: nums = [2,0,2,1,1,0]
Output: [0,0,1,1,2,2]
Example 2:

Input: nums = [2,0,1]
Output: [0,1,2]


Constraints:

n == nums.length
1 <= n <= 300
nums[i] is either 0, 1, or 2.


Follow up: Could you come up with a one-pass algorithm using only constant extra space?
"""

from typing import List


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # my1
        # res = sorted(nums)
        # for i in range(len(nums)):
        #     nums[i] = res[i]

        # # my2
        # c = Counter(nums)
        # i = 0
        # for n in range(3):
        #     j = 0
        #     for j in range(c[n]):
        #         ind = i + j
        #         nums[ind] = n
        #     i += j + 1

        zero = -1
        one = -1
        two = -1

        for num in nums:
            if num == 0:
                two += 1
                one += 1
                zero += 1
                nums[two] = 2
                nums[one] = 1
                nums[zero] = 0
            elif num == 1:
                two += 1
                one += 1
                nums[two] = 2
                nums[one] = 1
            else:
                two += 1
                nums[two] = 2


if __name__ == "__main__":
    a = [2, 0, 2, 1, 1, 0]
    Solution().sortColors(a)
    assert a == [0, 0, 1, 1, 2, 2]

    a = [2, 0, 1]
    Solution().sortColors(a)
    assert a == [0, 1, 2]
