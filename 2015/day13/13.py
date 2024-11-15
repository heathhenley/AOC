import collections
from common.utils import problem_harness, timeit, read_input


def get_happiness_map(lines):
  happiness_map = collections.defaultdict(dict)
  for line in lines:
    line = line.rstrip('.').split(" happiness units by sitting next to ")
    p1, str_res, p2 = *line[0].split(' would '), line[-1]
    action, value = str_res.split(' ')
    value = int(value)
    happiness_map[p1][p2] = value if 'gain' in action else -value
  return happiness_map


def yield_permutations(lst):
  if len(lst) == 1:
    yield lst
  for i in range(len(lst)):
    for perm in yield_permutations(lst[:i] + lst[i+1:]):
      yield [lst[i]] + perm


def get_max_happiness(happiness_map):
  best_happiness = -1e9
  for ordering in yield_permutations(list(happiness_map.keys())):
    # handle circular seating
    happiness = happiness_map[ordering[0]][ordering[-1]]
    happiness += happiness_map[ordering[-1]][ordering[0]]
    # handle the rest of the seating
    for i in range(1, len(ordering)):
      p1 = ordering[i-1]
      p2 = ordering[i]
      happiness += happiness_map[p1][p2] + happiness_map[p2][p1]
    best_happiness = max(best_happiness, happiness)
  return best_happiness


@timeit
def part1(filename: str) -> int:
  happiness_map = get_happiness_map(read_input(filename))
  return get_max_happiness(happiness_map)


@timeit
def part2(filename: str) -> int:
  happiness_map = get_happiness_map(read_input(filename))
  # add myself to the happiness map - I have 0 happiness with everyone
  happiness_map['me'] = { person: 0 for person in happiness_map.keys() }
  for person in happiness_map.keys():
    happiness_map[person]['me'] = 0
  return get_max_happiness(happiness_map)


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()