from common.utils import problem_harness, timeit, read_input


def blink(stones: list[int]) -> list[int]:
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

# read about peoples recursive solutions - implementing that way too to improve 
# my understanding - this is based on this comment on the aoc subreddit
# https://www.reddit.com/r/adventofcode/comments/1hbo9m6/comment/m1k0qnz
def blink_recursive(stone: int, blinks_left: int, memo: dict) -> int:
  if blinks_left == 0:
    return 1
  
  if blinks_left in memo:
    if stone in memo[blinks_left]:
      return memo[blinks_left][stone]

  # missed, need to calculate and cache
  new_stones = 0
  if stone == 0:
    new_stones = blink_recursive(1, blinks_left - 1, memo)
  elif len(str(stone)) % 2 == 0:
    mid = len(str(stone)) // 2
    sl, sr = int(str(stone)[:mid]), int(str(stone)[mid:])
    new_stones = (
      blink_recursive(sl, blinks_left - 1, memo)
      + blink_recursive(sr, blinks_left - 1, memo)
    )
  else:
    new_stones = blink_recursive(stone * 2024, blinks_left - 1, memo)

  # memoize the result
  if blinks_left not in memo:
    memo[blinks_left] = {}
  memo[blinks_left][stone] = new_stones

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

  # this is an alternative solution using recursion and memo (learned about it
  # afterward) - it's about the same speed as the original solution below at
  # least for these implementations and inputs
  #memo = {}
  #return sum([blink_recursive(stone, steps, memo) for stone in stones])

  # keep a count of the stones we have at all times (this is the original 
  # solution I used before I read about the recursive solution)
  d = { x: stones.count(x) for x in stones }
  for _ in range(steps):
    new_d = d.copy()
    stones = [x for x in d.keys() if d[x] > 0]
    for stone in stones:
      count = d[stone]
      # we have count stones that will transform into new stones
      new_stones = blink([stone])
      # remove the stones we are about to transform
      new_d[stone] -= count
      # each of the count stones we had become new_stones (one or two stones)
      # eg - remove 'count' of the old stones, and add count of each new stone
      # the weird copying of the dict is because two different stones could make
      # the same new stone - couldn't figure out the logic to this in place
      # with out some slightly off results - so just copy the dict for now
      for s in new_stones:
        new_d[s] = new_d.get(s, 0) + count
    d = new_d.copy()
  return sum(new_d.values())


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
