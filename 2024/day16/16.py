from common.utils import problem_harness, timeit, read_input


def valid(r, c, grid):
  return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def find(grid, target):
  for r in range(len(grid)):
    for c in range(len(grid[0])):
      if grid[r][c] == target:
        return (r, c)
  return None

def rotate_90deg_right(direction):
  return {
    "N": "E",
    "E": "S",
    "S": "W",
    "W": "N"
  }[direction]

def rotate_90deg_left(direction):
  return {
    "N": "W",
    "W": "S",
    "S": "E",
    "E": "N"
  }[direction]

dir_map = {
  'N': (-1, 0),
  'E': (0, 1),
  'S': (1, 0),
  'W': (0, -1)
}

@timeit
def part1(filename: str) -> int:
  grid = [list(line.strip()) for line in read_input(filename)]
  for row in grid:
    print("".join(row))
  
  start = find(grid, 'S')

  min_cost = float('inf')
  stack = [(start, 0, 'E', set())]


  while stack:

    (r, c), cost, direction, visited = stack.pop()

    if cost > min_cost:
      continue
    
    if (r, c, direction) in visited:
      continue
    visited.add((r, c, direction))

    if grid[r][c] == 'E':
      min_cost = min(min_cost, cost)
      best_path = visited
      print("current_best", min_cost)
      continue
    # the options are to keep going in the same dir for a cost of 1
    # or to turn left or right 90 degrees for a cost of 1000
    # enqueue all of these options and track the min
    # probably need to use djikstra's for pt2 but let's start with dfs
    # try walk forward
    dr, dc = dir_map[direction]
    new_r, new_c = r + dr, c + dc
    if valid(new_r, new_c, grid) and grid[new_r][new_c] != '#':
      stack.append(((new_r, new_c), cost + 1, direction, visited.copy()))

    # try turn right 90 degrees
    new_direction = rotate_90deg_right(direction)
    stack.append(((r, c), cost + 1000, new_direction, visited.copy()))

    # try turn left 90 degrees
    new_direction = rotate_90deg_left(direction)
    stack.append(((r, c), cost + 1000, new_direction, visited.copy()))

  return min_cost


@timeit
def part2(filename: str) -> int:
  return 0


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
