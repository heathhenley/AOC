from dataclasses import dataclass
import numpy as np
import re
from scipy.optimize import minimize

from common.utils import problem_harness, timeit, read_input


PATTERN = r"(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)"


# named tuple for ingredients
@dataclass
class Ingredient:
  name: str
  capacity: int
  durability: int
  flavor: int
  texture: int
  calories: int

  @classmethod
  def from_tuple_of_str(cls, t: tuple[str]) -> 'Ingredient':
    return cls(t[0], int(t[1]), int(t[2]), int(t[3]), int(t[4]), int(t[5]))


def parse_line(line: str) -> Ingredient:
  return Ingredient.from_tuple_of_str(re.match(PATTERN, line).groups())


# trying this with scipy - this the objective function - basically score
# for the current teaspoons of each ingredient (x)
def obj(x, ingredients: list[Ingredient]) -> np.float64:
  score = 1.0
  for attr in ['capacity', 'durability', 'flavor', 'texture']:
    score *= max(
        0,
        x[0] * getattr(ingredients[0], attr)
      + x[1] * getattr(ingredients[1], attr)
      + x[2] * getattr(ingredients[2], attr)
      + x[3] * getattr(ingredients[3], attr)
    )
  return -np.float64(score) # scipy minimizes, so we need to negate the score


def must_be_100(x) -> int:
  return sum(x) - 100


def solve_using_scipy(ingredients: list[Ingredient]) -> int:
  # Set up the optimization problem - it is super sensitive to the initial guess
  # so really would have to try a bunch of them
  initial_guess = [25, 25, 25, 25]
  constraints = ({'type': 'eq', 'fun': must_be_100},
                 {'type': 'ineq', 'fun': lambda x: x[0]},
                 {'type': 'ineq', 'fun': lambda x: x[1]},
                 {'type': 'ineq', 'fun': lambda x: x[2]},
                 {'type': 'ineq', 'fun': lambda x: x[3]})
  result = minimize(
    lambda x: obj(x, ingredients),
    initial_guess, constraints=constraints)

  optimal_allocation = result.x

  rounded_allocation = [round(teaspoon) for teaspoon in optimal_allocation]
  print("Rounded allocation:", rounded_allocation)
  score = obj(rounded_allocation, ingredients)
  print("Score for rounded allocation:", score)
  return -score # negate the score to get the actual score


def get_best_cookie_score(
    ingredients: list[Ingredient],
    max_ingredients: int,
    max_calories: int | None = None,
) -> int:
  """ Brute force solution to find the best cookie score """
  best_score = 0
  save = None
  # loop through all possible combinations of ingredients
  for i in range(max_ingredients):
    for j in range(max_ingredients):
      for k in range(max_ingredients):
        h = max_ingredients - i - j - k
        if h < 0:
          continue
        # for each combination, calculate the score
        score = 1
        for attr in ['capacity', 'durability', 'flavor', 'texture']:
          score *= max(
              0,
              i * getattr(ingredients[0], attr)
            + j * getattr(ingredients[1], attr)
            + k * getattr(ingredients[2], attr)
            + h * getattr(ingredients[3], attr)
          )
        calories = (
            i * ingredients[0].calories
          + j * ingredients[1].calories
          + k * ingredients[2].calories
          + h * ingredients[3].calories
        )
        if max_calories is not None and calories != max_calories:
          continue
        if score > best_score:
          best_score = max(best_score, score)
          save = (i, j, k, h)
  print(f"Best score: {best_score} with {save}")
  return best_score


@timeit
def part1(filename: str) -> int:
  return get_best_cookie_score(list(map(parse_line, read_input(filename))), 100)


@timeit
def part2(filename: str) -> int:
  return get_best_cookie_score(
    list(map(parse_line, read_input(filename))), 100, 500)


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
