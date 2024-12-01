from common.utils import problem_harness, timeit, read_input


def get_lists(lines: list[str]) -> tuple[list[int], list[int]]:
  left = sorted([int(x[0]) for x in lines])
  right= sorted([int(x[1]) for x in lines])
  return left, right


def get_diff(left: list[int], right: list[int]) -> int:
  return sum([abs(l - r) for l, r in zip(left, right)])


def get_similarity(left: list[int], right: list[int]) -> int:
  d = {}
  for r in right:
    d[r] = d.get(r, 0) + 1
  return sum([l * d.get(l, 0) for l in left])


@timeit
def part1(filename: str) -> int:
  left, right = get_lists(
    [line for line in read_input(filename, sep="  ")]
  )
  return get_diff(left, right)


@timeit
def part2(filename: str) -> int:
  left, right = get_lists(
    [line for line in read_input(filename, sep="  ")]
  )
  return get_similarity(left, right)


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
