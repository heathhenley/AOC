# Day 3: Perfectly Spherical Houses in a Vacuum
# https://adventofcode.com/2015/day/3
from typing import Tuple

from common.utils import problem_harness, timeit, read_input


direction_map = {
  '^': (0, 1),
  'v': (0, -1),
  '<': (-1, 0),
  '>': (1, 0)
}


MOVE_ELF = 0
MOVE_SANTA = 1


def process_moves_part1(moves: str, start: Tuple[int, int] = (0, 0)) -> None:
  current = start
  visited = set((current, ))
  for move in moves:
    dx, dy = direction_map[move]
    current = (current[0] + dx, current[1] + dy)
    visited.add(current)
  return len(visited)


def process_moves_part2(moves: str, start: Tuple[int, int] = (0, 0)) -> None:
  current_santa, current_elf = start, start
  visited = set((current_santa, ))
  for idx, move in enumerate(moves):
    dx, dy = direction_map[move]
    if idx % 2 == MOVE_SANTA:
      current_santa = (current_santa[0] + dx, current_santa[1] + dy)
      visited.add(current_santa)
    else:
      current_elf = (current_elf[0] + dx, current_elf[1] + dy)
      visited.add(current_elf)
  return len(visited)


@timeit
def part1(filename: str) -> int:
  print("Using input file:", filename)
  # there's only one line in the input, but my little test input has multiple
  return sum(map(process_moves_part1, read_input(filename)))


@timeit
def part2(filename: str) -> int:
  print("Using input file:", filename)
  # there's only one line in the input, but my little test input has multiple
  return sum(map(process_moves_part2, read_input(filename)))


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()