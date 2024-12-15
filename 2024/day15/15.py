from common.utils import problem_harness, timeit, read_input


def robot_at(grid: list[list[str]]) -> tuple[int, int]:
  for r in range(len(grid)):
    for c in range(len(grid[0])):
      if grid[r][c] == "@":
        return (r, c)
  raise ValueError("No robot found!")

def boxes_at(grid: list[list[str]]) -> list[tuple[int, int]]:
  boxes = []
  for r in range(len(grid)):
    for c in range(len(grid[0])):
      if grid[r][c] == "O":
        boxes.append((r, c))
  return boxes

def walls_at(grid: list[list[str]]) -> list[tuple[int, int]]:
  walls = []
  for r in range(len(grid)):
    for c in range(len(grid[0])):
      if grid[r][c] == "#":
        walls.append((r, c))
  return walls

move_map = {
  ">": (0, 1),
  "<": (0, -1),
  "^": (-1, 0),
  "v": (1, 0)
}

def valid(grid: list[list[str]], r: int, c: int) -> bool:
  return (r >= 0 and r < len(grid)
          and c >= 0 and c < len(grid[0]) and grid[r][c] != "#")


def simulate(grid: list[list[str]], moves: list[str]) -> list[list[str]]:
  rr, rc = robot_at(grid)
  print("Robot at", rr, rc)
  while moves:
    m = moves.pop(0)
    dir = move_map[m]
    #print("try to move: " , dir, m, rr, rc)
    # check if we can move - how many open space '.' are there in this dir?
    move_ok = False
    space = None
    r, c = rr, rc
    while valid(grid, r, c):
      r += dir[0]
      c += dir[1]
      if grid[r][c] == ".":
        move_ok = True
        space = (r, c)
        break
    if not move_ok: # easy we can't move
    # print("Can't move")
      continue
    # there's an open space, move the robot
    # next space in the direction we care about is at 'space'
    # robot space is now empty
    grid[rr][rc] = "."
    r, c = rr + dir[0], rc + dir[1]
    # move everything over one space in the direction we care about
    # start at 'space' and move everything over one space
    while (r, c) != space:
      grid[r + dir[0]][c + dir[1]] = grid[r][c]
      r, c = r + dir[0], c + dir[1]

    rr, rc = rr + dir[0], rc + dir[1]
    # robot is now at space
    grid[rr][rc] = "@"


    #for g in grid:
    #  print("".join(g))

  return grid


def gps(box: tuple[int, int]) -> int:
  return 100 * box[0] + box[1]


def part1(filename: str) -> int:
  grid = []
  moves = []
  for line in read_input(filename):
    if "#" in line or "." in line:
      grid.append(list(line))
    elif line:
      moves.extend(list(line))
  for g in grid:
    print("".join(g))
  #print(moves)

  grid = simulate(grid, moves)

  return sum([gps(box) for box in boxes_at(grid)])


@timeit
def part2(filename: str) -> int:
  return 0


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
