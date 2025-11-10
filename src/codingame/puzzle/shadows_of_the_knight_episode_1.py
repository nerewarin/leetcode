"""
https://www.codingame.com/ide/puzzle/shadows-of-the-knight-episode-1
"""

import sys

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in input().split()]
n = int(input())  # maximum number of turns before game over.
x0, y0 = [int(i) for i in input().split()]

print(f"{w=}", file=sys.stderr, flush=True)
print(f"{h=}", file=sys.stderr, flush=True)
print(f"{n=}", file=sys.stderr, flush=True)
print(f"{x0=}", file=sys.stderr, flush=True)
print(f"{y0=}", file=sys.stderr, flush=True)

min_x = 0
max_x = w
min_y = 0
max_y = h

# game loop
while True:
    bomb_dir = input()  # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    bomb_y, bomb_x = direction = {
        "U": (-1, 0),
        "R": (0, 1),
        "D": (1, 0),
        "L": (0, -1),
        "UR": (-1, 1),
        "UL": (-1, -1),
        "DR": (1, 1),
        "DL": (1, -1),
    }[bomb_dir]

    def get_diff(bomb_x, x0, min_x, max_x):
        if not bomb_x:
            x_diff = 0
            # x_diff = (w - x0) * bomb_x
            min_x = x0
            max_x = x0
        elif bomb_x == 1:
            x_diff = (max_x - x0) * bomb_x // 2
            min_x = x0
        else:
            x_diff = (x0 - min_x) * bomb_x // 2
            max_x = x0
        return x_diff, min_x, max_x

    print(f"{bomb_dir=} ({direction=})", file=sys.stderr, flush=True)

    x0_diff, min_x, max_x = get_diff(bomb_x, x0, min_x, max_x)
    x0 += x0_diff
    print(f"{x0_diff=} ({x0=})", file=sys.stderr, flush=True)

    print(f"{bomb_y=} {y0=} {min_y=} {max_y=}", file=sys.stderr, flush=True)
    y0_diff, min_y, max_y = get_diff(bomb_y, y0, min_y, max_y)
    y0 += y0_diff
    print(f"{y0_diff=} ({y0=})", file=sys.stderr, flush=True)

    # the location of the next window Batman should jump to.
    print(f"{x0} {y0}")
