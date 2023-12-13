from common.utils import read_input
import sys

def parse_to_grids(lines: list) -> list:
  grids = []
  grid = []
  for line in lines:
    print(line)
    if line == '':
      grids.append(grid)
      grid = []
    else:
      grid.append(list(line))
  grids.append(grid)
  return grids

def counts(grid: list) -> tuple:
  row_counts = []
  col_counts = []
  for row in grid:
    row_counts.append(row.count('#'))
  for i in range(len(grid[0])):
    col_counts.append([row[i] for row in grid].count('#'))
  return row_counts, col_counts

def get_reflection_points(counts_grid) -> tuple[list, list]:
  # find indices where two adjacent entries have the same value
  # in the row_counts and col_counts
  row_counts, col_counts = counts_grid
  row_reflection_points = []
  for j in range(len(row_counts) - 1):
    if row_counts[j] == row_counts[j+1]:
      row_reflection_points.append(j)
  col_reflection_points = []
  for j in range(len(col_counts) - 1):
    if col_counts[j] == col_counts[j+1]:
      col_reflection_points.append(j)
  return row_reflection_points, col_reflection_points

def get_valid_reflection_points(
    grid: list, reflection_points: tuple[list, list]) -> list:
  col_reflection_points, row_reflection_points = reflection_points
  # check row reflection points
  valid_row_points = []
  print(row_reflection_points)
  for row_point in row_reflection_points:
    valid = True
    left = row_point
    right = row_point + 1
    # move left and right outwards, checking that the grid is symmetric
    # at each step
    while left >= 0 and right < len(grid):
      # compare the rows at left and right
      for i in range(len(grid[left])):
        if grid[left][i] != grid[right][i]:
          valid = False
          break
      left -= 1
      right += 1
    if valid:
      valid_row_points.append(row_point)
  # check col reflection points
  valid_col_points = []
  for col_point in col_reflection_points:
    valid = True
    top = col_point
    bottom = col_point + 1
    # move top and bottom outwards, checking that the grid is symmetric
    # at each step
    while top >= 0 and bottom < len(grid):
      # compare the cols at top and bottom
      for i in range(len(grid)):
        if grid[i][top] != grid[i][bottom]:
          valid = False
          break
      top -= 1
      bottom += 1
    if valid:
      valid_col_points.append(col_point)
  return valid_row_points, valid_col_points

def part1(filename: str) -> int:
  lines = read_input(filename)
  grids = parse_to_grids(lines)
  print(len(grids))
  # the rows or cols that we can reflect around are easier to see in counts
  # but this can obviously give false positives. Could use it to screen out
  # grids that are definitely not symmetric, and then check the candidates
  # manually to see if they are symmetric. (eg start at possible reflection
  # point with two 'pointers' and move them outwards, checking that the grid
  # is symmetric at each step)
  all_counts = [counts(g) for g in grids]
  r, c = all_counts[0]
  print(r)
  print(c)
  # Identify possible reflection points using row counts / col counts
  # Check each possible reflection point:
  #   - compute the distance from the point to teach hash, negative on left
  #   of the point, positive on the right
  #   - Add them up, if they are all zero then the grid is symmetric
  all_possible = [get_reflection_points(c) for c in all_counts]
  print(all_possible)
  # check each possible reflection point
  all_valid = [
      get_valid_reflection_points(g, c) for g, c in zip(grids, all_possible)
    ]
  print(all_valid)
  
  
def part2(filename: str) -> int:
  print("Using input file:", filename)
  pass


def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")
  input_file = sys.argv[1]

  print("Part 1:", part1(input_file))
  print("Part 2:", part2(input_file))


if __name__ == '__main__':
  main()
