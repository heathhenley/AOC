from functools import cache
from common.utils import problem_harness, timeit, read_input


@cache
def can_make_design(design: str, towel_ptns: tuple[str]) -> bool:
  if len(design) == 0:
    return True
  if all([ptc not in design for ptc in towel_ptns]):
    return False 
  # try all the patterns that fit the beginning of the design, and recurse
  # with the design minus the pattern we used
  for towel_ptn in towel_ptns:
    if design.startswith(towel_ptn):
      if can_make_design(design[len(towel_ptn):], towel_ptns):
        return True
  return False


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
      if can_make_design(design[len(towel_ptn):], towel_ptns):
        count += make_design_count(design[len(towel_ptn):], towel_ptns)
  return count



@timeit
def part1(filename: str) -> int:
  # Can we make each design with the towel patterns?
  towel_ptns = []
  designs = []
  for line in read_input(filename):
    if "," in line:
      towel_ptns.extend([l.strip() for l in line.split(",")])
    elif line:
      designs.append(line.strip())
  towel_ptns = tuple(towel_ptns)
  return sum([1 for design in designs if can_make_design(design, towel_ptns)])


@timeit
def part2(filename: str) -> int:
  # In how many ways can we make each design with the towel patterns?
  towel_ptns = []
  designs = []
  for line in read_input(filename):
    if "," in line:
      towel_ptns.extend([l.strip() for l in line.split(",")])
    elif line:
      designs.append(line.strip())
  towel_ptns = tuple(towel_ptns)
  return sum([make_design_count(design, towel_ptns) for design in designs])


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
