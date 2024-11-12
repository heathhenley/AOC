import json
from common.utils import problem_harness, timeit, read_input


def walk_json(obj, skip_red=False):
  total = 0
  if isinstance(obj, dict):
    for value in obj.values():
      if skip_red and value == 'red':
        return 0
      total += walk_json(value, skip_red)
  elif isinstance(obj, list):
    for item in obj:
      total += walk_json(item, skip_red)
  elif isinstance(obj, int):
    total += obj
  return total 


@timeit
def part1(filename: str) -> int:
  return walk_json(json.loads(read_input(filename)[0]))
    

@timeit
def part2(filename: str) -> int:
  return walk_json(json.loads(read_input(filename)[0]), skip_red=True)


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()