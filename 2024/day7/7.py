import numpy as np
from common.utils import problem_harness, timeit, read_input


def cat(a, b):
  return int(str(a) + str(b))


def is_solveable(target, args, with_cat=False):
  def solve(curr, idx):
    if idx == len(args):
      return curr == target
    return (
      curr <= target and (
        solve(curr + args[idx], idx + 1)
        or solve(curr * args[idx], idx + 1)
        or (with_cat and solve(cat(curr, args[idx]), idx + 1))
      )
    )
  return solve(args[0], 1)


def is_solveable_optimized(target, args, with_cat=False):
  """ Optimized version of is_solveable - based on solution from reddit

  Goes backwards from the target to the first number in the list, culling
  possible solutions before pushing them to the stack.
  """
  stack = [[target, len(args)-1]]
  while stack:
    target, next_idx = stack.pop()
    if next_idx == 0 and target == args[0]:
      return True
    if next_idx == 0:
      continue
    if target - args[next_idx] >= args[0]:
      stack.append([target - args[next_idx], next_idx - 1])
    if target % args[next_idx] == 0:
      stack.append([target // args[next_idx], next_idx - 1])
    if with_cat:
      if str(target).endswith(str(args[next_idx])):
        d = int(np.log10(args[next_idx])) + 1
        stack.append([target // (10 ** d), next_idx - 1])
  return False


def parse(line):
  target, args = line.split(':')
  target = int(target)
  args = list(map(int, args.strip().split(' ')))
  return target, args


@timeit
def part1(filename: str) -> int:
  ans = 0
  for line in read_input(filename):
    target, args = parse(line)
    if is_solveable_optimized(target, args):
      ans += target
  return ans


@timeit
def part2(filename: str) -> int:
  ans = 0
  for line in read_input(filename):
    target, args = parse(line)
    if is_solveable_optimized(target, args, with_cat=True):
      ans += target
  return ans


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
