from common.utils import problem_harness, timeit, read_input


def blink(stones):
  new_stones = []
  for stone in stones:
    if stone == 0:
      new_stones.append(1)
    elif len(str(stone)) % 2 == 0:
      mid = len(str(stone)) // 2
      new_stones.append(int(str(stone)[:mid]))
      new_stones.append(int(str(stone)[mid:]))
    else:
      new_stones.append(stone * 2024)
  return new_stones


@timeit
def part1(filename: str) -> int:
  stones = list(map(int, read_input(filename)[0].split()))
  steps = 25
  for _ in range(steps):
    stones = blink(stones)
  return len(stones)


@timeit
def part2(filename: str) -> int:
  stones = [x for x in map(int, read_input(filename)[0].split())]
  steps = 75
  d = { x: stones.count(x) for x in stones }
  for _ in range(steps):
    stones = blink([s for s in d.keys()])
    for stone in stones:
      d[stone] = d.get(stone, 0) + 1
  return sum(d.values())


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
