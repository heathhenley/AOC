from functools import cache
import sys
from common.utils import read_input

def parse(lines: list[str]) -> list[str, tuple]:
  check = []
  report = []
  for line in lines:
    r, c = line.split(" ")
    report.append(r)
    check.append([int(x) for x in c.split(",")])
  return report, check

def check_valid(report: str, check: tuple) -> int:
  # get continuous #'s and count them, compare to check
  groups_count =  [x.count("#") for x in report.split(".") if x]
  if len(groups_count) != len(check):
    return False
  for i in range(len(check)):
    if groups_count[i] != check[i]:
      return False
  return True

def get_ways(report: str, check: tuple) -> int:
  @cache
  def calc_combo(rep: str):
    # flip each ? to # or . recursively to
    # generate all possible options (don't actually need them though,
    # just need to count them)
    if rep.count("?") == 0:
      return 1 if check_valid(rep, check) else 0
    return (calc_combo(rep.replace("?", "#", 1))
            + calc_combo(rep.replace("?", ".", 1)))
  return calc_combo(report)

def part1(filename: str) -> int:
  # This uses the naive approach of just generating all possible
  # combinations (each ? is either a . or #) and checking them as they are
  # made (no need to save them all) to see if they match the group check. It's 
  # slow but it works. Probably need to find a better way to do this for part 2 
  # as the input is much much larger...
  report, check = parse(read_input(filename))
  count_ways = [get_ways(r, c) for r, c in zip(report, check)]
  return sum(count_ways)

def part2(filename: str) -> int:
  # recursive function is still taking the whole string then matching against
  # all of the groups in the check, which is still slow. Need to split it up
  # into smaller "subproblems" so that the the groups that are already matched
  # don't need to be checked again...
  pass

def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")
  input_file = sys.argv[1]

  print("Part 1:", part1(input_file))
  print("Part 2:", part2(input_file))


if __name__ == '__main__':
  main()
