from common.utils import read_input
import sys


def get_diff(series: list) -> int:
  diff = []
  for i in range(1, len(series)):
    diff.append(series[i] - series[i-1])
  return diff

def get_prediction(series: list) -> list:
  d = get_diff(series)
  diffs = [d]
  while len(d) > 1 and any([_d != d[0] for _d in d]):
    d = get_diff(d) 
    diffs.append(d)
  # loop from last to first
  for i in range(len(diffs)-2, -1, -1):
    diffs[i][-1] = diffs[i+1][-1] + diffs[i][-1]
  return series[-1] + diffs[0][-1]

def get_prediction_left(series: list) -> list:
  d = get_diff(series)
  diffs = [d]
  while len(d) > 1 and any([_d != d[0] for _d in d]):
    d = get_diff(d) 
    diffs.append(d)
  # loop from last to first
  for i in range(len(diffs)-2, -1, -1):
    diffs[i][0] = diffs[i][0] - diffs[i+1][0]
  return series[0] - diffs[0][0] 

def part1(filename: str) -> int:
  report_series = [[int(x) for x in row]
                   for row in read_input(filename, sep=" ")]
  predictions = [
      get_prediction(series) for series in report_series
  ]
  return sum(predictions)

def part2(filename: str) -> int:
  report_series = [[int(x) for x in row]
                   for row in read_input(filename, sep=" ")]
  predictions = [
      get_prediction_left(series) for series in report_series
  ]
  return sum(predictions)


def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")
  input_file = sys.argv[1]

  print("Part 1:", part1(input_file))
  print("Part 2:", part2(input_file))


if __name__ == '__main__':
  main()
