from collections import defaultdict
from functools import cache
import heapq
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

@cache
def move_to_target(
    start: tuple[int, int],
    target: str,
    keypad_idx: int) -> list[str]:
  
  """ Ways to get to a target from start for a given keypad option """
  r, c = start 
  kp = keypads[keypad_idx]
  tr, tc = find(kp, target)
  dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
  d = {(0, 1): '>', (0, -1): '<', (1, 0): 'v', (-1, 0): '^'}
  q = [(0, r, c)]
  v = set()
  min_cost = defaultdict(lambda: float('inf'))
  min_cost[(r, c)] = 0
  parents = defaultdict(list)
  while q:
    cost, r, c = heapq.heappop(q)
    if (r, c) == (tr, tc):
      break
    if cost > min_cost[(r, c)]: # we've already found a better path
      continue
    if (r, c) in v:
      continue
    v.add((r, c))
    for dr, dc in dirs:
      nr, nc = r + dr, c + dc
      if valid(nr, nc, kp) and kp[nr][nc] is not None:
        if cost + 1 < min_cost[(nr, nc)]:
          min_cost[(nr, nc)] = cost + 1
          parents[(nr, nc)] = [(r, c)]
        elif cost + 1 == min_cost[(nr, nc)]:
          parents[(nr, nc)].append((r, c))
        heapq.heappush(q, (cost + 1, nr, nc))
  
  # reconstruct the valid paths
  paths = []
  rr, rc = start
  def dfs(r, c, moves):
    if (r, c) == (rr, rc):
      paths.append(moves)
      return
    for pr, pc in parents[(r, c)]:
      if (pr, pc) == (r, c):
        continue
      dfs(pr, pc, moves + [d[(r - pr, c - pc)]])
  dfs(tr, tc, [])
  for p in paths:
    p.append('A')
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

def process_code(code: str) -> int:
  min_len = float("inf")
  # robot 1
  ways = all_possible_seqs(code, (3, 2), 0)
  # robot 2
  ways2 = []
  for way in ways:
    ways2.extend(all_possible_seqs(way, (0, 2), 1))
  # robot 3
  ways3 = []
  for way in ways2:
    ways3.extend(all_possible_seqs(way, (0, 2), 1))
  # me
  for way in ways3:
    min_len = min(all_possible_seqs(way, (0, 2), 1), min_len)
  return min_len
 
@timeit
def part1(filename: str) -> int:
  for line in read_input(filename):
    print(process_code(line.strip()))
    break
  return 0


@timeit
def part2(filename: str) -> int:
  return 0


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
