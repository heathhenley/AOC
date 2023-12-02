import collections
import re

def read_input(filename: str, sep: str | None = None):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
    if sep is None:
      return  lines
    return [[val.strip() for val in line.split(sep)] for line in lines]

def parse_colors(line: str) -> dict[str, int]:
  pattern = r"(?P<count>[\d]+)\s(?P<color>[a-z]+),*"
  color_count = {}
  for count, color in re.findall(pattern, line):
    color_count[color] = int(count)
  return color_count

def is_possible_set(
    game_set: dict[str, int], colors: dict[str, int]) -> bool:
  for color, count in game_set.items():
    if count > colors[color]:
      return False
  return True

def get_possible_games(results_dict: dict[str, list[dict[str, int]]],
                        colors: dict[str, int]) -> list[int]:
  ids = []
  for gid, game_sets in results_dict.items():
    if all(is_possible_set(game_set, colors) for game_set in game_sets):
      ids.append(int(gid))
  return ids

def get_game_power(
    results_dict: dict[str, list[dict[str, int]]]) -> int:
  for _, game_sets in results_dict.items():
    max_seen_per_color = collections.defaultdict(int)
    for game_set in game_sets:
      for color, count in game_set.items():
        max_seen_per_color[color] = max(max_seen_per_color[color], count)
    game_power = 1
    for color, count in max_seen_per_color.items():
      game_power *= count
    yield game_power


def main():
  input_filename  = "input.txt" 
  #input_filename  = "test_input.txt"

  results_dict = collections.defaultdict(list)
  # Read and parse
  for result in read_input(input_filename, sep=":"):
    gid = result[0].split()[1]
    for game_set in result[1].split(";"):
      results_dict[gid].append(parse_colors(game_set))
  # results_dict = {gid: [{color: count}, {color: count}, ...]}

  # Part 1 - How many games possible with 12 red, 13 green, 14 blue?
  print("Part 1", sum(
    get_possible_games(
      results_dict, {"red": 12, "green": 13, "blue": 14})))
  
  # Part 2 - Min number of red, green, blue to play each --> power --> sum
  print("Part 2", sum(get_game_power(results_dict)))



if __name__ == '__main__':
  main()
