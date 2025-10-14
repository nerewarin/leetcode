from typing import List, Optional, Set
import unittest
import collections

DEBUG = False


class Solution:
    def __init__(self, world=None, visited: Optional[Set[int]] = None):
        self.world = world

        self.visited = set([])
        if visited is not None:
            self.visited = visited.copy()

    @property
    def start(self):
        vals = self.world[1]
        assert len(vals) == 1
        return vals[0]

    @property
    def end(self):
        vals = self.world[2]
        assert len(vals) == 1
        return vals[0]

    @property
    def obstacles(self):
        return self.world[-1]

    @property
    def emptiness(self):
        return self.world[0]

    def is_empty(self, xy):
        return xy in self.emptiness

    def get_possible_directions(self, xy):
        for x, y in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            p = xy[0] + x, xy[1] + y
            if p in self.visited:
                continue

            if self.is_empty(p):
                yield p

            # +1 for start but end itself not included yet
            to_visit = len(self.emptiness) + 1
            if p == self.end and len(self.visited) == to_visit:
                yield p

    def init_world(self, grid):
        if self.world:
            return False

        world = collections.defaultdict(list)
        for i, row in enumerate(grid):
            for j, el in enumerate(row):
                world[el].append((i, j))

        self.world = world
        return True

    def uniquePathsIII(self, grid: List[List[int]]) -> int:
        self.init_world(grid)
        return len(self._get_unique_path(grid))

    def _get_unique_path(self, grid: List[List[int]], path=None, start=None) -> set:
        visited = self.visited
        start = start or self.start
        path = path or tuple()

        to_visit: collections.deque = collections.deque()
        to_visit.append(start)

        unique_paths: Set[tuple] = set([])
        while to_visit:
            node = to_visit.popleft()
            path += (node,)
            visited.add(node)

            if self.end == node:
                if path is None:
                    return unique_paths

                unique_paths.add(path)
                continue

            neighboors = self.get_possible_directions(node)
            if DEBUG:
                neighboors = list(neighboors)

            for neighboor in neighboors:
                if neighboor in visited:
                    continue

                paths = self.__class__(self.world, visited)._get_unique_path(
                    grid, path, neighboor
                )
                unique_paths = unique_paths.union(paths)

        return unique_paths


class Test(unittest.TestCase):
    def _run(self, grid, output):
        global DEBUG
        DEBUG = True
        self.assertEqual(Solution().uniquePathsIII(grid), output)
        DEBUG = False

    def test1(self):
        self._run(grid=[[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, -1]], output=2)

    def test2(self):
        self._run(grid=[[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]], output=4)

    def test_no_solution(self):
        self._run(grid=[[0, 1], [2, 0]], output=0)

    def test_pribitive(self):
        self._run(grid=[[1, 2], [0, 0]], output=1)
