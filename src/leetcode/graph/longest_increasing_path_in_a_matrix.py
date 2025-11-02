"""
https://leetcode.com/problems/longest-increasing-path-in-a-matrix/?envType=problem-list-v2&envId=graph
"""

import collections

import pytest


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

    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        if not matrix:
            return 0

        rows = len(matrix)
        cols = len(matrix[0])
        matrix_size = rows, cols

        max_path_by_cell = [[0 for _ in range(cols)] for _ in range(rows)]

        for i, row in enumerate(matrix):
            for j, cell in enumerate(row):
                # compute max_path for cell expanding all paths from it, update all neighbors subpaths too

                # we can't just ignore visited, we can get there with longer path - store it
                visited_with_path_len: dict = {}
                cur_path_len = 1
                queue = collections.deque([(i, j, cur_path_len)])
                max_path_for_cell = 1
                while queue:
                    x, y, cur_path_len = queue.popleft()
                    value = matrix[x][y]
                    visited_with_path_len[(x, y)] = cur_path_len

                    all_neighbors = list(self._get_neighbors(x, y, matrix_size))

                    neighbors = []
                    for neighbor in all_neighbors:
                        if neighbor in visited_with_path_len:
                            if visited_with_path_len[neighbor] >= cur_path_len:
                                continue
                        neighbors.append(neighbor)

                    max_path_by_neighbor = [cur_path_len] * len(neighbors)
                    for n, neighbor in enumerate(neighbors):
                        n_x, n_y = neighbor
                        # if (n_x, n_y) in visited:
                        #     continue

                        n_value = self._get_value_by_pos_tuple(neighbor, matrix)

                        if n_value > value:
                            precomputed = self._get_by_tuple(neighbor, max_path_by_cell)
                            if precomputed:
                                max_path_by_neighbor[n] += precomputed
                            else:
                                # explore deeper
                                queue.append((n_x, n_y, cur_path_len + 1))
                                max_path_by_neighbor[n] += 1

                    if max_path_by_neighbor:
                        max_path_for_cell = max(max_path_for_cell, max(max_path_by_neighbor))

                max_path_by_cell[i][j] = max_path_for_cell

        absolute_max_path = 0
        for i, row in enumerate(max_path_by_cell):
            for j, max_path in enumerate(row):
                absolute_max_path = max(absolute_max_path, max_path)
        return absolute_max_path


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
            dict(matrix=[[7, 6, 1, 1], [2, 7, 6, 0], [1, 3, 5, 1], [6, 6, 3, 2]]),
            7,
        ),
    ],
)
def test(inp, expected):
    assert main(**inp) == expected
