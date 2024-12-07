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
    if is_solveable(target, args):
      ans += target
  return ans


@timeit
def part2(filename: str) -> int:
  ans = 0
  for line in read_input(filename):
    target, args = parse(line)
    if is_solveable(target, args, with_cat=True):
      ans += target
  return ans


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
