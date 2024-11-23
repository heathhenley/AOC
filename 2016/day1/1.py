from common.utils import problem_harness, timeit, read_input


@timeit
def part1(filename: str) -> int:
  return 0


def apply_turn(current: str, turn: str) -> str:
  if current == "N":
    return "W" if turn == "L" else "E"
  if current == "S":
    return "E" if turn == "L" else "W"
  if current == "E":
    return "N" if turn == "L" else "S"
  if current == "W":
    return "S" if turn == "L" else "N"

def direction_to_vector(d: str) -> tuple:
  if d == "N":
    return 0, 1
  if d == "S":
    return 0, -1
  if d == "E":
    return 1, 0
  if d == "W":
    return -1, 0

def parse(s: str) -> tuple:
  return s[0], int(s[1:])

@timeit
def part2(filename: str) -> int:
  inst = [parse(l) for l in read_input(filename)[0].split(", ")]
  x, y, d = 0, 0, "N"
  visited = set()
  while inst:
    turn, move = inst.pop(0)
    d = apply_turn(d, turn)
    dx, dy = direction_to_vector(d)
    for _ in range(move):
      x += dx
      y += dy
      if (x, y) in visited:
        return abs(x) + abs(y)
      visited.add((x, y))
  return None



def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()