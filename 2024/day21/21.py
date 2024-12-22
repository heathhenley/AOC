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

@cache
def move_to_target(
    start: tuple[int, int],
    target: str,
    keypad_idx: int) -> list[str]:
  
  """ Ways to get to a target from start for a given keypad option """
  kp = keypads[keypad_idx]
  tr, tc = find(kp, target)
  r, c = start 
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
    r, c = start
    for move in path[:-1]:
      dr, dc = to_dir[move]
      r, c = r + dr, c + dc
      if kp[r][c] is None:
        break
    else:
      paths.append(path)
  return paths, (tr, tc)

@cache
def all_possible_seqs(
  code: str, curr: tuple[int, int], keypad_idx: int) -> list[str]:
  possible_ways = []
  for c in code:
    c = c.strip()
    moves, curr = move_to_target(curr, c, keypad_idx)
    new_ways = []
    for m in moves:
      if possible_ways:
        for prev in possible_ways:
          new_ways.append(prev + m)
      else:
        new_ways.append(m)
    possible_ways = new_ways.copy() 
  return ["".join(p) for p in possible_ways]

def process_code(code: str, levels: int) -> int:
  # robot 1 - at numeric keypad
  ways = all_possible_seqs(code, (3, 2), 0)
  # the rest
  for _ in range(levels - 1):
    tmp_ways = []
    for way in ways:
      tmp_ways.extend(all_possible_seqs(way, (0, 2), 1))
    ways = tmp_ways.copy()
  #s = ""
  #for w in ways:
  #  if len(w) < len(s) or s == "":
  #    s = w
  #print(s)
  return min([len(w) for w in ways])


@timeit
def part1(filename: str) -> int:
  c = 0
  for line in read_input(filename):
    d = int(re.sub(r"[A-Za-z]", "", line))
    l = process_code(line.strip(), 3)
    #print(line, d, l)
    c += d * l
  return c


@timeit
def part2(filename: str) -> int:
  return 0


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
