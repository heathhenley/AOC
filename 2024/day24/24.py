from itertools import combinations
import matplotlib.pyplot as plt
import networkx as nx
from common.utils import problem_harness, timeit, read_input


ops = {
  "AND": lambda a, b: a & b,
  "XOR": lambda a, b: a ^ b,
  "OR": lambda a, b: a | b,
}

def parse(lines):
  exprs = {}
  for line in lines:
    if ":" in line:
      var, val = line.split(": ")
      exprs[var] = int(val)
    if "->" in line:
      gate, out = line.split(" -> ")
      a, op, b = gate.split(" ") 
      exprs[out] = (a, op, b)
  return exprs

# evaluate recursively - if both a and b are ints, do the op and put it in val
# if a or b is a string, we need to look up that value in teh op
def solve(exprs, out):
  if isinstance(exprs[out], int):
    return exprs[out]
  a, op, b = exprs[out]
  if isinstance(a, str):
    a = solve(exprs, a)
  if isinstance(b, str):
    b = solve(exprs, b)
  exprs[out] = ops[op](a, b)
  return exprs[out]


def get_decimal(exprs, prefix):
  zs = {out: exprs[out] for out in exprs.keys() if out.startswith(prefix)}
  zs = sorted(zs.items(), key=lambda x: x[0], reverse=True)
  num = "".join([str(v) for _, v in zs])
  return int(num, 2)


def get_z(exprs):
  for out in exprs.keys():
    if not out.startswith("z"):
      continue
    solve(exprs, out)
  return get_decimal(exprs, "z")

@timeit
def part1(filename: str) -> int:
  exprs = parse(read_input(filename))
  return get_z(exprs)

@timeit
def part2(filename: str) -> int:
  exprs = parse(read_input(filename))

  # turns out we're trying to add the values in x and z together
  # to end up with the value in z
  x = get_decimal(exprs, "x")
  y = get_decimal(exprs, "y")
  z = get_z(exprs.copy())

  print(f"{x} + {y} = {x + y} but we have: {z}")
  # which bits are correct?
  # left pad the binary strings to make them the same length
  print(f"{z:048b}")
  print(f"{x + y:048b}")
  # find the bits that are already correct
  correct = z & (x + y) | (~z & ~(x + y)) & 0xFFFFFFFFFFFF
  incorrect = ~correct & 0xFFFFFFFFFFFF
  # count incorrect bits
  print(bin(incorrect).count('1'))

  # swap - manually inspecting each adder where the output to z is not an XOR
  exprs["z05"], exprs["frn"] = exprs["frn"], exprs["z05"]
  exprs["z21"], exprs["gmq"] = exprs["gmq"], exprs["z21"]
  exprs["z39"], exprs["wtt"] = exprs["wtt"], exprs["z39"]
  exprs["wnf"], exprs["vtj"] = exprs["vtj"], exprs["wnf"]
  z = get_z(exprs.copy())
  print(f"{z:048b}")
  print(f"{x + y:048b}")
  # find the bits that are already correct
  correct = z & (x + y) | (~z & ~(x + y)) & 0xFFFFFFFFFFFF
  incorrect = ~correct & 0xFFFFFFFFFFFF
  # count incorrect bits
  print(bin(incorrect).count('1'))
  # find which bits are incorrect
  for i in range(48):
    if incorrect & (1 << i):
      print("bit", i, "is incorrect")
  # all the assignments to Z should be XORs (they're all output from full
  # adders)
  sus_gates = []
  for out in exprs.keys():
    if not out.startswith("z"):
      continue
    a, op, b = exprs[out]
    if op != "XOR":
      sus_gates.append(out)
  sus_gates.sort()
  print(sus_gates[:-1]) # z45 is the last carry so it should be an or (it is)

  swapped = ["z05", "z21", "z39", "wnf", "frn", "gmq", "wtt", "vtj"]
  return ",".join(sorted(swapped))


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
