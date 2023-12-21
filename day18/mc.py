from dataclasses import dataclass
import matplotlib.animation as animation
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

def part2(filename: str) -> int:
  moves = [x.split() for x in read_input(filename)]
  moves = correct_moves(moves)
  start = (0,0)
  path = walk_pt2(start, moves)
  actual_area = (perimeter(path) / 2 + 1)  + shoelace_area(path)

  # get bounding box of path
  bbox = get_bbox(path)
  bbox_area = (bbox[1] - bbox[0]) * (bbox[3] - bbox[2])

  fig, ax = plt.subplots()

  ax.plot([p.x for p in path], [p.y for p in path], color='black')
  label = ax.text(0.0, 2.32e7, "label")
  ins = ax.plot([], [], 'o', color='red', markersize=0.25)[0]
  out = ax.plot([], [], '.', color='blue', markersize=0.25)[0]

  # compute area by 'thowing darts' at the bounding box
  # and counting how many land inside the path
  n_steps = 1000 # per frame
  total = 500000 # total number of steps
  yin, xin = [], []
  yout, xout = [], []
  inside = 0
  def update(frame):
    nonlocal inside
    for _ in range(n_steps):
      x = np.random.randint(bbox[0], bbox[1])
      y = np.random.randint(bbox[2], bbox[3])
      if is_point_in_poly(path, Point(x,y)):
        inside += 1
        xin.append(x)
        yin.append(y)
        ins.set_xdata(xin)
        ins.set_ydata(yin)
      else:
        xout.append(x)
        yout.append(y)
        out.set_xdata(xout)
        out.set_ydata(yout)
        
    estimated_area = inside / ((frame + 1) * n_steps)
    area = actual_area / bbox_area
    error = (abs(area - estimated_area) / area) * 100
    label.set_text((f"Actual area:       {area:0.7f}\n"
              f"Estimated area: {estimated_area:.7f}\n"
              f"Error: {error:.2f}%,  Steps: {frame * n_steps}"))
  ani = animation.FuncAnimation(fig, update, frames=total//n_steps, interval=100)
  ani.save('animation.gif', fps=60)
  plt.show()



def main():
  if not sys.argv[1:]:
    sys.exit("Usage: python <day>.py <input_file>")
  input_file = sys.argv[1]

  tic = time.perf_counter()
  print("Part 2:", part2(input_file))
  toc = time.perf_counter()
  print(f"  Part 2 took {toc - tic:0.4f} seconds")


if __name__ == '__main__':
  main()
