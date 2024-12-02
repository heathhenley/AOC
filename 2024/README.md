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
