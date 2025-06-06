# AOC 2015
## Advent of Code 2015 (after the event)
### Day 1: Not Quite Lisp
This was straight forward, the easiest way is a running count - `(` is +1, `)`
is -1. The first part is just the sum of the counts, the second part is the
position of the first time the count is -1.

Using it as a chance to learn go, but after solving in python.

Also went back to do this in Ocaml - man that's a mind f for me. I think what
takes me 2 minutes in took me 2 hours in Ocaml, but gotta start somewhere.

### Day 2: I Was Told There Would Be No Math
This was also straight forward, just calculating what it asked for. Good
practice for reading files and parsing strings in Go, I finished Python in a few
minutes, but then spent quite a while trying how to split / parse / convert etc
in Go - but that's to be expected on day 2 of using GO.

UPDATE: went back to do this in Ocaml - starting to make more sense but it's
still hard to do everything without iteration. Also got my env set up correctly
now so that vscode is working with ocaml-lsp ✅

### Day 3: Perfectly Spherical Houses in a Vacuum
Basically just walked a path and marked houses as visited.

### Day 4: The Ideal Stocking Stuffer
Straightforward 'mining' with different difficulty levels. Would have been
harder to implement md5 from scratch but I'm not really interested in that.

### Day 5: Doesn't He Have Intern-Elves For This?
Checking whether strings meet certain criteria, this also felt straight
forward, in python at least. I'm going to have more trouble in go _I think_.
--> UPDATE: go wasn't bad because it has strings.Contains and strings.Count - so
very similar to python here. I expected it to have nothing 🤷‍♂️

### Day 6: Probably a Fire Hazard
Hardest part of this one was parsing the input - skipping go for this one, I get
it, don't feel like I would gain anything by doing this one in go. Might start
using go first...

### Day 7: Some Assembly Required
There must be a nice way to do this, I got it work but just iterating and
resolving operations until there were all integers left. I guess you could start
with the input nodes, and push anything that depends on them to a queue, and so
on, and then resolve in order so you don't have to do weird iterations and
checking.

UPDATE: Got it set up with the recursive solution, way cleaner - but I bet it
would hit a wall with a larger input and would have to be rewritten to be
iterative again. Wish I had thought of that first as it's much nicer and was
a bit easier to debug.

### Day 8: Matchsticks
This was straight forward - got python done in a few minutes and then took a
while to get go working, just because I'm not familiar with regexp, escaping,
etc, in go yet. Python you can also eval the string in the first part to get
the printed version, so it was a little easier to fly through that part in 
python. In go I just actually replaced the necessary characters and then took
the differences.

### Day 9: All in a Single Night
This was fun! Wondering when we would see some path finding type questions, I've
only completed 2023 and there were a lot in there. I used a dfs to find all the
paths that went through all nodes just once and tracked the min / max distances,
and tried starting from each node (it allowed starting from any node).

### Day 10: Elves Look, Elves Say
This was easy, but a good one to get me more go practice, especially with
strings. Go version is ~9x faster than python.

### Day 11: Corporate Policy
Boom! Did this on in Ocaml first - took quite a while to get it tbh, but mostly
it was really tedious to get all the checks right.

I looked at the the password as a base 26 number so the approach is:
1. convert to a base 10 number
2. increment by 1
3. convert back to base 26
4. check if it meets the criteria
There a lot of conversions so it's not efficient at all, but it works and the 
Ocaml syntax and the FP approach in general are both starting to come together 
for me.

### Day 12: JSAbacusFramework.io
This was straight forward but good to get more practice with recursion.

### Day 13: Knights of the Dinner Table
Got all the permutations and then calculated the happiness for each, nothing too
fancy.

### Day 14: Reindeer Olympics
Can calculate the distance for each reindeer using a cycle for part 1, but for
part 2 I had to just simulate it because of the scoring system.

### Day 15: Science for Hungry People
Brute forced this one too - though I looked at how you could set it up as an
optimization problem - it works to solve the continuous case and then round -
but it's sensitive to the initial guess. It's small enough that brute force is
fine.

### Day 16
This was also straight forward, parsing and checking the criteria.

## Day 17: No Such Thing as Too Much
This is the coin change problem, part two is a slight variation on it. I did it
using top down recursion, don't need to memoize because the input is small.

# Day 19: Medicine for Rudolph
This was was kind of hard - the first part was straight forward, but the second
part was tricking - tried to brute force it and that was really bad. Went back-
wards instead (start with the target molecule) and that turned out to be the
way to do it.

# Day 20: Infinite Elves and Infinite Houses
Did this one by getting all the factors of the number and using them to compute
the gifts for each house. Had some issues with the logic for part 2 - I was
trying to build it into the factor function, but in the end it was easier to get
all the factors and then filter the ones that were too big out.

# Day 21: RPG Simulator 20XX
This was super brutal but mostly because I had mistake in the "who won" logic -
naturally I didn't think it was there and it was subtle enough that it didn't
happen all the time, so that took quite a while to debug. Also some silly things
due to not understanding ocaml well yet - but got it done!
Solved by recursively making all the possible choices, and then checking them,
memoizing the results helped a ton.

# Day 22: Wizard Simulator 20XX
This was pretty tedious to debug but managed to get it working. Chose to switch
back to python again for this one. The same type game as Day 21, except you
have spells that you can choose from and they have different effects. So it
sort of makes a tree of all the possible choices you can make with recursion.
The key optimization that makes it not take forever is to exit early if you
have already spent more mana than the current minimum - there's no need to play
out the rest of those games.

# Day 23: Opening the Turing Lock
This one is a mini assembly language - it was good practice to do some pattern
matching in Ocaml.

# Day 24: It Hangs in the Balance
In this one you have a list of presents that are all some weight - they need
to be split into 3 evenly weighted groups. We are interested in the single group
with the least number of presents in it, when there are more than one way to
have the minimum number of presents, we want the one with the smallest product.

I first tried to generate all the possible combinations of presents in different
groups - but this is actually not needed. You can just generate combinations
that sum to the target weight and then filter for the ones that we're interested
in (the smallest number, etc). The other groups don't actually matter.

# Day 25: Let It Snow
Calculated the next number and next row / col each time - just stopping when
the target row / col was reached. I made the mistake of trying to actually store
it at first, and that was getting complicated - wasn't needed at all though.