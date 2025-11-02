"""
https://leetcode.com/problems/clone-graph/?envType=problem-list-v2&envId=graph
"""

from typing import Optional


# # Definition for a Node.
class Node:
    def __init__(self, val: int = 0, neighbors: list["Node"] | None = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
        if not node:
            return None

        cloned: dict[Node, Node] = {}  # original node -> cloned node

        def dfs(cur: "Node") -> "Node":
            if cur in cloned:
                return cloned[cur]

            copy = Node(cur.val)
            cloned[cur] = copy
            for nei in cur.neighbors:
                copy.neighbors.append(dfs(nei))
            return copy

        return dfs(node)
