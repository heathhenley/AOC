import re
x = []
with open("1.txt", "r") as f:
    x = [i.strip() for i in f.readlines()]

# Part 2
#ans = 0
#for s in x:
#  d = []
#  for i in range(len(s)):
#    if s[i] in "0123456789":
#      d.append(s[i])
#      break
#  s = s[::-1]
#  for i in range(len(s)):
#    if s[i] in "0123456789":
#      d.append(s[i])
#      break
#  print(s, d)
#  ans += int("".join(d))
#print("part1:", ans)

# Part 2
m = {
  "one": 1,
  "two": 2,
  "three": 3,
  "four": 4,
  "five": 5,
  "six": 6,
  "seven": 7,
  "eight": 8,
  "nine": 9,
}

ans = 0
for s in x:
  d_idx = []
  for k, v in m.items():
    if k in s:
      d_idx.extend([[a.start(), k] for a in list(re.finditer(k, s))])
  s1 = s[::] 
  s2 = s[::]
  d_idx.sort()
  if d_idx:
    start_idx, n = d_idx[0][0], len(d_idx[0][1])
    s1 = s[:start_idx] + str(m[d_idx[0][1]]) + s[start_idx+n:]
    start_idx, n = d_idx[-1][0], len(d_idx[-1][1])
    s2 = s[:start_idx] + str(m[d_idx[-1][1]]) + s[start_idx+n:]
  d = []
  for i in range(len(s1)):
    if s1[i] in "123456789":
      d.append(s1[i])
      break
  s2 = s2[::-1]
  for i in range(len(s2)):
    if s2[i] in "123456789":
      d.append(s2[i])
      break
  ans += int("".join(d)) 
print("part2:", ans)