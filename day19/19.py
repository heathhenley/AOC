from dataclasses import dataclass
import sys
import time
import re
from common.utils import read_input


@dataclass
class Part:
  x: int = -1
  m: int = -1
  a: int = -1
  s: int = -1

@dataclass
class Workflow:
  name: str
  rules: list[str]

def parse_part_info(part: str) -> Part: 
  p = Part()
  for x in part[1:-1].split(","):
    k, v = x.split("=")
    setattr(p, k, int(v))
  return p

def parse_workflow(workflow: str) -> Workflow:
  name, rest = workflow.split("{")
  rest = rest[:-1]
  rules = [parse_rule(r) for r in rest.split(",")]
  return Workflow(name, rules)

def parse_rule(rule: str):
  r = rule.split(":")
  condition = None
  result = r[-1]
  if len(r) == 2:
    if m := re.match(r"([xmsa]{1})([><]{1})(\d+)", r[0]):
      condition = m.groups()
  return condition, result

def parse(lines: list[str]) -> tuple[dict[str, list[str]], dict[str, str]]:
  workflows = []
  parts = []
  parts_start = lines.index('')
  workflows = [parse_workflow(x) for x in lines[:parts_start]]
  parts = [parse_part_info(x) for x in lines[parts_start + 1:]]
  return workflows, parts

def process_parts(
    parts: list[Part], workflows: dict[str, Workflow]) -> list[Part]:
  starting_wf_name = "in"
  accepted = []
  for part in parts:
    queue = [workflows[starting_wf_name]]
    # apply all rules to part from relevant workflows
    while queue:
      wf = queue.pop(0)
      for rule in wf.rules:
        condition, dest_wf = rule
        if condition is None:
          if dest_wf == "A":
            accepted.append(part)
            break
          if dest_wf == "R":
            break
          # no condition, just apply
          queue.append(workflows[dest_wf])
          break
        k, op, v = condition
        # apply condition to part
        part_value = getattr(part, k)
        if op == ">":
          if part_value > int(v):
            if dest_wf == "A":
              accepted.append(part)
              break
            if dest_wf == "R":
              break
            queue.append(workflows[dest_wf])
            break
        if op == "<":
          if part_value < int(v):
            if dest_wf == "A":
              accepted.append(part)
              break
            if dest_wf == "R":
              break
            queue.append(workflows[dest_wf])
            break
  return accepted
 

def part1(filename: str) -> int:
  workflows, parts = parse(read_input(filename))
  workflows = {w.name: w for w in workflows} # easier to lookup
  accepted = process_parts(parts, workflows)
  ans = 0
  for p in accepted:
    ans += p.x + p.m + p.a + p.s
  return ans


def part2(filename: str) -> int:
  print("Using input file:", filename)
  pass


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
