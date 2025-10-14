import dataclasses
from enum import Enum
from typing import List
import logging

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Vector:
    x: int
    y: int

    def is_vertical(self):
        return bool(self.y)


class Direction(Enum):
    right = Vector(1, 0)
    left = Vector(-1, 0)
    bot = Vector(0, 1)
    top = Vector(0, -1)


DIRECTIONS_CYCLE = (Direction.right, Direction.bot, Direction.left, Direction.top)


class Solution:
    def _get(self, x, y):
        return self.matrix[y][x]

    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        self.matrix = matrix

        m = len(matrix)
        n = len(matrix[0])

        i, j = 0, 0
        direction = Direction.right

        res = [self._get(i, j)]
        visited = {(i, j)}

        turns = 0
        while len(res) != n * m:
            # consider candidate to continue moving in same direction
            x = i + direction.value.x
            y = j + direction.value.y

            if 0 <= x < n and 0 <= y < m and (x, y) not in visited:
                # we can move
                i += direction.value.x
                j += direction.value.y
                res.append(self._get(i, j))
                visited.add((i, j))
                logger.debug(f"temp {res=}")
            else:
                turns += 1
                direction = DIRECTIONS_CYCLE[turns % len(DIRECTIONS_CYCLE)]
                logger.debug(f"{turns=}, direction={direction}")

        logger.debug(f"final {res=}")
        return res


if __name__ == "__main__":
    do = Solution().spiralOrder

    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    res = do(matrix)
    assert res == [1, 2, 3, 6, 9, 8, 7, 4, 5], f"{res=}, {matrix=}"

    matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    res = do(matrix)
    assert res == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7], f"{res=}, {matrix=}"

    matrix = [
        [23, 18, 20, 26, 25],
        [24, 22, 3, 4, 4],
        [15, 22, 2, 24, 29],
        [18, 15, 23, 28, 28],
    ]
    res = do(matrix)
