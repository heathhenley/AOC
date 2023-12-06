import sys


def read_input(filename: str, sep: str | None = None):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
    if sep is None:
      return  lines
    return [[val.strip() for val in line.split(sep)] for line in lines]

def parse_race_records(lines: list[str]) -> list[tuple[str, str]]:
  times = [int(x) for x in lines[0].split(":")[1].strip().split()]
  records = [int(x) for x in lines[1].split(":")[1].strip().split()]
  return list(zip(times, records))


def count_ways_to_win(duration: int, record: int) -> int:
  # you can 1 mm / ms for duration - 1 ms 
  # you can 2 mm / ms for duration - 2 ms
  # ...
  win = 0
  for i in range(1, duration):
    distance = i * (duration - i)
    if distance > record:
      win += 1
  return win

def get_long_race_input(records: list[tuple[int, int]]) -> tuple[int, int]:
  time = "".join(str(x[0]) for x in records)
  record = "".join(str(x[1]) for x in records)
  return (int(time), int(record))

def bs_for_left_boundary(duration: int, record: int) -> int:
  max_time = duration // 2 # max time to hold
  left_time, right_time = 1, max_time
  while left_time <= right_time:
    mid_time = (left_time + right_time) // 2
    mid_distance = mid_time * (duration - mid_time)
    if mid_distance > record:
      right_time = mid_time - 1
    if mid_distance < record:
      left_time = mid_time + 1
  return right_time

def bs_for_right_boundary(duration: int, record: int) -> int:
  max_time = duration // 2 # max time to hold
  left_time, right_time = max_time, duration - 1
  while left_time <= right_time:
    mid_time = (left_time + right_time) // 2
    mid_distance = mid_time * (duration - mid_time)
    if mid_distance > record:
      left_time = mid_time + 1
    if mid_distance < record:
      right_time = mid_time - 1
  return right_time

def get_ways_to_win_long(duration: int, record: int) -> int:
  # start at max_time and go left and right to find first
  # time that will lose, that different is the number of ways to win
  # get left boundary
  start_time = bs_for_left_boundary(duration, record)
  # get right boundary, same thing but start at max_time and go right
  end_time = bs_for_right_boundary(duration, record)
  return end_time - start_time
    

def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")

  input_file = sys.argv[1]
  print("Using input file", input_file)
  records = parse_race_records(read_input(input_file))


  # Part 1 - product of the number of ways to win each
  ways_to_win  = (count_ways_to_win(duration, record)
                  for duration, record in records)
  product = 1
  for ways in ways_to_win:
    product *= ways
  print("Part 1:", product)

  # Part 2 - longer race..
  duration, record = get_long_race_input(records)
  print("Part 2:", get_ways_to_win_long(duration, record))

if __name__ == '__main__':
  main()
