import collections

from common.utils import problem_harness, timeit, read_input


def parse_line(line: str) -> tuple:
  cities, miles = line.split(' = ')
  city1, city2 = cities.split(' to ')
  return city1, city2, int(miles)

@timeit
def part1(filename: str) -> int:
  graph = collections.defaultdict(list)
  for line in read_input(filename):
    city1, city2, miles = parse_line(line)
    graph[city1].append((city2, miles))
    graph[city2].append((city1, miles))
  
  # Find all possible paths
  cities = list(graph.keys())
  min_cost = float('inf')
  save_path = []

  # all the possible starts
  for city in cities:
    
    # DFS
    stack = [(city, 0, [])]
    while stack:
      current_city, cost, visited = stack.pop()
      if current_city in visited:
        continue
      visited.append(current_city)

      if len(visited) == len(cities):
        if cost < min_cost:
          min_cost = cost
          save_path = visited.copy()
        continue

      for neighbor, miles in graph[current_city]:
        if neighbor not in visited:
          stack.append((neighbor, cost + miles, visited.copy()))
  #print("Shortest miles: ", min_cost)
  #print(" -> ".join(save_path)) 
  return min_cost


@timeit
def part2(filename: str) -> int:
  graph = collections.defaultdict(list)
  for line in read_input(filename):
    city1, city2, miles = parse_line(line)
    graph[city1].append((city2, miles))
    graph[city2].append((city1, miles))
  
  # Find all possible paths
  cities = list(graph.keys())
  max_cost = float('-inf')
  save_path = []

  # all the possible starts
  for city in cities:
    
    # DFS
    stack = [(city, 0, [])]
    while stack:
      current_city, cost, visited = stack.pop()
      if current_city in visited:
        continue
      visited.append(current_city)

      if len(visited) == len(cities):
        if cost > max_cost:
          max_cost = cost
          save_path = visited.copy()
        continue

      for neighbor, miles in graph[current_city]:
        if neighbor not in visited:
          stack.append((neighbor, cost + miles, visited.copy()))
  
  #print("Longest miles: ", max_cost)
  #print(" -> ".join(save_path)) 

  return max_cost


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()