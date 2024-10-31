from typing import Tuple, NamedTuple

from common.utils import problem_harness, timeit, read_input


# what can we do to the lights?
commands_pt1 = {
  "turn_on": lambda x: 1,
  "turn_off": lambda x: 0,
  "toggle": lambda x: 1 if x == 0 else 0
}


commands_pt2 = {
  "turn_on": lambda x: 1 + x,
  "turn_off": lambda x: max(0, x-1),
  "toggle": lambda x: x + 2
}


Grid = NamedTuple("Grid", [("lights", list), ("size", int)])
Light = NamedTuple("Light", [("x", int), ("y", int), ("state", int)])
Cmd = NamedTuple("Cmd",
  [("cmd", str), ("start", Tuple[int, int]), ("end", Tuple[int, int])])


def parse_line(line: str) -> Cmd:
  """ Parse a line of input into a command and range """
  line = (
    line
      .replace("turn ", "turn_")
      .replace("through", "")
      .split(" ")
  )
  start = [int(x) for x in line[1].split(",")]
  end = [int(x) for x in line[3].split(",")]
  return Cmd(
    cmd=line[0],
    start=(*start, ),
    end=(*end,)
  )


@timeit
def part1(filename: str) -> int:
  grid = Grid(lights=[0]*1000*1000, size=1000)
  for line in read_input(filename):
    cmd = parse_line(line)
    for x in range(cmd.start[0], cmd.end[0]+1):
      for y in range(cmd.start[1], cmd.end[1]+1):
        idx = x + y * grid.size
        grid.lights[idx] = commands_pt1[cmd.cmd](grid.lights[idx])
  return sum(grid.lights)


@timeit
def part2(filename: str) -> int:
  grid = Grid(lights=[0]*1000*1000, size=1000)
  for line in read_input(filename):
    cmd = parse_line(line)
    for x in range(cmd.start[0], cmd.end[0]+1):
      for y in range(cmd.start[1], cmd.end[1]+1):
        idx = x + y * grid.size
        grid.lights[idx] = commands_pt2[cmd.cmd](grid.lights[idx])
  return sum(grid.lights)


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()