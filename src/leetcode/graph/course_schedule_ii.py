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
    @staticmethod
    def _is_cyclic_dfs_with_colors(numCourses: int, prerequisites: list[list[int]]) -> bool:
        # format adj lists
        adj_list = collections.defaultdict(list)
        for u, v in prerequisites:
            adj_list[u].append(v)

        states: collections.defaultdict[int, State] = collections.defaultdict(lambda: State.unvisited)

        def dfs(u):
            assert (not states[u]) == (states[u] == State.unvisited)
            if not states[u]:
                states[u] = State.visiting

            for v in adj_list.get(u, []):
                if states[v] == State.unvisited:
                    dfs(v)
                if states[v] == State.visiting:
                    raise CycleDetected(f"Visited cycle detected at node {v!r}!")

            states[u] = State.explored

        # for every node
        for u in adj_list:
            try:
                dfs(u)
            except CycleDetected:
                return True
        return False

    def _is_cycle_kahn(self, numCourses: int, prerequisites: list[list[int]]):
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
        while queue:
            u = queue.popleft()
            taken_count += 1
            for v in directed_adj_list[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        # if equals - no cycle
        return taken_count != numCourses

    def canFinish(
        self,
        numCourses: int,
        prerequisites: list[list[int]],
        alg: str = "Kahn’s Algorithm (BFS / in-degree)",
    ) -> bool:
        if alg == "Kahn’s Algorithm (BFS / in-degree)":
            res = not self._is_cycle_kahn(numCourses, prerequisites)
        elif alg == "DFS with colors (cycle detection)":
            # need to search for cyclic reference
            res = not self._is_cyclic_dfs_with_colors(numCourses, prerequisites)
        else:
            raise NotImplementedError(f"{alg} not implemented")
        return res

    ### everything above is a copy from course_schedule.py
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        if not self.canFinish(numCourses, prerequisites):
            return []
        return []  # TODO


def main(numCourses: int, prerequisites: list[list[int]]):
    return Solution().findOrder(numCourses, prerequisites)


@pytest.mark.parametrize(
    "input,expected",
    [
        pytest.param(
            dict(numCourses=2, prerequisites=[[1, 0]]),
            [0, 1],
            id="""Example 1:
                Input: numCourses = 2, prerequisites = [[1,0]]
                Output: [0,1]
                Explanation: There are a total of 2 courses to take. To take course 1 you should have finished course 0.
                So the correct course order is [0,1].
            """,
        ),
        pytest.param(
            dict(numCourses=4, prerequisites=[[1, 0], [2, 0], [3, 1], [3, 2]]),
            False,
            id="""Example 2:
                Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
                Output: [0,2,1,3]
                Explanation: There are a total of 4 courses to take. To take course 3 you should have finished both
                courses 1 and 2. Both courses 1 and 2 should be taken after you finished course 0.
                So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].
            """,
        ),
    ],
)
def test(input, expected):
    assert main(**input) == expected
