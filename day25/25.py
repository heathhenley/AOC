import collections
import sys
import time

import matplotlib.pyplot as plt
import networkx as nx

from common.utils import read_input

def parse(lines: list[str]) -> int:
  g =  collections.defaultdict(set)
  g = nx.Graph()
  for line in lines:
    node, connections = line.split(":")
    for connection in connections.split(" "):
      if connection:
        g.add_edge(node, connection)
  return g

def bfs(graph, start):
  visited = set()
  queue = collections.deque([start])
  count = 0
  while queue:
    node = queue.popleft()
    if node not in visited:
      count += 1
      visited.add(node)
      queue.extend(graph[node] - visited)
  return count

def part1(filename: str) -> int:
  graph = parse(read_input(filename))
  print(graph)
  #nx.draw(graph, with_labels=True)
  #plt.show()

  # remove edges - based on visual inspection of graph lol
  graph.remove_edge("cbl", "vmq")
  graph.remove_edge("nvf", "bvz")
  graph.remove_edge("xgz", "klk")
  #nx.draw(graph, with_labels=True)
  #plt.show()

  l = [len(g) for g in nx.connected_components(graph)]
  return  l[0] * l[1]


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
