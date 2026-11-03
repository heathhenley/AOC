fn step(pos: &(i32, i32), dir: i32) -> (i32, i32) {
    let &(x, y) = pos;
    match dir {
        1 => (x + 1, y), // right
        2 => (x, y + 1), // up
        3 => (x - 1, y), // left
        4 => (x, y - 1), // down
        _ => unreachable!("unsupported direction, you seem lost"),
    }
}

fn spiral_index_to_2d(target_idx: u32) -> (i32, i32) {
    let mut position = (0, 0);
    let mut idx = 1;
    let mut seg_max = 1;
    let mut seg_count = 0;
    let mut points_in_seg = 0;
    let mut current_dir = 1;
    while idx != target_idx {
        // take a step in direction dir
        position = step(&position, current_dir);
        idx += 1;

        // update segment tracking
        points_in_seg += 1;
        if points_in_seg >= seg_max {
            // completed a seg
            seg_count += 1;
            if seg_count >= 2 {
                // bump to next len
                seg_max += 1;
                seg_count = 0;
            }
            points_in_seg = 0;
            // rotate for next time, we completed a seg
            current_dir = current_dir % 4 + 1;
        }
    }
    position
}

pub fn part1(s: &str) -> String {
    let (x, y) = spiral_index_to_2d(s.trim().parse().expect("input should be an int"));
    let d = x.abs() + y.abs();
    return format!("Part 1: {}", d);
}

pub fn part2(_: &str) -> String {
    return "Part 2: 0".to_string();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_ex() {
        assert_eq!(part1("1"), "Part 1: 0");
        assert_eq!(part1("12"), "Part 1: 3");
        assert_eq!(part1("23"), "Part 1: 2");
        assert_eq!(part1("1024"), "Part 1: 31");
    }
}
