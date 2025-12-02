# Advent of Code 2025
## using OCaml ( and maybe other languages )

## Day 1
Nice start to the year! Straightforward and fun to do in OCaml - had some silly
mistakes with the counting logic for part 2 to sort out.

### Day 2
Mostly straightforward again - had a lot of weird trouble just getting the input
parsed etc but that's just an Ocaml-with-no-autocompletion problem. The first
approach was split the string for part 1 and compare the halves. Then for part 2
I used a pretty simple regex with capture group and backref to check if it was
made entirely of repeating digits.

I tried to switch away from string manipulation and use math instead, which made part 1 faster but part 2 slower. So, I landed on a using math for part 1
and a regex for part 2 🤷‍♂️
