"""
https://leetcode.com/problems/reconstruct-itinerary/description/?envType=problem-list-v2&envId=graph
"""

import collections
import copy

import pytest


class Solution:
    @staticmethod
    def _get_possible_dst(src, left_tickets, itinerary_for_debug):
        def reachable(c, updated_left_tickets):
            for destinations in updated_left_tickets.values():
                if c in destinations:
                    return True
            return False

        candidates = left_tickets[src]
        final_candidates = []
        for candidate in candidates:
            # if itinerary_for_debug == ["JFK", "SFO", "JFK", "ATL"] and candidate == "AAA":
            #     debug = True  # debug case inp2 (starting from 0)
            updated_left_tickets = copy.deepcopy(left_tickets)
            updated_left_tickets[src].remove(candidate)
            if not updated_left_tickets[src]:
                updated_left_tickets.pop(src)

            # check that any left candidate is reachable
            other_candidates = [c for c in candidates if c != candidate]

            for another_candidate in other_candidates:
                left_tickets_except_another = copy.deepcopy(updated_left_tickets)
                left_tickets_except_another[src].remove(another_candidate)
                if not left_tickets_except_another[src]:
                    left_tickets_except_another.pop(src)

                # we want every another is reachable from the rest part of this graph (with src - another_candidate edge cutted)
                another_is_reachable_not_from_src = reachable(another_candidate, left_tickets_except_another)
                # but it's not always possible. another way is to get back to src at least and go to another from src.
                # so now but branch another->src (if exists) and check src is still reachable from our cutted graph left
                left_tickets_except_src_from_another = copy.deepcopy(updated_left_tickets)
                if src in left_tickets_except_src_from_another.get(another_candidate, []):
                    left_tickets_except_src_from_another[another_candidate].remove(src)
                    if not left_tickets_except_src_from_another[another_candidate]:
                        left_tickets_except_src_from_another.pop(another_candidate)

                is_reachable = another_is_reachable_not_from_src or reachable(src, left_tickets_except_src_from_another)
                if is_reachable:
                    continue
                else:
                    break
            else:
                final_candidates.append(candidate)

        return final_candidates

    def findItinerary(self, tickets: list[list[str]], f=None) -> list[str]:
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

        def dfs(src, left_tickets, itinerary, level):
            if not left_tickets:
                return itinerary

            if not left_tickets.get(src):
                return None

            if left_tickets[src]:
                possible_dst = list(self._get_possible_dst(src, left_tickets, itinerary))

                for dst in possible_dst:
                    updated_left_tickets = copy.deepcopy(left_tickets)
                    updated_left_tickets[src].remove(dst)
                    if not updated_left_tickets[src]:
                        updated_left_tickets.pop(src)

                    new_itinerary = dfs(dst, updated_left_tickets, itinerary + [dst], level + 1)
                    if new_itinerary is not None:
                        return new_itinerary

            nonlocal probe
            if f:
                print(f"{probe}. lvl={level}. left={len(left_tickets)} for {itinerary} len of {len(itinerary)}", file=f)
            probe += 1
            return None

        final_itinerary = dfs(start, adj_list, start_itinerary, level=0)
        if f:
            print(f"{probe}. success: {final_itinerary}", file=f)

        return final_itinerary


def main(tickets: list[list[str]], f) -> list[str]:
    return Solution().findItinerary(tickets, f)


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
        pytest.param(
            dict(tickets=[["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]]),
            ["JFK", "NRT", "JFK", "KUL"],
        ),
    ],
)
def test(inp, expected, request):
    test_id = request.node.callspec.id
    import pathlib

    file_ = pathlib.Path(__file__)
    path = file_.parent / (file_.stem + f"-test-{test_id}.txt")
    with path.open("w") as f:
        assert main(**inp, f=f) == expected
