import collections
import math
import re
import sys

def read_input(filename: str, sep: str | None = None):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
    if sep is None:
      return  lines
    return [[val.strip() for val in line.split(sep)] for line in lines]

def parse_input(lines: list[str]):
  graph = collections.defaultdict(list)
  pattern = r"([A-Z]{3}).*\(([A-Z]{3}),\s([A-Z]{3})\)"
  for line in lines:
    match = re.match(pattern, line)
    if match:
      parent, child1, child2 = match.groups()
      graph[parent].append(child1)
      graph[parent].append(child2)
  return lines[0], graph

def path_length_for_start(
    graph: dict[str, list[str]], indices: list[int], instruction: str):
  n = len(instruction)
  to_z_from_a = []
  for i in indices:
    steps = 0
    current = list(graph.keys())[i]
    while current[-1] != "Z":
      if instruction[steps % n] == "L":
        current = graph[current][0]
      else:
        current = graph[current][1]
      steps += 1
    to_z_from_a.append(steps)
  return to_z_from_a


def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")

  input_file = sys.argv[1]
  print("Using input file", input_file)
  lines = read_input(input_file)
  instruction, graph = parse_input(lines)

  # Part 1
  n = len(instruction)
  steps = 0
  current = "AAA" # start at AAA
  while current != "ZZZ":
    if instruction[steps % n] == "L":
      current = graph[current][0]
    else:
      current = graph[current][1]
    steps += 1
  print("Part 1:", steps, current)

  # Part 2 - walk in "parallel", start at all nodes that end in A

  # Find indices of all nodes that end in A
  indices = [i for i, n in enumerate(graph.keys()) if n[-1] == "A"]

  # Walk to Z from all nodes that end in A to get the length of the
  # the path following these directions
  to_z_from_a = path_length_for_start(graph, indices, instruction)

  # Find the LCM of all these lengths
  lcm_of_lengths = math.lcm(*to_z_from_a)
  print("Part 2:", lcm_of_lengths)


# This was too slow for part 2
#  # Start at all nodes that end in A and walk
#  steps = 0
#  current = [list(graph.keys())[i] for i in indices]
#  while any([c[-1] != "Z" for c in current]):
#    for i, c in enumerate(current):
#      if instruction[steps % n] == "L":
#        current[i] = graph[c][0]
#      else:
#        current[i] = graph[c][1]
#    steps += 1
#  print("Part 2:", steps, current)

if __name__ == '__main__':
  main()
