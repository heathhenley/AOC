import re
from common.utils import problem_harness, timeit, read_input

PATTERN = r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.'


def try_int(s):
  try:
    return int(s)
  except ValueError:
    return s


def distance_at_t(time, speed, dist, rest):
  repeats = time // (dist + rest)
  leftover = time - repeats * (dist + rest)
  return repeats * dist * speed + min(dist, leftover) * speed

@timeit
def part1(filename: str) -> int:

  # Fixed input - 2503 seconds
  race_len = 2503

  winner = None
  for line in read_input(filename):
    if not (m := re.match(PATTERN, line)):
      assert False, "Invalid input"
    deer, speed, dist, rest = [try_int(x) for x in m.groups()]
    total_dist = distance_at_t(race_len, speed, dist, rest)
    if not winner or total_dist > winner[1]:
      winner = (deer, total_dist)
  return winner[1]


@timeit
def part2(filename: str) -> int:

  # Fixed input - 2503 seconds
  seconds = 2503 

  deer = []
  for line in read_input(filename):
    if not (m := re.match(PATTERN, line)):
      assert False, "Invalid input"
    deer.append([try_int(x) for x in m.groups()])

  score = {}
  for race_len in range(1, seconds + 1):
    race_results = {}
    for d, speed, dist, rest in deer:
      race_results[d] = distance_at_t(race_len, speed, dist, rest)
    # current winner - add to score
    for d, dist in race_results.items():
      if dist == max(race_results.values()):
        score[d] = score.get(d, 0) + 1
  return max(score.items(), key=lambda x: x[1])[1]


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()