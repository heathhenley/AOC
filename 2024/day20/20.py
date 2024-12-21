from collections import defaultdict
from common.utils import problem_harness, timeit, read_input

def find(grid, target):
  for r in range(len(grid)):
    for c in range(len(grid[0])):
      if grid[r][c] == target:
        return (r, c)
  return None

def valid(r, c, grid):
  return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def get_neighbors(r, c, grid):
  dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
  return [(r + dr, c + dc) for dr, dc in dirs if valid(r + dr, c + dc, grid)]

def dist_along_path(grid, start, end):
  dist = defaultdict(lambda: float('inf'))
  dist[end] = 0
  stack = [end]
  visited = set()
  while stack:
    r, c = stack.pop()
    if (r, c) in visited:
      continue
    visited.add((r, c))
    if (r, c) == start:
      break
    for nr, nc in get_neighbors(r, c, grid):
      if grid[nr][nc] == '#' or (nr, nc) in visited:
        continue
      dist[(nr, nc)] = dist[(r, c)] + 1
      stack.append((nr, nc))
  return dist

@timeit
def part1(filename: str) -> int:
  grid = [ [c for c in line.strip()] for line in read_input(filename) ]
  start = find(grid, 'S')
  end = find(grid, 'E')
  dist = dist_along_path(grid, start, end)

  # walk the path starting at start - check which nodes we can reach in 2 steps
  # and how much we save
  start_to_end = list(dist.keys())[::-1]
  cheats = []
  for (r, c) in start_to_end:
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dr, dc in dirs:
      nr, nc = r + dr, c + dc
      if not valid(nr, nc, grid) or grid[nr][nc] != '#':
        continue
      nnr, nnc = nr + dr, nc + dc
      if not valid(nnr, nnc, grid) or grid[nnr][nnc] == '#':
        continue
      # we can walk from (r, c) to (nnr, nnc) in 2 steps (through a wall)
      savings = (dist[(r, c)] - dist[(nnr, nnc)]) - 2
      if savings > 0:
        cheats.append((savings, (r, c), (nr, nc), (nnr, nnc))) 
  # count how many cheats we found for each length of savings
  counter = defaultdict(int)
  for s, a, b, c in cheats:
    counter[s] += 1
  return sum([counter[c] for c in counter if c >= 100])


@timeit
def part2(filename: str) -> int:
  # This is slow, but it works. I looked at other solutions and they just used a
  # 'circle' around the each point on the path with a radius of 20 (a diamond
  # kind of I guess) - that's probably faster than a bunch of bfs - there's a
  # bunch of paths that don't matter
  grid = [ [c for c in line.strip()] for line in read_input(filename) ]
  start = find(grid, 'S')
  end = find(grid, 'E')
  dist = dist_along_path(grid, start, end)

  # walk the path starting at start - check which nodes we can reach in 20 steps
  # or fewer and how much we save going to each one
  start_to_end = list(dist.keys())[::-1]
  # the same start end point can have multiple cheats, and they
  cheats = {}
  for idx, (r, c) in enumerate(start_to_end):
    if idx % 100 == 0:
      print(f"{idx} of {len(start_to_end)}")
    # walk up to 20 steps in any direction
    q = [(0, r, c)]
    visited = set()
    while q:
      steps, nr, nc = q.pop(0)
      if (nr, nc, steps) in visited:
        continue
      visited.add((nr, nc, steps))

      if grid[nr][nc] != '#':
        # we could step and maybe save distance
        abs_distance = abs(r - nr) + abs(c - nc)
        # distance to end at new spot - distance to end at current spot
        # but the best possible walk there is abs_distance
        savings = (dist[(r, c)] - dist[(nr, nc)]) - abs_distance
        if savings > 0:
          cheats[((r, c), (nr, nc))] = max(
            savings,
            cheats.get(((r, c), (nr, nc)), 0)
          )
      # we can step through the wall
      for row, col in get_neighbors(nr, nc, grid):
        if steps < 20: # can we take another step?
          q.append((steps + 1, row, col))
  
  # count how many cheats we found for each length of savings
  counter = defaultdict(int)
  for (start, end), s in cheats.items():
    counter[s] += 1
  for c in sorted(counter.keys()):
    if c >= 100:
      print(c, counter[c])
  return sum([counter[c] for c in counter if c >= 100])


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
