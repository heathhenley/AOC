import collections
import sys


def read_input(filename: str, sep: str | None = None):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
    if sep is None:
      return  lines
    return [[val.strip() for val in line.split(sep)] for line in lines]
   
def parse(lines: list[str]) -> tuple[list[str], list[str]]:
  return [line.split() for line in lines]

def make_hands_dict(hands_bids: list[list[str]]) -> dict[str, list[str]]:
  hands_dict = []
  for hand, _ in hands_bids:
    d = collections.defaultdict(int)
    for c in hand:
      d[c] += 1
    hands_dict.append(d)
  return hands_dict


# part 2 set up, part 1 used map with J in the right place
card_rank_map = {
  'A': 12,
  'K': 11,
  'Q': 10,
  'T': 9,
  '9': 8,
  '8': 7,
  '7': 6,
  '6': 5,
  '5': 4,
  '4': 3,
  '3': 2,
  '2': 1,
  'J': 0,
}

hand_rank_map = {
  'high card': 1,
  'one pair': 2,
  'two pair': 3,
  'three of a kind': 4,
  'full house': 5,
  'four of a kind': 6,
  'five of a kind': 7,
}

reverse_hand_rank_map = {
  1: 'high card',
  2: 'one pair',
  3: 'two pair',
  4: 'three of a kind',
  5: 'full house',
  6: 'four of a kind',
  7: 'five of a kind',
}

def get_hand_type(hand_d: dict) -> str:
  m = 0
  for k, v in hand_d.items():
    if k == "J":
      continue
    m = max(m, v)
  # m is the max number of non-J cards
  # js is the number of J cards
  js = hand_d['J']
  if js == 5 or js == 4:
    return 'five of a kind'
  if js == 3:
    if m == 2:
      return 'five of a kind'
    return 'four of a kind'
  if js == 2:
    if m == 3:
      return 'five of a kind'
    if m == 2:
      return 'four of a kind'
    return 'three of a kind'
  if js == 1:
    if m == 4:
      return 'five of a kind'
    if m == 3:
      return 'four of a kind'
    if m == 2:
      if list(hand_d.values()).count(2) == 2:
        return 'full house'
      return 'three of a kind'
    if m == 1:
      return 'one pair'
  if m == 5:
    return 'five of a kind'
  if m == 4:
    return 'four of a kind'
  if m == 3:
    if list(hand_d.values()).count(2) == 1:
      return 'full house'
    return "three of a kind"
  if m == 2:
    if list(hand_d.values()).count(2) == 2:
      return 'two pair'
    return 'one pair'
  return 'high card'

def sort_key(hbr) -> tuple[int, int]:
  ([hand, _], rank) = hbr
  card_rank = 0
  for idx, c in enumerate(hand):
    card_rank += card_rank_map[c] * 13**(5-idx-1)
  return (rank, card_rank)

def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")

  input_file = sys.argv[1]
  print("Using input file", input_file)

  # Part 1/2 - Modified part 1 for part 2 this time like a true
  # professional lol, might fix up eventually.
  hands_bids = parse(read_input(input_file))
  hands_ranks = [
    hand_rank_map[get_hand_type(f)] for f in  make_hands_dict(hands_bids)]
  hbr = [x for x in zip(hands_bids, hands_ranks)]
  hbr.sort(key=sort_key)
  winnings = 0
  for idx, ([_, bid], _) in enumerate(hbr):
    winnings += int(bid) * (idx + 1) 

  print(f"Winnings: {winnings}")

if __name__ == '__main__':
  main()
