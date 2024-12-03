import re
from common.utils import problem_harness, timeit, read_input


@timeit
def part1(filename: str) -> int:
  mult_ptn = re.compile(r"mul\((\d+),(\d+)\)")
  s = 0
  for line in read_input(filename):
    for g in mult_ptn.findall(line):
      x, y = int(g[0]), int(g[1])
      s += x * y
  return s


@timeit
def part2(filename: str) -> int:
  mult_ptn = re.compile(r"mul\((\d+),(\d+)\)")
  do_ptn = r"(do\(\))|(don't\(\))"

  # process as a single string (easier for idx's)
  line = "".join(read_input(filename)) 

  mults = []
  for m in mult_ptn.finditer(line):
    x, y = m.groups()
    mults.append((int(x), int(y), m.start(0)))

  controls = [(0, True)] # on by default
  for m in re.finditer(do_ptn, line):
    controls.append((m.start(0), m.group(0) == "do()"))
  controls.append((len(line), True)) # so we go to the end
  
  s = 0
  for i in range(len(controls) - 1):
    start, on = controls[i]
    end = controls[i+1][0]
    if on:
      s += sum(x * y for x, y, idx in mults if start <= idx < end)
  return s


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()