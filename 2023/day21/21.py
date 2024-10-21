import matplotlib.pyplot as plt
import sys
import time
import numpy as np
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


def walk_grid_bfs(
    grid: list,
    goal: int, # number steps
    start: tuple[int, int], # (x, y)
    periodic: bool = False, # if True, grid is infinite
    parity: int = 0) -> int: # 0 = even, 1 = odd
  # BFS - count if we come to this spot on the parity we care about
  queue = [(start, 0)]
  seen = set()
  count = 0
  while queue:
    (x, y), steps_from_start = queue.pop(0)
    if steps_from_start > goal:
      continue
    if (x, y) in seen:
      continue
    seen.add((x, y))
    # coords in original image
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
      if not periodic:
        continue
    if grid[x % len(grid)][y % len(grid[0])] == '#':
      continue
    count += steps_from_start % 2 == parity
    # try all directions from here
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
      tx, ty = x + dx, y + dy
      queue.append(((tx, ty), steps_from_start + 1))
  return count


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
  # Due to how the input is constructed, the number of spaces you
  # can reach grows quadratically with the number of steps
  # I didn't find this on my own, I looked the reddit. I was
  # origially trying to find a pattern in the number of odd and
  # even "tiles" you can reach, but I couldn't get it working. 
  grid = [[x for x in line] for line in read_input(filename)]
  start = find_start(grid)
  steps = 26501365
  w = len(grid)
  hw = w // 2
  a, b = [], []
  for r in [hw, w + hw, 2 * w + hw]:
    b.append(walk_grid_bfs(grid, r, start, True, r % 2))
    a.append([r**2, r, 1])
    #print(r, b[-1])
  a = np.array(a)
  b = np.array(b)
  x = np.linalg.solve(a, b)
  a, b, c = x
  return int(np.round(a * steps**2 + b * steps + c))


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
