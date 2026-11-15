fn rev_section_in_place(nums: &mut [i32], start: usize, stop: usize) {
    let n = nums.len();
    let (mut start, mut stop) = (start, stop);
    while start < stop {
        let real_start = start % n;
        let real_stop = stop % n;
        (nums[real_start], nums[real_stop]) = (nums[real_stop], nums[real_start]);
        start += 1;
        if stop == 0 {
            stop = n
        }
        stop -= 1;
    }
}

fn single_knot_round(
    nums: &[i32],
    lens: &[i32],
    start_pos: usize,
    start_skip: i32,
) -> (Vec<i32>, usize, i32) {
    let mut nums = &mut nums.to_vec();
    let (mut pos, mut skip) = (start_pos, start_skip);
    for &l in lens {
        let len: i32 = l - 1 + (pos as i32);
        assert!(len >= 0);
        rev_section_in_place(&mut nums, pos, len as usize);
        pos += (l + skip) as usize;
        skip += 1;
    }
    (nums.to_vec(), pos, skip)
}

fn part1_internal(s: &str, n: i32) -> i32 {
    let lens: Vec<i32> = s
        .trim()
        .split(',')
        .map(|c| c.parse().expect("should be an int"))
        .collect();
    let nums: Vec<i32> = (0..n).collect();
    let (nums, _, _) = single_knot_round(&nums, &lens, 0, 0);
    nums[0] * nums[1]
}

fn part2_internal(s: &str, n: i32) -> String {
    let lens: Vec<i32> = s.trim().chars().map(|c| c as i32).collect();
    let fixed = vec![17, 31, 73, 47, 23];
    let lens = [lens, fixed.clone()].concat();

    // 64 rounds...
    let (mut skip, mut pos) = (0, 0);
    let mut nums: Vec<i32> = (0..n).collect();
    for _ in 0..64 {
        // run round
        (nums, pos, skip) = single_knot_round(&nums, &lens, pos, skip);
    }
    nums.chunks(16)
        .map(|chunk| chunk.iter().fold(0, |acc, val| acc ^ val))
        .map(|n| format!("{:02x}", n))
        .collect()
}

pub fn part1(s: &str) -> String {
    let res = part1_internal(s, 256);
    return format!("Part 1: {}", res);
}

pub fn part2(s: &str) -> String {
    let res = part2_internal(s, 256);
    return format!("Part 2: {}", res);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_ex1() {
        assert_eq!(part1_internal("3,4,1,5", 5), 12);
    }

    #[test]
    fn p2_ex1() {
        assert_eq!(
            part2_internal("1,2,3", 256),
            "3efbe78a8d82f29979031a4aa0b16a9d"
        );
        assert_eq!(part2_internal("", 256), "a2582a3a0e66e6e86e3812dcb672a272");
        assert_eq!(part2_internal("AoC 2017", 256), "33efeb34ea91902bb2f59c9920caa6cd");
    }
}
