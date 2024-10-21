from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
from common.utils import read_input

@dataclass
class Point:
  x: int
  y: int


def walk(start: tuple, moves: list) -> list:
  # start at 0,0, apply moves to get path
  start = Point(0,0)
  path = [start]
  for move in moves:
    # first string is direction, second is number of steps
    direction, steps, color = move[0], int(move[1]), int(move[2][2:-1], 16)
    direction = move[0]
    steps = int(move[1])
    last = path[-1]
    if direction == 'U':
      new_point = Point(last.x, last.y + steps)
    elif direction == 'D':
      new_point = Point(last.x, last.y - steps)
    elif direction == 'L':
      new_point = Point(last.x - steps, last.y)
    elif direction == 'R':
      new_point = Point(last.x + steps, last.y)
    path.append(new_point)
  return path

def walk_pt2(start: tuple, moves: list) -> list:
  # this is the same part 1 but I didn't feel like
  # refactoring the code to make it work for both rn
  # start at 0,0, apply moves to get path
  start = Point(0,0)
  path = [start]
  for move in moves:
    # first string is direction, second is number of steps
    direction, steps = move
    last = path[-1]
    if direction == 'U':
      new_point = Point(last.x, last.y + steps)
    elif direction == 'D':
      new_point = Point(last.x, last.y - steps)
    elif direction == 'L':
      new_point = Point(last.x - steps, last.y)
    elif direction == 'R':
      new_point = Point(last.x + steps, last.y)
    path.append(new_point)
  return path

def shoelace_area(path: list) -> int:
  # using numpy here so that it's faster
  y = np.array([p.y for p in path], dtype=np.int64)
  x = np.array([p.x for p in path], dtype=np.int64)
  return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def perimeter(path: list) -> int:
  perimeter = 0
  for i in range(len(path)-1):
    perimeter += abs(path[i+1].x - path[i].x) + abs(path[i+1].y - path[i].y)
  return perimeter

def get_bbox(path: list) -> tuple:
  # get bounding box of path
  min_x = min([p.x for p in path])
  max_x = max([p.x for p in path])
  min_y = min([p.y for p in path])
  max_y = max([p.y for p in path])
  return (min_x, max_x, min_y, max_y)

def is_on_path(point: Point, path: list) -> bool:
  # check if point is on the path
  for i in range(1, len(path)):
    if path[i] == point:
      return True
    # check if point is on line segment
    if path[i-1].x == path[i].x and point.x == path[i].x:
      # vertical line
      if point.y >= min(path[i-1].y, path[i].y) and point.y <= max(path[i-1].y, path[i].y):
        return True
    elif path[i-1].y == path[i].y and point.y == path[i].y:
      # horizontal line
      if point.x >= min(path[i-1].x, path[i].x) and point.x <= max(path[i-1].x, path[i].x):
        return True
  return False
    

def find_enclosed(path: list, bbox: tuple) -> int:
  x_min, x_max, y_min, y_max = bbox
  # check each point in bounding box to see if it is enclosed
  # by the path
  count_points = 0
  fill = []
  for x in range(x_min, x_max+1):
    for y in range(y_min, y_max+1):
      # if it's on the path, skip
      if is_on_path(Point(x, y), path):
        continue
      # check if point is enclosed by path
      if is_point_in_poly(path, Point(x,y)):
        fill.append(Point(x, y))
        count_points += 1
  return count_points, fill

def is_point_in_poly(
    poly: list[Point], point: Point) -> bool:
  # copy/pasta
  x, y = point.x, point.y
  n = len(poly)
  inside = False
  p1x, p1y = poly[0].x, poly[0].y
  for i in range(n + 1):
    p2x, p2y = poly[i % n].x, poly[i % n].y
    if y > min(p1y, p2y):
      if y <= max(p1y, p2y):
        if x <= max(p1x, p2x):
          if p1y != p2y:
            xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
          if p1x == p2x or x <= xints:
            inside = not inside
    p1x, p1y = p2x, p2y
  return inside  

def parse_move(move: str) -> list:
  # parse hex color into direction and steps
  move = move[2:-1]
  distance = int(move[:-1], 16)
  direction = int(move[-1]) 
  if direction == 0:
    direction = 'R'
  elif direction == 1:
    direction = 'D'
  elif direction == 2:
    direction = 'L'
  elif direction == 3:
    direction = 'U'
  return [direction, distance]

def correct_moves(moves: list) -> list:
  # The 'corrected' moves for part 2
  corrected = []
  for move in moves:
    corrected.append(parse_move(move[2]))
  return corrected


def shoelace_on_the_fly(moves: list) -> int:
  # this one works better, less space!
  # but then we can't plot the sweet path
  area = 0
  perim = 0
  x, y = 0, 0
  for dir, dist in moves:
    dx, dy = 0, 0
    if dir == 'U':
      dy = dist
    elif dir == 'D':
      dy = -dist
    elif dir == 'L':
      dx = -dist
    elif dir == 'R':
      dx = dist
    next_x = x + dx
    next_y = y + dy
    area += x * next_y - y*next_x
    x = next_x
    y = next_y
    perim += dist
  return abs(area) / 2 + perim / 2 + 1


def part1(filename: str) -> int:
  moves = [x.split() for x in read_input(filename)]
  start = (0,0)
  path = walk(start, moves)
  #plt.plot([p.x for p in path], [p.y for p in path])
  #plt.show()
  bbox = get_bbox(path)
  count_points, _ = find_enclosed(path, bbox)
  return perimeter(path) + count_points

def part2(filename: str) -> int:
  moves = [x.split() for x in read_input(filename)]
  moves = correct_moves(moves)
  return shoelace_on_the_fly(moves)
  # this was the original part 2, but we don't actually need
  # to store the path (accept for plotting)
  # start = (0,0)
  # path = walk_pt2(start, moves)
  # return (perimeter(path) / 2 + 1)  + shoelace_area(path)

def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")
  input_file = sys.argv[1]

  tic = time.perf_counter()
  print("Part 1:", part1(input_file))
  toc = time.perf_counter()
  print(f"  Part 1 took {toc - tic:0.4f} seconds")
  tic = time.perf_counter()
  print("Part 2:", part2(input_file))
  toc = time.perf_counter()
  print(f"  Part 2 took {toc - tic:0.4f} seconds")


if __name__ == '__main__':
  main()
