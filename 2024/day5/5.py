from functools import cmp_to_key
from common.utils import problem_harness, timeit, read_input


def parse_input(filename: str):
  orders = []
  updates = []
  for line in read_input(filename):
    if not line:
      continue
    if "|" in line:
      orders.append(line)
    else:
      updates.append(line)
  orders = [list(map(int, order.split("|"))) for order in orders] 
  updates = [list(map(int, update.split(","))) for update in updates]
  return orders, updates


def is_bad(update, orders):
  for lower, upper in orders:
    if lower in update and upper in update:
      idx_l = update.index(lower)
      idx_u = update.index(upper)
      if idx_l > idx_u:
        return True
  return False


def cmp(a, b, orders):
  for lower, upper in orders:
    if a == lower and b == upper:
      return -1 
    if a == upper and b == lower:
      return 1
  return 0


@timeit
def part1(filename: str) -> int:
  orders, updates = parse_input(filename)
  good_updates = [u for u in updates if not is_bad(u, orders)]
  return sum([l[len(l)//2] for l in good_updates])


@timeit
def part2(filename: str) -> int:
  orders, updates = parse_input(filename)
  bad_updates = [
    sorted(u, key=cmp_to_key(lambda a, b: cmp(a, b, orders)))
    for u in updates if is_bad(u, orders)
  ]
  return sum([l[len(l)//2] for l in bad_updates])


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
