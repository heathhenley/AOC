import re
from common.utils import problem_harness, timeit, read_input


@timeit
def part1(filename: str) -> int:
  mult_ptn = re.compile(r"mul\((\d+),(\d+)\)")
  s = 0
  for line in read_input(filename):
    for g in mult_ptn.findall(line):
      x, y = int(g[0]), int(g[1])
      s += x * y
  return s


@timeit
def part2(filename: str) -> int:
  # one pattern to match them all
  ptn = re.compile(r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)")
  enabled, s = True, 0
  # one loop to find them
  for m in ptn.finditer("".join(read_input(filename))):
    match m.group(0):
      case "do()":
        enabled = True
      case "don't()":
        enabled = False
      case _:
        if enabled:
          x, y = map(int, m.groups())
          s += x * y
  return s


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
