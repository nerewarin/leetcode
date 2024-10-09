"""
https://leetcode.com/problems/all-ancestors-of-a-node-in-a-directed-acyclic-graph/?envType=daily-question&envId=2024-06-29


"""
from typing import List


class Graph:
    def __init__(self,  edges: List[List[int]]):
        self.edges = edges
        self._ancestors = {}

    def get_ancestors(self, i):
        if i in self._ancestors:
            return self._ancestors[i]

        lefts = []
        for edge in self.edges:
            left, right = edge
            if i != right:
                continue

            lefts.append(left)

        ancestors = []
        while lefts:
            v = lefts.pop(0)
            if v in ancestors:
                continue
            ancestors.append(v)

            another_lefts = self.get_ancestors(v)
            for a in another_lefts:
                if a not in ancestors:
                    ancestors.append(a)

        self._ancestors[i] = sorted(ancestors)

        return self._ancestors[i]


class Solution:
    def getAncestors(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        g = Graph(edges)

        res = []
        for i in range(n):
            r = g.get_ancestors(i)
            res.append(r)

        return res


import unittest
class TestSolution(unittest.TestCase):
    def _test(self, n, edgeList, expected):
        self.assertEqual(Solution().getAncestors(n, edgeList), expected)

    def test_case_00(self):
        n = 8
        edgeList = [[0, 3], [0, 4], [1, 3], [2, 4], [2, 7], [3, 5], [3, 6], [3, 7], [4, 6]]
        expected = [[], [], [], [0, 1], [0, 2], [0, 1, 3], [0, 1, 2, 3, 4], [0, 1, 2, 3]]

        self._test(n, edgeList, expected)

    def test_case_01(self):
        n = 6
        edgeList = [[0,3],[5,0],[2,3],[4,3],[5,3],[1,3],[2,5],[0,1],[4,5],[4,2],[4,0],[2,1],[5,1]]
        expected = [[2,4,5],[0,2,4,5],[4],[0,1,2,4,5],[],[2,4]]

        self._test(n, edgeList, expected)
