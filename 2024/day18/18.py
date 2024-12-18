import heapq
from common.utils import problem_harness, timeit, read_input


def valid(r, c, rmax, cmax):
  return 0 <= r < rmax and 0 <= c < cmax


def get_neighbors(r, c, rmax, cmax):
  dirs = [
    (-1, 0), # up
    (1, 0), # down
    (0, -1), # left
    (0, 1) # right
  ]
  return [
    (r+dr, c+dc) for dr, dc in dirs
    if valid(r+dr, c+dc, rmax, cmax)
  ]


def find_path(bad, start, end, rmax, cmax) -> int | None:
  """ Min cost or None if no path exists """
  visited = set()
  q = [(0, *start)]
  min_cost = None
  while q:
    cost, r, c = heapq.heappop(q)
    if (r, c) == end:
      min_cost = cost
      break # can stop because it's dijkstra
    if (r, c) in visited:
      continue
    visited.add((r, c))
    for (nr, nc) in get_neighbors(r, c, rmax + 1, cmax + 1):
      if (nr, nc) in bad: # skip 'corrupted' locations
        continue
      heapq.heappush(q, (cost+1, nr, nc))
  return min_cost


def parse(line):
  c, r = list(map(int, line.split(',')))
  return r, c


@timeit
def part1(filename: str) -> int:
  rmax, cmax = 70, 70
  locs = [parse(line) for line in read_input(filename)][:1024]
  return find_path(locs, (0, 0), (rmax, cmax), rmax, cmax)


@timeit
def part2(filename: str) -> int:
  rmax, cmax = 70, 70
  locs = [parse(line) for line in read_input(filename)]

  left_ptr, right_ptr = 0, len(locs) - 1
  # binary search for the first location that breaks the path
  while left_ptr < right_ptr:
    mid = (left_ptr + right_ptr) // 2
    bad_locs = locs[:mid+1]
    start = (0, 0)
    end = (rmax, cmax)
    if find_path(bad_locs, start, end, rmax, cmax) is None:
      right_ptr = mid
    else:
      left_ptr = mid + 1
  return locs[left_ptr][1], locs[left_ptr][0]


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
