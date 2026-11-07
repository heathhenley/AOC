fn solve(instr: &mut [i32], update_fn: fn(offset: i32) -> i32) -> usize {
    let mut ptr: i32 = 0;
    let mut counter: usize = 0;
    let n = instr.len() as i32;

    while ptr >= 0 && ptr < n {
        let offset = instr[ptr as usize];
        instr[ptr as usize] += update_fn(offset);
        ptr += offset;
        counter += 1;
    }
    counter
}

pub fn part1(s: &str) -> String {
    let mut instructions: Vec<i32> = s
        .trim()
        .lines()
        .into_iter()
        .map(|line| line.trim().parse().expect("should be an int"))
        .collect();
    let res = solve(&mut instructions, |_| 1);
    return format!("Part 1: {res}");
}

pub fn part2(s: &str) -> String {
    let mut instructions: Vec<i32> = s
        .trim()
        .lines()
        .into_iter()
        .map(|line| line.trim().parse().expect("should be an int"))
        .collect();
    let res = solve(&mut instructions, |offset| {
        if offset >= 3 {
            return -1;
        }
        1
    });
    return format!("Part 2: {res}");
}

#[cfg(test)]
mod tests {
    use super::*;

    const EX1: &str = "
    0
    3
    0
    1
    -3
    ";

    #[test]
    fn p1_ex1() {
        assert_eq!(part1(EX1), "Part 1: 5");
    }

    #[test]
    fn p2_ex1() {
        assert_eq!(part2(EX1), "Part 2: 10");
    }
}
