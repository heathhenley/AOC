fn solve(nums: &Vec<u32>, step: usize) -> u32 {
    let n = nums.len();
    let mut sum = 0;
    for (idx, &num) in nums.iter().enumerate() {
        let next = (idx + step) % n; // wrap around
        if num == nums[next] {
            sum += num;
        }
    }
    sum
}

pub fn part1(s: &str) -> String {
    let nums: Vec<u32> = s.trim().chars().map(|c| c.to_digit(10).unwrap()).collect();
    let res = solve(&nums, 1);
    return format!("Part 1: {res}");
}

pub fn part2(s: &str) -> String {
    let nums: Vec<u32> = s.trim().chars().map(|c| c.to_digit(10).unwrap()).collect();
    let step = nums.len() / 2;
    let res = solve(&nums, step);
    return format!("Part 2: {res}");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_ex1() {
        assert_eq!(part1("1122"), "Part 1: 3");
        assert_eq!(part1("1111"), "Part 1: 4");
        assert_eq!(part1("1234"), "Part 1: 0");
        assert_eq!(part1("91212129"), "Part 1: 9");
    }

    #[test]
    fn p2_ex2() {
        assert_eq!(part2("1212"), "Part 2: 6");
        assert_eq!(part2("1221"), "Part 2: 0");
        assert_eq!(part2("123425"), "Part 2: 4");
        assert_eq!(part2("123123"), "Part 2: 12");
        assert_eq!(part2("12131415"), "Part 2: 4");
    }
}
