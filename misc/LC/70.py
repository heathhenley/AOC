# LC Question 70. Climbing Stairs (easy)
# Trying practice coming up with the table form of dp problems
from functools import cache
import time

@cache
def climbStairs(n: int) -> int:
  # This is the recursive solution, we can memoize it
  # base cases
  if n == 1:
    return 1
  if n == 2:
    return 2
  return climbStairs(n-1) + climbStairs(n-2)  


def climbStairsDP(n: int) -> int:
  # This is the iterative dp solution
  # base cases
  if n == 1:
    return 1
  if n == 2:
    return 2
  dp = [0] * n
  dp[0] = 1
  dp[1] = 2
  for i in range(2, n):
    dp[i] = dp[i-1] + dp[i-2]
  return dp[n-1]


def main():
  for i in range(1, 10):
    n = 2**i
    print("n:", n)
    tic = time.perf_counter()
    try:
      res1 = climbStairs(n)
      print("  recursive time:", time.perf_counter() - tic)
    except RecursionError:
      print("  recursive: RecursionError")

    tic = time.perf_counter()
    res2 = climbStairsDP(n)
    print("  dp time:", time.perf_counter() - tic)


if __name__ == "__main__":
  main()