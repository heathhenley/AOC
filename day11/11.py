from common.utils import read_input
import sys

def find_empty_rows(grid: list) -> list[int]:
  # find rows that are all '.'
  row_idx_to_expand = []
  for i, row in enumerate(grid):
    if "#" not in row:
      row_idx_to_expand.append(i)
  return row_idx_to_expand

def find_empty_cols(grid: list) -> list[int]:
  # find columns that are all '.'
  col_idx_to_expand = []
  for i in range(len(grid[0])):
    if "#" not in [row[i] for row in grid]:
      col_idx_to_expand.append(i)
  return col_idx_to_expand

def expand_grid(grid: list) -> list:
  row_idx_to_expand = find_empty_rows(grid)
  col_idx_to_expand = find_empty_cols(grid) 
  # expand grid
  added = 0
  for idx in row_idx_to_expand:
    grid.insert(idx + added, ['.'] * len(grid[0]))
    added += 1
  added = 0
  for idx in col_idx_to_expand:
    for row in grid:
      row.insert(idx + added, '.')
    added += 1
  return grid

def find_galaxy_locations(grid: list) -> list[int, int]:
  idx_galaxies = []
  for i in range(len(grid)):
    for j in range(len(grid[0])):
      if grid[i][j] == '#':
        idx_galaxies.append((i, j))
  return idx_galaxies

def distance_between_galaxies(
    galaxy1: tuple[int, int], galaxy2: tuple[int, int]) -> int:
  # distance between two points in the grid without diagonal movement
  return abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])

def distance_between_galaxies_ex(
    galaxy1: tuple[int, int],
    galaxy2: tuple[int, int],
    rows_to_expand: list[int],
    cols_to_expand: list[int],
    expansion_factor: int) -> int:
  # count the number of rows to expand between the two galaxies
  rows_between = 0
  for row_idx in rows_to_expand:
    if row_idx > galaxy1[0] and row_idx < galaxy2[0] or (
        row_idx > galaxy2[0] and row_idx < galaxy1[0]
    ):
      rows_between += expansion_factor - 1
  # count the number of columns to expand between the two galaxies
  cols_between = 0
  for col_idx in cols_to_expand:
    if col_idx > galaxy1[1] and col_idx < galaxy2[1] or (
        col_idx > galaxy2[1] and col_idx < galaxy1[1]
    ):
      cols_between += expansion_factor - 1
  # distance between two points in the grid without diagonal movement
  return (
    abs(galaxy1[0] - galaxy2[0]) + rows_between
    + abs(galaxy1[1] - galaxy2[1]) + cols_between)

def get_galactic_distances(galaxies: list[tuple[int, int]]) -> list[list[int]]:
  distance = []
  for i in range(len(galaxies)):
    for j in range(i + 1, len(galaxies)):
      distance.append(distance_between_galaxies(galaxies[i], galaxies[j]))
  return distance

def get_galactic_distances_expand(
    galaxies: list[tuple[int, int]],
    rows_to_expand: list[int],
    cols_to_expand: list[int],
    expansion_factor: int) -> list[list[int]]:
  distance = []
  for i in range(len(galaxies)):
    for j in range(i + 1, len(galaxies)):
      distance.append(
        distance_between_galaxies_ex(
          galaxies[i], galaxies[j], rows_to_expand, cols_to_expand, expansion_factor))
  return distance

def part1(filename: str) -> int:
  # For part 1 we actually expand the grid, but we don't need to,
  # for example see part 2 :)
  space_grid = [[x for x in line] for line in read_input(filename)]
  expanded_grid = expand_grid(space_grid)
  galaxies = find_galaxy_locations(expanded_grid)
  inter_galactic_distances = get_galactic_distances(galaxies)
  return sum(inter_galactic_distances)

def part2(filename: str) -> int:
  # For part 2 we can't actually expand the grid because the expansion
  # factor is too big, so we have to calculate the distances between
  # the galaxies taking the expansion into account but without actually
  # expanding the grid.
  #
  # Each empty row/col becomes 1M rows
  inter_galactic_expansion_factor = 1_000_000
  space_grid = [[x for x in line] for line in read_input(filename)]
  galaxies = find_galaxy_locations(space_grid)
  rows_to_expand = find_empty_rows(space_grid)
  cols_to_expand = find_empty_cols(space_grid)
  return sum(get_galactic_distances_expand(
    galaxies,
    rows_to_expand,
    cols_to_expand,
    inter_galactic_expansion_factor))


def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")
  input_file = sys.argv[1]

  print("Part 1:", part1(input_file))
  print("Part 2:", part2(input_file))


if __name__ == '__main__':
  main()
