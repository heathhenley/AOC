# 2016 Advent of Code

## Day 1: No Time for a Taxicab
Unreasonable struggles with the first problem, part 1 was super easy, part 2
was tough to track the visited locations recursively. I spent way too much time
trying to figure it out, eventually wrote it in Python in like 5 minutes and
then used that as a guide (even though I didn't use functional programming in
Python).

## Day 2: Bathroom Security
Moved around in the keypad checking that the move was valid - for practice I
switched my original python soln to be totally functional and then translated it
to ocaml.

## Days 2-8
Mostly been straightforward so far but fun to do in OCaml.

### Day 9: Explosives in Cyberspace
This was similar to one of the stones problems from 2024 - I gambled on not
actually making the string for part 1 and just computing the length and that
helped (part 2 would blow up otherwise but can might be able to be memod)

### Day 10: Balance Bots
Got stuck on part 2 for a while, got some AI guidance to get it working. I can
see how to to do it with a simple queue/stack and while loop but I really wanted
to get it to work recursively. I'm really not happy with it in this case and I
think it's probably way more readable to do it with a stack and loop.. Eg any
bots with two values get put in the queue and then processed one at a time - as
the rules are applied, if applying the rule results in a bot with two values,
it gets put back in the queue. For processing, otherwise the bot or output just
gets updated and we move on. We're doing the same in the recursive solution but
it's super hard to read and debug and it hurt my head. Maybe I modeled the
/ state / types / problem incorrectly... Might come back to it and switch to an
iterative solution to compare.
