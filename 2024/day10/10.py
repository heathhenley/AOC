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


def walk_grid(
    grid: list[list[int]], start: tuple[int, int]) -> list[list[tuple[int, int]]]:
  """ Walk the grid and return the path - stops on 9, only go up by 1 """
  r, c = start 
  stack = [(r, c, [(r, c)])]
  paths = []
  while stack:
    r, c, path = stack.pop()
    if grid[r][c] == 9:
      paths.append(path)
      continue
    for dr, dc in DIRS:
      nr = r + dr
      nc = c + dc
      if valid(grid, nr, nc) and (grid[nr][nc] - grid[r][c]) == 1:
        stack.append((nr, nc, path + [(nr, nc)]))
  return paths


@timeit
def part1(filename: str) -> int:
  grid = [list(map(int, list(line))) for line in read_input(filename)]
  starts = find_starts(grid)
  score = 0
  for start in starts:
    paths = walk_grid(grid, start)
    score +=  len(set([path[-1] for path in paths]))
  return score


@timeit
def part2(filename: str) -> int:
  grid = [list(map(int, list(line))) for line in read_input(filename)]
  starts = find_starts(grid)
  return sum([len(walk_grid(grid, start)) for start in starts])


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
