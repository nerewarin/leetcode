"""
https://leetcode.com/problems/reconstruct-itinerary/description/?envType=problem-list-v2&envId=graph
"""

import collections

import pytest


class Solution:
    def findItinerary(self, tickets: list[list[str]]) -> list[str]:
        _adj_list: collections.defaultdict[str, list[str]] = collections.defaultdict(list)
        for u, v in tickets:
            _adj_list[u].append(v)
        adj_list: dict[str, list[str]] = {u: sorted(v) for u, v in _adj_list.items()}

        src = "JFK"

        itinerary = [src]

        while adj_list.get(src):
            possible_dst = adj_list[src]
            dst = possible_dst.pop(0)
            itinerary.append(dst)
            src = dst

        return itinerary


def main(tickets: list[list[str]]) -> list[str]:
    return Solution().findItinerary(tickets)


@pytest.mark.parametrize(
    "inp,expected",
    [
        pytest.param(
            dict(tickets=[["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]),
            ["JFK", "MUC", "LHR", "SFO", "SJC"],
        ),
        pytest.param(
            dict(tickets=[["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]),
            ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"],
        ),
    ],
)
def test(inp, expected):
    assert main(**inp) == expected
