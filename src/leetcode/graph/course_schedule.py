"""
https://leetcode.com/problems/course-schedule/?envType=problem-list-v2&envId=graph

"""

from typing import List

import pytest
import collections


class CycleDetected(Exception):
    pass


class Solution:
    @staticmethod
    def _is_cyclic(adj_list: collections.defaultdict[int, list]):
        visited = set()

        def dfs(u):
            if u not in visited:
                visited.add(u)
            else:
                raise CycleDetected

            for v in adj_list.get(u, []):
                dfs(v)

        for u in adj_list:
            try:
                dfs(u)
            except CycleDetected:
                return True
        return False

    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # need to search for cyclic reference

        # format adj lists
        adj_list = collections.defaultdict(list)
        for u, v in prerequisites:
            adj_list[u].append(v)

        res = not self._is_cyclic(adj_list)
        return res


def main(numCourses: int, prerequisites: List[List[int]]):
    return Solution().canFinish(numCourses, prerequisites)


@pytest.mark.parametrize(
    "input,expected",
    [
        pytest.param(
            dict(numCourses=2, prerequisites=[[1, 0]]),
            True,
            id="""Example 1:
                Input: numCourses = 2, prerequisites = [[1,0]]
                Output: true
                Explanation: There are a total of 2 courses to take.
                To take course 1 you should have finished course 0. So it is possible.e
            """,
        ),
        pytest.param(
            dict(numCourses=2, prerequisites=[[1, 0], [0, 1]]),
            False,
            id="""Example 2:
                Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
                Output: false
                Explanation: There are a total of 2 courses to take.
                To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.
            """,
        ),
        pytest.param(
            dict(numCourses=5, prerequisites=[[1, 4], [2, 4], [3, 1], [3, 2]]),
            True,
            id="""Example 3: [[1,4],[2,4],[3,1],[3,2]]

            1  <- 4
            ^     |
            |     v
            3  <- 2

            """,
        ),
    ],
)
def test(input, expected):
    assert main(**input) == expected
