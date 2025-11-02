"""
https://leetcode.com/problems/find-median-from-data-stream/description/
"""

import heapq


class MedianFinder:
    def __init__(self):
        self.arr = []

        # Max heap to store the smaller half of numbers
        self.left_max_heap: list[float] = []

        # Min heap to store the greater half of numbers
        self.right_min_heap: list[float] = []

        self.last_processed = -1

        self.last_median: float | None = None

    def addNum(self, num: int) -> None:
        self.arr.append(num)

    def findMedian(self) -> float:
        for num in self.arr[self.last_processed + 1 :]:
            # Insert new element into
            # max heap
            num = float(num)
            heapq.heappush(self.left_max_heap, -num)

            # Move the top of max heap to min heap to maintain order
            temp = -heapq.heappop(self.left_max_heap)
            heapq.heappush(self.right_min_heap, temp)

            # Balance heaps if min heap has more elements
            if len(self.right_min_heap) > len(self.left_max_heap):
                temp = heapq.heappop(self.right_min_heap)
                heapq.heappush(self.left_max_heap, -temp)

            # Compute median based on heap sizes
            if len(self.left_max_heap) != len(self.right_min_heap):
                median = -self.left_max_heap[0]
            else:
                median = (-self.left_max_heap[0] + self.right_min_heap[0]) / 2.0

            self.last_median = median

            self.last_processed += 1

        if self.last_median is None:
            raise RuntimeError("programming error: self.last_median is None")
        return self.last_median


# Your MedianFinder object will be instantiated and called as such:
if __name__ == "__main__":
    obj = MedianFinder()
    for num in [5, 15, 1, 3, 2, 8]:
        obj.addNum(num)
    param_2 = obj.findMedian()
    print(param_2)
