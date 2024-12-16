from collections import defaultdict
import heapq
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


def find_min_cost(grid):
  start = find(grid, 'S')
  min_cost = float('inf')
  q = [(0, start,'E')]
  visited = set()
  while q:
    cost, (r, c), direction = heapq.heappop(q)

    if (r, c, direction) in visited:
      continue
    visited.add((r, c, direction))

    if grid[r][c] == 'E':
      min_cost = min(min_cost, cost)
      continue
    # the options are to keep going in the same dir for a cost of 1
    # or to turn left or right 90 degrees for a cost of 1000 - needed to use a
    # heap to ensure we explore the lowest cost paths first (I think it's
    # basically dijkstra's algorithm but I might be missing something
    # try walk forward
    dr, dc = dir_map[direction]
    new_r, new_c = r + dr, c + dc
    if valid(new_r, new_c, grid) and grid[new_r][new_c] != '#':
      heapq.heappush(q, (cost + 1, (new_r, new_c), direction))

    # try turn right 90 degrees
    new_direction = rotate_90deg_right(direction)
    heapq.heappush(q, (cost + 1000, (r, c), new_direction))

    # try turn left 90 degrees
    new_direction = rotate_90deg_left(direction)
    heapq.heappush(q, (cost + 1000, (r, c), new_direction))
  return min_cost

def dijkstra_min_cost(grid, start, end):
  """ Returns a dict of min cost to reach each cell from start, and a dict of
  parents for each cell. The parents dict is used to reconstruct the paths
  later in pt 2 """
  visited = set()
  parents = defaultdict(list)
  min_cost = defaultdict(lambda: float('inf'))
  min_cost[(start)] = 0
  q = [(0, *start)]

  while q:
    cost, r, c, direction = heapq.heappop(q)

    if (r, c, direction) in visited:
        continue
    visited.add((r, c, direction))

    if (r, c) == end:
        continue

    # try walk forward
    dr, dc = dir_map[direction]
    new_r, new_c = r + dr, c + dc
    if valid(new_r, new_c, grid) and grid[new_r][new_c] != '#':
        new_cost = cost + 1
        if new_cost < min_cost[(new_r, new_c, direction)]:
            min_cost[(new_r, new_c, direction)] = new_cost
            heapq.heappush(q, (new_cost, new_r, new_c, direction))
            parents[(new_r, new_c, direction)] = [(r, c, direction)]
        elif new_cost == min_cost[(new_r, new_c, direction)]:
            if (r, c, direction) not in parents[(new_r, new_c, direction)]:
                parents[(new_r, new_c, direction)].append((r, c, direction))

    # try turn
    for d in [rotate_90deg_right, rotate_90deg_left]:
        new_direction = d(direction)
        new_cost = cost + 1000
        if new_cost < min_cost[(r, c, new_direction)]:
            min_cost[(r, c, new_direction)] = new_cost
            heapq.heappush(q, (new_cost, r, c, new_direction))
            parents[(r, c, new_direction)] = [(r, c, direction)]
        elif new_cost == min_cost[(r, c, new_direction)]:
            if (r, c, direction) not in parents[(r, c, new_direction)]:
                parents[(r, c, new_direction)].append((r, c, direction))
  return min_cost, parents

@timeit
def part1(filename: str) -> int:
  grid = [list(line.strip()) for line in read_input(filename)]
  start = (*find(grid, 'S'), "E")
  end = find(grid, 'E')
  min_costs, _ = dijkstra_min_cost(grid, start, end)
  return min(min_costs[(end[0], end[1], d)] for d in ['N', 'E', 'S', 'W'])


@timeit
def part2(filename: str) -> int:
  grid = [list(line.strip()) for line in read_input(filename)]

  start = (*find(grid, 'S'), "E") # always start facing east
  end = find(grid, 'E')
  min_cost, parents = dijkstra_min_cost(grid, start, end)

  # Now rebuild the paths and count the unique grid cells visited on the min
  # cost paths
  min_ = min(min_cost[(end[0], end[1], d)] for d in ['N', 'E', 'S', 'W'])
  print('Found a min cost of (should match part 1): ', min_)

  # What direction does the end need to be facing to have the min cost?
  end_dir = None
  for d in ['N', 'E', 'S', 'W']:
    if min_cost[(end[0], end[1], d)] == min_:
      end_dir = d
      break
  print('End direction: ', end_dir)

  # DFS to build all the paths from the parent dict
  stack = [((*end, end_dir), [(*end, end_dir)])]
  all_paths = []
  while stack:
      (r, c, current_direction), current_path = stack.pop()
      if (r, c, current_direction) == start:
          all_paths.append([(r, c) for (r, c, _) in current_path])
          continue
      for parent in parents.get((r, c, current_direction), []):
          stack.append((parent, current_path + [parent]))


  #for i in range(len(grid)):
  #  for j in range(len(grid[0])):
  #    if (i, j) in set([p for path in all_paths for p in path]):
  #      print('O', end='')
  #    else:
  #      print(grid[i][j], end='')
  #  print()
  
  return len(set([p for path in all_paths for p in path]))


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
