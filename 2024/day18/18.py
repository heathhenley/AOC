import heapq
from common.utils import problem_harness, timeit, read_input

def valid(r, c, rmax, cmax):
  return 0 <= r < rmax and 0 <= c < cmax

dirs = [
  (-1, 0), # up
  (1, 0), # down
  (0, -1), # left
  (0, 1) # right
]

def get_neighbors(r, c, rmax, cmax):
  return [
    (r+dr, c+dc) for dr, dc in dirs
    if valid(r+dr, c+dc, rmax, cmax)
  ]


@timeit
def part1(filename: str) -> int:
  rmax, cmax = 70, 70
  locs = []
  for line in read_input(filename):
    c, r = list(map(int, line.split(',')))
    locs.append((r, c))

  # draw grid and mark locations
  #grid = [['.' for _ in range(cmax+1)] for _ in range(rmax+1)]
  #for i in range(1024):
  #  grid[locs[i][0]][locs[i][1]] = '#'
  #for i in range(rmax+1):
  #  print(''.join(grid[i]))

  # only the first 1024 locations
  locs = locs[:1024]   

  start = (0, 0)
  end = (rmax, cmax)
  visited = set()
  q = [(0, *start)]
  while q:
    cost, r, c = heapq.heappop(q)

    if (r, c) == end:
      min_cost = cost
      break # can stop because it's dijkstra

    if (r, c) in visited:
      continue
    visited.add((r, c))

    for (nr, nc) in get_neighbors(r, c, rmax + 1, cmax + 1):
      if (nr, nc) in locs: # skip 'corrupted' locations
        continue
      heapq.heappush(q, (cost+1, nr, nc))

  return min_cost


@timeit
def part2(filename: str) -> int:
  rmax, cmax = 6, 6
  locs = []
  for line in read_input(filename):
    c, r = list(map(int, line.split(',')))
    locs.append((r, c))
  
  # what is the first byte that blocks exit?
  # - instead of simulating the walk - what if we flood fill - I think that
  #   anytime you can go from side to side or top to bottom on corrupted spots,
  #   you can't exit
  


  return 0


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
