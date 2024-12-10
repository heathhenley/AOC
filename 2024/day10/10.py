from common.utils import problem_harness, timeit, read_input


def find_starts(grid: list[list[int]]) -> list[tuple[int, int]]:
  starts = []
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      if grid[i][j] == 0:
        starts.append((i, j))
  return starts

def valid(grid: list[list[int]], i: int, j: int) -> bool:
  return i >= 0 and i < len(grid) and j >= 0 and j < len(grid[i])

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

@timeit
def part1(filename: str) -> int:
  grid = [list(map(int, list(line))) for line in read_input(filename)]
  # the potential starts are any grids that are 0
  starts = find_starts(grid)
  # try each start - how many grids with a value of 9 can be reached?
  score = { start : 0 for start in starts }

  for start in starts:
    stack = [start]
    nines = set()
    while stack:
      r, c = stack.pop()

      if grid[r][c] == 9:
        nines.add((r, c))
        continue

      for dr, dc in DIRS:
        nr = r + dr
        nc = c + dc
        # stay on the grid - and must go uphill by 1 exactly
        if valid(grid, nr, nc) and (grid[nr][nc] - grid[r][c]) == 1:
          stack.append((nr, nc))
    score[start] = len(nines)

  return sum(score.values())



@timeit
def part2(filename: str) -> int:
  grid = [list(map(int, list(line))) for line in read_input(filename)]
  # the potential starts are any grids that are 0
  starts = find_starts(grid)
  # try each start - how many grids with a value of 9 can be reached?
  score = { start : 0 for start in starts }

  # going to try the same approach as part 1, but store the whole path instead?
  # maybe need to use backtracking instead? lets see how bad it is if it can
  # work on the small input
  all_paths = {start: [] for start in starts}

  for start in starts:
    r, c = start 
    p = set()
    p.add((r, c))
    stack = [(r, c, p)]
    while stack:
      r, c, path = stack.pop()

      if grid[r][c] == 9:
        all_paths[start].append(path)
        continue

      for dr, dc in DIRS:
        nr = r + dr
        nc = c + dc
        # stay on the grid - and must go uphill by 1 exactly
        if valid(grid, nr, nc) and (grid[nr][nc] - grid[r][c]) == 1:
          p = path.copy()
          p.add((nr, nc))
          stack.append((nr, nc, p))
  return sum(len(all_paths[start]) for start in starts)


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
