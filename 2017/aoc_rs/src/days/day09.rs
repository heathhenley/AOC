fn process(chars: &[char], lb: i32, lc: i32, sc: i32, gb: i32) -> (i32, i32) {
    // TODO: doesn't work in debug need to switch to loop (stack overflow)
    // works in release probably gets optimized to loop
    match chars {
        [] => (sc, gb),
        [c, rest @ ..] if *c == '{' => {
            if lc > 0 {
                return process(rest, lb, lc, sc, gb + 1);
            }
            process(rest, lb + 1, lc, sc, gb)
        }
        [c, rest @ ..] if *c == '}' => {
            if lc > 0 {
                return process(rest, lb, lc, sc, gb + 1);
            }
            process(rest, lb - 1, lc, sc + lb, gb)
        }
        [c, rest @ ..] if *c == '<' => {
            if lc > 0 {
                return process(rest, lb, lc, sc, gb + 1);
            }
            process(rest, lb, lc + 1, sc, gb)
        }
        [c, rest @ ..] if *c == '>' => process(rest, lb, lc - 1, sc, gb),
        [c, rest @ ..] if *c == '!' => process(&rest[1..], lb, lc, sc, gb),
        [_, rest @ ..] => {
            if lc > 0 {
                return process(rest, lb, lc, sc, gb + 1);
            }
            process(rest, lb, lc, sc, gb)
        }
    }
}

pub fn part1(s: &str) -> String {
    let chars: Vec<char> = s.trim().chars().collect();
    let (sc, _) = process(&chars, 0, 0, 0, 0);
    return format!("Part 1: {}", sc);
}

pub fn part2(s: &str) -> String {
    let chars: Vec<char> = s.trim().chars().collect();
    let (_, garb) = process(&chars, 0, 0, 0, 0);
    return format!("Part 2: {}", garb);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_ex1() {
        assert_eq!(part1("{}"), "Part 1: 1");
        assert_eq!(part1("{{{}}}"), "Part 1: 6");
        assert_eq!(part1("{{}{}}"), "Part 1: 5");
        assert_eq!(part1("{<a>,<a>,<a>,<a>}"), "Part 1: 1");
        assert_eq!(part1("{{<ab>},{<ab>},{<ab>},{<ab>}}"), "Part 1: 9");
        assert_eq!(part1("{{<a!>},{<a!>},{<a!>},{<ab>}}"), "Part 1: 3");
    }

    #[test]
    fn p2_ex1() {
        assert_eq!(part2("<>"), "Part 2: 0");
        assert_eq!(part2("<random characters>"), "Part 2: 17");
        assert_eq!(part2("<{!>}>"), "Part 2: 2");
        assert_eq!(part2("<{o\"i!a,<{i<a>,"), "Part 2: 10");
    }
}
