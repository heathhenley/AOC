from common.utils import read_input
from functools import cache
import sys
import time
from typing import NamedTuple

class Point(NamedTuple):
  row: int
  col: int

class Direction(NamedTuple):
  drow: int # change in row, pos to right
  dcol: int # change in col, pos down

class Node(NamedTuple):
  loc: Point
  dir: Direction

def walk_grid(grid: list[list[str]], start: Node) -> None:
  """ Traverse using dfs"""
  # we need to store the direction with the node because
  # it changes how the path is traversed
  #start = Node(Point(0, 0), Direction(0, 1))
  stack = [start]
  seen = []
  while stack:
    current = stack.pop()
    row, col  = current.loc
    drow, dcol = current.dir
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
      continue
    if current in seen:
      # already been here going this direction
      continue
    seen.append(current)
    # decide which nodes are visited next stick in stack
    sym = grid[row][col]
    if sym == '.':
      # continue in the same direction
      r = row + drow
      c = col + dcol
      stack.append(Node(Point(r, c), current.dir))
      continue
    if sym == '-':
      # if going left or right, continue in same direction
      if drow == 0:
        # going left or right
        c = col + dcol
        stack.append(Node(Point(row, c), current.dir))
        continue
      # going up or down - 'splits' the path
      c = col + 1
      right = Direction(0, 1)
      stack.append(Node(Point(row, c), right))
      c = col - 1
      left = Direction(0, -1)
      stack.append(Node(Point(row, c), left))
    if sym == '|':
      # if going up or down, continue in same direction
      if dcol == 0:
        # going up or down
        r = row + drow 
        stack.append(Node(Point(r, col), current.dir))
        continue
      # going left or right - 'splits' the path
      r = row + 1
      down = Direction(1, 0)
      stack.append(Node(Point(r, col), down))
      r = row - 1
      up = Direction(-1, 0)
      stack.append(Node(Point(r, col), up))
      continue
    if sym == '\\':
      # if going right
      if drow == 0 and dcol == 1:
        # continue down
        r = row + 1
        stack.append(Node(Point(r, col), Direction(1, 0)))
        continue
      # if going left
      if drow == 0 and dcol == -1:
        # continue up
        r = row - 1
        stack.append(Node(Point(r, col), Direction(-1, 0)))
        continue
      # if going up
      if drow == -1 and dcol == 0:
        # continue left
        c = col - 1
        stack.append(Node(Point(row, c), Direction(0, -1)))
        continue 
      # if going down
      if drow == 1 and dcol == 0:
        # continue right
        c = col + 1
        stack.append(Node(Point(row, c), Direction(0, 1)))
        continue
    if sym == '/':
      # if going right
      if drow == 0 and dcol == 1:
        # continue up
        r = row - 1
        stack.append(Node(Point(r, col), Direction(-1, 0)))
        continue
      # if going left
      if drow == 0 and dcol == -1:
        # continue down
        r = row + 1
        stack.append(Node(Point(r, col), Direction(1, 0)))
        continue
      # if going up
      if drow == -1 and dcol == 0:
        # continue right
        c = col + 1
        stack.append(Node(Point(row, c), Direction(0, 1)))
        continue 
      # if going down
      if drow == 1 and dcol == 0:
        # continue left
        c = col - 1
        stack.append(Node(Point(row, c), Direction(0, -1)))
        continue
  return seen

def get_unique_visited(visited: list[Node]) -> list[Node]:
  """ Get the unique nodes visited by their index
      (don't care about direction)"""
  seen = []
  for node in visited:
    if node.loc not in seen:
      seen.append(node.loc)
  return seen

def part1(filename: str) -> int:
  grid = [[x for x in line] for line in read_input(filename)]
  visited = walk_grid(grid, Node(Point(0, 0), Direction(0, 1)))
  unique_visited = get_unique_visited(visited)
  return len(unique_visited)

def part2(filename: str) -> int:
  grid = [[x for x in line] for line in read_input(filename)]
  n, m = len(grid), len(grid[0])
  max_energized = 0
  # top - going down
  for i in range(m):
    print(f"top {i}/{m}")
    visited = walk_grid(grid, Node(Point(0, i), Direction(1, 0)))
    unique_visited = get_unique_visited(visited)
    max_energized = max(max_energized, len(unique_visited))
  # bottom - going up
  for i in range(m):
    print(f"bottom {i}/{m}")
    visited = walk_grid(grid, Node(Point(n - 1, i), Direction(-1, 0)))
    unique_visited = get_unique_visited(visited)
    max_energized = max(max_energized, len(unique_visited))
  # left - going right
  for i in range(n):
    print(f"left {i}/{n}")
    visited = walk_grid(grid, Node(Point(i, 0), Direction(0, 1)))
    unique_visited = get_unique_visited(visited)
    max_energized = max(max_energized, len(unique_visited))
  # right - going left
  for i in range(n):
    print(f"right {i}/{n}")
    visited = walk_grid(grid, Node(Point(i, m - 1), Direction(0, -1)))
    unique_visited = get_unique_visited(visited)
    max_energized = max(max_energized, len(unique_visited))
  return max_energized

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
