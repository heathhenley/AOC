# Advent of Code 2023: Day 1 - Calibration
# https://adventofcode.com/2023/day/1
# I reworked this to clean it up, and also solve in a slightly different way
# than I did the first time around (which you can see in the git history).

import re
from common.utils import problem_harness, timeit, read_input


words_to_numbers = {
  "one": 1,
  "two": 2,
  "three": 3,
  "four": 4,
  "five": 5,
  "six": 6,
  "seven": 7,
  "eight": 8,
  "nine": 9,
}
digits = "0123456789"


def get_number(match: str) -> int:
  try:
    return int(match)
  except ValueError:
    return words_to_numbers[match]


def get_all_match_idx(
    line: str, targets: list, idx_accum: list = [], curr: int = 0) -> list:
  if not line or not targets or curr == len(line):
    return idx_accum
  for t in targets:
    if t in line[curr:]:
      idx = line[curr:].index(t) + curr
      idx_accum.append({"index": idx + curr, "matched": get_number(t)})
  return get_all_match_idx(line, targets, idx_accum, curr + 1)


def get_calibration_value(line: str) -> int:
  try:
    left = int(re.search(r'\d{1}', line).group(0))
    right = int(re.search(r'\d{1}', line[::-1]).group(0))
  except AttributeError:
    print("no digits found in line:", line)
    return 0
  return left * 10 + right


def get_calibration_value_with_words(line: str) -> int:
  targets = list(words_to_numbers.keys()) + list(digits)
  matches = []
  # find the indices of all the matches (words or digits)
  if not(matches := get_all_match_idx(line, targets, matches)):
    raise ValueError("This should not happen if the input is correct")
  # then grab the first and last match idx and use them
  matches.sort(key=lambda x: x["index"])
  return matches[0]["matched"] * 10 + matches[-1]["matched"]
  

@timeit
def part1(filename: str) -> int:
  print("Using input file:", filename)
  return sum(map(get_calibration_value, read_input(filename)))


@timeit
def part2(filename: str) -> int:
  return sum(map(get_calibration_value_with_words, read_input(filename)))


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
