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


@timeit
def part1(filename: str) -> int:
  orders, updates = parse_input(filename)
  good_updates = [u for u in updates if not is_bad(u, orders)]
  return sum([l[len(l)//2] for l in good_updates])

@timeit
def part2(filename: str) -> int:
  orders, updates = parse_input(filename)
  bad_updates = [u for u in updates if is_bad(u, orders)]
  # fix the bad updates by continuously swapping the bad elements
  updates = [] 
  while bad_updates:
    bad_update = bad_updates.pop()
    for lower, upper in orders:
      if lower in bad_update and upper in bad_update:
        idx_l = bad_update.index(lower)
        idx_u = bad_update.index(upper)
        if idx_l > idx_u:
          bad_update[idx_l], bad_update[idx_u] = bad_update[idx_u], bad_update[idx_l]
          break
    # it could be bad again for another order push it back in if it is
    if is_bad(bad_update, orders):
      bad_updates.append(bad_update)
    else:
      updates.append(bad_update) 
  return sum([u[len(u)//2] for u in updates])


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
