"""
https://leetcode.com/problems/clone-graph/?envType=problem-list-v2&envId=graph
"""

from typing import Optional
import copy


# Definition for a Node.
class Node:
    def __init__(self, val: int = 0, neighbors: Optional[list["Node"]] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


#
# class RawNode:
#     def __init__(self, val: int = 0, neighbors_indexes: Optional[list[int]] = None):
#         self.val = val
#         self.neighbors_indexes = neighbors_indexes if neighbors_indexes is not None else []


class Solution:
    # def _copy_node(self, node: Node, node_copy_by_index: dict[int, Node]) -> "Node":
    #     if node.val in node_copy_by_index:
    #         return node_copy_by_index[node.val]
    #
    #     val = node.val

    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
        # if node is None:
        #     return None
        #
        # node_copy_by_index = {}
        #
        # val = node.val
        # neighbors = []
        # for orig_neighbor in node.neighbors:
        #     if orig_neighbor.val in node_copy_by_index:
        #         neighbor = node_copy_by_index[orig_neighbor.val]
        #     else:
        #         neighbor = self._copy_node(orig_neighbor, node_copy_by_index)
        #         node_copy_by_index[orig_neighbor.val] = neighbor
        #     neighbors.append(neighbor)
        #
        # return Node(val, neighbors)
        return copy.deepcopy(node)


# def create_graph()


def main(adjList):
    return Solution().cloneGraph(adjList)


def _test(adjList):
    # raw_nodes = []
    # for ind, neighbors in enumerate(node_neighbors):
    #     raw_nodes.append(RawNode(ind + 1, neighbors))
    #
    # nodes_by_index = {}
    # for ind, raw_node in enumerate(raw_nodes):
    #     if ind in nodes_by_index:
    #         continue
    #
    #     val = raw_node.val
    #     neighbors = []
    #     for neighbor_ind in raw_node.neighbors_indexes:
    #         if neighbor_ind in nodes_by_index:
    #             neighbor = nodes_by_index[neighbor_ind]
    #         else:
    #             neighbor = Node(neighbor_ind)
    #             nodes_by_index[neighbor_ind] = neighbor
    #         neighbors.append(neighbor)
    #
    #     nodes_by_index[ind] = Node(val, neighbors)

    res = main(adjList)
    assert main(adjList) == adjList
    assert main(adjList) is not res


#
if __name__ == "__main__":
    """
    Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
    Output: [[2,4],[1,3],[2,4],[1,3]]
    Explanation: There are 4 nodes in the graph.
    1st node (val = 1)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
    2nd node (val = 2)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).
    3rd node (val = 3)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
    4th node (val = 4)'s neighbors are 1st node (val = 1) and 3rd node (val = 3)."""
    adjList = [[2, 4], [1, 3], [2, 4], [1, 3]]
    _test(adjList)
