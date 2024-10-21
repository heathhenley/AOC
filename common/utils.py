from collections.abc import Callable
import sys
import time


def timeit(func):
  def wrapper(*args, **kwargs):
    tic = time.perf_counter()
    result = func(*args, **kwargs)
    toc = time.perf_counter()
    print(f"  {func.__name__} took {toc - tic:0.4f} seconds")
    return result
  return wrapper


def read_input(filename: str, sep: str | None = None):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
    if sep is None:
      return  lines
    return [[val.strip() for val in line.split(sep)] for line in lines]
  

def problem_harness(
    part1: Callable[[str], int] = None,
    part2: Callable[[str], int] = None):

  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")

  input_file = sys.argv[1]

  if part1:
    print(f"Part 1: {part1(input_file)}")
  if part2:
    print(f"Part 2: {part2(input_file)}")