"""
https://www.codingame.com/ide/puzzle/death-first-search-episode-2
"""

import collections
import sys

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


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


def risk_factor(u, distances, nodes_connected_to_gates):
    # computes risk of vertex u
    ...
    dist = distances[u]
    gates_connected = len(nodes_connected_to_gates[u])

    risk = gates_connected - dist
    return risk


def main(si, adj_list, gateways):
    distances = calc_distances(si, adj_list)

    nodes_connected_to_gates = collections.defaultdict(set)
    for u in gateways:
        for n in adj_list[u]:
            if n not in gateways:
                nodes_connected_to_gates[n].add(u)

    node_to_block = None
    max_risk = float("-inf")
    for node in nodes_connected_to_gates:
        risk = risk_factor(node, distances, nodes_connected_to_gates)
        debug(f"risk_factor({node})={risk}")
        if risk > max_risk:
            max_risk = risk
            node_to_block = node

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


DEBUG = False
if DEBUG:
    n = 8
    l = 13  # noqa: E741
    e = 2
    # len(edges)=13
    edges = [(6, 2), (7, 3), (6, 3), (5, 3), (3, 4), (7, 1), (2, 0), (0, 1), (0, 3), (1, 3), (2, 3), (7, 4), (6, 5)]
    adj_list = {
        6: [2, 3, 5],
        2: [6, 0, 3],
        7: [3, 1, 4],
        3: [7, 6, 5, 4, 0, 1, 2],
        5: [3, 6],
        4: [3, 7],
        1: [7, 0, 3],
        0: [2, 1, 3],
    }
    degree = {6: 3, 2: 3, 7: 3, 3: 7, 5: 2, 4: 2, 1: 3, 0: 3}
    gateways = [4, 5]
    si = 0

    main(0, adj_list, gateways)
    main(6, adj_list, gateways)
else:
    n, l, e = [int(i) for i in input().split()]  # noqa: E741

    edges = []
    adj_list = collections.defaultdict(list)
    degree = collections.defaultdict(int)
    for i in range(l):
        # n1: N1 and N2 defines a link between these nodes
        n1, n2 = [int(j) for j in input().split()]
        # debug(f"{n1=}, {n2=}")
        edges.append((n1, n2))
        adj_list[n1].append(n2)
        adj_list[n2].append(n1)
        degree[n1] += 1
        degree[n2] += 1

    adj_list = dict(adj_list)
    degree = dict(degree)

    # the index of a gateway node
    gateways = [int(input()) for i in range(e)]

    debug(f"{n=}")
    debug(f"{l=}")
    debug(f"{e=}")
    debug(f"{edges=}")
    debug(f"{adj_list=}")
    debug(f"{degree=}")
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
