"""
https://leetcode.com/explore/interview/card/top-interview-questions-medium/112/design/813/

Implement the RandomizedSet class:

RandomizedSet() Initializes the RandomizedSet object.
bool insert(int val) Inserts an item val into the set if not present. Returns true if the item was not present, false otherwise.
bool remove(int val) Removes an item val from the set if present. Returns true if the item was present, false otherwise.
int getRandom() Returns a random element from the current set of elements (it's guaranteed that at least one element exists when this method is called). Each element must have the same probability of being returned.
You must implement the functions of the class such that each function works in average O(1) time complexity.

"""

import random


# class RandomizedSet:
#   def __init__(self):
#     """
#     Initialize your data structure here.
#     """
#     self.vals = []
#     self.valToIndex = collections.defaultdict(int)
#
#   def insert(self, val: int) -> bool:
#     """
#     Inserts a value to the set. Returns true if the set did not already contain the specified element.
#     """
#     if val in self.valToIndex:
#       return False
#
#     self.valToIndex[val] = len(self.vals)
#     self.vals.append(val)
#     return True
#
#   def remove(self, val: int) -> bool:
#     """
#     Removes a value from the set. Returns true if the set contained the specified element.
#     """
#     if val not in self.valToIndex:
#       return False
#
#     index = self.valToIndex[val]
#     self.valToIndex[self.vals[-1]] = index
#     del self.valToIndex[val]
#     self.vals[index] = self.vals[-1]
#     self.vals.pop()
#     return True
#
#   def getRandom(self) -> int:
#     """
#     Get a random element from the set.
#     """
#     index = random.randint(0, len(self.vals) - 1)
#     return self.vals[index]


class RandomizedSet:
    def __init__(self):
        self.vals = set([])

    def insert(self, val: int) -> bool:
        if val in self.vals:
            return False

        self.vals.add(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.vals:
            return False

        self.vals.remove(val)
        return True

    def getRandom(self) -> int:
        return random.choice(list(self.vals))


if __name__ == "__main__":
    r = RandomizedSet()
    [
        "RandomizedSet",
        "insert",
        "remove",
        "insert",
        "getRandom",
        "remove",
        "insert",
        "getRandom",
    ]
    [[], [1], [2], [2], [], [1], [2], []]
    # Output
    # [null, true, false, true, 2, true, false, 2]
    assert r.insert(1) is True
    assert r.remove(2) is False
    assert r.insert(2) is True
    x = r.getRandom()
    assert x in (1, 2), x
    assert r.remove(1) is True
    assert r.insert(2) is False
    assert r.getRandom() == 2
