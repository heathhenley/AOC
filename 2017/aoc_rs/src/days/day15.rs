const MOD: u64 = 2147483647;
const FORTY_MIL: usize = 40_000_000;
const FIVE_MIL: usize = 5_000_000;
const MASK: u64 = (1 << 16) - 1;

struct Generator {
    fact: u64,
    div: u64,
    current: u64,
}

impl Generator {
    fn new(fact: u64, div: u64, current: u64) -> Self {
        Generator { fact, div, current }
    }
}

impl Iterator for Generator {
    type Item = u64;

    fn next(&mut self) -> Option<Self::Item> {
        let mut val;
        loop {
            val = (self.current * self.fact) % MOD;
            self.current = val;
            if val % self.div == 0 {
                return Some(val);
            }
        }
    }
}

pub fn part1(s: &str) -> String {
    let seeds = s
        .trim()
        .lines()
        .map(|line| {
            line.split_whitespace()
                .last()
                .expect("bad input, empty line")
                .parse()
                .expect("expected int")
        })
        .collect::<Vec<u64>>();
    assert!(seeds.len() == 2, "should only be two");

    let gen_a = Generator::new(16807, 1, seeds[0]);
    let gen_b = Generator::new(48271, 1, seeds[1]);

    let res = gen_a.zip(gen_b).take(FORTY_MIL).fold(0, |acc, (a, b)| {
        if (a & MASK) == (b & MASK) {
            return acc + 1;
        }
        acc
    });
    return format!("Part 1: {}", res);
}

pub fn part2(s: &str) -> String {
    let seeds = s
        .trim()
        .lines()
        .map(|line| {
            line.split_whitespace()
                .last()
                .expect("bad input, empty line")
                .parse()
                .expect("expected int")
        })
        .collect::<Vec<u64>>();
    assert!(seeds.len() == 2, "should only be two");

    let gen_a = Generator::new(16807, 4, seeds[0]);
    let gen_b = Generator::new(48271, 8, seeds[1]);

    let res = gen_a.zip(gen_b).take(FIVE_MIL).fold(0, |acc, (a, b)| {
        if (a & MASK) == (b & MASK) {
            return acc + 1;
        }
        acc
    });
    return format!("Part 2: {}", res);
}

#[cfg(test)]
mod tests {
    use super::*;

    const EX: &str = "
    Generator A starts with 65
    Generator B starts with 8921
    ";

    #[test]
    fn p1_ex1() {
        assert_eq!(part1(EX), "Part 1: 588");
    }
    #[test]
    fn p2_ex1() {
        assert_eq!(part2(EX), "Part 2: 309");
    }
}
