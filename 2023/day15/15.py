import collections
from functools import cache
from common.utils import read_input
import re
import sys

@cache
def hash(image: str) -> int:
  h = 0
  for c in image:
    h += ord(c)
    h *= 17
    h %= 256
  return h 

def parse(seq: str) -> tuple:
  pattern = r"(?P<label>\w+)(?P<op>[=\-]{1})(?P<lens>[0-9]{0,1})"
  m = re.match(pattern, seq)
  return m.group("label"), m.group("op"), m.group("lens")

def get_focus_power(box_map: list) -> int:
  pwr = 0
  for idx, box in enumerate(box_map):
    slot = 1
    for label, lens in box.items():
      if lens == -1:
        continue
      pwr += (1 + idx) * slot * lens
      slot += 1
  return pwr

def part1(filename: str) -> int:
  sequence = read_input(filename, sep=",")[0]
  return sum([hash(seq) for seq in sequence])

def part2(filename: str) -> int:
  sequence = read_input(filename, sep=",")[0]
  box_map = [{} for _ in range(256)]
  for seq in sequence:
    label, op, lens = parse(seq)
    box_idx = hash(label)
    if op == "=":
      if label in box_map[box_idx]:
        box_map[box_idx][label] = int(lens)
      else:
        box_map[box_idx].update({label: int(lens)})
    elif op == "-":
      # delete the label in this box
      if label in box_map[box_idx]:
        del box_map[box_idx][label]
  return get_focus_power(box_map)


def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")
  input_file = sys.argv[1]

  print("Part 1:", part1(input_file))
  print("Part 2:", part2(input_file))


if __name__ == '__main__':
  main()
