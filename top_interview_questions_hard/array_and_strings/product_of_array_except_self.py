"""
https://leetcode.com/explore/interview/card/top-interview-questions-hard/116/array-and-strings/827/

Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.



Example 1:

Input: nums = [1,2,3,4]
Output: [24,12,8,6]
Example 2:

Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]


Constraints:

2 <= nums.length <= 105
-30 <= nums[i] <= 30
The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.


Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)
"""
from typing import List



class Solution:
    @staticmethod
    def productExceptSelf(nums: List[int]) -> List[int]:
        """
        An approach using prefix and suffix multiplication: Create two extra space,
        i.e. two extra arrays to store the product of all the array elements from start,
         up to that index and another array to store the product of all the array elements
         from the end of the array to that index.
        To get the product excluding that index, multiply the prefix product up to index i-1 with
         the suffix product up to index i+1.

        from here: https://www.geeksforgeeks.org/a-product-array-puzzle/
        """
        l = len(nums)
        prefix = [0] * l
        suffix = [0] * l

        for i, num in enumerate(nums):
            j = l - i - 1
            if i == 0:
                prefix[i] = 1
                suffix[j] = 1
                continue

            # For every index i update prefix[i] as prefix[i] = prefix[i-1] * array[i-1],
            # i.e store the product upto i-1 index from the start of array.
            prefix[i] = prefix[i - 1] * nums[i-1]

            suffix[j] = suffix[j + 1] * nums[j+1]

        return [prefix[i] * suffix[i] for i in range(l)]


if __name__ == '__main__':
    for in_, out in (
                            ([1, 2, 3], [6, 3, 2]),
                            ([3, 2, 1], [2, 3, 6]),
    ):
        assert Solution.productExceptSelf(in_) == out, f"expected {out=} for {in_=}"
