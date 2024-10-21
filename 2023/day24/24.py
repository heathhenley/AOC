import sys
import time

import numpy as np
import matplotlib.pyplot as plt
from sympy import Symbol, solve_poly_system

from common.utils import read_input

def parse(line: str) -> int:
  pos, vel = line.split("@")
  pos = map(int, pos.strip().split(","))
  vel = map(int, vel.strip().split(","))
  return list(pos), list(vel)

def get_rhs(x1, x2):
  return np.array(
    [x1[0] - x2[0], # x's
     x1[1] - x2[1]] # y's
  )

def get_lhs(v1, v2):
  return np.array(
    [[-v1[0], v2[0]], # x's coord v
     [-v1[1], v2[1]]] # y's coord v
  )

def solve_for_path_crossing(hailstone1, hailstone2):
  pos1, vel1 = hailstone1
  pos2, vel2 = hailstone2
  rhs = get_rhs(pos1, pos2)
  lhs = get_lhs(vel1, vel2)
  try:
    t = np.linalg.solve(lhs, rhs)
    return t
  except np.linalg.LinAlgError:
    return None

def get_xy_at_time(hailstone, t):
  pos, vel = hailstone
  return [pos[0] + t*vel[0], pos[1] + t*vel[1]]

def count_collisions(
    hailstones: list, min_pos: int, max_pos: int) -> int:
  collisions = 0
  for i in range(len(hailstones)):
    for j in range(i+1, len(hailstones)):
      t = solve_for_path_crossing(hailstones[i], hailstones[j])
      if t is None:
        continue
      if np.any(t < 0):
        continue
      x, y = get_xy_at_time(hailstones[i], t[0])
      if min_pos <= x <= max_pos and min_pos <= y <= max_pos:
        collisions += 1
  return collisions

def find_best_path4(hailstones):
  # using sympy
  x, y, z = Symbol('x'), Symbol('y'), Symbol('z')
  vx, vy, vz = Symbol('vx'), Symbol('vy'), Symbol('vz')
  eqs = []
  times = []
  for idx, hailstone in enumerate(hailstones[:3]):
    pos, vel = hailstone
    t = Symbol(f't{idx}')
    eqs.append(x + vx * t - pos[0] - vel[0] * t)
    eqs.append(y + vy * t - pos[1] - vel[1] * t)
    eqs.append(z + vz * t - pos[2] - vel[2] * t)
    times.append(t)
  sol = solve_poly_system(eqs, *([x, y, z, vx, vy, vz] + times))
  return sol


def part1(filename: str) -> int:
  hailstones = [parse(line) for line in read_input(filename)]
  return count_collisions(
    hailstones, 200_000_000_000_000, 400_000_000_000_000)


def part2(filename: str) -> int:
  hailstones = [parse(line) for line in read_input(filename)]
  return sum(find_best_path4(hailstones)[0][:3])


def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")
  input_file = sys.argv[1]

  tic = time.perf_counter()
  print("Part 1:", part1(input_file))
  toc = time.perf_counter()
  print(f"  Part 1 took {toc - tic:0.4f} seconds")

  tic = time.perf_counter()
  print("Part 2:", part2(input_file))
  toc = time.perf_counter()
  print(f"  Part 2 took {toc - tic:0.4f} seconds")


if __name__ == '__main__':
  main()
