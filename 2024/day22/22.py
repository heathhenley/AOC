from collections import defaultdict
from common.utils import problem_harness, timeit, read_input


def generate(seed: int, n: int) -> int:
  a = 16777216
  res = seed
  for _ in range(n):
    res = ((res * 64) ^ res) % a
    res = (int(res / 32) ^ res) % a
    res = ((res * 2048) ^ res) % a
  return res

def get_price_list(seed: int, n: int) -> list:
  prices = [seed]
  rand = seed
  while len(prices) < n:
    rand = generate(rand, 1)
    prices.append(int(str(rand)[-1]))
  return prices

def get_diffs(prices: list) -> list:
  diffs = [0 for _ in range(len(prices))]
  for i in range(1, len(prices)):
    diffs[i] = prices[i] - prices[i - 1]
  return diffs

@timeit
def part1(filename: str) -> int:
  return 0
  seeds = [int(line.strip()) for line in read_input(filename)]
  return sum([generate(s, 2000) for s in seeds])


@timeit
def part2(filename: str) -> int:
  seeds = [int(line.strip()) for line in read_input(filename)]
  prices = [get_price_list(seed, 2000) for seed in seeds]
  diffs = [get_diffs(p) for p in prices]

  mem = defaultdict(dict)
  for idx in range(len(prices)):
    for i in range(3, len(diffs[idx])):
      diff = diffs[idx]
      a, b, c, d = diff[i - 3], diff[i-2], diff[i-1], diff[i]
      if idx not in mem[(a, b, c, d)]:
        mem[(a, b, c, d)][idx] = prices[idx][i]


  max_bananas = -1
  # for the possible sequences, add up their bananas
  for seq, cached in mem.items():
    res = sum([v for v in cached.values()])
    if res > max_bananas:
      max_bananas = res
      best_seq = seq
  
  return max_bananas


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
