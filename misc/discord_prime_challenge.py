from functools import cache
import sys
import time


@cache
def is_prime(n: int) -> bool:
  # checks and easy cases
  if n < 1:
    raise ValueError("Number must be greater than 0")
  if n < 4:
    return n == 2 or n == 3
  if n % 2 == 0 or n % 3 == 0:
    return False

  # keep checking for divisors less than sqrt(n)
  i = 5
  while i * i <= n:
    if n % i == 0 or n % (i + 2) == 0:
      return False
    i += 6
  return True


def closest_prime(n: int) -> int:
  """ Returns the closest prime number less than n """
  if n <= 2:
    raise ValueError("Starting value must be greater than 2")
  candidate = n - 1 if n % 2 == 0 else n - 2
  # TODO: try Miller-Rabin primality test for larger numbers?
  while not is_prime(candidate):
    candidate -= 2
  return candidate


def test_is_prime():
  print("Testing is_prime:")
  primes_list = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
    71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
    151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
    233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
    317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
    419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
    503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
    607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
    701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
    811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907,
    911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009,
    1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087,
    1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171,
    1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259,
    1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327,
    1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447,
    1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523,
    1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607,
  ]
  for i in range(2, max(primes_list) + 1):
    assert is_prime(i) == (i in primes_list), f"{i} is prime: {is_prime(i)}"


def main():


  print("Checking for 60 billion:")
  tic = time.perf_counter()
  print(f"   closest prime less than 60 billion: {closest_prime(60_000_000_000)}")
  toc = time.perf_counter()
  print(f"   took {toc - tic:0.4f} seconds")


  print("Checking for 2^2 to 2^64:")
  for i in range(0, 65, 8):
    if i < 2:
      continue
    n = 2 ** i
    print(f"Checking closest prime for (2^{i}) {n}:")
    tic = time.perf_counter()
    closest = closest_prime(n)
    toc = time.perf_counter()
    print(f"   closest prime less than {n}: {closest}")
    print(f"   took {toc - tic:0.4f} seconds")
  return 0


if __name__ == "__main__":
  sys.exit(main())
