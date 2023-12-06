from functools import cache
import sys


def read_input(filename: str, sep: str | None = None):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
    if sep is None:
      return  lines
    return [[val.strip() for val in line.split(sep)] for line in lines]

def parse(lines: list[str]):
  seeds = [int(x) for x in lines[0].split("seeds: ")[1].split()]
  maps = []
  current_map = []
  for line in lines[1:]:
    if line.endswith("map:"):
      if not current_map:
        continue
      maps.append(current_map)
      current_map = []
      continue
    if line:
      current_map.append([int(x) for x in line.split()])
  if current_map:
    maps.append(current_map)
  return seeds, maps

def move_through_map(seed: str, map: list[list[str]]):
  for dst_start, src_start, rng in map:
    if seed >= src_start and seed <= src_start + rng:
      seed = dst_start + (seed - src_start)
      break
  return seed

def move_through_maps(seed: int, maps: list[list[str]]):
  current_val = seed
  for map in maps:
    current_val = move_through_map(current_val, map)
  return current_val

def expand_seeds(seeds: list[int]):
  for i in range(0, len(seeds), 2):
    print("set i", i // 2)
    start, num = seeds[i], seeds[i+1]
    for j in range(num):
      yield start + j

def part_2_maps_via_ranges(seeds: list[int], maps: list[list[str]]) -> int:
  # sort map rows by src_start
  maps = [sorted(map, key=lambda x: x[1]) for map in maps]
  # put all ranges in a list
  deque = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]
  # map through all maps
  for map in maps:
    # for each map iterate as many times as there are ranges in the deque 
    for _ in range(len(deque)):
      start, num = deque.pop(0) # get the next range
      for dst_start, src_start, rng in map:
        if start < src_start and start + num < src_start:
          # everything is smaller than the map
          #   range --> add to deque for next map
          deque.append([start, num]) 
          break

        if start >= src_start + rng:
          # everything is bigger than this map range
          continue
        
        # we have overlap...
        # split the range and push the non-overlapping part
        if start < src_start:
          # split the range into two ranges
          #  - the part that is not overlapping --> add to deque
          deque.append([start, src_start - start])
          # this is the overlapping part that needs to be mapped
          # through this part of the filter
          start = src_start
          num = num - (src_start - start)

        # we are in the overlapping part, need to map it through
        # the filter
        new_start = start - src_start + dst_start # mapped start
        new_num = min(src_start + rng - 1, start + num -1)
        deque.append([new_start, new_num - start + 1])

        num = num - (new_num - start + 1)
        start = new_num + 1
        if num == 0:
          break

      if num > 0:
        deque.append([start, num])
    
  location = 100000000000000000
  for start, num in deque:
    location = min(location, start)
  return location

def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python 5.py <input_file>")

  input_file = sys.argv[1]
  print("Using input file", input_file)
  seeds, maps = parse(read_input(input_file))

  # Part 1
  location = min(
    [move_through_maps(seed, maps) for seed in seeds])
  print("Part 1:", location)

  # Part 2 - this is too slow :(
  # location = float("inf")
  # for seed in expand_seeds(seeds):
  #   location = min(move_through_maps(seed, maps), location)
  # print("Part 2:", location)

  # Part 2 - this is faster :)
  print("Part 2:", part_2_maps_via_ranges(seeds, maps))

if __name__ == '__main__':
  main()
