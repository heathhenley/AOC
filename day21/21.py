import matplotlib.pyplot as plt
import sys
import time
from common.utils import read_input


def grid_to_img(grid: list) -> list:
  # just for plotting
  # convert the grid to an image
  img = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
  for i in range(len(grid)):
    for j in range(len(grid[0])):
      if grid[i][j] == '#':
        img[i][j] = 1
      elif grid[i][j] == 'S':
        img[i][j] = 2
      elif grid[i][j] == '.':
        img[i][j] = 3
      elif grid[i][j] == 'X':
        img[i][j] = 4
  return img


def walk_grid_bfs(grid: list, goal: int, start: tuple[int, int]) -> int:
  # BFS, track even / odd and skip if further away than goal
  queue = [(start, 0)]
  dp = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
  while queue:
    (x, y), steps_from_start = queue.pop(0)
    if steps_from_start > goal:
      continue
    if dp[x][y] != -1:
      continue
    dp[x][y] = steps_from_start % 2
    # try all directions from here
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
      tx, ty = x + dx, y + dy
      if tx < 0 or ty < 0 or tx >= len(grid) or ty >= len(grid[0]):
        continue
      if grid[tx][ty] == '#':
        continue
      queue.append(((tx, ty), steps_from_start + 1))
  return sum([x.count(0) for x in dp])


def find_start(grid: list) -> tuple[int, int]:
  for i in range(len(grid)):
    for j in range(len(grid[0])):
      if grid[i][j] == 'S':
        return (i, j)


def part1(filename: str) -> int:
  grid = [[x for x in line] for line in read_input(filename)]
  #plt.imshow(grid_to_img(grid))
  #plt.show()
  goal = 64 # steps
  start = find_start(grid)
  return walk_grid_bfs(grid, goal, start)


def part2(filename: str) -> int:
  print("Using input file:", filename)
  pass


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
