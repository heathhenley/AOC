fn min_max_diff(nums: &[i32]) -> i32 {
    let (min, max) = nums.iter().fold((i32::MAX, i32::MIN), |(mn, mx), &num| {
        (mn.min(num), mx.max(num))
    });
    max - min
}

fn even_div(nums: &[i32]) -> i32 {
    let n = nums.len();
    for i in 0..n {
        for j in 0..n {
            if i != j && nums[i] % nums[j] == 0 {
                return nums[i] / nums[j];
            }
        }
    }
    unreachable!("if input is valid...")
}

fn solve(s: &str, f: fn(&[i32]) -> i32) -> i32 {
    s.lines()
        .map(|line| {
            line.split_whitespace()
                .filter_map(|n| n.parse().ok())
                .collect::<Vec<_>>()
        })
        .map(|row| f(&row))
        .sum()
}

pub fn part1(s: &str) -> String {
    let res = solve(s, min_max_diff);
    return format!("Part 1: {res}");
}

pub fn part2(s: &str) -> String {
    let res = solve(s, even_div);
    return format!("Part 2: {res}");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_row() {
        assert_eq!(min_max_diff(&[5, 1, 9, 5]), 8);
        assert_eq!(min_max_diff(&[7, 5, 3]), 4);
        assert_eq!(min_max_diff(&[2, 4, 6, 8]), 6);
    }

    #[test]
    fn p1_ex() {
        assert_eq!(
            part1(
                "5 1 9 5
                 7 5 3
                 2 4 6 8"
            ),
            "Part 1: 18"
        );
    }

    #[test]
    fn p2_row() {
        assert_eq!(even_div(&[5, 9, 2, 8]), 4);
        assert_eq!(even_div(&[9, 4, 7, 3]), 3);
        assert_eq!(even_div(&[3, 8, 6, 5]), 2);
    }

    #[test]
    fn p2_ex() {
        assert_eq!(
            part2(
                "5 9 2 8
                 9 4 7 3
                 3 8 6 5"
            ),
            "Part 2: 9"
        );
    }
}
