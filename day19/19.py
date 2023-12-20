from copy import deepcopy
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

@dataclass
class State:
  x: tuple[int, int]
  m: tuple[int, int]
  a: tuple[int, int]
  s: tuple[int, int]
  wf_name: str

def part2(filename: str) -> int:
  workflows, _ = parse(read_input(filename))
  workflows = {w.name: w for w in workflows} # easier to lookup
  # plan is
  # - start with min / max values
  # - move through the workflow, apply rules - eg split
  #   in to new min / max's and pass to the next workflow
  # - repeat until we have processed all and we can see the
  #   final min / max values in accepted
  starting_wf_name = "in"
  min_val = 1
  max_val = 4000
  # state is this set of min max values
  # each time we split on a filter
  starting_state = State(
    x=(min_val, max_val),
    m=(min_val, max_val),
    a=(min_val, max_val),
    s=(min_val, max_val),
    wf_name=starting_wf_name
  )
  accepted = []
  state_queue = [starting_state]
  while state_queue:
    for _ in range(len(state_queue)):
      # get next unprocessed state
      s = state_queue.pop(0)
      # move this one through the workflows
      # apply rules and add new states to the queue if needed
      queue = [workflows[s.wf_name]]
      while queue:
        wf = queue.pop(0)
        for rule in wf.rules:
          # no condition, just move to next
          condition, dest_wf = rule
          print(s)
          print(wf)
          print(rule)
          print(s.wf_name)
          if condition is None:
            if dest_wf == "A":
              accepted.append(deepcopy(s))
              break
            if dest_wf == "R":
              break
            queue.append(workflows[dest_wf])
            s.dest_wf = dest_wf
            break

          # apply condition to number ranges
          k, op, v = condition
          if op == ">":
            # need to make new states for each split
            current_min, current_max = getattr(s, k)
            # the greater than part goes to the next workflow
            if current_min > int(v):
              if dest_wf == "A":
                accepted.append(deepcopy(s))
              elif dest_wf != "R":
                queue.append(workflows[dest_wf])
                s.wf_name = dest_wf
              continue
            if current_max <= int(v):
              # it's all unaffected by this rule, just move on
              continue
            # here's the interesting bit
            # we need to split the state into two, one to move on
            # and one part that is not affected
            # we can do this by creating a new state with the
            # min / max values that are not affected by this rule
            # and adding that to the state queue, but we have to adjust
            # the min / max values of the current state to reflect the update
            # from the rule
            # we must have min < v and max > v here
            # that part that is not affected is the min, v - 1
            not_affected = (current_min, int(v) - 1)
            # the part that is affected is v, max - move along and adjust
            affected = (int(v), current_max)
            setattr(s, k, affected)
            if dest_wf == "A":
              accepted.append(deepcopy(s))
            elif dest_wf != "R":
              queue.append(workflows[dest_wf])
              s.wf_name = dest_wf
            # add the not affected part to the queue, needs to be processed
            new_state = deepcopy(s)
            setattr(new_state, k, not_affected)
            state_queue.append(new_state)
            break # ned to stop applying rules to this state

          # same as above but for less than
          if op == "<":
            current_min, current_max = getattr(s, k)
            if current_max < int(v):
              # it's all affected by this rule push to next workflow
              if dest_wf == "A":
                accepted.append(deepcopy(s))
              elif dest_wf != "R":
                queue.append(workflows[dest_wf])
                s.wf_name = dest_wf
              continue
            if current_min >= int(v):
              # it's all unaffected by this rule, just move on
              continue
            # here's the interesting bit
            # this time the affected part is the min, v - 1
            # and the not affected part is v, max
            affected = (current_min, int(v) - 1)
            not_affected = (int(v), current_max)
            setattr(s, k, affected)
            if dest_wf == "A":
              accepted.append(deepcopy(s))
            elif dest_wf != "R":
              queue.append(workflows[dest_wf])
              s.wf_name = dest_wf
            # add the not affected part to the queue, needs to be processed
            new_state = deepcopy(s)
            setattr(new_state, k, not_affected)
            state_queue.append(new_state)
            break # ned to stop applying rules to this state
  seen = set()
  ans = 0
  for a in accepted:
    if (a.x, a.m, a.a, a.s) in seen:
      continue
    seen.add((a.x, a.m, a.a, a.s))
    print(a)
    ans += count_numbers(a)
  return ans

def count_numbers(s: State) -> int:
  prod = 1
  for k in ["x", "m", "a", "s"]:
    min_val, max_val = getattr(s, k)
    prod *= (max_val - min_val + 1)
  return prod

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
