fn process(chars: &[char]) -> (i32, i32) {
    let mut lb = 0;
    let mut lc = 0;
    let mut sc = 0;
    let mut gb = 0;
    let mut ch = chars;
    loop {
        ch = match ch {
            [] => return (sc, gb),
            ['{', rest @ ..] => {
                if lc > 0 {
                    gb = gb + 1;
                } else {
                    lb = lb + 1;
                }
                rest
            }
            ['}', rest @ ..] => {
                if lc > 0 {
                    gb += 1;
                } else {
                    sc += lb;
                    lb -= 1;
                }
                rest
            }
            ['<', rest @ ..] => {
                if lc > 0 {
                    gb += 1;
                } else {
                    lc += 1;
                }
                rest
            }
            ['>', rest @ ..] => {
                lc -= 1;
                rest
            }
            ['!', _, rest @ ..] => rest,
            [_, rest @ ..] => {
                if lc > 0 {
                    gb += 1;
                }
                rest
            }
        };
    }
}

pub fn part1(s: &str) -> String {
    let chars: Vec<char> = s.trim().chars().collect();
    let (sc, _) = process(&chars);
    return format!("Part 1: {}", sc);
}

pub fn part2(s: &str) -> String {
    let chars: Vec<char> = s.trim().chars().collect();
    let (_, garb) = process(&chars);
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
