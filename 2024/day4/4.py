from common.utils import problem_harness, timeit, read_input


dirs_part1 = [
  # sides
  [(0, 0-i) for i in range(4)],
  [(0, 0+i) for i in range(4)],
  # up down
  [(0-i, 0) for i in range(4)],
  [(0+i, 0) for i in range(4)],
  # diagonals
  [(0-i, 0-i) for i in range(4)],
  [(0-i, 0+i) for i in range(4)],
  [(0+i, 0-i) for i in range(4)],
  [(0+i, 0+i) for i in range(4)]
]


dirs_part2 = [
  [(1, 1), (0, 0), (-1, -1)],
  [(1, -1), (0, 0), (-1, 1)],
]


def dir_to_word(grid, row, col, d):
  """ get the word at row, col by applying the dr, dc offsets in d """
  word = ""
  for dr, dc in d:
    r = row + dr
    c = col + dc
    if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
      return None
    word += grid[r][c]
  return word


@timeit
def part1(filename: str) -> int:
  lines = read_input(filename)
  grid = [list(l) for l in lines]
  # the word needs to start on x - so we can check each possible
  # direction when we reach an X and increment the count
  count = 0
  for row in range(len(grid)):
    for col in range(len(grid[0])):
      if grid[row][col] != "X":
        continue
      count += sum(
        [dir_to_word(grid, row, col, d) == "XMAS" for d in dirs_part1]
      )
  return count


@timeit
def part2(filename: str) -> int:
  lines = read_input(filename)
  grid = [list(l) for l in lines]
  # start on A this time - the middle needs to be an A and we need two
  # MASs diagonally crossing
  count = 0
  for row in range(len(grid)):
    for col in range(len(grid[0])):
      if grid[row][col] != "A":
        continue
      for d in dirs_part2:
        word = dir_to_word(grid, row, col, d)
        if word != "MAS" and word != "SAM":
          break
      else:
        count += 1
  return count


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
