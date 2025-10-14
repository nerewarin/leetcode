"""
https://leetcode.com/problems/add-two-numbers/?difficulty=MEDIUM


You are given two non-empty linked lists representing two non-negative integers.
The digits are stored in reverse order, and each of their nodes contains a single digit.
Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.
"""
import pytest
from typing import Optional
from pydantic import BaseModel, Field

class SingleDigitModel(BaseModel):
    value: int = Field(ge=0, le=9)  # 0 <= value <= 9

class OverflowModel(BaseModel):
    value: int = Field(ge=0, le=1)  # 0 <= value <= 1

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None) -> None:
        self.val = val
        self.next = next

    @classmethod
    def from_list(cls, lst: list[int]) -> "ListNode":
        prev_node = None
        for value in reversed(lst):
            node = cls()
            node.val = value
            node.next = prev_node
            prev_node = node

        return prev_node

    @classmethod
    def create_nodes(cls, *lists: list[int]) -> tuple["ListNode", ...]:
        return tuple(
            cls.from_list(l) for l in lists
        )

    def as_list(self) -> list[int]:
        vals = [self.val]
        node = self
        while next_node := node.next:
            vals.append(next_node.val)
            node = next_node

        return vals

    def __str__(self) -> str:
        return " -> ".join(map(str, self.as_list()))

    @staticmethod
    def _add_digits(*values: tuple[int]) -> tuple[SingleDigitModel, OverflowModel]:
        overflow, value = divmod(sum(values), 10)
        return SingleDigitModel(value=value), OverflowModel(value=overflow)

    def __add__(self, other: "ListNode") -> "ListNode":
        left = self
        right = other

        prev, prev_overflow = self._handle_pair(left, right, prev=None, prev_overflow=OverflowModel(value=0))
        first_elm = prev

        while left.next is not None or right.next is not None:
            if (left := left.next) is None:
                left = ListNode()
            if (right := right.next) is None:
                right = ListNode()

            prev, prev_overflow = self._handle_pair(left, right, prev, prev_overflow)

        if not isinstance(first_elm, ListNode):
            raise RuntimeError(f"expected ListNode, got {first_elm}")

        if prev_overflow.value:
            self._handle_pair(ListNode(), ListNode(), prev, prev_overflow)

        return first_elm

    def _handle_pair(self, left: "ListNode", right: "ListNode", prev: Optional["ListNode"], prev_overflow: OverflowModel) -> tuple["ListNode", OverflowModel]:
        res = self.__class__()
        value, overflow = self._add_digits(left.val, right.val, prev_overflow.value)
        res.val = value.value
        if prev is not None:
            prev.next = res
        return res, overflow


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        if l1 is None:
            return l2
        if l2 is None:
            return l1
        return l1 + l2

class TestListNode:
    def test_as_list(self):
        assert ListNode.from_list([2,4,3]).as_list() == [2,4,3]

    def test_create_node(self):
        assert str(ListNode.from_list([2,4,3])) == "2 -> 4 -> 3"

    def test_create_nodes(self):
        l1, l2 = ListNode.create_nodes([2,4,3], [5,6,4])
        assert str(l1) == "2 -> 4 -> 3"
        assert str(l2) == "5 -> 6 -> 4"


class TestSolution:
    """
    Input: l1 = [2,4,3], l2 = [5,6,4]
    Output: [7,0,8]
    Explanation: 342 + 465 = 807.
    Example 2:

    Input: l1 = [0], l2 = [0]
    Output: [0]
    Example 3:

    Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
    Output: [8,9,9,9,0,0,0,1]

    """
    @pytest.mark.parametrize("l1_raw,l2_raw,expected", [
        ([2, 4, 3], [5, 6, 4], [7, 0, 8]),
        ([0], [0], [0]),
        ([9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9], [8, 9, 9, 9, 0, 0, 0, 1]),
    ], ids=[
        "same_length_342_plus_465",
        "zeros",
        "different_length_large_carry",
    ])
    def test_add_two_numbers(self, l1_raw, l2_raw, expected):
        l1, l2 = ListNode.create_nodes(l1_raw, l2_raw)
        result = Solution().addTwoNumbers(l1, l2)
        assert result.as_list() == expected
