from collections import defaultdict
import math
from common.utils import problem_harness, timeit, read_input


def valid(grid, x, y):
  return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def find_antennas(grid):
  antennas = defaultdict(list)
  for r in range(len(grid)):
    for c in range(len(grid[0])):
      if grid[r][c] != '.':
        antennas[grid[r][c]].append((r, c))
  return antennas


def find_antinodes(grid, antennas, all_mults=False):
  anti_nodes = defaultdict(set)
  for freq, ants in antennas.items():
    if len(ants) <= 1:
      continue
    for i in range(len(ants)):
      for j in range(i + 1, len(ants)):
        dr, dc = ants[j][0] - ants[i][0], ants[j][1] - ants[i][1]

        if not all_mults:
          n1r, n1c = ants[i][0] + 2 * dr, ants[i][1] + 2 * dc
          n2r, n2c = ants[j][0] - 2 * dr, ants[j][1] - 2 * dc
          if valid(grid, n1r, n1c):
            anti_nodes[freq].add((n1r, n1c))
          if valid(grid, n2r, n2c):
            anti_nodes[freq].add((n2r, n2c))
          continue

        gcd = math.gcd(dr, dc)
        dr //= gcd
        dc //= gcd
        for d in [1, -1]:
          k = 0
          while True:
            n1r, n1c = ants[i][0] + dr * k * d, ants[i][1] + dc * k * d
            if not valid(grid, n1r, n1c):
              break
            anti_nodes[freq].add((n1r, n1c))
            k += 1
  return anti_nodes


@timeit
def part1(filename: str) -> int:
  grid = [list(line) for line in read_input(filename)]
  antennas = find_antennas(grid)
  all_nodes = set()
  for v in find_antinodes(grid, antennas).values():
    all_nodes.update(v)
  return len(all_nodes)


@timeit
def part2(filename: str) -> int:
  grid = [list(line) for line in read_input(filename)]
  antennas = find_antennas(grid)
  all_nodes = set()
  for v in find_antinodes(grid, antennas, all_mults=True).values():
    all_nodes.update(v)
  return len(all_nodes)


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
