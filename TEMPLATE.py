from common.utils import problem_harness, timeit

@timeit
def part1(filename: str) -> int:
  print("Using input file:", filename)
  pass

@timeit
def part2(filename: str) -> int:
  print("Using input file:", filename)
  pass


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()