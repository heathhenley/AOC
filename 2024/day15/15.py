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
      if grid[r][c] == "O" or grid[r][c] == "[":
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
  """ Part 1 - simpler rules (boxes only push their direct neighbors)"""

  def try_push(
      box: tuple[int, int], dir: tuple[int, int]) -> bool:
    next_space = (box[0] + dir[0], box[1] + dir[1])
    if not valid(grid, next_space[0], next_space[1]):
      return False
    if grid[next_space[0]][next_space[1]] == "#":
      return False
    # the next space is open or a box
    # it's open just move the box and return True
    if grid[next_space[0]][next_space[1]] == ".":
      grid[next_space[0]][next_space[1]] = grid[box[0]][box[1]]
      grid[box[0]][box[1]] = "."
      return True
    # the next space is a box, try to push it - if we do, move the box and return
    # true
    if try_push(next_space, dir):
      grid[next_space[0]][next_space[1]] = grid[box[0]][box[1]]
      grid[box[0]][box[1]] = "."
      return True
    return False

  rr, rc = robot_at(grid)
  for move in moves:
    if try_push((rr, rc), move_map[move]):
      rr, rc = rr + move_map[move][0], rc + move_map[move][1]
    #for g in grid:
    #  print("".join(g))
    #print()
  return grid

def simulate_2(grid: list[list[str]], moves: list[str]) -> list[list[str]]:
  def can_move(box: tuple[int, int], dir: tuple[int, int]) -> bool:
    """ Similar to before - but without actually switching - this is to check
    if a box can be moved in a certain direction """
    next_space = (box[0] + dir[0], box[1] + dir[1])
    if not valid(grid, next_space[0], next_space[1]):
      return False
    if grid[next_space[0]][next_space[1]] == "#":
      return False
    if grid[next_space[0]][next_space[1]] == ".":
      return True
    if grid[next_space[0]][next_space[1]] == "[":
      return can_move(next_space, dir) and can_move((next_space[0], next_space[1] + 1), dir)
    if grid[next_space[0]][next_space[1]] == "]":
      return can_move(next_space, dir) and can_move((next_space[0], next_space[1] - 1), dir)
    return False

  def try_push(
      box: tuple[int, int], dir: tuple[int, int]) -> bool:
    next_space = (box[0] + dir[0], box[1] + dir[1])
    if not valid(grid, next_space[0], next_space[1]):
      return False
  
    curr_val = grid[box[0]][box[1]]
    next_val = grid[next_space[0]][next_space[1]]
    match next_val:
      case "#":
        return False
      case ".":
        grid[next_space[0]][next_space[1]] = curr_val
        grid[box[0]][box[1]] = "."
        return True
      case "[":
        if dir[0] == 0: # left / right is straight forward
          if try_push(next_space, dir):
            grid[next_space[0]][next_space[1]] = curr_val
            grid[box[0]][box[1]] = "."
            return True
          return False

        # up / down is a bit more complicated
        other_half = (next_space[0], next_space[1] + 1)
        if not can_move(other_half, dir) or not can_move(next_space, dir):
          return False
        
        if try_push(next_space, dir) and try_push(other_half, dir):
          grid[next_space[0]][next_space[1]] = curr_val
          grid[box[0]][box[1]] = "."
          return True
        return False
      case "]":
        if dir[0] == 0: # left / right is straight forward
          if try_push(next_space, dir):
            grid[next_space[0]][next_space[1]] = curr_val
            grid[box[0]][box[1]] = "."
            return True
          return False

        other_half = (next_space[0], next_space[1] - 1)
        # up / down is a bit more complicated
        if not can_move(other_half, dir) or not can_move(next_space, dir):
          return False
        if try_push(next_space, dir) and try_push(other_half, dir):
          grid[next_space[0]][next_space[1]] = curr_val
          grid[box[0]][box[1]] = "."
          return True
        return False
      case _ :
        raise ValueError(f"Unexpected value {next_val}")


  rr, rc = robot_at(grid)
  for move in moves:


    if try_push((rr, rc), move_map[move]):
      rr, rc = rr + move_map[move][0], rc + move_map[move][1]

    for r in range(len(grid)):
      for c in range(len(grid[0])):
        match grid[r][c]:
          case "[":
            if grid[r][c + 1] != "]":
              print(f"Unmatched box at {r}, {c}")
              for g in grid:
                print("".join(g))
              print()
              raise ValueError(f"Unmatched box at {r}, {c}")
          case "]":
            if grid[r][c - 1] != "[":
              print(f"Unmatched box at {r}, {c}")
              for g in grid:
                print("".join(g))
              print()
              raise ValueError(f"Unmatched box at {r}, {c}")
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


def expand_grid(og_grid):
  grid_expanded = []
  for og_row in og_grid:
    expanded_row = []
    for val in og_row:
      match val:
        case "O":
          expanded_row.extend(["[", "]"])
        case "@":
          expanded_row.extend(["@", "."])
        case "#":
          expanded_row.extend(["#", "#"])
        case ".":
          expanded_row.extend([".", "."])
        case _:
          raise ValueError(f"Unexpected value {val}")
    grid_expanded.append(expanded_row)
  return grid_expanded
  


@timeit
def part2(filename: str) -> int:
  # part 2 seems like a beast, and definitely seems better suited for recursion
  # bascially try_push((r, c), dir) -> bool - it calls it self recursively on
  # the spaces that matter in the direction we care about until it can or can't
  # move
  # rewrote part 1 to be recursive - definitely cleaner should have done that in
  # the first place - ideally, part 2 is the same, except that we neeed to call
  # the recursive function with more than one 'neighbor' depending on the spots
  # the box touches
  grid = []
  moves = []
  for line in read_input(filename):
    if "#" in line or "." in line:
      grid.append(list(line))
    elif line:
      moves.extend(list(line))

  grid_expanded = expand_grid(grid)
  #grid_expanded = [
  #  list("##########"),
  #  list("####.....##"),
  #  list("##[]....##"),
  #  list("##.[]...##"),
  #  list("##..@..####"),
  #  list("##########"),
  #]
  #moves = ["^", "^"]
  #for g in grid_expanded:
  #  print("".join(g))

  grid_expanded = simulate_2(grid_expanded, moves)

  for g in grid_expanded:
    print("".join(g))

  return sum([gps(box) for box in boxes_at(grid_expanded)])


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
