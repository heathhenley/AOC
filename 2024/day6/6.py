from common.utils import problem_harness, timeit, read_input


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
    # try move if we can
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


def find_start(grid):
  rows = len(grid)
  cols = len(grid[0])
  for i in range(rows):
    for j in range(cols):
      if grid[i][j]  in ['^', 'v', '<', '>']:
        return (i, j)
  return None 


@timeit
def part1(filename: str) -> int:
  grid = [list(line.strip()) for line in read_input(filename)]
  start = find_start(grid) 
  return len(set([(x, y) for x, y, _ in list(get_visited(grid, start)[0])]))


@timeit
def part2(filename: str) -> int:
  grid = [list(line.strip()) for line in read_input(filename)]
  start = find_start(grid)
  original_visited = list(get_visited(grid, start)[0])
  obstacle_positions = set()
  # we only need to check the places we visited on the original path
  for (i, j, _) in original_visited:
      if (i, j) == start:
        continue
      new_grid = [row[:] for row in grid]
      new_grid[i][j] = "#"
      # test if there is a cycle
      if get_visited(new_grid, start)[1]:
        obstacle_positions.add((i, j))
  return len(obstacle_positions)


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
