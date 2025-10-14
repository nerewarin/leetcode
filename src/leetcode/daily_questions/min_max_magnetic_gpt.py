def maxDistance(position, m):
    position.sort()

    def canPlaceBalls(min_dist):
        count = 1  # Place the first ball in the first basket
        last_position = position[0]

        for i in range(1, len(position)):
            if position[i] - last_position >= min_dist:
                count += 1
                last_position = position[i]
                if count == m:
                    return True
        return False

    # Binary search on the answer
    left, right = 1, position[-1] - position[0]
    best = 0

    while left <= right:
        mid = (left + right) // 2
        if canPlaceBalls(mid):
            best = mid
            left = mid + 1
        else:
            right = mid - 1

    return best


# Example 1
position1 = [1, 2, 3, 4, 99]
m1 = 3
print(maxDistance(position1, m1))  # Output: 3

# Example 2
position2 = [5, 4, 3, 2, 1, 1000000000]
m2 = 2
print(maxDistance(position2, m2))  # Output: 999999999
