from common.utils import problem_harness, timeit, read_input
import re

def periodic_boundary(x: int, y: int, lim: tuple[int, int]) -> tuple[int, int]:
  return x % lim[0], y % lim[1]

def robo_walk(
    robot: tuple[int, int, int, int],
    t: int,
    lim: tuple[int, int]) -> tuple[int, int]:
  x, y, vx, vy = robot
  return periodic_boundary(x + t * vx, y +  t * vy, lim)

def print_grid(locs: list[tuple[int, int]], lim: tuple[int, int]):
  grid = [['.' for _ in range(lim[0])] for _ in range(lim[1])]
  for x, y in locs:
    grid[y][x] = str(int(grid[y][x]) + 1) if grid[y][x] != '.' else str(1)
  for row in grid:
    print(''.join(row))

def print_grid_r(locs: list[tuple[int, int, int, int]], lim: tuple[int, int]):
  grid = [['.' for _ in range(lim[0])] for _ in range(lim[1])]
  for x, y, _, _ in locs:
    grid[y][x] = str(int(grid[y][x]) + 1) if grid[y][x] != '.' else str(1)
  for row in grid:
    print(''.join(row))

def advance(
    robot: tuple[int, int, int, int],
    lim: tuple[int, int]) -> list[tuple[int, int, int, int]]:
  x, y, vx, vy = robot
  x, y = periodic_boundary(x + vx, y + vy, lim)
  return (x, y, vx, vy)

@timeit
def part1(filename: str) -> int:
  re_ptn = re.compile(r"^p=([-]*\d+),([-]*\d+) v=([-]*\d+),([-]*\d+)$")
  robots = []
  for line in read_input(filename):
    if m := re_ptn.match(line):
      x, y, vx, vy = map(int, m.groups())
      robots.append((x, y, vx, vy))

  #lim = (11, 7) # sample
  lim = (101, 103) # input

  # run all the robots for 100 seconds
  locs = [robo_walk(r, 100, lim) for r in robots]

  # count the number of robots in each quadrant
  # - robots exactly in the middle don't count (hor or ver)
  quads = [
    [[0, 0], [lim[0] // 2, lim[1] // 2]], # top left quad
    [[lim[0] // 2, 0], [lim[0], lim[1] // 2]], # top right quad
    [[0, lim[1] // 2], [lim[0] // 2, lim[1]]], # bottom left quad
    [[lim[0] // 2, lim[1] // 2], [lim[0], lim[1]]] # bottom right quad
  ]

  prod = 1
  for i, quad in enumerate(quads):
    count = 0
    for x, y in locs:
      if quad[0][0] <= x <= quad[1][0] and quad[0][1] <= y <= quad[1][1]:
        if x != lim[0] // 2 and y != lim[1] // 2: # middle
          count += 1
    prod *= count
    print(f"Quadrant {i} has {count} robots")
  return prod

def count_neighbors(
    robot: tuple[int, int, int, int],
    robots: list[tuple[int, int, int, int]]) -> int:
  x, y, _, _ = robot
  count = 0
  for r in robots:
    if r != robot:
      rx, ry, _, _ = r
      if abs(rx - x) <= 1 and abs(ry - y) <= 1:
        count += 1
  return count

@timeit
def part2(filename: str) -> int:
  re_ptn = re.compile(r"^p=([-]*\d+),([-]*\d+) v=([-]*\d+),([-]*\d+)$")
  robots = []
  for line in read_input(filename):
    if m := re_ptn.match(line):
      x, y, vx, vy = map(int, m.groups())
      robots.append((x, y, vx, vy))

  lim = (101, 103) # input, cycle = 10403

  t = 0
  max_navg = 0
  max_robot_dist = []
  while t < 10403:
    # advance all the robots by 1 second
    robots = [advance(r, lim) for r in robots]
    # how many neighbors does each robot have?
    # numpy would make this way faster but idc rn
    neighbors = [count_neighbors(r, robots) for r in robots]
    navg = sum(neighbors) / len(neighbors)
    if navg > max_navg:
      #print(f"Time: {t}, Average neighbors: {navg}")
      #print_grid_r(robots, lim)
      max_navg = navg
      t_max = t
      max_robot_dist = [r for r in robots if count_neighbors(r, robots) > 1]
    if t % 1000 == 0:
      print(f"Time: {t}, Max Average neighbors: {max_navg}, t_max: {t_max}")
    
    t += 1
  print_grid_r(max_robot_dist, lim)

  return t_max + 1


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
