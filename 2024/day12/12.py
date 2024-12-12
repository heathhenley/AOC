from common.utils import problem_harness, timeit, read_input


DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def valid(r, c, rmax, cmax):
  return 0 <= r < rmax and 0 <= c < cmax


def get_perimeter(region):
  perimeter = 0
  for r, c in region:
    # check each neighbor - each one that is not in the region
    # contributes to the perimeter
    for dr, dc in DIRS:
      nr, nc = r + dr, c + dc
      if (nr, nc) not in region: # invalid allowed so we can count the perimeter
        perimeter += 1
  return perimeter


def get_number_of_sides(region):
  sides = 0
  for (r, c) in region:
    # up is in out blob
    if (r - 1, c) in region:
      # check for internal corner - two in region but the diagonal
      # right
      if (r, c + 1) in region and not (r - 1, c + 1) in region:
        sides += 1
      # left
      if (r, c - 1) in region and not (r - 1, c - 1) in region:
        sides += 1
    else:
      # external two not in region
      sides += ((r, c + 1) not in region) + ((r, c - 1) not in region)
    # down is in our blob
    if (r + 1, c) in region:
      # right
      if (r, c + 1) in region and (r + 1, c + 1) not in region:
        sides += 1
      # left
      if (r, c - 1) in region and (r + 1, c - 1) not in region:
        sides += 1
    else:
      # external
      sides += ((r, c + 1) not in region) +  ((r, c - 1) not in region)
  return sides

    

@timeit
def part1(filename: str) -> int:
  grid = [list(line) for line in read_input(filename)]

  rows = len(grid)
  cols = len(grid[0])
  total_price = 0
  visited = set()
  for row in range(rows):
    for col in range(cols):
      if (row, col) in visited:
        continue
      region = set()
      queue = [(row, col)]
      val = grid[row][col]
      while queue:
        r, c = queue.pop(0)
        region.add((r, c))
        if (r, c) in visited:
          continue
        visited.add((r, c))
        for dr, dc in DIRS:
          nr, nc = r + dr, c + dc
          if (valid(nr, nc, rows, cols) and grid[nr][nc] == val):
            queue.append((nr, nc))
      total_price += len(region) * get_perimeter(region)

  return total_price


@timeit
def part2(filename: str) -> int:
  grid = [list(line) for line in read_input(filename)]

  rows = len(grid)
  cols = len(grid[0])
  total_price = 0
  visited = set()
  for row in range(rows):
    for col in range(cols):
      if (row, col) in visited:
        continue
      region = set()
      queue = [(row, col)]
      val = grid[row][col]
      while queue:
        r, c = queue.pop(0)
        region.add((r, c))
        if (r, c) in visited:
          continue
        visited.add((r, c))
        for dr, dc in DIRS:
          nr, nc = r + dr, c + dc
          if (valid(nr, nc, rows, cols) and grid[nr][nc] == val):
            queue.append((nr, nc))
      total_price += len(region) * get_number_of_sides(region)
  return total_price


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
