"""
https://leetcode.com/problems/maximum-students-taking-exam/description/
"""
import unittest
from typing import List


class Solution:
    # def maxStudents(self, seats: List[List[str]]) -> int:
    #     m = len(seats)
    #     n = len(seats[0])
    #     cols2seats = {}
    #     even_vs_odd_columns = [0, 0]
    #     # for row_idx, row in enumerate(seats):
    #     # for col_ind in range(m):
    #     for col_ind in range(n):
    #         cols2seats[col_ind] = 0
    #         # even_vs_odd_columns[j] = 0
    #         # for j, value in enumerate(row):
    #         for row_idx, row in enumerate(seats):
    #             if row[col_ind] == ".":
    #                 cols2seats[col_ind] += 1
    #                 print(f"found {row_idx=}, {col_ind=}")
    #                 if col_ind % 2:
    #                     even_vs_odd_columns[1] += 1
    #                 else:
    #                     even_vs_odd_columns[0] += 1
    #
    #     print(even_vs_odd_columns)
    #     print(cols2seats)
    #
    #     most_effective_columns = sorted(cols2seats, key=lambda k: (cols2seats[k], even_vs_odd_columns[k % 2]), reverse=True)
    #     world = [[0] * n for _ in range(m)]
    #     places = 0
    #     for col_idx in most_effective_columns:
    #         column = [row[col_idx] for row in seats]
    #         for row_idx, el in enumerate(column):
    #             if el == ".":
    #                 # check conflicts
    #                 if col_idx > 0:
    #                     left = [row[col_idx - 1] for row in world]
    #                     if left[row_idx]:
    #                         continue
    #                     if row_idx - 1 > 0 and left[row_idx - 1]:
    #                         continue
    #                     if row_idx + 1 < m and left[row_idx + 1]:
    #                         continue
    #                 if col_idx + 1 < n:
    #                     right = [row[col_idx + 1] for row in world]
    #                     if right[row_idx]:
    #                         continue
    #                     if row_idx - 1 > 0 and right[row_idx - 1]:
    #                         continue
    #                     if row_idx + 1 < m and right[row_idx + 1]:
    #                         continue
    #                 world[row_idx][col_idx] = 1
    #                 places += 1
    #
    #     for row in world: print(row)
    #     print(places)
    #     return places
    def maxStudents(self, seats):
        m, n = len(seats), len(seats[0])

        def can_place(i, j):
            if seats[i][j] == '#' or (j > 0 and seats[i][j - 1] == 'S') or (
                    j < n - 1 and seats[i][j + 1] == 'S') or (
                    i > 0 and j > 0 and seats[i - 1][j - 1] == 'S') or (
                    i > 0 and j < n - 1 and seats[i - 1][j + 1] == 'S'):
                return False
            return True

        def count_students(seating):
            return sum(row.count('S') for row in seating)

        def backtrack(seating, row):
            if row == m:
                return count_students(seating)

            max_students = 0
            for j in range(n):
                if can_place(row, j):
                    seating[row][j] = 'S'
                    max_students = max(max_students, backtrack(seating, row + 1))
                    seating[row][j] = '.'

            return max_students

        return backtrack(seats, 0)

class Test1(unittest.TestCase):
    def _test(self, data, expected):
        for row in data:
            print("".join(row))
        res = (
            Solution().maxStudents(data)
        )
        self.assertEqual(expected, res)

    def test1(self):
        self._test(
            [
                ["#", ".", "#", "#", ".", "#"],
                [".", "#", "#", "#", "#", "."],
                ["#", ".", "#", "#", ".", "#"]
            ],
            4,
        )

    def test2(self):
        self._test(
            [
                [".", "#"],
                ["#", "#"],
                ["#", "."],
                ["#", "#"],
                [".", "#"]],
            3,
        )

    def test3(self):
        self._test(
            [
                ["#", ".", ".", ".", "#"],
                [".", "#", ".", "#", "."],
                [".", ".", "#", ".", "."],
                [".", "#", ".", "#", "."],
                ["#", ".", ".", ".", "#"]
            ]
            , 10
        )

    def test4(self):
        self._test(
            [
                ["#", "#", "."],
                ["#", ".", "."],
                [".", ".", "#"]
            ],
            3,
        )

    def test5(self):
        self._test(
            [
                ["#", "#", "#", ".", "#"],
                [".", ".", "#", ".", "."],
                ["#", ".", "#", ".", "#"],
                [".", ".", ".", ".", "."],
                [".", ".", ".", "#", "."]
            ],
            9,
        )