from common.utils import read_input
import sys

def parse_to_grids(lines: list) -> list:
  grids = []
  grid = []
  for line in lines:
    if line == '':
      grids.append(grid)
      grid = []
    else:
      grid.append(list(line))
  grids.append(grid)
  return grids

def find_row_flip(grid: list) -> int:
  for flip_row in range(1, len(grid)):
    valid = True
    top = flip_row
    bottom = flip_row - 1
    while bottom >= 0 and top < len(grid):
      for i in range(len(grid[0])):
        if grid[top][i] != grid[bottom][i]:
          valid = False
          break
      top += 1
      bottom -= 1
    if valid:
      return flip_row

def find_col_flip(grid: list) -> int:
  for flip_col in range(0, len(grid[0]) - 1):
    valid = True
    left = flip_col
    right = flip_col + 1
    while left >= 0 and right < len(grid[0]):
      for i in range(len(grid)):
        if grid[i][left] != grid[i][right]:
          valid = False
          break
      left -= 1
      right += 1
    if valid:
      return flip_col + 1

def find_col_flip_off(grid: list) -> int:
  """ Find a reflection line that is off by one"""
  for flip_col in range(0, len(grid[0]) - 1):
    valid = False
    left = flip_col
    right = flip_col + 1
    diff = 0
    while left >= 0 and right < len(grid[0]):
      for i in range(len(grid)):
        if grid[i][left] != grid[i][right]:
          diff += 1
          if diff > 1:
            valid = False
            break
          if diff == 1:
            valid = True
      left -= 1
      right += 1
    if valid:
      return flip_col + 1

def find_row_flip_off(grid: list) -> int:
  for flip_row in range(1, len(grid)):
    valid = False
    top = flip_row
    bottom = flip_row - 1
    diff = 0
    while bottom >= 0 and top < len(grid):
      for i in range(len(grid[0])):
        if grid[top][i] != grid[bottom][i]:
          diff += 1
          if diff > 1:
            valid = False
            break
          if diff == 1:
            valid = True
      top += 1
      bottom -= 1
    if valid:
      return flip_row

def part1(filename: str) -> int:
  lines = read_input(filename)
  grids = parse_to_grids(lines)
  ans = 0
  for g in grids:
    r = find_row_flip(g)
    c = find_col_flip(g)
    if c:
      ans += c
    if r:
      ans += r * 100 
  return ans
  
  
def part2(filename: str) -> int:
  # part 2 - we need to find a *different* reflection
  # line from the one we found in part 1, by only
  # changing one . to a # or vice versa
  # 1. find the reflection lines (part1)
  # 2. find a new line, that is exactly one off being valid
  lines = read_input(filename)
  grids = parse_to_grids(lines)
  ans = 0
  for g in grids:
    # part 1 vals
    r = find_row_flip_off(g)
    c = find_col_flip_off(g)
    if c:
      ans += c
    if r:
      ans += r * 100 
  return ans


def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")
  input_file = sys.argv[1]

  print("Part 1:", part1(input_file))
  print("Part 2:", part2(input_file))


if __name__ == '__main__':
  main()
