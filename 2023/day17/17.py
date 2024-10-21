from functools import cache
from queue import PriorityQueue
from heapq import heappush, heappop
import sys
import time

from common.utils import read_input


def walk_dijkstra(
    grid: list, start: tuple, end: tuple,
    max_straight: int = 3,
    min_straight: int = 0) -> list:

  # (heat, (r, c), (rdir, cdir), consecutive_straight_steps_left)
  sright = (grid[0][1], (0, 1), (0, 1), max_straight - 1)
  sdown = (grid[1][0], (1, 0), (1, 0), max_straight - 1)

  visited = set()
  q = [sright, sdown]

  while q:
    heat, (r, c), (rdir, cdir), straight = heappop(q)
    consec_straight = max_straight - straight
    if (r, c) == end:
      if consec_straight >= min_straight:
        return heat
    if ((r, c), (rdir, cdir), straight) in visited:
      continue
    visited.add(((r, c), (rdir, cdir), straight))

    # straight
    if straight > 0:
      nr = r + rdir
      nc = c + cdir
      if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
        heappush(
          q, (heat + grid[nr][nc], (nr, nc), (rdir, cdir), straight - 1))
    
    # turning 
    # it can only turn if if has made at least 4 consecutive straight steps
    if consec_straight < min_straight:
      continue
    for nr_dir, nc_dir in ((0, 1), (0, -1), (1, 0), (-1, 0)):
      # already handled straight
      if (nr_dir, nc_dir) == (rdir, cdir):
        continue
      # can't turn around
      if (nr_dir, nc_dir) == (-rdir, -cdir):
        continue
      nr = r + nr_dir
      nc = c + nc_dir
      if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
        heappush(
          q,
          (heat + grid[nr][nc], (nr, nc), (nr_dir, nc_dir), max_straight - 1))

def part1(filename: str) -> int:
  grid = [[int(x) for x in line] for line in read_input(filename)]
  start = (0, 0)
  end = (len(grid)-1, len(grid[0])-1)
  return walk_dijkstra(grid, start, end)

def part2(filename: str) -> int:
  grid = [[int(x) for x in line] for line in read_input(filename)]
  start = (0, 0)
  end = (len(grid)-1, len(grid[0])-1)
  return walk_dijkstra(
    grid, start, end, max_straight=10, min_straight=4)

def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")
  input_file = sys.argv[1]

  tic = time.perf_counter()
  print("Part 1:", part1(input_file))
  toc = time.perf_counter()
  print(f"  Part 1 took {toc - tic:0.4f} seconds")
  tic = time.perf_counter()
  print("Part 2:", part2(input_file))
  toc = time.perf_counter()
  print(f"  Part 2 took {toc - tic:0.4f} seconds")


if __name__ == '__main__':
  main()
