from functools import cache
from common.utils import timeit
# Three step - can take 1, 2, 3 steps to get up staircase of n steps
# - How many ways can you get up the staircase?


@timeit
def three_step(n: int) -> int:
  return _three_step(n)


@cache
def _three_step(n: int) -> int:
  # Top down recursive solution
  # This is the recursive solution, we can memoize it
  # base cases
  if n <= 0:
    return 0
  if n == 1:
    return 1
  if n == 2:
    # (2), (1, 1)
    return 2
  if n == 3:
    # (3), (1, 1, 1), (1, 2), (2, 1)
    return 4
  return _three_step(n-1) + _three_step(n-2) + _three_step(n-3)


@timeit
def three_stepDP(n: int) -> int:
  # Bottom up iterative solution
  if n <= 0:
    return 0
  if n == 1:
    return 1
  if n == 2:
    return 2
  if n == 3:
    return 4
  # Bottom up DP problem
  dp = [0 for _ in range(n)]

  # base cases
  dp[0] = 1 # one way to get to first step
  dp[1] = 2 # two ways to get to the 2nd (2), (1, 1)
  dp[2] = 4 # 3, (1, 1, 1), (2, 1), (1, 2)
  
  # bottom up
  for i in range(3, n):
    dp[i] = dp[i-1] + dp[i-2] + dp[i-3]
  return dp[-1]




def main():
  for i in range(1, 50):
    n = i
    print("n:", n)
    print("  rc:", three_step(n))
    print("  dp:", three_stepDP(n))


if __name__ == "__main__":
  main()