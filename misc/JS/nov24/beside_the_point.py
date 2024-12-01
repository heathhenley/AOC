import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.integrate import dblquad


def closest_edge(x, y):
    distances = {
        "bottom": y,
        "top": 1 - y,
        "left": x,
        "right": 1 - x,
    }
    closest = min(distances, key=distances.get)
    return closest


def simulate(n=500_000_000, xtest=None, ytest=None):
  good_xy_pairs = []
  counter = 0
  for _ in range(n):
    x1 = xtest or np.random.uniform(0, 1.0, 1)[0]
    y1 = ytest or np.random.uniform(0, 1.0, 1)[0]
    x2 = np.random.uniform(0, 1.0, 1)[0]
    y2 = np.random.uniform(0, 1.0, 1)[0]
    e = closest_edge(x1, y1)
    c = (x1**2 + y1**2 - x2**2 - y2**2)
    match e:
      case "bottom":
        if 0.0 <= c / (2 * (x1 - x2)) <= 1.0:
          good_xy_pairs.append([x2, y2])
          counter += 1
      case "top":
        if 0.0 <= (c - 2 * (y1-y2)) / (2 * (x1 - x2)) <= 1.0:
          good_xy_pairs.append([x2, y2])
          counter += 1
      case "left":
        if 0.0 <= (c / (2 * (y1 - y2))) <= 1.0:
          good_xy_pairs.append([x2, y2])
          counter += 1
      case "right":
        if 0.0 <= (c - (2 * (x1 - x2))) / (2 * (y1 - y2)) <= 1.0:
          good_xy_pairs.append([x2, y2])
          counter += 1
  return good_xy_pairs, counter / n

def sim():

  # good pairs only useful for fixed xtest, ytest (for debugging + making plots)
  xtest, ytest = 0.1, 0.1
  good_pairs, avg = simulate(n=1000_000, xtest=xtest, ytest=ytest)
  print(f"avg: {avg}")
  plt.scatter(*zip(*good_pairs), s=1)
  plt.plot(xtest, ytest, 'ro')
  plt.grid()
  plt.xlim(0, 1)
  plt.ylim(0, 1)
  plt.show()


def numeric():

  def a(x, y):
    ra = (x**2 + y**2) ** 0.5
    rb = ((1-x)**2 + y**2) ** 0.5
    sa = ra**2 * math.pi / 4.0
    sb = rb**2 * math.pi / 4.0
    term1 = ra**2 * math.acos( (1 + ra**2 - rb**2) / (2 * ra) )
    term2 = rb**2 * math.acos( (1 + rb**2 - ra**2) / (2 * rb) )
    term3 = -0.5 *( (-1 + ra + rb) * (1 + ra - rb) * (1 - ra + rb) * (1 + ra + rb) ) ** 0.5
    sab = term1 + term2 + term3
    return sa + sb - sab 

  # Quick spot check against simulation
  # spot checking points against mc simulation (they match well)
  for x, y in [[0.5, 0.001],
               [0.5, 0.491],
               [0.7, 0.10],
                [0.1, 0.1]]:
    print(f"({x}, {y})")
    print(f"  a(x, y) = {a(x, y):.3f}")
    print(f"  ms(x, y) = {simulate(n=10_000, xtest=x, ytest=y)[1]:.3f}")
 

  # Numeric integration using scipy (guassian quadrature)
  #  way easier to get an accurate answer in two dimensions than 4
  # need to swap the order of variables for dblquad
  a_swapped = lambda y, x: a(x, y)
  area = dblquad(
    a_swapped, 0, 0.5, lambda x: 0, lambda x: x, epsabs=1e-13, epsrel=1e-13)
  print(f"quad: {area[0]*8}, error: {area[1]}")

if __name__ == "__main__":
  numeric()
  sim()
