import sys
import time

import matplotlib.pyplot as plt

from common.utils import read_input


def grid_to_img(grid: list) -> list:
  # just for plotting
  # convert the grid to an image
  img = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
  for i in range(len(grid)):
    for j in range(len(grid[0])):
      if grid[i][j] == '#':
        img[i][j] = 3
      elif grid[i][j] in ">v<^":
        img[i][j] = 1
  return img

def get_dirs(c: str, slopes_matter=True) -> list:
  # dirs we are alloed to go based on the current char
  if slopes_matter:
    if c == '>':
      return [(0, 1)]
    elif c == '<':
      return [(0, -1)]
    elif c == '^':
      return [(-1, 0)]
    elif c == 'v':
      return [(1, 0)]
  return [(1, 0), (-1, 0), (0, 1), (0, -1)]

def walk_grid_dfs(
    grid: list, start: tuple[int, int], end: tuple[int, int],
    slopes: bool = True) -> int:
  stack = [(start, set())]
  longest = 0
  while stack:
    (x, y), path = stack.pop()
    if (x, y) == end:
      longest = max(len(path), longest)
      #print(f"Found: {len(path)}, longest: {longest}")
      continue
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
      continue
    if grid[x][y] == '#':
      continue
    if (x, y) in path:
      continue
    path.add((x, y))
    for dx, dy in get_dirs(grid[x][y], slopes):
      tx, ty = x + dx, y + dy
      stack.append(((tx, ty), path.copy()))
  return longest

def get_start(grid: list) -> tuple[int, int]:
    for j in range(len(grid[0])):
      if grid[0][j] == '.':
        return (0, j)

def get_end(grid: list) -> tuple[int, int]:
    for j in range(len(grid[0])):
      if grid[-1][j] == '.':
        return (len(grid) - 1, j)


def part1(filename: str) -> int:
  lines = read_input(filename)
  grid = [[x for x in line] for line in lines]
  start, end = get_start(grid), get_end(grid)
  return walk_grid_dfs(grid, start, end)
  
def part2(filename: str) -> int:
  lines = read_input(filename)
  grid = [[x for x in line] for line in lines]
  start, end = get_start(grid), get_end(grid)
  return walk_grid_dfs(grid, start, end, slopes=False)


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
