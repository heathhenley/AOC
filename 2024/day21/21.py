from functools import cache
from itertools import permutations
import re
from common.utils import problem_harness, timeit, read_input

def find(keys, target):
  for r in range(len(keys)):
    for c in range(len(keys[0])):
      if keys[r][c] == target:
        return (r, c)
  return None


def valid(r, c, grid):
  return 0 <= r < len(grid) and 0 <= c < len(grid[0])

keypads  = [
  [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A']
  ],
  [
    [None, '^', 'A'],
    ['<', 'v', '>'],
  ]
]

to_dir = {
  ">": (0, 1),
  "<": (0, -1),
  "^": (-1, 0),
  "v": (1, 0)
}


def move_to_target(
    start: str,
    target: str,
    keypad_idx: int) -> list[str]:
  
  """ Ways to get to a target from start for a given keypad option """
  kp = keypads[keypad_idx]
  tr, tc = find(kp, target)
  r, c = find(kp, start)
  sr, sc = r, c
  dr, dc = tr - r, tc - c
  moves = ""
  if dr > 0:
    moves += "v" * dr
  elif dr < 0:
    moves += "^" * abs(dr)
  if dc > 0:
    moves += ">" * dc
  elif dc < 0:
    moves += "<" * abs(dc)

  any_paths = set(["".join(x) + "A" for x in permutations(moves)])
  paths = []
  # clean out bad paths (if they cross the None spot)
  for path in any_paths:
    r, c = sr, sc
    for move in path[:-1]:
      dr, dc = to_dir[move]
      r, c = r + dr, c + dc
      if kp[r][c] is None:
        break
    else:
      paths.append(path)
  return paths


@cache
def min_ways(start, target, keypad_idx, depth=0):
  if depth == 0:
    return min([len(x) for x in move_to_target(start, target, 1)])
  ways = move_to_target(start, target, keypad_idx) 
  min_count = float("inf")
  for way in ways:
    count = 0
    w = "A"
    for i in range(len(way)):
      count += min_ways(w, way[i], 1, depth - 1)
      w = way[i]
    min_count = min(min_count, count)
  return min_count


def process_code(code: str, depth: int) -> int:
  curr, count = "A", 0
  for c in code:
    res = min_ways(curr, c, 0, depth)
    count += res
    curr = c
  return count


@timeit
def part1(filename: str) -> int:
  c = 0
  for line in read_input(filename):
    d = int(re.sub(r"[A-Za-z]", "", line))
    l = process_code(line.strip(), 2)
    #print(line, d, l)
    c += d * l
  return c


@timeit
def part2(filename: str) -> int:
  c = 0
  for line in read_input(filename):
    d = int(re.sub(r"[A-Za-z]", "", line))
    l = process_code(line.strip(), 25)
    c += d * l
  return c


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
