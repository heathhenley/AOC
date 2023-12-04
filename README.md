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
many copies their are of that card.