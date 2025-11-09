"""
https://www.codingame.com/ide/puzzle/death-first-search-episode-2
"""

import collections
import os
import sys


# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways
def debug(msg):
    print(msg, file=sys.stderr, flush=True)


def calc_distances(si, adj_list):
    # computes a distances to si for every node
    min_distances = {x: float("inf") for x in range(n)}
    min_distances[si] = 0
    for x in adj_list[si]:
        min_distances[x] = 1

    queue = collections.deque()
    queue.append(si)

    visited = {si}

    while queue:
        u = queue.popleft()
        visited.add(u)
        for v in adj_list[u]:
            dist_to_si = min_distances[u]

            dist = dist_to_si + 1

            min_distances[v] = min(min_distances[v], dist)

            if v not in visited:
                queue.append(v)

    return min_distances


def compute_risks(si, adj_list, nodes_connected_to_gates, gateways):
    """
    For every node connected to gate, compute how dangerous it is for agent to reach in current state aka
        "risk" =  gates_connected  - distance (to agent) + accumulated_gates_connected
    where accumulated_gates_connected is amount of gates connected to nodes at previous steps on path to considered node.
    this way between two paths we (and agent) will prefer path with more gates on it.
    The idea is "if there are other gates on the path to it, we should spend some time to close another gates during
    this path, so its more dangerous".

    Note that in this algorythm we consider only shortest paths, not the most dangerous,
    TBH, I'm not sure if it works on cases containing more dangerous but longer path.
    But provided tests work like a charm.
    Feel free to contribute such case as an issue here :)
    https://github.com/nerewarin/leetcode/issues?q=sort%3Aupdated-desc+is%3Aissue+is%3Aopen

    """
    queue = collections.deque()
    queue.append((si, 0, 0))

    risks = dict()
    visited_nodes_to_min_dist = {}  # with min distances
    while queue:
        u, distance, accumulated_gates_connected = queue.popleft()
        if u in nodes_connected_to_gates:
            gates_connected = len(nodes_connected_to_gates[u])
        else:
            gates_connected = 0

        new_risk = gates_connected - distance + accumulated_gates_connected

        accumulated_gates_connected += gates_connected

        if gates_connected:
            risks[u] = max(risks.get(u, float("-inf")), new_risk)
        visited_nodes_to_min_dist[u] = distance

        for v in adj_list[u]:
            dist = distance + 1
            if v in gateways:
                continue

            if visited_nodes_to_min_dist.get(v, float("inf")) > dist:
                queue.append((v, dist, accumulated_gates_connected))

    return risks


def main(si, adj_list, gateways):
    distances = calc_distances(si, adj_list)

    nodes_connected_to_gates = collections.defaultdict(set)
    for u in gateways:
        for n in adj_list[u]:
            if n not in gateways:
                nodes_connected_to_gates[n].add(u)

    risks = compute_risks(si, adj_list, nodes_connected_to_gates, gateways)

    node_to_block = None
    max_risk = float("-inf")
    min_dist = float("inf")
    for node in sorted(list(nodes_connected_to_gates)):
        risk = risks[node]
        dist = distances[node]
        debug(f"risk_factor({node})={risk}")
        if risk > max_risk:
            max_risk = risk
            node_to_block = node
            min_dist = dist
        elif risk == max_risk:
            if dist < min_dist:
                node_to_block = node
                min_dist = dist

    if not node_to_block:
        debug(f"{node_to_block=}")
        return None

    gates_connected = nodes_connected_to_gates[node_to_block]
    gate_to_close = gates_connected.pop()

    edge_to_cut = (node_to_block, gate_to_close)
    debug(f"{edge_to_cut=}")

    # update state
    adj_list[gate_to_close].remove(node_to_block)
    adj_list[node_to_block].remove(gate_to_close)

    if adj_list[gate_to_close] == 0:
        adj_list.pop(adj_list)
        gateways.remove(gate_to_close)

    return edge_to_cut


DEBUG = os.getenv("DEBUG")
if DEBUG:
    ##################
    # 01 Robust double gateways
    ##################
    # n = 8
    # l = 13 # noqa: E741
    # e = 2
    # edges = [(6, 2), (7, 3), (6, 3), (5, 3), (3, 4), (7, 1), (2, 0), (0, 1), (0, 3), (1, 3), (2, 3), (7, 4), (6, 5)]
    # adj_list = {6: [2, 3, 5], 2: [6, 0, 3], 7: [3, 1, 4], 3: [7, 6, 5, 4, 0, 1, 2], 5: [3, 6], 4: [3, 7], 1: [7, 0, 3],
    #             0: [2, 1, 3]}
    # points = (0, 3, 6, 3)
    # gateways = [4, 5]

    ##################
    # 03  Leading up to a double gateway
    ##################
    n = 12
    l = 20  # noqa: E741
    e = 2
    edges = [
        (0, 9),
        (6, 1),
        (0, 6),
        (0, 3),
        (0, 2),
        (11, 5),
        (10, 11),
        (11, 9),
        (10, 9),
        (8, 9),
        (5, 9),
        (4, 5),
        (0, 4),
        (0, 1),
        (3, 4),
        (8, 10),
        (0, 5),
        (1, 2),
        (6, 7),
        (2, 3),
    ]
    adj_list = {
        0: [9, 6, 3, 2, 4, 1, 5],
        9: [0, 11, 10, 8, 5],
        6: [1, 0, 7],
        1: [6, 0, 2],
        3: [0, 4, 2],
        2: [0, 1, 3],
        11: [5, 10, 9],
        5: [11, 9, 4, 0],
        10: [11, 9, 8],
        8: [9, 10],
        4: [5, 0, 3],
        7: [6],
    }
    gateways = [0, 7]
    points = [8, 9]

    ##################
    # 05 Complex mesh
    ##################
    # n = 37
    # l = 81 # noqa: E741
    # e = 4
    # edges = [
    #     (2, 5), (14, 13), (16, 13), (19, 21), (13, 7), (16, 8), (35, 5), (2, 35), (10, 0), (8, 3), (23, 16),
    #     (0, 1), (31, 17), (19, 22), (12, 11), (1, 2), (1, 4), (14, 9), (17, 16), (30, 29), (32, 22), (28, 26),
    #     (24, 23), (20, 19), (15, 13), (18, 17), (6, 1), (29, 28), (15, 14), (9, 13), (32, 18), (25, 26), (1, 7),
    #     (34, 35), (33, 34), (27, 16), (27, 26), (23, 25), (33, 3), (16, 30), (25, 24), (3, 2), (5, 4), (31, 32),
    #     (27, 25), (19, 3), (17, 8), (4, 2), (32, 17), (10, 11), (29, 27), (30, 27), (6, 4), (24, 15), (9, 10),
    #     (34, 2), (9, 7), (11, 6), (33, 2), (14, 10), (12, 6), (0, 6), (19, 17), (20, 3), (21, 20), (21, 32),
    #     (15, 16), (0, 9), (23, 27), (11, 0), (28, 27), (22, 18), (3, 1), (23, 15), (18, 19), (7, 0), (19, 8),
    #     (21, 22), (7, 36), (13, 36), (8, 36),
    # ]
    # adj_list = {
    #     2: [5, 35, 1, 3, 4, 34, 33], 5: [2, 35, 4], 14: [13, 9, 15, 10], 13: [14, 16, 7, 15, 9, 36],
    #     16: [13, 8, 23, 17, 27, 30, 15], 19: [21, 22, 20, 3, 17, 18, 8], 21: [19, 20, 32, 22],
    #     7: [13, 1, 9, 0, 36], 8: [16, 3, 17, 19, 36], 35: [5, 2, 34], 10: [0, 11, 9, 14],
    #     0: [10, 1, 6, 9, 11, 7], 3: [8, 33, 2, 19, 20, 1], 23: [16, 24, 25, 27, 15], 1: [0, 2, 4, 6, 7, 3],
    #     31: [17, 32], 17: [31, 16, 18, 8, 32, 19], 22: [19, 32, 18, 21], 12: [11, 6], 11: [12, 10, 6, 0],
    #     4: [1, 5, 2, 6], 9: [14, 13, 10, 7, 0], 30: [29, 16, 27], 29: [30, 28, 27], 32: [22, 18, 31, 17, 21],
    #     28: [26, 29, 27], 26: [28, 25, 27], 24: [23, 25, 15], 20: [19, 3, 21], 15: [13, 14, 24, 16, 23],
    #     18: [17, 32, 22, 19], 6: [1, 4, 11, 12, 0], 25: [26, 23, 24, 27], 34: [35, 33, 2], 33: [34, 3, 2],
    #     27: [16, 26, 25, 29, 30, 23, 28], 36: [7, 13, 8],
    # }
    # gateways = [0, 16, 18, 26]
    # si = 2

    for point in points:
        main(point, adj_list, gateways)

else:
    n, l, e = [int(i) for i in input().split()]  # noqa: E741

    edges = []
    adj_list = collections.defaultdict(list)
    for i in range(l):
        # n1: N1 and N2 defines a link between these nodes
        n1, n2 = [int(j) for j in input().split()]
        # debug(f"{n1=}, {n2=}")
        edges.append((n1, n2))
        adj_list[n1].append(n2)
        adj_list[n2].append(n1)

    adj_list = dict(adj_list)

    # the index of a gateway node
    gateways = [int(input()) for i in range(e)]

    debug(f"{n=}")
    debug(f"{l=} # noqa: E741")
    debug(f"{e=}")
    debug(f"{edges=}")
    debug(f"{adj_list=}")
    debug(f"{gateways=}")

    # game loop
    while True:
        si = int(input())  # The index of the node on which the Bobnet agent is positioned this turn
        debug(f"{si=}")

        edge_to_cut = main(si, adj_list, gateways)

        if edge_to_cut:
            # Example: 3 4 are the indices of the nodes you wish to sever the link between
            print(" ".join(str(x) for x in edge_to_cut))
        else:
            print("")
