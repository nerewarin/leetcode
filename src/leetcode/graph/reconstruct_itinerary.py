"""
https://leetcode.com/problems/reconstruct-itinerary/description/?envType=problem-list-v2&envId=graph
"""

import collections
import copy

import pytest


class Solution:
    def findItinerary(self, tickets: list[list[str]]) -> list[str]:
        _adj_list: collections.defaultdict[str, list[str]] = collections.defaultdict(list)
        for u, v in tickets:
            _adj_list[u].append(v)
        adj_list: dict[str, list[str]] = {u: sorted(v) for u, v in _adj_list.items()}

        # check if only 1 ticket between any 2 cities exists
        for u, vs in adj_list.items():
            assert len(set(vs)) == len(vs), f"many tickets from {u} detected: {[x for x in vs]}"

        start = "JFK"

        start_itinerary = [start]
        probe = 0
        with open("./test.txt", "w") as f:

            def dfs(src, left_tickets, itinerary, level):
                if not left_tickets:
                    return itinerary

                if not left_tickets.get(src):
                    return None

                possible_dst = left_tickets[src]

                for dst in possible_dst:
                    updated_left_tickets = copy.deepcopy(left_tickets)
                    updated_left_tickets[src].remove(dst)
                    if not updated_left_tickets[src]:
                        updated_left_tickets.pop(src)

                    new_itinerary = dfs(dst, updated_left_tickets, itinerary + [dst], level + 1)
                    if new_itinerary is not None:
                        return new_itinerary

                nonlocal probe
                print(f"{probe}. lvl={level}. left={len(left_tickets)} for {itinerary} len of {len(itinerary)}", file=f)
                probe += 1
                return None

            final_itinerary = dfs(start, adj_list, start_itinerary, level=0)
            return final_itinerary


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
        pytest.param(
            dict(
                tickets=[
                    ["JFK", "SFO"],
                    ["JFK", "ATL"],
                    ["SFO", "JFK"],
                    ["ATL", "AAA"],
                    ["AAA", "ATL"],
                    ["ATL", "BBB"],
                    ["BBB", "ATL"],
                    ["ATL", "CCC"],
                    ["CCC", "ATL"],
                    ["ATL", "DDD"],
                    ["DDD", "ATL"],
                    ["ATL", "EEE"],
                    ["EEE", "ATL"],
                    ["ATL", "FFF"],
                    ["FFF", "ATL"],
                    ["ATL", "GGG"],
                    ["GGG", "ATL"],
                    ["ATL", "HHH"],
                    ["HHH", "ATL"],
                    ["ATL", "III"],
                    ["III", "ATL"],
                    ["ATL", "JJJ"],
                    ["JJJ", "ATL"],
                    ["ATL", "KKK"],
                    ["KKK", "ATL"],
                    ["ATL", "LLL"],
                    ["LLL", "ATL"],
                    ["ATL", "MMM"],
                    ["MMM", "ATL"],
                    ["ATL", "NNN"],
                    ["NNN", "ATL"],
                ],
            ),
            [
                "JFK",
                "SFO",
                "JFK",
                "ATL",
                "AAA",
                "ATL",
                "BBB",
                "ATL",
                "CCC",
                "ATL",
                "DDD",
                "ATL",
                "EEE",
                "ATL",
                "FFF",
                "ATL",
                "GGG",
                "ATL",
                "HHH",
                "ATL",
                "III",
                "ATL",
                "JJJ",
                "ATL",
                "KKK",
                "ATL",
                "LLL",
                "ATL",
                "MMM",
                "ATL",
                "NNN",
                "ATL",
            ],
        ),
    ],
)
def test(inp, expected):
    assert main(**inp) == expected
