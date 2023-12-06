# Advent of Code 2023
## using Python

### Day 1:
I just slammed out some gross python code, that second
part was tough.

### Day 2:
This felt a little easier than day one to me, but there
was more to parse out correctly. I made the script less
gross this time.

### Day 3:
This was brutal! I basically brute forced it - and the
approach I took worked, but I had some weird edge cases
and bugs to figure out. In particular, I had one bug
that missed a single gear in my input data, and I spent
a while tracking it down. It was related to the number
being adjacent to the symbol and also being the last
number in the line. 🤦‍♂️

There's probably a really nice sliding window approach
that would make more sense for this problem, looking
forward to seeing other solutions.

### Day 4:
This one was pretty easy, not complaining though! For part
one I used a dictionary to track the count of winning numbers
and then added their count to the match count for each of the
numbers we had in the winning set. For part two, I used
another dictionary to track the current count of cards, when
cards win they update their count in the dictionary by however
many copies there are of that card.

### Day 5:
I had a lot of trouble with the second part of this one. First
was only a few minutes, but the second part couldn't be brute
forced, at least in the time that I had. I ended up looking
at the subreddit for help... we have to move through the maps
in ranges instead, which is no big deal if the seed range doesn't
overlap the map range. If it's overlapping, you can split it into
two ranges, map the overlapping range through the map, and leave
non overlapping ranges alone. It's day 5! I'm a little scared for
the rest of the month. 😅
