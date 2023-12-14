from functools import cache
from common.utils import read_input
import sys

def process_column(col: list) -> str:
  # plan:
  # find the next '#' in the column
  # count "O" between next and last "#" (or start)
  # update the last '# pointer to the current '#'
  last = -1
  current = col.index('#') if "#" in col else len(col)
  weight = 0
  while last != len(col):
    if last == -1:
      count_o = col[:current].count('O')
    else:
      count_o = col[last:current].count('O')
    for idx in range(count_o):
      weight += len(col) - (last + idx + 1)
    last = current
    current = col.index('#', last + 1) if "#" in col[last + 1:] else len(col)
  return weight

@cache
def process_and_move(col: str) -> list:
  """ This takes a str and moves rocks from right to left
  
  Returns the new arrangment of the rocks. This is cached
  because if there are cycles, we can just return the same
  result as before.
  """
  col = list(col)
  consist_o = col.count('O')
  consist_h = col.count('#')
  last = -1
  current = col.index('#') if "#" in col else len(col)
  while last != len(col):
    if last == -1:
      count_o = col[:current].count('O')
    else:
      count_o = col[last:current].count('O')
    for idx in range(count_o):
      col[last + idx + 1] = 'O'
    for idx in range(last + count_o + 1, current):
      col[idx] = '#' if col[idx] == '#' else '.'
    last = current
    current = col.index('#', last + 1) if "#" in col[last + 1:] else len(col)
  return col

def count_rocks(grid: list[list], rock_type: str) -> int:
  rocks = 0
  for row in grid:
    rocks += row.count(rock_type)
  return rocks

def get_col(grid: list, col: int) -> list:
  return [grid[i][col] for i in range(len(grid[0]))]

def read_grid_from_hash(grid_hash: str, n: int, m: int) -> list[list]:
  grid = [[0 for _ in range(m)] for _ in range(n)]
  for i in range(n):
    for j in range(m):
      grid[i][j] = grid_hash[i * m + j]
  return grid

@cache
def cycle(grid: str, n: int, m: int) -> list[list]:
  # north tilt (bottom to top) - same as part 1
  # works on columns (O's move up)
  grid = read_grid_from_hash(grid, n, m)
  rock_c = count_rocks(grid, 'O')
  for i in range(len(grid[0])):
    col = "".join(get_col(grid, i))
    col = process_and_move(col)
    for j in range(len(grid[0])):
      grid[j][i] = col[j]
  # west tilt (right to left)
  for i in range(len(grid)):
    row = "".join(grid[i])
    grid[i][:] = process_and_move(row)[:]
  # south tilt (top to bottom) (flip for processing)
  for i in range(len(grid[0])):
    col = "".join(get_col(grid, i))
    col = process_and_move(col[::-1])[::-1]
    for j in range(len(grid)):
      grid[j][i] = col[j]
  # east tilt (left to right) (flip for processing)
  for i in range(len(grid)):
    row = "".join(grid[i])
    grid[i][:] = process_and_move(row[::-1])[::-1]
  return grid

def get_weight(grid: list[list]) -> int:
  weight = 0
  for j in range(len(grid[0])):
    col = get_col(grid, j)
    for idx, c in enumerate(col):
      if c == 'O':
        weight += len(col) - idx
  return weight

def part1(filename: str) -> int:
  grid = [[x for x in line] for line in read_input(filename)]
  weight = [
      process_column(get_col(grid, col)) for col in range(len(grid))
    ]
  return sum(weight)

def part2(filename: str) -> int:
  # plan:
  # a 'cycle' is north, west, south, east tilt
  #   - bottom to top, right to left, top to bottom, left to right
  #   - reuse part 1 code, but instead of getting weight, move
  #     the rocks and return the new grid
  #   - cache the results of each transformation so if it cycles
  #     we can just return the same result as before
  num_cycles = 1_000_000_000
  grid = [[x for x in line] for line in read_input(filename)]
  n = len(grid)
  m = len(grid[0])
  cache = {}
  cycle_len = 0
  start = 0
  for i in range(num_cycles):
    grid_hash = "".join(["".join(row) for row in grid]) 
    if grid_hash not in cache:
      cache[grid_hash] = i
    else:
      print("Cycle found at", i)
      start = i
      cycle_len = i - cache[grid_hash]
      print("Cycle length:", cycle_len)
      break
    grid = cycle(grid_hash, n, m)
    grid_hash = "".join(["".join(row) for row in grid])
  
  offset = (start - cycle_len)
  index = (num_cycles - offset) % cycle_len + offset
  for grid_hash, i in cache.items():
    if i == index:
      grid = read_grid_from_hash(grid_hash, n, m)
      break
  return get_weight(grid)


def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")
  input_file = sys.argv[1]

  print("Part 1:", part1(input_file))
  print("Part 2:", part2(input_file))


if __name__ == '__main__':
  main()
