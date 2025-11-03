"""
https://leetcode.com/problems/longest-increasing-path-in-a-matrix/?envType=problem-list-v2&envId=graph
"""

import pytest


class Solution:
    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        if not matrix:
            return 0

        rows, cols = len(matrix), len(matrix[0])
        memo: dict[tuple[int, int], int] = {}

        def dfs(i, j):
            if (i, j) in memo:
                return memo[(i, j)]

            max_length = 1
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < rows and 0 <= nj < cols and matrix[ni][nj] > matrix[i][j]:
                    max_length = max(max_length, 1 + dfs(ni, nj))

            memo[(i, j)] = max_length
            return max_length

        return max(dfs(i, j) for i in range(rows) for j in range(cols))


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
        pytest.param(
            dict(matrix=[[3, 4, 5], [3, 2, 6], [7, 2, 1]]),
            4,
            id="""Input: matrix = [[3,4,5],[3,2,6],[7,2,1]]
            Output: 4
            Explanation: The longest increasing path is [3, 4, 5, 6]. Moving diagonally is not allowed.
            """,
        ),
        pytest.param(
            dict(matrix=[[1, 2]]),
            2,
        ),
        pytest.param(
            dict(matrix=[[7, 6, 1, 1], [2, 7, 6, 0], [1, 3, 5, 1], [6, 6, 3, 2]]),
            7,
        ),
        pytest.param(
            dict(
                matrix=[
                    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    [19, 18, 17, 16, 15, 14, 13, 12, 11, 10],
                    [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
                    [39, 38, 37, 36, 35, 34, 33, 32, 31, 30],
                    [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
                    [59, 58, 57, 56, 55, 54, 53, 52, 51, 50],
                    [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
                    [79, 78, 77, 76, 75, 74, 73, 72, 71, 70],
                    [80, 81, 82, 83, 84, 85, 86, 87, 88, 89],
                    [99, 98, 97, 96, 95, 94, 93, 92, 91, 90],
                    [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
                    [119, 118, 117, 116, 115, 114, 113, 112, 111, 110],
                    [120, 121, 122, 123, 124, 125, 126, 127, 128, 129],
                    [139, 138, 137, 136, 135, 134, 133, 132, 131, 130],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ],
            ),
            140,
            id="""
            case 6: big matrix
                    0   1   2   3   4   5   6   7   8   9
                    19  18  17  16  15  14  13  12  11  10
                    20  21  22  23  24  25  26  27  28  29
                    39  38  37  36  35  34  33  32  31  30
                    40  41  42  43  44  45  46  47  48  49
                    59  58  57  56  55  54  53  52  51  50
                    60  61  62  63  64  65  66  67  68  69
                    79  78  77  76  75  74  73  72  71  70
                    80  81  82  83  84  85  86  87  88  89
                    99  98  97  96  95  94  93  92  91  90
                    100 101 102 103 104 105 106 107 108 109
                    119 118 117 116 115 114 113 112 111 110
                    120 121 122 123 124 125 126 127 128 129
                    139 138 137 136 135 134 133 132 131 130
                    0   0   0   0   0   0   0   0   0   0
            """,
        ),
    ],
)
def test(inp, expected):
    assert main(**inp) == expected


if __name__ == "__main__":
    res = main(
        matrix=[
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [19, 18, 17, 16, 15, 14, 13, 12, 11, 10],
            [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
            [39, 38, 37, 36, 35, 34, 33, 32, 31, 30],
            [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
            [59, 58, 57, 56, 55, 54, 53, 52, 51, 50],
            [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
            [79, 78, 77, 76, 75, 74, 73, 72, 71, 70],
            [80, 81, 82, 83, 84, 85, 86, 87, 88, 89],
            [99, 98, 97, 96, 95, 94, 93, 92, 91, 90],
            [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            [119, 118, 117, 116, 115, 114, 113, 112, 111, 110],
            [120, 121, 122, 123, 124, 125, 126, 127, 128, 129],
            [139, 138, 137, 136, 135, 134, 133, 132, 131, 130],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
    )
    print(res)
