from common.utils import problem_harness, timeit, read_input


def is_safe(level: list) -> bool:
  diff = [level[i] - level[i+1] for i in range(len(level)-1)]
  max_diff = max([abs(level[i] - level[i+1]) for i in range(len(level)-1)])
  if max_diff > 3:
    return False
  if max_diff < 1:
    return False
  if not all(d > 0 for d in diff) and not all(d < 0 for d in diff):
    return False
  return True


@timeit
def part1(filename: str) -> int:
  safe_count = 0
  for line in read_input(filename, sep=" "):
    level = [int(x) for x in line]
    if is_safe(level):
      safe_count += 1
  return safe_count


@timeit
def part2(filename: str) -> int:
  safe_count = 0
  for line in read_input(filename, sep=" "):
    level = [int(x) for x in line]
    # if we can remove a single element and still have a safe level
    # then we can count this one as safe
    if is_safe(level):
      safe_count += 1
      continue
    # if it's not safe - just naively try to remove each element and check if
    # it's safe now
    for i in range(len(level)):
      if is_safe(level[:i] + level[i+1:]):
        safe_count += 1
        break
  return safe_count


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()