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