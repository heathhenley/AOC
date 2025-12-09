# Advent of Code 2025
## using OCaml ( and maybe other languages )

### Day 1

[day01.ml](lib/day01.ml)

Nice start to the year! Straightforward and fun to do in OCaml - had some silly
mistakes with the counting logic for part 2 to sort out.

### Day 2

[day02.ml](lib/day02.ml)

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

EDIT2: after all that debugging - the math version (at least my impl) is still
slower than the regex version 🤷‍♂️ - for part 2 it's roughly 1.5 the runtime.
It's about 5x faster for part 1 though. At least I guess I learned a cool trick.

EDIT3: Just realized that the approach above lets you not check each number -
duh! Need to rearrange but then it can get just produce the multiple of the
pattern that are within the range instead of checking.

Another update: implemented based on that reddit solution and it's super fast!

### Day 3:

[day03.ml](lib/day03.ml)

Originally brute forced part 1, used greedy approach for part 2 - it always
the largest digit that will leave enough digits left to take to create the
number. I had the solution approach pretty early but I've been bumping against
my Ocaml-incompetence lol.

### Day 4

[day04.ml](lib/day04.ml)

Very straightforward grid problem - probably a bit of foreshadowing for what is
to come... At least I'll have some grid parsing / walking down for the those.

### Day 5

[day05.ml](lib/day05.ml)

This was a cool one - merging ranges, just did part 1 brute force but for part 2
had to merge the ranges together. Really similar to a problem for last year or
2023 I think, so I recognized what to do right away.

### Day 6

[day06.ml](lib/day06.ml)

Really interesting part 2 of this one, I had to stop thinking about the input
as a bunch of rows of numbers when to parsing chars down the the columns
instead. I'm really struggling with the string manip stuff in ocaml, this was
one where I was feeling to the pull to switch to python and just bang it out..
but managed to push through it. Not tricky algorithm or anything though, just
reads down the nth column of each line, pushes the non ' ' chars to a string,
and then converts to an int. Anytime all the columns are ' ' chars, we've read
the whole problem.

### Day 7

[day07.ml](lib/day07.ml)

Another grid problem - really forced being able to re-use my bfs util, but I
wasn't able to re-use it on part 2 to get the paths. Might need to extent it
a bit more to be able to handle that or add a new util function - I feel like
number of paths comes up a lot.
Less of a twist from part 1 to part 2 compared to yesterday, but I'm also tired
so I'm cool with that!
I used my bfd util to get the start node (overkill) and then used again in part
1 to walk the grid and count the splits. Part 2 I had to kind of re-write it
because with the visited set inside my bfd impl I coulnd't figure out how to
set it up to track paths. Same idea though, but for each neighbor node, if you
have already been there, add the paths to the current node to the neighbor node,
otherwise add the number of paths - used a hashtbl for this and returned the
sum of the paths to the last row.

UPDATE: Didn't think of this while solving, but there's a way simpler dfs
solution. Implemented to test it out in `count_paths_dfs`.


### Day 8

[day08.ml](lib/day08.ml)

This was brutal for me. I was not really able to see the right approach. First
I tried an octree to keep track of the points / find the closest points - I was
struggling to get that to do what I wanted so I switched to managing my own
lists of circuits and merging them when needed, that wasn't working correctly
either, but it felt like union / find - and then I finally got it working with
a crappy union / find implementation. I definitely did not choose the right data
structures at all for this and it's pretty slow but got the stars.

Really need to clean this one up please don't look.
