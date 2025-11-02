"""
https://leetcode.com/problems/course-schedule-ii/?envType=problem-list-v2&envId=graph
"""

import collections
import enum

import pytest


class State(enum.IntEnum):
    unvisited = 0
    visiting = 1
    explored = 2


class CycleDetected(Exception):
    pass


class Solution:
    def _path_by_kahn(self, numCourses: int, prerequisites: list[list[int]]):
        adj_list = collections.defaultdict(list)
        for u, v in prerequisites:
            adj_list[u].append(v)

        # Build adjacency list adj[b] contains all a with edges b → a.
        directed_adj_list = collections.defaultdict(list)
        # Compute inDegree[a] = number of prerequisites (incoming edges) to a.
        in_degree: dict[int, int] = {}
        for u, _prerequisites in adj_list.items():
            in_degree[u] = len(_prerequisites)
            for v in _prerequisites:
                directed_adj_list[v].append(u)

        for u in range(numCourses):
            if u not in in_degree:
                in_degree[u] = 0
        in_degree = dict(in_degree)

        queue: collections.deque = collections.deque()
        for u, prerequisites_counter in in_degree.items():
            if prerequisites_counter == 0:
                queue.append(u)

        taken_count = 0
        path = []
        while queue:
            u = queue.popleft()
            path.append(u)
            taken_count += 1
            for v in directed_adj_list[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        # if not equals cycle exists
        if taken_count != numCourses:
            return []

        return path

    ### everything above is a copy from course_schedule.py
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        return self._path_by_kahn(numCourses, prerequisites)


def main(numCourses: int, prerequisites: list[list[int]]):
    return Solution().findOrder(numCourses, prerequisites)


@pytest.mark.parametrize(
    "input,expected_options",
    [
        pytest.param(
            dict(numCourses=2, prerequisites=[[1, 0]]),
            {(0, 1)},
            id="""Example 1:
                Input: numCourses = 2, prerequisites = [[1,0]]
                Output: [0,1]
                Explanation: There are a total of 2 courses to take. To take course 1 you should have finished course 0.
                So the correct course order is [0,1].
            """,
        ),
        pytest.param(
            dict(numCourses=4, prerequisites=[[1, 0], [2, 0], [3, 1], [3, 2]]),
            {(0, 1, 2, 3), (0, 2, 1, 3)},
            id="""Example 2:
                Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
                Output: [0,2,1,3]
                0 -> 1
                |    |
                v    v
                2 -> 3
                Explanation: There are a total of 4 courses to take. To take course 3 you should have finished both
                courses 1 and 2. Both courses 1 and 2 should be taken after you finished course 0.
                So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].
            """,
        ),
    ],
)
def test(input, expected_options):
    assert tuple(main(**input)) in expected_options
