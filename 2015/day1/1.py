import sys
import time
from common.utils import read_input

def part1(filename: str) -> int:
  print("Using input file:", filename)
  d = {}
  for char in read_input(filename)[0]:
    d[char] = d.get(char, 0) + 1
  return d.get("(", 0) - d.get(")", 0)

def part2(filename: str) -> int:
  print("Using input file:", filename)
  dir_map = {"(": 1, ")": -1}
  floor = 0
  for idx, char in enumerate(read_input(filename)[0]):
    floor += dir_map[char]
    if floor == -1:
      return idx + 1
  assert False, "Should not reach here if there's a solution" 
    


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
