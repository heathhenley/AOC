from common.utils import problem_harness, timeit, read_input

def get_height(key):
  counts = []
  for j in range(len(key[0])):
    count = -1
    for i in range(len(key)):
      if key[i][j] == "#":
        count += 1
    counts.append(count)
  return counts 

@timeit
def part1(filename: str) -> int:
  keys, locks = [], []
  grids = [] 
  grid = []
  for line in read_input(filename):
    line = line.strip()
    if line:
      grid.append(list(line))
    else:
      grids.append(grid)
      grid = []
  grids.append(grid) 
  for grid in grids:
    if all(grid[0][i] == "#" for i in range(len(grid[0]))):
      locks.append(grid)
    else:
      keys.append(grid)
  
  print("KEYS:")
  for key in keys:
    for k in key:
      print(k)
    print(get_height(key))
    print()
  print("LOCKS:")
  for lock in locks:
    for l in lock:
      print(l)
    print(get_height(lock))
    print()

  matches = 0
  for i, key in enumerate(keys):
    for j, lock in enumerate(locks):
      kh = get_height(key)
      lh = get_height(lock)
      if all(k + l <= len(key[0]) for k, l in zip(kh, lh)):
        matches += 1
  return matches


@timeit
def part2(filename: str) -> int:
  return 0


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
