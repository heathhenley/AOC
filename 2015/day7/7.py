from typing import Dict
import re

from common.utils import problem_harness, timeit, read_input


REGEX_ARGS = r"(\d+|[a-z]+){0,1}\s{0,1}(AND|OR|LSHIFT|RSHIFT|NOT) (\d+|[a-z]+)"


functions = {
  "AND": lambda a, b: (a & b) & 0xFFFF,
  "OR": lambda a, b: (a | b) & 0xFFFF,
  "LSHIFT": lambda a, b: (a << b) & 0xFFFF,
  "RSHIFT": lambda a, b: (a >> b) &  0xFFFF,
  # passing 2 args but only using the second one, so that the functions all
  # have the same signature ('NOT A' parses as [None, 'NOT', 'A'])
  "NOT": lambda a, b: ~b & 0xFFFF
}


def try_int(val: str) -> int | str:
  """ Try to convert a string to an integer, if it fails return the string """
  if val is None:
    return val
  try:
    return int(val)
  except ValueError:
    return val


def parse_cmd(cmd: str) -> tuple:
  """ Return tuple of arg1 operator arg2 or just the number """
  m = re.match(REGEX_ARGS, cmd)
  if m is None:
    # it's just a number or a wire label
    return try_int(cmd)
  return [try_int(m.group(1)), m.group(2), try_int(m.group(3))] 


def get_value_at_node(label: str, graph: Dict) -> int:
  """ Recursively compute the value at a node in the graph """

  # if the value is an integer return it we're done
  if isinstance(graph[label], int):
    return graph[label]

  # if the value is a string we need to compute it it's probably a label of
  # another node that isn't computed yet, or that one could be a number
  if isinstance(graph[label], str):
    return get_value_at_node(graph[label], graph)

  # pull out the args and operator
  arg1, operator, arg2 = graph[label]

  # left and right args
  left = get_value_at_node(arg1, graph) if isinstance(arg1, str) else arg1
  right = get_value_at_node(arg2, graph) if isinstance(arg2, str) else arg2

  # save the new value in the graph
  graph[label] = functions[operator](left, right)

  return graph[label]


@timeit
def part1(filename: str) -> int:
  graph = dict()
  for line in read_input(filename):
    cmd, out = [x.strip() for x in line.split("->")]
    graph[out] = parse_cmd(cmd)
  return get_value_at_node('a', graph)


@timeit
def part2(filename: str) -> int:
  graph = dict()
  for line in read_input(filename):
    cmd, out = [x.strip() for x in line.split("->")]
    graph[out] = parse_cmd(cmd)
  graph['b'] = part1(filename)
  return get_value_at_node('a', graph)


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
