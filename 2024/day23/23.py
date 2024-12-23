from collections import defaultdict
from common.utils import problem_harness, timeit, read_input


@timeit
def part1(filename: str) -> int:
  adj = defaultdict(list)
  for line in read_input(filename):
    a, b = line.strip().split("-")
    adj[a].append(b)
    adj[b].append(a)

  # how many cycles of length 3 are there that contain at least one node that
  # starts with t?
  # - start with each node
  # - walk to each neighbor 
  # - push cycle if we ever find start

  cycles = []

  for k in adj.keys():
    stack = [(k, set())]
    while stack:
      node, nodes = stack.pop()
      if node == k and len(nodes) == 3:
        cycles.append(nodes)
        continue
      if len(nodes) > 3:
        continue
      for neighbor in adj[node]:
        if neighbor not in nodes:
          stack.append((neighbor, nodes | {neighbor}))

  # should do this part as we go above 
  cycles_unique = set()
  for c in cycles:
    a, b, c = sorted(list(c))
    if (a, b, c) not in cycles_unique:
      cycles_unique.add((a, b, c))

  count = 0
  for a, b, c in cycles_unique:
    if a.startswith('t') or b.startswith('t') or c.startswith('t'):
      count += 1

  return count


@timeit
def part2(filename: str) -> int:
  adj = defaultdict(list)
  for line in read_input(filename):
    a, b = line.strip().split("-")
    adj[a].append(b)
    adj[b].append(a)
  
  # looking for the largest "complete subgraph" in the input...
  # - definitely can do this with networkx... but searching to see if there's
  #   a simple way to do it manually....
  def bron_kerbosch(current_clique, potential, visited, clique):
    # - "Bron kerbosch" algorithm on wiki:
    #  - https://en.wikipedia.org/wiki/Clique_problem 
    #  - https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    if len(potential) == 0 and len(visited) == 0:
      clique.append(current_clique)
    for node in potential.copy():
      neighbors = adj[node]
      new_clique = current_clique + [node]
      new_potential = potential.intersection(neighbors)
      new_visited = visited.intersection(neighbors)
      # Try adding node to clique
      bron_kerbosch(new_clique, new_potential, new_visited, clique)
      potential.remove(node)
      visited.add(node)
  
  current = []
  available = set(adj.keys())
  visited = set()
  clique = []
  bron_kerbosch(current, available, visited, clique)

  #print('Found cliques: ')
  #for c in clique:
  #  print(c)
  clique.sort(key=lambda x: len(x), reverse=True)
  c = ",".join(sorted(clique[0]))
  return c


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
