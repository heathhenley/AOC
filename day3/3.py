import sys


def read_input(filename: str, sep: str | None = None):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
    if sep is None:
      return  lines
    return [[val.strip() for val in line.split(sep)] for line in lines]


def is_symbol(s: str) -> bool:
  return s not in ["."] and not any([x in "01234456789" for x in s])


def adjacent_symbol(
    engine_schematic: list[list[str]], i: int, j: int) -> bool:
    for x in range(i-1, i+2):
      for y in range(j-1, j+2):
        if x == i and y == j:
          continue
        if x < 0 or y < 0:
          continue
        if x >= len(engine_schematic) or y >= len(engine_schematic[i]):
          continue
        if is_symbol(engine_schematic[x][y]):
          return True
    return False


def contains_symbol(s):
  return any([is_symbol(x) for x in s])


def find_numbers(
    engine_schematic: list[list[str]]) -> list[tuple[int, int, str]]:
  numbers = []
  digits = []
  for r, row in enumerate(engine_schematic):
    if digits:
      # this is kind of a hack for a weird edge case
      # computing the start col position when it ends the
      # row and the number starts with a symbol
      start_number = c - len(digits)
      if is_symbol(engine_schematic[r][start_number]):
        start_number += 1
      numbers.append((r-1, c-len(digits)+1, "".join(digits)))
      digits = []
    for c, col in enumerate(row):
      if col != "." and not is_symbol(col):
        digits.append(col)
      else:
        if digits:
          numbers.append((r, c-len(digits), "".join(digits)))
          digits = []
  if digits:
    numbers.append((r, c-len(digits), "".join(digits)))
  return numbers


def find_possible_gears(
    engine_schematic: list[list[str]]) -> list[tuple[int, int]]:
  gears = []
  for r, row in enumerate(engine_schematic):
    for c, col in enumerate(row):
      if col == "*":
        gears.append((r, c))
  return gears


def get_adjacent_numbers(
    numbers: list[tuple[int, int, str]], i: int, j: int):
  adjacent_numbers = []
  for row, col, number in numbers:
    if row == i and col == j:
      continue
    for k in range(len(number)):
      if abs(row - i) <= 1 and abs(col + k  - j) <= 1:
        adjacent_numbers.append(number)
        break
  return adjacent_numbers


def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python 3.py <input_file>")

  input_filename = sys.argv[1]
  print("Using input file", input_filename)

  engine_schematic = read_input(input_filename)

  # Part 1 - Find sum of all valid numbers
  ans = []
  for row, col, number in find_numbers(engine_schematic):
    for d_idx, d in enumerate(number):
      if adjacent_symbol(engine_schematic, row, col + d_idx):
        ans.append(int(number))
        break
  print("Part 1", sum(ans))

  # Part 2 - Find sum of all "gear ratios"
  sum_gear_ratios = 0
  numbers = find_numbers(engine_schematic)
  for row, col in find_possible_gears(engine_schematic):
    adjacent_numbers = get_adjacent_numbers(numbers, row, col)
    if len(adjacent_numbers) == 2:
      sum_gear_ratios += int(adjacent_numbers[0]) * int(adjacent_numbers[1])
  print("Part 2", sum_gear_ratios) 




if __name__ == '__main__':
  main()
