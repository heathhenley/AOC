import collections
from dataclasses import dataclass
import sys
import time
from common.utils import read_input

@dataclass
class Cube:
  x: int
  y: int
  z: int

@dataclass
class Brick:
  start: Cube
  end: Cube
  label: str = None

def letter_generator():
  counter = -1
  next_letter = ord("A")
  def increment():
    nonlocal counter
    counter += 1
    return chr(next_letter + counter)
  return increment

next_letter = letter_generator()

def parse(line: str) -> Brick:
  start, end = line.strip().split("~")
  start = Cube(*map(int, start.split(",")))
  end = Cube(*map(int, end.split(",")))
  return Brick(start, end, label=next_letter())

def get_xyz_max(bricks: list[Brick]) -> tuple[int, int, int]:
  maxx, maxy, maxz = 0, 0, 0
  for brick in bricks:
    maxx = max(maxx, brick.end.x)
    maxy = max(maxy, brick.end.y)
    maxz = max(maxz, brick.end.z)
  return maxx, maxy, maxz

def get_grid(bricks: list[Brick]) -> list[list[list[bool]]]:
  maxx, maxy, maxz = get_xyz_max(bricks)
  grid = [[[False for _ in range(maxy + 1)] for _ in range(maxx + 1)] for _ in range(maxz + 1)]
  for brick in bricks:
    for x in range(brick.start.x, brick.end.x + 1):
      for y in range(brick.start.y, brick.end.y + 1):
        for z in range(brick.start.z, brick.end.z + 1):
          grid[z][x][y] = True
  return grid

def print_bricks(bricks: list[Brick]):
  maxx, maxy, maxz = get_xyz_max(bricks)
  print("XZ")
  for z in range(maxz, -1, -1):
    for x in range(maxx + 1):
      for brick in bricks:
        if brick.start.x <= x <= brick.end.x and brick.start.z <= z <= brick.end.z:
          print(brick.label, end="")
          break
      else:
        print(".", end="")
    print()
  
  print("YZ")
  for z in range(maxz, -1, -1):
    for y in range(maxy + 1):
      for brick in bricks:
        if brick.start.y <= y <= brick.end.y and brick.start.z <= z <= brick.end.z:
          print(brick.label, end="")
          break
      else:
        print(".", end="")
    print()

def is_supported(brick: Brick, grid: list[list[list[bool]]]) -> bool:
  sx, sy, sz = brick.start.x, brick.start.y, brick.start.z
  ex, ey, ez = brick.end.x, brick.end.y, brick.end.z
  for x in range(sx, ex + 1):
    for y in range(sy, ey + 1):
      if grid[sz-1][x][y]:
        return True
  return False

def process_bricks(bricks: list[Brick]):
  maxx, maxy, maxz = get_xyz_max(bricks)
  grid = get_grid(bricks)
  stack = [*bricks][::-1]
   # don't need stack if we move as much as possible but w/e
  while stack:
    brick = stack.pop()

    # if it has nothing below it in z, in both
    # x and y, then it can be moved down
    # and the grids need to be updated
    if brick.start.z == 1 or brick.end.z == 1:
      # on the ground - all goood
      continue

    if is_supported(brick, grid):
      continue # all good

    # update grid
    for x in range(brick.start.x, brick.end.x + 1):
      for y in range(brick.start.y, brick.end.y + 1):
        for z in range(brick.start.z, brick.end.z + 1):
          grid[z][x][y] = False
    
    # brick can move down
    brick.start.z -= 1
    brick.end.z -= 1

    # update grid
    for x in range(brick.start.x, brick.end.x + 1):
      for y in range(brick.start.y, brick.end.y + 1):
        for z in range(brick.start.z, brick.end.z + 1):
          grid[z][x][y] = True
    
    # add to stack (because we're only move 1z at a time)
    stack.append(brick)

def get_support_graph(bricks: list[Brick]) -> dict[str, set[str]]:
  supported_by_graph = collections.defaultdict(list)
  supports_graph = collections.defaultdict(list)
  for brick in bricks:
    for other_brick in bricks:
      if brick.label == other_brick.label:
        continue
      if brick.end.z + 1 == other_brick.start.z:
        # other_brick is above brick in z (directly above)

        # does it overlap in x and y?
        for x in range(brick.start.x, brick.end.x + 1):
          for y in range(brick.start.y, brick.end.y + 1):
            if other_brick.start.x <= x <= other_brick.end.x and other_brick.start.y <= y <= other_brick.end.y:
              supported_by_graph[other_brick.label].append(brick.label)
              supports_graph[brick.label].append(other_brick.label)
  return supported_by_graph, supports_graph

def count_removeable_bricks(bricks: list[Brick]) -> int:
 # what can we remove?
  # any brick that:
  #  - supports nothing (easy case)
  #  - is supporting sometihng that has other support
  # So take each brick:
  #  - if it supports nothing, count it as removed
  #  - check the bricks it supports
  #    - if any of those bricks have other support, count it as removed
  count = 0
  supported_by, supports = get_support_graph(bricks)
  for brick in bricks:
    if not supports[brick.label]:
      count += 1
      continue
    for supported_brick in supports[brick.label]:
      if len(supported_by[supported_brick]) > 1:
        count += 1
        break
  return count

def part1(filename: str) -> int:
  bricks = [parse(line) for line in read_input(filename)]
  bricks.sort(key=lambda brick: brick.start.z)
  process_bricks(bricks) # modifies bricks in place 
  supported_by, supports = get_support_graph(bricks)
  return count_removeable_bricks(bricks) 

def part2(filename: str) -> int:
  print("Using input file:", filename)
  pass


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
