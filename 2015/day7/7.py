from common.utils import problem_harness, timeit, read_input



def parse_cmd(cmd: str) -> tuple:
  cmd = cmd.split(" ")
  if len(cmd) == 1:
    try:
      return int(cmd[0])
    except ValueError:
      return cmd[0]
  if len(cmd) == 2: # NOT
    try:
      return [cmd[0], int(cmd[1])]
    except ValueError:
      return [cmd[0], cmd[1]]
  try:
    return [int(cmd[0]), cmd[1], int(cmd[2])]
  except ValueError:
    try:
      return [cmd[0], cmd[1], int(cmd[2])]
    except ValueError:
      try:
        return [int(cmd[0]), cmd[1], cmd[2]]
      except ValueError:
        return [cmd[0], cmd[1], cmd[2]]


@timeit
def part1(filename: str) -> int:
  graph = dict()
  for line in read_input(filename):
    cmd, out = [x.strip() for x in line.split("->")]
    graph[out] = parse_cmd(cmd)
  

  count_of_ints = len([1 for k, v in graph.items() if type(v) == int])

  while count_of_ints < len(graph):
    # replacing all labels with their values if they are available
    count_of_ints = len([1 for k, v in graph.items() if type(v) == int])

    for k, v in graph.items():
      if isinstance(v, int):
        for key, cmd in graph.items():
          if isinstance(cmd, list):
            if k in cmd:
              graph[key][graph[key].index(k)] = int(graph[k])
      if isinstance(v, str):
        graph[k] = graph[v]
    # compute any values that can be computed
    for key, cmd in graph.items():
      if isinstance(cmd, list):
        if len(cmd) == 2: # NOT
          if type(cmd[1]) == int:
            graph[key] = ~cmd[1] & 0xFFFF
          continue
        if type(cmd[0]) == int and type(cmd[2]) == int:
          if "AND" in cmd:
            graph[key] = (cmd[0] & cmd[2]) & 0xFFFF
          elif "OR" in cmd:
            graph[key] = (cmd[0] | cmd[2]) & 0xFFFF
        if cmd[1] =="LSHIFT" and type(cmd[0]) == int:
          graph[key] = (cmd[0] << int(cmd[2])) & 0xFFFF
        if cmd[1] =="RSHIFT" and type(cmd[0]) == int:
          graph[key] = (cmd[0] >> int(cmd[2])) & 0xFFFF

  return graph.get("a", 0)



@timeit
def part2(filename: str) -> int:
  graph = dict()
  for line in read_input(filename):
    cmd, out = [x.strip() for x in line.split("->")]
    graph[out] = parse_cmd(cmd)

  graph["b"] = part1(filename) 

  count_of_ints = len([1 for k, v in graph.items() if type(v) == int])

  while count_of_ints < len(graph):
    # replacing all labels with their values if they are available
    count_of_ints = len([1 for k, v in graph.items() if type(v) == int])

    for k, v in graph.items():
      if isinstance(v, int):
        for key, cmd in graph.items():
          if isinstance(cmd, list):
            if k in cmd:
              graph[key][graph[key].index(k)] = int(graph[k])
      if isinstance(v, str):
        graph[k] = graph[v]
    # compute any values that can be computed
    for key, cmd in graph.items():
      if isinstance(cmd, list):
        if len(cmd) == 2: # NOT
          if type(cmd[1]) == int:
            graph[key] = ~cmd[1] & 0xFFFF
          continue
        if type(cmd[0]) == int and type(cmd[2]) == int:
          if "AND" in cmd:
            graph[key] = (cmd[0] & cmd[2]) & 0xFFFF
          elif "OR" in cmd:
            graph[key] = (cmd[0] | cmd[2]) & 0xFFFF
        if cmd[1] =="LSHIFT" and type(cmd[0]) == int:
          graph[key] = (cmd[0] << int(cmd[2])) & 0xFFFF
        if cmd[1] =="RSHIFT" and type(cmd[0]) == int:
          graph[key] = (cmd[0] >> int(cmd[2])) & 0xFFFF
  return graph.get("a", 0)


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()