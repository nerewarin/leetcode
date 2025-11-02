"""
https://leetcode.com/problems/longest-increasing-path-in-a-matrix/?envType=problem-list-v2&envId=graph
"""

import pytest


class Solution:
    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        if not matrix:
            return 0

        if len(matrix) == 1:
            return 1

        # TODO
        return -1


def main(matrix: list[list[int]]) -> int:
    return Solution().longestIncreasingPath(matrix)


@pytest.mark.parametrize(
    "inp,expected",
    [
        pytest.param(
            dict(matrix=[[9, 9, 4], [6, 6, 8], [2, 1, 1]]),
            4,
            id="""Input: matrix = [[9,9,4],[6,6,8],[2,1,1]]
            Output: 4
            Explanation: The longest increasing path is [1, 2, 6, 9].
            """,
        ),
        pytest.param(
            dict(matrix=[[3, 4, 5], [3, 2, 6], [2, 2, 1]]),
            4,
            id="""Input: matrix = [[3,4,5],[3,2,6],[2,2,1]]
            Output: 4
            Explanation: The longest increasing path is [3, 4, 5, 6]. Moving diagonally is not allowed.
            """,
        ),
        pytest.param(
            dict(matrix=[[1]]),
            1,
            id="""Input: matrix = [[1]]
            Output: 1""",
        ),
    ],
)
def test(inp, expected):
    assert main(**inp) == expected
