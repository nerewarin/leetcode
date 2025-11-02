"""
https://leetcode.com/problems/add-two-numbers/?difficulty=MEDIUM


You are given two non-empty linked lists representing two non-negative integers.
The digits are stored in reverse order, and each of their nodes contains a single digit.
Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.
"""

from typing import Optional


# Definition for singly-linked list.
# COMMENT OUT THIS CLASS BEFORE SEND TO LEETCODE
class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


class SingleDigit:
    def __init__(self, value: int):
        if not 0 <= value <= 9:
            raise ValueError("value must be between 0 and 9")
        self.value = value


class Overflow:
    def __init__(self, value: int):
        if not 0 <= value <= 1:
            raise ValueError("value must be between 0 and 9")
        self.value = value


class Solution:
    def addTwoNumbers(self, l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
        if l1 is None:
            return l2
        if l2 is None:
            return l1
        return self._sum(l1, l2)

    @staticmethod
    def _add_digits(*values: int) -> tuple[SingleDigit, Overflow]:
        overflow, value = divmod(sum(values), 10)
        return SingleDigit(value=value), Overflow(value=overflow)

    @classmethod
    def _handle_pair(
        cls,
        left: "ListNode",
        right: "ListNode",
        prev: Optional["ListNode"],
        prev_overflow: Overflow,
    ) -> tuple["ListNode", Overflow]:
        res = ListNode()
        value, overflow = cls._add_digits(left.val, right.val, prev_overflow.value)
        res.val = value.value
        if prev is not None:
            prev.next = res
        return res, overflow

    def _sum(cls, left: "ListNode", right: "ListNode") -> "ListNode":
        prev, prev_overflow = cls._handle_pair(left, right, prev=None, prev_overflow=Overflow(value=0))
        first_elm = prev

        while left.next is not None or right.next is not None:
            left_next = left.next
            if left_next is None:
                left = ListNode()
            else:
                left = left_next
            right_next = right.next
            if right_next is None:
                right = ListNode()
            else:
                right = right_next

            prev, prev_overflow = cls._handle_pair(left, right, prev, prev_overflow)

        if not isinstance(first_elm, ListNode):
            raise RuntimeError(f"expected ListNode, got {first_elm}")

        if prev_overflow.value:
            cls._handle_pair(ListNode(), ListNode(), prev, prev_overflow)

        return first_elm
