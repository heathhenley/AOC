use std::collections::HashSet;

fn maxi(a: &[i32]) -> (usize, i32) {
    a.iter().enumerate().fold((0, i32::MIN), |acc, (idx, &v)| {
        if v > acc.1 {
            return (idx, v);
        }
        acc
    })
}

fn find_cycle(blocks: &[i32]) -> (i32, Vec<i32>) {
    let mut blocks = blocks.to_vec();
    let n = blocks.len();
    let mut hs = HashSet::new();
    let mut count = 0;
    while hs.insert(blocks.clone()) {
        let (idx, block) = maxi(&blocks);
        blocks[idx] = 0;
        for i in (idx + 1)..=(idx + block as usize) {
            blocks[i % n] += 1;
        }
        count += 1;
    }
    (count, blocks)
}

pub fn part1(s: &str) -> String {
    let blocks: Vec<i32> = s
        .trim()
        .split_whitespace()
        .map(|n| n.parse().expect("should be an int"))
        .collect();
    let (count, _) = find_cycle(&blocks);
    return format!("Part 1: {count}");
}

pub fn part2(s: &str) -> String {
    let mut blocks: Vec<i32> = s
        .trim()
        .split_whitespace()
        .map(|n| n.parse().expect("should be an int"))
        .collect();
    (_, blocks) = find_cycle(&blocks);
    let (count, _) = find_cycle(&blocks);
    return format!("Part 2: {count}");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_ex1() {
        assert_eq!(part1("0 2 7 0"), "Part 1: 5");
    }
}
