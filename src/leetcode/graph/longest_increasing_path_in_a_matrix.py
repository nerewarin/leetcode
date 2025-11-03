"""
https://leetcode.com/problems/longest-increasing-path-in-a-matrix/?envType=problem-list-v2&envId=graph
"""

import pytest

print_backup = print
# print = lambda x: None


class Solution:
    def _get_neighbors(self, i, j, matrix_size):
        for step in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = i + step[0], j + step[1]
            for axis in range(2):
                if not 0 <= neighbor[axis] < matrix_size[axis]:
                    break
            else:
                yield neighbor

    def _get_value_by_pos_tuple(self, pos_tuple, matrix):
        return self._get_by_tuple(pos_tuple, matrix)

    def _get_by_tuple(self, pos_tuple, list2d):
        x, y = pos_tuple
        return list2d[x][y]

    def dfs(self, i, j, matrix, cache, matrix_size):
        if (i, j) in cache:
            return cache[(i, j)], cache

        max_path = 1

        value = matrix[i][j]

        neighbors = list(self._get_neighbors(i, j, matrix_size))

        for n, neighbor in enumerate(neighbors):
            n_x, n_y = neighbor

            n_value = self._get_value_by_pos_tuple(neighbor, matrix)

            if n_value > value:
                neighbor_path_len, cache = self.dfs(n_x, n_y, matrix, cache, matrix_size)
                path_len = 1 + neighbor_path_len
                max_path = max(max_path, path_len)

        cache[(i, j)] = max_path

        return max_path, cache

    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        if not matrix:
            return 0

        rows = len(matrix)
        cols = len(matrix[0])
        matrix_size = rows, cols

        max_path_cache: dict[int, int] = {}
        max_path_len = 1

        for i, row in enumerate(matrix):
            for j, cell in enumerate(row):
                import time

                start = time.time()
                print(f"considering ({i}, {j}) = {cell}")

                path_len, max_path_cache = self.dfs(i, j, matrix, max_path_cache, matrix_size)

                print(f"done in {time.time() - start} seconds. res = {path_len}")

                max_path_len = max(max_path_len, path_len)

        return max_path_len


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
    print_backup(res)
