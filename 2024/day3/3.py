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

  # this was the source of my hour of suffering - put the whole file on a line
  # so the indexes are good to go and we don't restart the switches every line (
  # eg it's only 'enabled' on the very start of the 'program', NOT the start of 
  # every line)
  line = "".join(read_input(filename)) 

  mults = []
  controls = [(0, True)] # start with do()
  s = 0
  for m in mult_ptn.finditer(line):
    idx = m.start(0)
    x, y = m.groups()
    x, y = int(x), int(y)
    mults.append((x, y, idx))

  do = r"(do\(\))"
  dont = r"(don't\(\))"
  for m in re.finditer(do, line):
    controls.append((m.start(0), True))
  for m in re.finditer(dont, line):
    controls.append((m.start(0), False))

  mults.sort(key=lambda x: x[2])
  controls.sort(key=lambda x: x[0])
  controls.append((len(line), True))
  
  # we want to take the first control off, and apply
  # it to all the mults that come after it, but before the next control
  for i in range(len(controls) - 1):
    start, on = controls[i]
    end = controls[i+1][0]
    for x, y, idx in mults:
      if start <= idx < end and on:
        s += x * y
  return s


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()