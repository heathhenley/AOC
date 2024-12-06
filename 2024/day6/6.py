from common.utils import problem_harness, timeit, read_input
from functools import cache

# if you are this arrow when you hit a corner, you will turn to this direction
arrow_turns = { '^': '>', 'v': '<', '<': '^', '>': 'v' }


# arror dir
arrow_dir = {
  '^': (-1, 0),
  'v': (1, 0),
  '<': (0, -1),
  '>': (0, 1)
}

def valid(i, j, rows, cols):
  return i >= 0 and i < rows and j >= 0 and j < cols


def get_visited(grid, g_pos):
  """ Get a set of the list of visited positions in the original grid """
  rows = len(grid)
  cols = len(grid[0])
  visited = set()
  i, j = g_pos
  curr_dir = grid[i][j]
  while valid(i, j, rows, cols):
    if (i, j, curr_dir) in visited:
      return visited, True
    visited.add((i, j, curr_dir))
    # try move
    dr, dc = arrow_dir[curr_dir]
    tmp_i, tmp_j = i + dr, j + dc
    if tmp_i < 0 or tmp_i >= rows or tmp_j < 0 or tmp_j >= cols:
      # we got out
      break
    if grid[tmp_i][tmp_j] != "#":
      i, j = tmp_i, tmp_j
      continue
    # we need to turn first
    curr_dir = arrow_turns[curr_dir]
  return visited, False

@timeit
def part1(filename: str) -> int:
  grid = [list(line.strip()) for line in read_input(filename)]
  rows = len(grid)
  cols = len(grid[0])
  for i in range(rows):
    for j in range(cols):
      if grid[i][j] in ['^', 'v', '<', '>']:
        g_pos = (i, j)
        break 
  return len(set([(x, y) for x, y, _ in list(get_visited(grid, g_pos)[0])]))


@timeit
def part2(filename: str) -> int:
  grid = []
  for line in read_input(filename):
    grid.append(list(line.strip()))

  rows = len(grid)
  cols = len(grid[0])
  for i in range(rows):
    for j in range(cols):
      if grid[i][j]  in ['^', 'v', '<', '>']:
        g_pos = (i, j)
        break
    
  # - if we get to the same position twice heading the same direction we found a
  #   cycle
  # - we know that the new obstacle will have to be on the original path
  # - make a function that returns: the visited set for a grid, and whether
  #   it terminated in a cycle
  # - try adding an obstacle to any of the positions in the original path?
  # - once we've visited a node going in a direction it's a cycle
  # - answer is too low (1893 is too low on real input)
  #   - tried too add to any position in the entire grid to check the assumption
  #   - that it needs to be in the original path (we get the same answer) - so
  #   - that suggests to me that there's something wrong how I'm counting the
  #   - cycles or the visited positions, maybe existing too early in a rare case
  original_visited = list(get_visited(grid, g_pos)[0])
  # try to put an obstacle in each of the originally visited positions
  # test for a cycle, count them
  start_i, start_j = g_pos
  obstacle_positions = set()
  for (i, j, _) in original_visited:
      if (i, j) == (start_i, start_j):
        continue
      new_grid = [row[:] for row in grid]
      new_grid[i][j] = "#"
      # test if there is a cycle
      _, cycle = get_visited(new_grid, (start_i, start_j))
      if cycle:
        obstacle_positions.add((i, j))
  return len(obstacle_positions)


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()