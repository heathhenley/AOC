from common.utils import problem_harness, timeit


def look_and_say(s: str) -> str:
  res = ""
  last_count = 1
  for i in range(1, len(s) + 1):
    if i >= len(s) or s[i] != s[i-1]:
      res += f"{last_count}{s[i-1]}"
      last_count = 1
      continue
    last_count += 1
  return res 


@timeit
def part1(_: str) -> int:
  start_string = "1321131112"
  for _ in range(40):
    start_string = look_and_say(start_string)
  return len(start_string)


@timeit
def part2(_: str) -> int:
  start_string = "1321131112"
  for _ in range(50):
    start_string = look_and_say(start_string)
  return len(start_string)


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()