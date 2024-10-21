# Day 2 (2015) - 2.py - I was told there would be no math
# https://adventofcode.com/2015/day/2
from common.utils import problem_harness, timeit, read_input


def _one_box_area(l: int, w: int, h: int) -> int:
  lw = l * w
  wh = w * h
  hl = h * l
  return 2 * (lw + wh + hl) + min(lw, wh, hl)


def _one_box_ribbon(l: int, w: int, h: int) -> int:
  return min(2 * (l + w), 2 * (w + h), 2 * (h + l)) + l * w * h


@timeit
def part1(filename: str) -> int:
  print("Using input file:", filename)
  total = 0
  for l, w, h in read_input(filename, sep='x'):
    total += _one_box_area(int(l), int(w), int(h))
  return total


@timeit
def part2(filename: str) -> int:
  print("Using input file:", filename)
  total = 0
  for l, w, h in read_input(filename, sep='x'):
    total += _one_box_ribbon(int(l), int(w), int(h))
  return total


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
