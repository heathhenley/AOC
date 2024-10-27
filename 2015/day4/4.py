import hashlib

from common.utils import problem_harness, timeit, read_input


def mine(key: str = None, difficulty: int = 1) -> int:
  i = 0
  while i < 2**32:
    h = hashlib.md5((key + str(i)).encode()).hexdigest()
    if h[:difficulty] == "0" * difficulty:
      return i
    i += 1
  raise ValueError("No solution found")


@timeit
def part1(filename: str) -> int:
  return mine(read_input(filename)[0], 5)

@timeit
def part2(filename: str) -> int:
  return mine(read_input(filename)[0], 6)


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()