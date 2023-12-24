import sys
import time

import numpy as np
import scipy.optimize as opt

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


def distance(rock, hailstone):
  # rocks vector is (x + vt, y + vt, z + vt)
  # same for hailstone
  rpos, rvel = np.array(rock[0]), np.array(rock[1])
  hpos, hvel = np.array(hailstone[0]), np.array(hailstone[1])
  r = rpos - hpos
  cross = np.cross(hvel, rvel)
  dist = np.array([r, cross]) / np.linalg.norm(cross)
  dist = np.linalg.norm(dist)
  return dist

def get_obj(rock, hailstones):
  obj = 0
  for i in range(len(hailstones)):
    obj += abs(distance(rock, hailstones[i]))
  return obj


def find_best_path(hailstones):
  # this isn't working - it's converging to a min obj value
  # but it's not 0 - which I was hoping it would be meaning
  # it found a path with min distance of 0 between all hailstones
  # going to try a different approach
  xrock = [0, 0, 0]
  vrock = [10, 10, 1]
  dx = 0.00001
  dv = 0.00001
  dodx = [0, 0, 0]
  dodv = [0, 0, 0]
  step = 0.1
  obj, prev_obj = None, None
  while not prev_obj or obj is None or abs(obj - prev_obj) > 0.0001:
    prev_obj = obj
    obj = get_obj([xrock, vrock], hailstones)
    for i in range(3):
      # x dirs
      tmp = xrock[i]
      xrock[i] += dx
      obj2 = get_obj([xrock, vrock], hailstones)
      dodx[i] = (obj2 - obj) / dx
      xrock[i] = tmp

      # v dirs
      tmp = vrock[i]
      vrock[i] += dv
      obj2 = get_obj([xrock, vrock], hailstones)
      dodv[i] = (obj2 - obj) / dv
      vrock[i] = tmp

    # apply updates based on dodx and dodv
    for i in range(3):
      xrock[i] -= step * dodx[i]
      vrock[i] -= step * dodv[i]
  print(f"obj: {obj}")
  print(f"  xrock: {xrock}, vrock: {vrock}")


def get_rhs_3d(x1, x2, axis: tuple = (0, 1)):
  return np.array(
    [x1[0] - x2[0], # x's
     x1[1] - x2[1], # y's
     x1[2] - x2[2]] # z's
  )

def get_lhs_3d(v1, v2):
  return np.array(
    [[-v1[0], v2[0]], # x's coord v
     [-v1[1], v2[1]], # y's coord v
     [-v1[2], v2[2]]] # z's coord v
  )

def solve_for_path_crossing_3d(hailstone1, hailstone2):
  pos1, vel1 = hailstone1
  pos2, vel2 = hailstone2
  rhs = get_rhs_3d(pos1, pos2)
  lhs = get_lhs_3d(vel1, vel2)
  try:
    t = np.linalg.solve(lhs, rhs)
    return t
  except np.linalg.LinAlgError:
    print("singular matrix")
    return None

def get_f(xrock, vrock, ti, hailstones):
  F = np.zeros((len(hailstones) * 3, 1))
  print(len(hailstones))
  for i in range(len(hailstones)):
    hpos, hvel = np.array(hailstones[i][0]), np.array(hailstones[i][1])
    for j in range(3):
      F[ i * 3 + j] = ti[i] * (hvel[j] - vrock[j]) + hpos[j] - xrock[j]
  return F.reshape((12,))

def find_best_path2(hailstones):
  x0 = np.ones((12,))
  f = lambda x: get_f(x[0:3], x[3:6], x[6:], hailstones[:4])
  s = opt.fsolve(f, x0)
  print(s)


def find_best_path3(hailstones):
  # pick a velocity vector
  vmin, vmax = -250, 250
  # what are the equations if we pick a velocity vector? (they're linear now)
  for vi in range(vmin, vmax+1):
    for vj in range(vmin, vmax+1):
      for vk in range(vmin, vmax+1):
        # solve for t
        
  


          



def part1(filename: str) -> int:
  hailstones = [parse(line) for line in read_input(filename)]
  return count_collisions(
    hailstones, 200_000_000_000_000, 400_000_000_000_000)


def part2(filename: str) -> int:
  hailstones = [parse(line) for line in read_input(filename)]
  print(find_best_path3(hailstones))


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
