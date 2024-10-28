from typing import Dict
from common.utils import problem_harness, timeit, read_input


def has_double(s: str) -> bool:
  for i in range(1, len(s)):
    if s[i] == s[i - 1]:
      return True
  return False


def three_vowels(s: str) -> bool:
  return sum(map(s.count, list('aeiou'))) >= 3


def no_bad_strings(s: str) -> bool:
  return not any(bad in s for bad in ['ab', 'cd', 'pq', 'xy'])


def is_nice(s: str) -> int:
  return int(has_double(s) and three_vowels(s) and no_bad_strings(s))


def letter_sandwich(s: str) -> bool:
  """ xyx, or aaa, or efe """
  if len(s) < 3: # no sandwich possible
    return False

  for i in range(1, len(s) - 1):
    if s[i - 1] == s[i + 1]:
      return True
  return False


def two_pairs(s: str) -> bool:
  """ non overlapping pairs, xyxy or aaalskdjflskdjaa, not aaa"""
  for i in range(1, len(s)- 1):
    if s.count(s[i - 1:i + 1], i + 1):
      return True
  return False


def is_nice_part_2(s: str) -> int:
  return int(two_pairs(s) and letter_sandwich(s))


@timeit
def part1(filename: str) -> int:
  return sum(map(is_nice, read_input(filename)))


@timeit
def part2(filename: str) -> int:
  return sum(map(is_nice_part_2, read_input(filename)))


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()