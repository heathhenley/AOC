import math
import sys
import time
from common.utils import read_input

class Module:
  def __init__(self, label: str):
    self.label = label
    # the last input from each connected module
    self.inputs = {}
    # connected modules
    self.outputs = []

  def get_response(self, inp_label: str, sig: int) -> int | None:
    return sig

  def __repr__(self):
    return f"<{self.__class__.__name__} {self.label}>"

  def add_input(self, inp_label: str):
    self.inputs[inp_label] = 0

  def add_output(self, out_label: str):
    self.outputs.append(out_label)

class FlipFlop(Module):
  def __init__(self, label: str):
    super().__init__(label)
    self.on: bool = False

  def get_response(self, inp_label: str, sig: int) -> int | None:
    # high signal does nothing
    if sig == 1:
      return None
    # low signal toggles
    out = not self.on
    self.on = out
    return int(out)

class Conjunction(Module):

  def get_response(self, inp_label: str, sig: int) -> int | None:
    # update the state
    self.inputs[inp_label] = sig

    # if any input is low, output is high
    if 0 in self.inputs.values():
      return 1
    return 0


def get_mod(src: str) -> Module:
  if src == "broadcaster":
    return Module(src)
  if src == "output":
    return Module(src)
  if src[0] == "%":
    return FlipFlop(src[1:])
  return Conjunction(src[1:])

def parse_signal(line: str) -> int:
  src, dst = line.split(" -> ")
  return get_mod(src), dst.split(", ")

def push_button(
    mod_map: dict,
    start: str="broadcaster") -> int:
  count_signals, count_high = 1, 0
  start_mod = mod_map[start]
  # get the first signal
  signal = start_mod.get_response("start", 0)
  # who does it go to?
  recvs = start_mod.outputs
  signal_queue = [(signal, start_mod.label, recv) for recv in recvs]
  while signal_queue:
    sig, src, recv = signal_queue.pop(0)
    # get the module
    mod = mod_map[recv]
    # get the response
    resp = mod.get_response(src, sig)
    # if there is a response, send it to the outputs
    if resp is not None:
      signal_queue.extend([(resp, mod.label, out) for out in mod.outputs])
    count_signals += 1
    count_high += sig
  return count_signals - count_high, count_high

def push_button_pt2(
    mod_map: dict,
    rx_parent_tracking: dict,
    btn_idx: int=0,
    start: str="broadcaster",
    ref: str = 'rx') -> int:
  """ Copy of part 1 approach but returns True if ref has only 1 low signal"""
  start_mod = mod_map[start]
  signal = start_mod.get_response("start", 0)
  recvs = start_mod.outputs
  signal_queue = [(signal, start_mod.label, recv) for recv in recvs]
  while signal_queue:
    sig, src, recv = signal_queue.pop(0)

    # track the parent of rx when rx gets a signal
    if recv == ref:
      for parent, s in mod_map[src].inputs.items():
        if parent not in rx_parent_tracking and s == 1:
          rx_parent_tracking[parent] = btn_idx

    # get the module
    mod = mod_map[recv]
    # get the response
    resp = mod.get_response(src, sig)
    # if there is a response, send it to the outputs
    if resp is not None:
      signal_queue.extend([(resp, mod.label, out) for out in mod.outputs])
  return list(mod_map[ref].inputs.values()).count(0) == 1

def add_connections(signals: list, module_map: dict) -> list:
  for mod, dsts in signals:
    for dst in dsts:
      if dst not in module_map:
        module_map[dst] = get_mod(dst)
      module_map[dst].add_input(mod.label)
      module_map[mod.label].add_output(dst)
  return signals, module_map

def part1(filename: str) -> int:
  lines = read_input(filename)
  signals = [parse_signal(line) for line in lines]
  module_map = { mod.label: mod for mod, _ in signals}
  signals, module_map = add_connections(signals, module_map)
  low, high = 0, 0
  for _ in range(1000):
    lo, hi = push_button(module_map)
    low += lo
    high += hi
  return low * high

def part2(filename: str) -> int:
  lines = read_input(filename)
  signals = [parse_signal(line) for line in lines]
  module_map = { mod.label: mod for mod, _ in signals}
  signals, module_map = add_connections(signals, module_map)
  buttons = 1
  rx_parent_tracking = {}
  while not push_button_pt2(module_map, rx_parent_tracking, buttons, ref='rx'):
    # qt is the only module that sends a signal to rx, so we're looking for
    # qt's parents to cycle
    rx_parents = len(module_map['qt'].inputs)
    if len(rx_parent_tracking) == rx_parents:
      break
    buttons += 1
  return math.lcm(*rx_parent_tracking.values())

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
