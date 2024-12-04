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

@timeit
def part1(filename: str) -> int:
  lines = read_input(filename)
  # read into 2d array
  grid = [list(l) for l in lines]

  # the word needs to start on x - so we can check each possible
  # direction when we reach an X and increment the count
  count = 0
  for row in range(len(grid)):
    for col in range(len(grid[0])):
      if grid[row][col] != "X":
        continue
      for d in dirs_part1:
        word = ""
        for dr, dc in d:
          r = row + dr
          c = col + dc
          if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
            break
          word += grid[r][c]
        if word == "XMAS" or word == "SAMX":
          count += 1
  return count


@timeit
def part2(filename: str) -> int:
  lines = read_input(filename)
  # read into 2d array
  grid = [list(l) for l in lines]

  # start on A this time - the middle needs to be an A and we need two
  # MAS's diagonally crossing
  count = 0
  for row in range(len(grid)):
    for col in range(len(grid[0])):
      if grid[row][col] != "A":
        continue
      # word one is up left and down right neighbors
      check = 0
      for d in dirs_part2:
        word = ""
        for dr, dc in d:
          r = row + dr
          c = col + dc
          if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
            break
          word += grid[r][c]
        if word == "MAS" or word == "SAM":
          check += 1
      if check == 2:
        count += 1
  return count


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
