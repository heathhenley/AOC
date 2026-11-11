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

fn part1_internal(s: &str, n: i32) -> i32 {
    let lens: Vec<i32> = s
        .trim()
        .split(',')
        .map(|c| c.parse().expect("should be an int"))
        .collect();

    let (mut pos, mut skip): (usize, i32) = (0, 0);
    let mut nums: Vec<i32> = (0..n).collect();

    for &l in &lens {
        // rev len of nums
        //println!("{nums:?}");
        let len: i32 = l - 1 + (pos as i32);
        assert!(len >= 0);
        rev_section_in_place(&mut nums, pos, len as usize);
        //println!("{nums:?}");
        // increment skip and pos
        pos += (l + skip) as usize;
        skip += 1;
    }
    nums[0] * nums[1]
}

pub fn part1(s: &str) -> String {
    let res = part1_internal(s, 256);
    return format!("Part 1: {}", res);
}

pub fn part2(_: &str) -> String {
    return "Part 2: 0".to_string();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_ex1() {
        assert_eq!(part1_internal("3,4,1,5", 5), 12);
    }
}
