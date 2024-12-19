from functools import cache
from common.utils import problem_harness, timeit, read_input


@cache
def make_design_count(design: str, towel_ptns: tuple[str]) -> bool:
  if len(design) == 0:
    return 1
  if all([ptc not in design for ptc in towel_ptns]):
    return 0
  # try all the patterns that fit the beginning of the design, and recurse
  # with the design minus the pattern we used
  count = 0
  for towel_ptn in towel_ptns:
    if design.startswith(towel_ptn):
      count += make_design_count(design[len(towel_ptn):], towel_ptns)
  return count


def parse(lines: list[str]) -> tuple[list[str], tuple[str]]:
  # this is returning a ptn tuple so that we can cache the recursive function
  # that uses it
  towel_ptns = []
  designs = []
  for line in lines:
    if "," in line:
      towel_ptns.extend([l.strip() for l in line.split(",")])
    elif line:
      designs.append(line.strip())
  return designs, tuple(towel_ptns)


@timeit
def part1(filename: str) -> int:
  # Can we make each design with the towel patterns?
  designs, towel_ptns = parse(read_input(filename))
  return sum([1 for design in designs if make_design_count(design, towel_ptns)])


@timeit
def part2(filename: str) -> int:
  # In how many ways can we make each design with the towel patterns?
  designs, towel_ptns = parse(read_input(filename))
  return sum([make_design_count(design, towel_ptns) for design in designs])


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
