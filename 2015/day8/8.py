# Day 8 of Advent of Code 2015 - https://adventofcode.com/2015/day/8
from common.utils import problem_harness, timeit, read_input


@timeit
def part1(filename: str) -> int:
  return sum(len(line) - len(eval(line)) for line in read_input(filename))


def replace(line: str) -> str:
  line = line.replace('\\', '\\\\')
  line = line.replace('"', '\\"')
  line = line.replace(r'\x', '\\x')
  return f'"{line}"'


@timeit
def part2(filename: str) -> int:
  return sum(
    len(replace(line)) - len(line)
    for line in read_input(filename)
  )


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()