from typing import Tuple, List
from common.utils import problem_harness, timeit, read_input


def directon_to_delta(direction: str) -> tuple[int, int]:
  match direction:
    case 'U':
      return 0, -1
    case 'D':
      return 0, 1
    case 'L':
      return -1, 0
    case 'R':
      return 1, 0
    case _:
      raise ValueError(f'Invalid direction {direction}')

def move_rec(
    current_spot: Tuple[int, int],
    direction: str,
    keypad: List[List[int]]) -> Tuple[int, int]:
  match len(direction):
    case 0:
      return current_spot
    case _:
      dx, dy = directon_to_delta(direction[0])
      x, y = current_spot
      new_x = max(0, min(len(keypad)-1, x + dx))
      new_y = max(0, min(len(keypad)-1, y + dy))
      if keypad[new_y][new_x] != 0:
        x = new_x
        y = new_y
      return move_rec((x, y), direction[1:], keypad)
  return x, y

def get_code_rec(
    lines: List[str],
    keypad: List[List[int]],
    spot: Tuple[int, int],
    code: str) -> List[str]:

  if not lines:
    return code
  
  line = lines.pop(0)

  match line:
    case "":
      return get_code_rec(lines, keypad, spot, code)
    case _:
      new_spot = move_rec(spot, line, keypad)
      new_code = code + str(keypad[new_spot[1]][new_spot[0]])
      return get_code_rec(lines, keypad, new_spot, new_code)

@timeit
def part1(filename: str) -> int:
  keypad = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
  ]
  lines = read_input(filename)
  return get_code_rec(lines, keypad, (1, 1), "")

@timeit
def part2(filename: str) -> int:
  keypad = [
    [0, 0, 1, 0, 0],
    [0, 2, 3, 4, 0],
    [5, 6, 7, 8, 9],
    [0, 'A', 'B', 'C', 0],
    [0, 0, 'D', 0, 0]
  ]
  lines = read_input(filename)
  return get_code_rec(lines, keypad, (0, 2), "")


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()