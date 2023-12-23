import collections
import sys
import time

import matplotlib.pyplot as plt

from common.utils import read_input


def grid_to_img(grid: list) -> list:
  # just for plotting
  # convert the grid to an image
  img = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
  for i in range(len(grid)):
    for j in range(len(grid[0])):
      if grid[i][j] == '#':
        img[i][j] = 3
      elif grid[i][j] in ">v<^":
        img[i][j] = 1
  return img

def get_dirs(c: str, slopes_matter=True) -> list:
  # dirs we are alloed to go based on the current char
  if slopes_matter:
    if c == '>':
      return [(0, 1)]
    elif c == '<':
      return [(0, -1)]
    elif c == '^':
      return [(-1, 0)]
    elif c == 'v':
      return [(1, 0)]
  return [(1, 0), (-1, 0), (0, 1), (0, -1)]

def walk_grid_dfs(
    grid: list, start: tuple[int, int], end: tuple[int, int],
    slopes: bool = True) -> int:
  stack = [(start, set())]
  longest = 0
  while stack:
    (x, y), path = stack.pop()
    if (x, y) == end:
      longest = max(len(path), longest)
      #print(f"Found: {len(path)}, longest: {longest}")
      continue
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
      continue
    if grid[x][y] == '#':
      continue
    if (x, y) in path:
      continue
    path.add((x, y))
    for dx, dy in get_dirs(grid[x][y], slopes):
      tx, ty = x + dx, y + dy
      stack.append(((tx, ty), path.copy()))
  return longest

def get_start(grid: list) -> tuple[int, int]:
    for j in range(len(grid[0])):
      if grid[0][j] == '.':
        return (0, j)

def get_end(grid: list) -> tuple[int, int]:
    for j in range(len(grid[0])):
      if grid[-1][j] == '.':
        return (len(grid) - 1, j)

def get_adjacencies(grid: list) -> dict[tuple[int, int], list[tuple[int, int]]]:
  adjacencies = collections.defaultdict(list)
  for i in range(len(grid)):
    for j in range(len(grid[0])):
      if grid[i][j] == '#':
        continue
      for dx, dy in get_dirs(grid[i][j]):
        tx, ty = i + dx, j + dy
        if tx < 0 or ty < 0 or tx >= len(grid) or ty >= len(grid[0]):
          continue
        if grid[tx][ty] == '#':
          continue
        adjacencies[(i, j)].append((tx, ty))
  return adjacencies

def make_graph(grid: list) -> dict[tuple[int, int], list[tuple[int, int]]]:
  # make an adjacency list for the graph, where the key is the node and the
  # value is a list of all the nodes it can go to
  adjacencies = get_adjacencies(grid)
  # find intersections (nodes with 3 or more neighbors)
  intersections = []
  for node, neighbors in adjacencies.items():
    if len(neighbors) >= 3:
      intersections.append(node)
  # find the start / end
  start, end = get_start(grid), get_end(grid)

  # key points we don't want to squish together
  key_points = [start, *intersections, end]

  # new graph with the intersections and start / end and all
  # other's squished together
  graph = collections.defaultdict(dict)
  for node in key_points:
    queue = [(node, 1)]
    visited = set()
    while queue:
      n, dist = queue.pop(0)
      if n in visited:
        continue
      visited.add(n)
      for neighbor in adjacencies[n]:
        if neighbor == node:
          continue
        if neighbor not in key_points:
          queue.append((neighbor, dist + 1))
          continue
        graph[node][neighbor] = dist
        graph[neighbor][node] = dist
  return graph


def walk_graph_dfs(
    graph: dict[tuple[int, int], list[tuple[int, int]]], start, end) -> int:
  """ This works in that it finds the correct, max length path, but it
  there is a loop somewhere that, I haven't figured out the stop condition."""
  stack = [(start, set(), 0)]
  longest = 0
  while stack:
    node, path, dist = stack.pop()
    if node == end:
      longest = max(dist, longest)
      #print(f"Found: {dist}, longest: {longest}")
      continue
    if node in path:
      continue
    path.add(node)
    for neighbor, weight in graph[node].items():
      if neighbor in path:
        continue
      stack.append((neighbor, path.copy(), dist + weight))
  return longest

def part1(filename: str) -> int:
  lines = read_input(filename)
  grid = [[x for x in line] for line in lines]
  start, end = get_start(grid), get_end(grid)
  return walk_grid_dfs(grid, start, end)
  
def part2(filename: str) -> int:
  lines = read_input(filename)
  grid = [[x for x in line] for line in lines]
  start, end = get_start(grid), get_end(grid) 
  graph = make_graph(grid)
  return walk_graph_dfs(graph, start, end)


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
