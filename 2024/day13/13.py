from dataclasses import dataclass
import numpy as np
import re
from common.utils import problem_harness, timeit, read_input


@dataclass
class Button:
  cost: int
  dx: int
  dy: int


@dataclass
class Game:
  button_a: Button
  button_b: Button
  target: tuple[int, int]


def parse_lines(lines: list[str]) -> list[Game]:
  re_btn = re.compile(r"^Button ([A,B]): X\+(\d+), Y\+(\d+)$")
  re_prize = re.compile(r"Prize: X=(\d+), Y=(\d+)$")
  games = []
  for line in lines:
    if m := re_btn.match(line):
      if m.group(1) == 'A':
        buttona = Button(cost=3, dx=int(m.group(2)), dy=int(m.group(3)))
      else:
        buttonb = Button(cost=1, dx=int(m.group(2)), dy=int(m.group(3)))
      continue
    if m := re.match(re_prize, line):
      target = (int(m.group(1)), int(m.group(2)))
      games.append(Game(button_a=buttona, button_b=buttonb, target=target))
  return games


def play_game(game: Game, btn_max: int) -> int:
  """ Brute force solution - useful for debugging (I had a rounding error) """
  ba, bb = game.button_a, game.button_b
  tx, ty = game.target
  min_cost = float('inf')
  for na in range(btn_max + 1):
    for nb in range(btn_max + 1):
      x = na * ba.dx + nb * bb.dx
      y = na * ba.dy + nb * bb.dy
      if x == tx and y == ty:
        print(na, nb)
        min_cost = min(min_cost, na * ba.cost + nb * bb.cost)
  return min_cost if min_cost != float('inf') else 0



def is_int(n: float, tol=0.001) -> bool:
  return np.abs(n - np.round(n, 0)) <  tol


def solve(
    g: Game, offsets: np.ndarray = None, limits: list[int]= None) -> int:
  
  ba, bb = g.button_a, g.button_b
  tx, ty = g.target

  b = np.array(
    [[tx],
     [ty]]
  ).astype(np.int64)

  if offsets is not None:
    b = b + offsets
  
  A = np.zeros((2, 2)).astype(np.int64)
  A = np.array(
    [[ba.dx, bb.dx],
     [ba.dy, bb.dy]]
  ).astype(np.int64)

  # Does this have a solution?
  if np.linalg.det(A) == 0:
    print("No solution")
    print(g, A, b)
    return 0

  # Does it have many solutions?
  ranka = np.linalg.matrix_rank(A)
  rankb = np.linalg.matrix_rank(np.concatenate((A, b), axis=1))
  if ranka != rankb:
    # thankfully this never happens in my input or the samples, so it's not
    # really an optimization problem - just need to solve it
    raise Exception("Many solutions possible for this game!", g)
  
  # Solve
  x = np.linalg.solve(A, b)
  na, nb = x[0][0], x[1][0]
  if na < 0 or nb < 0:
    return 0
  if limits is not None:
    if na > limits[0] or nb > limits[1]:
      return 0
  if is_int(na) and is_int(nb): 
    na = np.round(na, 0).astype(np.int64)
    nb = np.round(nb, 0).astype(np.int64)
    return int(na * ba.cost + nb * bb.cost)
  return 0


@timeit
def part1(filename: str) -> int:
  games = parse_lines(read_input(filename))
  return sum([solve(g, limits=[100, 100]) for g in games])


@timeit
def part2(filename: str) -> int:
  games = parse_lines(read_input(filename))
  offsets = np.array(
    [[10000000000000],
     [10000000000000]]
  )
  return sum([solve(g, offsets=offsets) for g in games])


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
