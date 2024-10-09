"""
https://leetcode.com/problems/palindromic-substrings/?envType=daily-question&envId=2024-06-29
"""

class Solution:
    def countSubstrings(self, s: str) -> int:
        subs = []
        for i, letter in enumerate(s):
            fringe = [
                (
                    i,
                    letter
                )
            ]

            while fringe:
                idx, candidate = fringe.pop(0)
                if candidate[::-1] == candidate:
                    subs.append(candidate)

                if idx + len(candidate) < len(s):
                    fringe.append((idx, candidate + s[idx + len(candidate)]))

        return len(subs)



import unittest
class TestSolution(unittest.TestCase):
    def _test(self, s, expected):
        self.assertEqual(Solution().countSubstrings(s), expected)

    def test_case_00(self):
        s = "abc"
        expected = 3

        self._test(s, expected)

    def test_case_01(self):
        s = "aaa"
        expected = 6

        self._test(s, expected)
