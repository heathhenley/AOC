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

def find_antinodes(grid, antennas):
  anti_nodes = defaultdict(set)
  for freq, ants in antennas.items():
    if len(ants) <= 1:
      continue
    for i in range(len(ants)):
      for j in range(i + 1, len(ants)):
        dr = ants[j][0] - ants[i][0]
        dc = ants[j][1] - ants[i][1]
        n1r = ants[i][0] + dr * 2
        n1c = ants[i][1] + dc * 2
        n2r = ants[j][0] - dr * 2
        n2c = ants[j][1] - dc * 2
        if valid(grid, n1r, n1c):
          anti_nodes[freq].add((n1r, n1c))
        if valid(grid, n2r, n2c):
          anti_nodes[freq].add((n2r, n2c))
  return anti_nodes

def find_antinodes_p2(grid, antennas):
  anti_nodes = defaultdict(set)
  for freq, ants in antennas.items():
    if len(ants) <= 1:
      continue
    for i in range(len(ants)):
      for j in range(i + 1, len(ants)):
        # find the slope between them
        dr = ants[j][0] - ants[i][0]
        dc = ants[j][1] - ants[i][1]
        # need to reduce the slope to simplest integer form
        # find the gcd of the two numbers
        gcd = math.gcd(dr, dc)
        dr //= gcd
        dc //= gcd
        # generate the 'anti-nodes' stepping by dr, dc from an antenna in
        # both direction until we hit the edge of the grid
        # dir 1
        k = 0
        while True:
          n1r = ants[i][0] + dr * k
          n1c = ants[i][1] + dc * k
          if not valid(grid, n1r, n1c):
            break
          anti_nodes[freq].add((n1r, n1c))
          k += 1
        
        # dir 2
        k = 0
        while True:
          n1r = ants[i][0] - dr * k
          n1c = ants[i][1] - dc * k
          if not valid(grid, n1r, n1c):
            break
          anti_nodes[freq].add((n1r, n1c))
          k += 1
  return anti_nodes


@timeit
def part1(filename: str) -> int:
  grid = [list(line) for line in read_input(filename)]
  antennas = find_antennas(grid)
  anti_nodes = find_antinodes(grid, antennas)
  all = set()
  for v in anti_nodes.values():
    all.update(v)
  return len(all)


@timeit
def part2(filename: str) -> int:
  grid = [list(line) for line in read_input(filename)]
  antennas = find_antennas(grid)
  anti_nodes = find_antinodes_p2(grid, antennas)
  all = set()
  for v in anti_nodes.values():
    all.update(v)
  return len(all)


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
