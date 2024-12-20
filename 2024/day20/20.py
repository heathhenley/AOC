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

@timeit
def part1(filename: str) -> int:
  # a nother maze problem - but this time we can cheat for up to 2 steps in a
  # row (eg we can walk through the walls)
  # it's not actually a maze - it's a single path from start to finish
  # - I think walk the path backwards and compute how far each step is from
  # - the end
  # - then walk the path forwards and check which nodes in all directions we can
  # - reach in 2 steps
  # - track the biggest 'distance to end' we can save (the difference between
  #   the current distance to end the the distance to end at the new node)
  grid = [ [c for c in line.strip()] for line in read_input(filename) ]
  start = find(grid, 'S')
  end = find(grid, 'E')

  dist = defaultdict(lambda: float('inf'))
  # walk the path starting at end
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

  # walk the path starting at start - check which nodes we can reach in 2 steps
  # and how much we save
  start_to_end = list(dist.keys())[::-1]
  cheats = []
  for (r, c) in start_to_end:
    # check - is there a # as a neighbor? if so, try to go one more in that
    # direction and see if we save distance
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
  #for c in counter:
  #  print(f"cheats of length {c}: {counter[c]}")
  return sum([counter[c] for c in counter if c >= 100])


@timeit
def part2(filename: str) -> int:
  return 0


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
