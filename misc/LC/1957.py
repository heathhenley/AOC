# LC 1957 - Delete Characters to Make Fancy String
import time


def makeFancyString(s: str) -> str:
  # Simple way without caring about string building
  if len(s) < 3:
    return s
  out_str = s[:2]
  for i in range(2, len(s)):
    if s[i] != s[i-1] or s[i] != s[i-2]:
      out_str += s[i]
  return out_str



def main():
  tests = [
    ["leeetcode", "leetcode"],
    ["aaabaaaa", "aabaa"],
    ["aab", "aab"],
    ["a", "a"],
    ["", ""]
  ]

  with open("misc/LC/long_string.txt", "r") as f:
    ans, expected = f.readlines()
    tests.append([
      ans.strip().strip('"'),
      expected.strip().strip('"')
      ])
  
  
  for i, (s, expected) in enumerate(tests):
    print(f"Test {i}:")
    if len(s) > 20:
      print(f"  Input: {s[:10]}...{s[-10:]}")
    else:
      print(f"  Input: {s}")
    
    start = time.perf_counter()
    result = makeFancyString(s)
    stop = time.perf_counter()
    print(f"  Time: {stop-start:.8f} sec")
    print(f"  Time: {(stop-start)*1000:.8f} ms")
    assert result == expected, f"{i} failed:" # expected {expected}, got {result}"
  

if __name__ == "__main__":
  main()