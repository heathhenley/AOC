use std::collections::HashMap;

#[derive(Clone, Debug, Copy)]
enum Dir {
    Up,
    Left,
    Right,
    Down,
}

impl Dir {
    pub fn turn_left(self) -> Self {
        match self {
            Dir::Right => Dir::Up,
            Dir::Up => Dir::Left,
            Dir::Left => Dir::Down,
            Dir::Down => Dir::Right,
        }
    }
    pub fn to_delta(self) -> (i32, i32) {
        match self {
            Dir::Right => (1, 0),
            Dir::Up => (0, 1),
            Dir::Left => (-1, 0),
            Dir::Down => (0, -1),
        }
    }
}

struct Spiral {
    position: (i32, i32),
    seg_max: i32,
    seg_count: i32,
    points_in_seg: i32,
    direction: Dir,
}

impl Spiral {
    pub fn new() -> Self {
        Spiral {
            position: (0, 0),
            seg_max: 1,
            seg_count: 0,
            points_in_seg: 0,
            direction: Dir::Right,
        }
    }
}

impl Iterator for Spiral {
    type Item = (i32, i32);

    fn next(&mut self) -> Option<Self::Item> {
        let current = self.position;
        // take a step in direction dir
        let (dx, dy) = self.direction.to_delta();
        self.position = (self.position.0 + dx, self.position.1 + dy);

        // update segment tracking
        self.points_in_seg += 1;
        if self.points_in_seg >= self.seg_max {
            // completed a seg
            self.seg_count += 1;
            if self.seg_count >= 2 {
                // bump to next len
                self.seg_max += 1;
                self.seg_count = 0;
            }
            self.points_in_seg = 0;
            // rotate for next time, we completed a seg
            self.direction = self.direction.turn_left();
        }
        Some(current)
    }
}

fn neighbors((x, y): &(i32, i32)) -> Vec<(i32, i32)> {
    [
        (0, 1),
        (1, 0),
        (-1, 0),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, -1),
        (-1, 1),
    ]
    .iter()
    .map(|(dx, dy)| (x + dx, y + dy))
    .collect()
}

pub fn part1(s: &str) -> String {
    let n: usize = s.trim().parse().expect("input should be an int");
    let (x, y) = Spiral::new().nth(n - 1).unwrap();
    let d = x.abs() + y.abs();
    return format!("Part 1: {}", d);
}

pub fn part2(s: &str) -> String {
    let n: u32 = s.trim().parse().expect("input should be an int");
    let mut grid: HashMap<(i32, i32), u32> = HashMap::new();
    grid.insert((0, 0), 1);
    let res = Spiral::new()
        .skip(1)
        .map(|pt| {
            let v = neighbors(&pt).iter().filter_map(|pt| grid.get(pt)).sum();
            grid.insert(pt, v);
            v
        })
        .find(|&v| v > n)
        .unwrap();

    return format!("Part 2: {}", res);
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

    #[test]
    fn p2_ex() {
        assert_eq!(part2("1"), "Part 2: 2");
        assert_eq!(part2("4"), "Part 2: 5");
        assert_eq!(part2("5"), "Part 2: 10");
        assert_eq!(part2("25"), "Part 2: 26");
    }
}
