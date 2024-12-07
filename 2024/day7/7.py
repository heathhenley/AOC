from common.utils import problem_harness, timeit, read_input

ops = {
    '0': lambda x, y: x * y,
    '1': lambda x, y: x + y,
    '2': lambda x, y: int(str(x) + str(y))
}

@timeit
def part1(filename: str) -> int:
  # we can put either a + or * operator between each pair of numbers
  # - try and see which ones end up with the target number?
  count = 0 
  for _, line in enumerate(read_input(filename)):
    target, args = line.split(':')
    target = int(target)
    args = list(map(int, args.strip().split(' ')))
    # there are n-1 spots to put operators
    # they can be either + or * - 2^(n-1) spots
    # we can use a binary number to loop through all the possibilities
    # 0 means +, 1 means *
    n = len(args) - 1
    for i in range(2 ** n):
      # to binary
      i = f"{i:0{n}b}"
      total = args[0]
      for j, b in enumerate(i):
        total = ops[b](total, args[j + 1])
      if total == target:
        count += target
        break
  return count


def to_base_3(n):
  if n == 0:
    return '0'
  res = ''
  while n > 0:
    res = str(n % 3) + res
    n //= 3
  return res


@timeit
def part2(filename: str) -> int:
  count = 0 
  for line in read_input(filename):
    target, args = line.split(':')
    target = int(target)
    args = list(map(int, args.strip().split(' ')))
    n = len(args) - 1
    for i in range(3 ** n):
      i = to_base_3(i)
      i = f"{i:0>{n}}"
      total = args[0]
      for j, b in enumerate(i):
        total = ops[b](total, args[j + 1])
      if total == target:
        count += target
        break
  return count


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
