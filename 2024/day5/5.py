from common.utils import problem_harness, timeit, read_input


@timeit
def part1(filename: str) -> int:
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
 
  good_updates = []
  for update in updates:
    for order in orders:
      if order[0] in update and order[1] in update:
        idx_0 = update.index(order[0])
        idx_1 = update.index(order[1])
        if idx_0 > idx_1:
          break
    else:
      good_updates.append(update)

  return sum([l[len(l)//2] for l in good_updates])


def is_bad(update, orders):
  for lower, upper in orders:
    if lower in update and upper in update:
      idx_l = update.index(lower)
      idx_u = update.index(upper)
      if idx_l > idx_u:
        return True
  return False


@timeit
def part2(filename: str) -> int:
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
 
  bad_updates = []
  for update in updates:
    for order in orders:
      if order[0] in update and order[1] in update:
        idx_0 = update.index(order[0])
        idx_1 = update.index(order[1])
        if idx_0 > idx_1:
          bad_updates.append(update)
          break

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
  return sum([l[len(l)//2] for l in updates])


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
