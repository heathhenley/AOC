import collections
import sys

from common.utils import read_input

def parse(filename: str) -> list:
  return [[x for x in line] for line in read_input(filename)]

def find_start(grid: list[list[str]]) -> tuple:
  for x, row in enumerate(grid):
    for y, col in enumerate(row):
      if col == 'S':
        return (x, y)

def connected(neighbor_symbol: str, neighbor: tuple, cell: tuple) -> bool:
  """ Are these cells connected?, based on symbol """
  nr, nc = neighbor
  cr, cc = cell
  if neighbor_symbol == '|': # if it's above or below
    if nc == cc and (nr == cr - 1 or nr == cr + 1):
      return True
    return False
  if neighbor_symbol == '-': # if it's left or right
    if nr == cr and (nc == cc - 1 or nc == cc + 1):
      return True
    return False
  if neighbor_symbol == 'L': # if it's north or east
    if nr == cr + 1 and nc == cc:
      return True
    if nr == cr and nc == cc - 1:
      return True
    return False
  if neighbor_symbol == 'J': # if it's north or west 
    if nr == cr + 1 and nc == cc:
      return True
    if nr == cr and nc == cc + 1:
      return True
    return False
  if neighbor_symbol == '7': # if it's south or west
    if nr == cr - 1 and nc == cc:
      return True
    if nr == cr and nc == cc + 1:
      return True
    return False
  if neighbor_symbol == 'F': # if it's south or east
    if nr == cr - 1 and nc == cc:
      return True
    if nr == cr and nc == cc - 1:
      return True
    return False
  return False

def key_idx(key: str) -> tuple:
  return tuple([int(x) for x in key.split(',')])

def idx_key(idx: tuple) -> str:
  return f'{idx[0]},{idx[1]}'

def get_path(mem: dict, start: str) -> list:
  # dfs again until we come back to the start
  stack = [start]
  visited = set()
  path = []
  while stack:
    idx = stack.pop()
    if idx in visited:
      continue
    visited.add(idx)
    path.append(idx)
    for neighbor in mem[idx]:
      stack.append(neighbor)
  return path

def symbol_to_adjacency_idx(symbol: str) -> list[tuple[int, int]]:
  # the delta for the current index to neighbors based on the symbol
  if symbol == '|': # if it's above or below
    return [(0, 1), (0, -1)]
  if symbol == '-': # if it's left or right
    return [(1, 0), (-1, 0)]
  if symbol == 'L': # if it's north or east
    return [(1, 0), (0, -1)]
  if symbol == 'J': # if it's north or west
    return [(-1, 0), (0, -1)]
  if symbol == '7': # if it's south or west
    return [(-1, 0), (0, 1)]
  if symbol == 'F': # if it's south or east
    return [(1, 0), (0, 1)]
  return []

def build_graph(grid: list[list[str]], start: tuple) -> dict:
  ## build a graph from the grid using DSF and starting at S - I think this
  ## is better than just reading the grid and building a graph from it because
  ## we're only going to consider stuff that is reachable from S in some way
  stack = [start]
  visited = set()
  mem = collections.defaultdict(list) # directed graph, starting at S
  while stack:
    r, c = stack.pop()
    if (r, c) in visited:
      continue
    visited.add((r, c))
    if grid[r][c] == '.':
      continue
    # special case for start, we don't know what type of
    # of symbol is here, it just depends on what is around it
    # push onto stack depending on what is in the grid
    if grid[r][c] == 'S':
      for i in range(r - 1, r + 2):
        for j in range(c - 1, c + 2):
          if i == c and j == r:
            continue
          if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[i]):
            continue
          if connected(grid[i][j], (i, j), (r, c)):
            stack.append((i, j))
            mem[idx_key((i, j))].append(idx_key((r, c)))
            mem[idx_key((r, c))].append(idx_key((i, j)))
      continue
    # push onto stack depending on what is in the grid
    for dc, dr in symbol_to_adjacency_idx(grid[r][c]):
      row = r + dr
      col = c + dc
      # if it's out of bounds, skip
      if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[row]):
        continue
      if col == c and row == r:
        continue
      # add to stack to visit later, if it's not just ground (.)
      if grid[row][col] != '.':
        stack.append((row, col))
      # add to graph
      frm = idx_key((r, c))
      to = idx_key((row, col))
      if to not in mem[frm]:
        mem[frm].append(to)
      if frm not in mem[to]:
        mem[to].append(frm)
  return mem

def is_point_in_poly(
    poly: list[tuple[int, int]], point: tuple[int, int]) -> bool:
  x, y = point
  n = len(poly)
  inside = False
  p1x, p1y = poly[0]
  for i in range(n + 1):
    p2x, p2y = poly[i % n]
    if y > min(p1y, p2y):
      if y <= max(p1y, p2y):
        if x <= max(p1x, p2x):
          if p1y != p2y:
            xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
          if p1x == p2x or x <= xints:
            inside = not inside
    p1x, p1y = p2x, p2y
  return inside
  
def part1(filename: str) -> int:
  grid = parse(filename)
  start_row, start_col = find_start(grid)
  graph = build_graph(grid, (start_row, start_col))
  path = get_path(graph, idx_key((start_row, start_col)))
  return len(path) // 2

def part2(filename: str) -> int:
  grid = parse(filename)
  start_row, start_col = find_start(grid)
  graph = build_graph(grid, (start_row, start_col))
  path = get_path(graph, idx_key((start_row, start_col)))

  # at each grid point, find how many times we have crossed the path
  #  - if we have crossed it an even number of times, we are outside
  #  - if we have crossed it an odd number of times, we are inside
  #  - if we have crossed it 0 times, we are outside
  #  - if we are on the path, we can't be enclosed (based on problem)
  #  - anything that isn't on the path (other pipe and ground) is allowed 
  #  NOTE: this is the idea - I had a ton of trouble implmenting this correctly,
  #  so I just looked up a "point in polygon" implmentations (even odd rule)
  #  and used that instead of rolling my own. All the sources are in the readme
  #  for this day

  # build a polygon from the path + a new_grid that is 1 for path, 0 for not
  # mostly for visualization and debugging
  # 0 for everything that is not on the path, 1 for path:
  new_grid = [ [0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
  poly_path = []
  for idx in path:
    r, c = key_idx(idx)
    poly_path.append((r, c))
    new_grid[r][c] = 1

  # check each point in the grid and add them up
  crosses = [ [0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
  for row in range(len(grid)):
    for col in range(len(grid[row])):
      if new_grid[row][col] == 1:
        continue
      if is_point_in_poly(poly_path, (row, col)):
        crosses[row][col] = 1
  return sum([sum(x) for x in crosses])

def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")
  input_file = sys.argv[1]

  print("Part 1:", part1(input_file))
  print("Part 2:", part2(input_file))


if __name__ == '__main__':
  main()
