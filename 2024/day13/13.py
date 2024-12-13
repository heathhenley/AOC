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
  """ Plug in and filter non-int / out of bounds vals 

  Wrote it out on paper an realized because there are only two eqxs in two 
  unknowns you can just rearrange and solve - removes the overhead of np
  
  This doesn't work in general, but it does because it input is constrained and
  it turned that in my input / samples there was always a single solution or
  not. In general would probably need to go back to np and check coefficient
  matrix, to determine what to do."""
  ba, bb = g.button_a, g.button_b
  tx, ty = g.target
  if offsets is not None:
    tx += offsets[0][0]
    ty += offsets[1][0]
  nb = (tx / ba.dx - ty / ba.dy) / (bb.dx / ba.dx - bb.dy / ba.dy)
  na = (ty - nb * bb.dy) / ba.dy
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
