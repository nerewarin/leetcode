class Solution:
    def countGoodNumbers(self, n: int) -> int:
        quotient, remainder = divmod(n, 2)
        mod = 10**9 + 7
        x20 = pow(20, quotient, mod)
        combs = x20 * (5 * remainder if remainder else 1)
        return combs % mod


if __name__ == "__main__":
    Solution().countGoodNumbers(806166225460393)
