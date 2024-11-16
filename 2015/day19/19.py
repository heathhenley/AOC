from common.utils import problem_harness, timeit, read_input


def generate_strings(
    current: str, idx: int, subs: dict, strings: set):
  if idx == len(current):
    return
  # take the current character sub if possible
  if current[idx] in subs:
    for val in subs[current[idx]]:
      tmp = current[:]
      tmp = tmp[:idx] + val + tmp[idx+1:]
      strings.add(tmp)
      # recurse this is if we can make many replacements, we can only make
      # one though (at least in part 1 ...)
      #generate_strings(tmp, idx + len(val), subs)
  # try the same thing for two chars:
  substr = current[idx:idx+2]
  if substr in subs:
    for val in subs[substr]:
      tmp = current[:]
      tmp = tmp[:idx] + val + tmp[idx+2:]
      strings.add(tmp)
  # skip the current character
  generate_strings(current, idx + 1, subs, strings)


def parse_lines(lines: list[str]):
  subs = {}
  for line in lines:
    try:
      l, r = line.split(" => ")
      subs[l] = subs.get(l, []) + [r]
    except ValueError:
      start = line.strip()
  return start, subs


@timeit
def part1(filename: str) -> int:
  start, subs = parse_lines(read_input(filename))
  strings = set() 
  generate_strings(start, 0, subs, strings)
  return len(strings)


@timeit
def part2(filename: str) -> int:
  target, subs = parse_lines(read_input(filename))
  # starting with 'e', how many replacements do we need to make to get to the
  # target molecule?
  # swap subs around so we can go backwards - I tried to go forwards and it was
  # going to take until the next universe to finish (target has 488 chars, so
  # can't genterate them all starting from 'e')
  rev_subs = {}
  for k, v in subs.items():
    for val in v:
      rev_subs[val] = k
  # try replacing the first instance of a value in the target
  # molecule with the key that maps to it in rev_subs - 'greedy' approach
  # - I actually didn't think would work - I don't understand why it does, could
  #   we delete in different orders and get different results? Or will this
  #   always work to get the shortest path?
  count = 0
  while target != 'e':
    for k, v in rev_subs.items():
      if k in target:
        target = target.replace(k, v, 1)
        count += 1
        break
  return count


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()