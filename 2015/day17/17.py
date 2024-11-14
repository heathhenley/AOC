# Day 17: No Such Thing as Too Much
from typing import List
from common.utils import problem_harness, timeit, read_input


def count_ways(
    total: int, idx: int, containers: List[int]) -> int:
  """ Recursively compute the ways to make total
  """
  if total == 0:
    return 1 # we're done

  if total < 0 or idx >= len(containers):
    return 0

  # skip this container
  skip = count_ways(total, idx + 1, containers)

  # take this container
  take = count_ways(total - containers[idx], idx + 1, containers)

  return take + skip


def min_containers(
    total: int,
    idx: int,
    container_count: int,
    containers: List[int],
    save_count: List[int]) -> int:
  """ Recursively compute the minimum containers needed to make total
  """
  if total == 0:
    save_count.append(container_count)
    return container_count

  if total < 0 or idx >= len(containers):
    return 1e9

  # skip this container
  skip = min_containers(
    total,
    idx + 1,
    container_count,
    containers,
    save_count)

  # take this container
  take = min_containers(
    total - containers[idx],
    idx + 1, container_count + 1,
    containers,
    save_count)

  return min(skip, take)


@timeit
def part1(filename: str) -> int:
  containers = sorted(
    [int(x) for x in read_input(filename)], reverse=True)
  return count_ways(150, 0, containers)


@timeit
def part2(filename: str) -> int:
  containers = sorted(
    [int(x) for x in read_input(filename)], reverse=True)
  save_count = []
  return save_count.count(min_containers(150, 0, 0, containers, save_count))


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
