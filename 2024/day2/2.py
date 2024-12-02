from common.utils import problem_harness, timeit, read_input


def is_safe(level: list) -> bool:
  diff = [level[i] - level[i+1] for i in range(len(level)-1)]
  max_diff = max([abs(level[i] - level[i+1]) for i in range(len(level)-1)])
  if not 1 <= max_diff <= 3:
    return False
  return all(d > 0 for d in diff) or all(d < 0 for d in diff)


def is_safe_with_remove(level: list) -> bool:
  if is_safe(level):
    return True
  return any(is_safe(level[:i] + level[i+1:]) for i in range(len(level)))


@timeit
def part1(filename: str) -> int:
  return sum(
    [is_safe([int(x) for x in line]) for line in read_input(filename, sep=" ")]
  )


@timeit
def part2(filename: str) -> int:
  return sum(
    [is_safe_with_remove(
      [int(x) for x in l]) for l in read_input(filename, sep=" ")]
  )


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
