from typing import List


class Solution:
    def maxDistance(self, position: List[int], m: int) -> int:
        position.sort()
        original_position = list(position)

        p = len(position)

        if m < 2:
            return 0

        def calc_distance(position):
            res = float('inf')
            for previous, current in zip(position, position[1:]):
                res = min(res, current - previous)
            if res == float('inf'):
                return 0
            return res

        if p < m:
            return 0
        elif p == m:
            return calc_distance(position)

        # place first 2
        # indexes of placed balls
        placed = []

        def place(i):
            position.remove(i)
            placed.append(i)

        place(position[0])
        place(position[-1])

        return calc_distance(placed)



import unittest
class TestSolution(unittest.TestCase):
    def _test(self, position, m, expected):
        self.assertEqual(Solution().maxDistance(position, m), expected)

    def test_case_00(self):
        position = []
        m = 3
        expected = 0
        self._test(position, m, expected)

    def test_case_01(self):
        position = [1]
        m = 1
        expected = 0
        self._test(position, m, expected)

    def test_case_02(self):
        position = [1, 2]
        m = 2
        expected = 1
        self._test(position, m, expected)

    def test_case_1(self):
        position = [1,2,3,4,7]
        m = 3
        expected = 3
        self._test(position, m, expected)

    def test_case_2(self):
        position = [5, 4, 3, 2, 1, 1000000000]
        m = 2
        expected = 999999999
        self._test(position, m, expected)
