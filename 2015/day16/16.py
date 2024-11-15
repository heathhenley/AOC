import re
from common.utils import problem_harness, timeit, read_input


# Sue 500: cars: 1, perfumes: 6, vizslas: 1
PATTERN = r"Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)"


ticker_tape = {
  "children": 3,
  "cats": 7,
  "samoyeds": 2,
  "pomeranians": 3,
  "akitas": 0,
  "vizslas": 0,
  "goldfish": 5,
  "trees": 3,
  "cars": 2,
  "perfumes": 1,
}


def parse_line(line: str) -> dict:
  m = re.match(PATTERN, line)
  return (
    m.groups()[0],
    dict(zip(m.groups()[1::2], map(int, m.groups()[2::2])))
  )


@timeit
def part1(filename: str) -> int:
  for line in read_input(filename):
    aunt, props = parse_line(line)
    if all(ticker_tape[k] == v for k, v in props.items()):
      return aunt


@timeit
def part2(filename: str) -> int:
  for line in read_input(filename):
    aunt, props = parse_line(line)
    gt = {"cats", "trees"}
    lt = {"pomeranians", "goldfish"}
    if not all(
        ticker_tape[k] == v for k, v in props.items()
        if k not in gt and k not in lt):
      continue
    if all(
        ticker_tape[k] >= v for k, v in props.items() if k in gt):
      continue
    if all(ticker_tape[k] <= v for k, v in props.items() if k in lt):
      continue
    return aunt
  return 0


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
