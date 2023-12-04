import collections
import sys


def read_input(filename: str, sep: str | None = None):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
    if sep is None:
      return  lines
    return [[val.strip() for val in line.split(sep)] for line in lines]


def parse_cards_from(input_filename: str) -> list[int]:
  cards = [x.split(":")[1].split("|")
            for x in read_input(input_filename)]
  return [[x.split(), y.split()] for x, y in cards]


def get_count_dict(cards: list[str]) -> dict[str, int]:
  count_dict = collections.defaultdict(int)
  for card in cards:
    count_dict[int(card)] += 1
  return count_dict

def get_matches(winning: list[str], ours: list[str]) -> int:
  dwinning = get_count_dict(winning)
  matches = 0
  for number in ours:
    matches += dwinning[int(number)]
  return matches

def get_card_points(winning: list[str], ours: list[str]) -> int:
  matches = get_matches(winning, ours) 
  return 0 if matches == 0 else 2 ** (matches - 1)

def get_total_total_cards(cards: list[list[str]]) -> int:
  card_count = {i: 1 for i in range(len(cards))}
  for idx, (winning, ours) in enumerate(cards):
    matches = get_matches(winning, ours)
    for i in range(1, matches+1):
      card_count[idx + i] += card_count[idx]
  return sum(card_count.values())


def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python 3.py <input_file>")

  input_file = sys.argv[1]
  print("Using input file", input_file)

  # Part 1 - how many points are the cards worth
  cards = parse_cards_from(input_file)
  total_points = sum(
    get_card_points(winning, ours) for winning, ours in cards)
  print("Part 1:", total_points)

  # Part 2 - how many cards? (they copy now)
  total_cards = get_total_total_cards(cards)
  print("Part 2:", total_cards)

if __name__ == '__main__':
  main()
