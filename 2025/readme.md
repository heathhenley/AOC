# Advent of Code 2025
## using OCaml ( and maybe other languages )

## Day 1
Nice start to the year! Straightforward and fun to do in OCaml - had some silly
mistakes with the counting logic for part 2 to sort out.

### Day 2
Mostly straightforward again - had a lot of weird trouble just getting the input
parsed etc but that's just an Ocaml-with-no-autocompletion problem.

The first approach and what I used to get the star was split the string for part
1 and compare the halves. Then for part 2 I used a pretty simple regex with a
capture group and backref to check if it was made entirely of repeating digits.

I tried to switch away from string manipulation and use math instead, which made part 1 faster but part 2 slower. So, I landed on a using math for part 1
and a regex for part 2 🤷‍♂️

UPDATE: Read through more solutions - it turns out I didn't math hard enough! I
Think I'm going to update to use the approach I found on reddit, here's the
gh: https://github.com/ranjeethmahankali/adventofcode/blob/main/2025/src/day_2.rs

The idea is that any of the invalid numbers are multiples of a "pattern" number,
there is no way I would have figured that out on my own on the stop yesterday so
that's amazing that someone did.

Basically - a 4 digit number for example 1212 - the pattern number:
p = 10^(n_digits/2) + 1, so in this case p = 101

All the multiples of 101 are the 'invalid' numbers we are after, need to look in
the range given to find them. Eg 1010, 1111, 1212, etc.

For part 2, it's the same idea but more patterns to check - you need to check
all the possible divisors instead of just half the number of digits.
So for a six digit number like 121212 - it could be 2 segments of 3, 3 segments of 2, 6 segments of 1, etc.

The "period" is the segment length - and k is the number of times it repeats, in general for k repeats of the period, the pattern number is:
p = 1 + 10^(period) + 10^(2*period) + ... + 10^((k-1) * period)

so for a 6 digit number we need to check:
- 2 segments of 3: p = 1 + 10^3 = 1001 --> 100100, 200200, 300300, etc.
- 3 segments of 2: p = 1 + 10^2 + 10^4 = 10101 --> 101010, 202020, 303030, etc.
- 6 segments of 1: p = 1 + 10 + 10^2 + 10^3 + 10^4 + 10^5 = 111111 --> 111111, 222222, 333333, etc.

