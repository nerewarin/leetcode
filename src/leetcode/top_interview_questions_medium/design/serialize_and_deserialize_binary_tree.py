"""
https://leetcode.com/explore/interview/card/top-interview-questions-medium/112/design/812/

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

Clarification: The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.



Example 1:


Input: root = [1,2,3,null,null,4,5]
Output: [1,2,3,null,null,4,5]
Example 2:

Input: root = []
Output: []


Constraints:

The number of nodes in the tree is in the range [0, 104].
-1000 <= Node.val <= 1000

"""
import collections

# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.
        """
        if not root:
            return ""
        #
        # i = 0
        # vertex = root[i]
        # layer = 0
        #
        # ans = str(vertex)
        # nodes = [vertex]
        # while i < len(root):
        return ",".join(str(x) for x in root)

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        if not data:
            return []

        ans = []
        for el in data.split(","):
            if el == 'None':
                e = None
            else:
                e = int(el)
            ans.append(e)
        return ans





# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))
if __name__ == '__main__':
    ser = Codec()
    deser = Codec()
    root = [1, 2, 3, None, None, 4, 5]
    # assert root == deser.deserialize(ser.serialize(root))

    root = []
    assert root == deser.deserialize(ser.serialize(root))
