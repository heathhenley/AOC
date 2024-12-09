# Advent of Code 2024
## switching around between python, go and ocaml - sometimes all of them!

### Day 1
Did this one in Python and in Ocaml - it was straightforward reading in the data
and flipping it around into the right shape to do the calculations it was asking
for over the lists. Sorted them both for part 1, for part 2 used a hashtable to
count the occurrences of the number in the right hand list. Added go for funsies - haven't done any go in a while.

### Day 2
Python and Ocaml again! Python for speed, Ocaml for fun. I just implemented the
level checks that it asked for in part 1 and counted the valid levels. In part 2
I realized that the levels (rows) were not very long so it wasn't a big deal to
just brute force and try them all instead of trying to find a better way to find
out of the level can be made valid. Had a bit of trouble getting it going in
Ocaml - mostly with getting the diff list to work (just use mapi instead of map2)

EDIT: An example of the linear time solution in Python on reddit: https://www.reddit.com/r/adventofcode/comments/1h4ncyr/comment/m00dpfi/

EDIT2: I also added a Go solution for day 2

### Day 3
Part 1 in 4 minutes in Python! This was regex to grab the numbers and then just
multiply and sum them.

Part 2 was a different beast - I made a mistake with the new lines in the file,
I was processing line by line and resetting the ranges for the do/don't switch
with each line instead of keeping it going for the whole file - took me like an
hour to figure out what I was doing wrong.
I did the same regex to get the numbers, and to also get the do() and don't()
switches, tracked the indices of the switches and only applied the mults when
the switch was on. Cleaning up and adding an Ocaml solution tomorrow am!

EDIT: added part 1 Ocaml solution before work - part 2 will take some more
thinking (need to figure out how to do it functionally instead of imperatively)

EDIT2: cleaned up python part 2 more - thinking about how to do it in ocaml gave
me a better idea of how to do in general I think, tbd

### Day 4
Scanning around a grid to look for words (it's a word search puzzle). At first I
thought it would be really fast to just scan left/right, up/down, and then use
the diagonal traverse to check for diagonal - it was running but not quite 
right (I know now I was off by about 20 in my real input so I must have missed 
a case). Switched it to check all directions when it finds an 'X' (part 1), then
the same idea for part 2 (but with 'A' instead of 'X', and in the middle instead
of in the start)

EDIT: Added Ocaml solution at lunchtime to get some more practice. Basically
the same as the python solution, but figuring out the recursion traversal was a
bit tricky for me, I was double counting / revisting in the early versions.
Otherwise it's the same, look at each spot, make the word that you find in each
direction starting there (part 1) or centered there (part 2), and then check if
it's the word we're looking for.

### Day 5
Part 1 was checking the conditions to determine which 'updates' were in the
right order - I just looped through and checked them. Part 2 was to sort them
based on the conditions given - I started to implement a topo sort, but noticed
that that updates are all relatively small and had a hunch that I was
overthinking it (again) - so I just sorted them by swapping elements when the
condition was not met, and then repeating until it was sorted, I think it's kind
of bubble sort.
In Ocaml for part 2 - I put the conditions into a hashtable to make it easier to
use them to check if the condition was met, and then sorted using the built-in
sort function and a custom compare function (checking the conditions). I was
originally trying to do that in python too, but I didn't remember how to use a
custom compare function (not just key function) but I get it now - might
re-write it to use that in python too (need to use cmp_to_key from functools)

EDIT: reworked python to use cmp_to_key and a custom compare function for the
sort - it's a lot cleaner and ~5x faster

### Day 6
Part 1 was walking on the grid until an obstacle was hit, and then turning right
until leaving the grid - tracked the path and checked the number of unique
grids visited. Part 2 was running the same walk, but adding one '#' to the grid to see if it makes a cycle. More or less brute forced it except you only need to
try to put obstacles in the path followed by part 1.

I did it in python originally and then in Ocaml - for some reason, my ocaml is
running slower than my python solution... would like to understand that better 
lol.

### Day 7
We have a bunch of expressions like 156: 15 6 - for part 1 the goal is to
figure out if you can get to the number on the left by applying + or * to the
numbers on the right, from left to right. Part 2 is the same, but with a
concatenation op thrown in there.
Honestly couldn't really get going on this one - I went the recursive route
first and I think I as almost there but I had some weird bugs that were tough to
track down, so I switched to do it iteratively. Part 1 has 2 ops, part 2 has 3,
so they have 2^n-1 and 3^n-1 possibilities for the ops in the expression - just
checked them all and if it matched the target number, I added it to the count. I
bet there's a DP solution to this maybe? Will check out the subreddit later, and
revisit this one in Ocaml tomorrow.

EDIT: I realized that I was exiting too early in the recursive soln in stead of
or'ing all the subcases together  - oh well - would have been a bit faster. I
just implemented in ocaml - and IMO it's really nice, honestly should have done
this one in ocaml first, I just like the string manipulation in python better

EDIT2: Read about how others solved and implemented the backwards solution - if
you start from the right and go left you can trim out way more possibilities
and it runs way faster.

### Day 8
This was a cool one - a little bit hard to parse the problem description to be
honest - but it was finding the two locations (antinodes) that were along the 
same slope of each pair of specific points in the grid, as long as each 
"antinode" point was 2 times the distance between one of the points, and 1 
times the distance from the other - I just point 1 + 2 * (dr, dc) and point 2 -
2 * (dr, dc) - where (dr, dc) is the vector between the two points. For part to
is the same idea, but you need to get the all the valid grid points on the line
between them. The trick I think was to get the gcd and then use it to reduce the
slope to make sure you step through all the int grid points on the line. Did it
in Python to start, will do it in Ocaml "tomorrow" (today).

EDIT: did it in ocaml - this was another pretty tricky one for me to translate.

### Day 9
This was a tricky one to get right - for part 1 I read in the data and the moved
two pointers along from start and end, swapping whenever there was an empty spot
left and a full sport right.
Part 2, switched to do it in blocks for each either file or empty spot. For each
file from the right, stuck it into the first block that fits it. Not the most
optimal - but it works. Really didn't see a nice way to do it in ocaml in a
purely fp way, I saw some deque implementations that I might try to copy.

### Day 10
The input was a grid of numbers from 0 to 9 - we had to find (part 1) the number
of distinct 9's that you could reach from 0 while only moving up in value (and  left, right, up, down on the grid). The second part the score for each 0 (starting point) is the number of valid paths that get to a 9, instead of the
number of distinct 9's - actually used the same dfs function for both parts, returned the actual paths and then processed them differently for each part. I did it in Python first, and then in Ocaml - I actually really like the ocaml version this time!