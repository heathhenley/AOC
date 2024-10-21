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
  """ Part 1 - naive approach, gens the whole seq before checking validity"""
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

def get_ways_part2(report: str, check: tuple) -> int:
  @cache
  def calc_combo(
    rep: str, check: tuple, rep_idx: int, check_idx: int, hash_count: int):
    # Stop condition
    if rep_idx == len(rep):
      if check_idx == len(check) and hash_count == 0:
        return 1
      elif check_idx == len(check) - 1 and hash_count == check[check_idx]:
        return 1
      return 0
    # If it's a "#", then the group of "#"s is still going, move one in the
    # string, increment the hash counter, and stay on the same check group
    if rep[rep_idx] == "#":
      return calc_combo(rep, check, rep_idx + 1, check_idx, hash_count + 1)
    # If it's a ".", then the group of "#"s has ended (if not zero), move one
    # in the string, reset the hash counter, and decide whether to move to the 
    # next check
    if rep[rep_idx] == ".":
      if hash_count == 0:
        return calc_combo(rep, check, rep_idx + 1, check_idx, 0)
      if check_idx < len(check) and hash_count == check[check_idx]:
        # we closed the group
        return calc_combo(rep, check, rep_idx + 1, check_idx + 1, 0)
       # we closed a group of hashes, but it wasn't the right size for the
       # check group so we return 0
      return 0
    # We're here so we know it's a ? and id need to try both options
    #
    # if we put a hash, continue in the string, increment the hash counter,
    # and stay on the same check group
    use_hash = calc_combo(rep, check, rep_idx + 1, check_idx, hash_count + 1)
    # if we use a dot, continue in the string, reset the hash counter, and
    # decide whether to move to the next check
    use_dot = 0
    if hash_count == 0:
      use_dot = calc_combo(rep, check, rep_idx + 1, check_idx, 0)
    elif check_idx < len(check) and hash_count == check[check_idx]: # close idx
      use_dot = calc_combo(rep, check, rep_idx + 1, check_idx + 1, 0)
    return use_hash + use_dot
  return calc_combo(report, tuple(check), 0, 0, 0)

def part1(filename: str) -> int:
  # This uses the naive approach of just generating all possible
  # combinations (each ? is either a . or #) and checking them as they are
  # made (no need to save them all) to see if they match the group check. It's 
  # slow but it works. Probably need to find a better way to do this for part 2 
  # as the input is much much larger...
  report, check = parse(read_input(filename))
  count_ways = [get_ways(r, c) for r, c in zip(report, check)]
  return sum(count_ways)

def expand(report: list[str], check: list[tuple], factor: int) -> tuple:
  report = [
    "?".join([r for _ in range(factor)]) for r in report
  ]
  # for each check group, expand it by factor and flatten it
  check = [[c * factor for c in check]]
  # flatten check list
  check = [x for y in check for x in y]
  return report, check

def part2(filename: str) -> int:
  # same idea to recursively generate but checking along the way to
  # to reuse subproblems (if you already completed first group, you
  # know how many ways there were - so no need to run again for groups
  # further along in the string)
  report, check = parse(read_input(filename))
  report, check = expand(report, check, factor=5)
  count_ways = [get_ways_part2(r, c) for r, c in zip(report, check)]
  return sum(count_ways)

def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")
  input_file = sys.argv[1]

  print("Part 1:", part1(input_file))
  print("Part 2:", part2(input_file))


if __name__ == '__main__':
  main()
