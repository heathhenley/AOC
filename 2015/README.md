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