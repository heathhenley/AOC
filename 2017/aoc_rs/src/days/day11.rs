// using coord system in https://www.redblobgames.com/grids/hexagons/
#[derive(Debug, Clone)]
struct Cube {
    q: i32,
    r: i32,
    s: i32,
}

fn direction_diff(dir: &str) -> Cube {
    match dir {
        "n" => Cube { q: 0, r: -1, s: 1 },
        "ne" => Cube { q: 1, r: -1, s: 0 },
        "se" => Cube { q: 1, r: 0, s: -1 },
        "s" => Cube { q: 0, r: 1, s: -1 },
        "sw" => Cube { q: -1, r: 1, s: 0 },
        "nw" => Cube { q: -1, r: 0, s: 1 },
        s => panic!("Unexpected direction! {s}"),
    }
}

fn add(a: &Cube, b: &Cube) -> Cube {
    Cube {
        q: a.q + b.q,
        r: a.r + b.r,
        s: a.s + b.s,
    }
}

fn sub(a: &Cube, b: &Cube) -> Cube {
    Cube {
        q: a.q - b.q,
        r: a.r - b.r,
        s: a.s - b.s,
    }
}

fn abs(a: &Cube) -> Cube {
    Cube {
        q: a.q.abs(),
        r: a.r.abs(),
        s: a.s.abs(),
    }
}

fn dist(a: &Cube, b: &Cube) -> i32 {
    let vec = sub(&a, &b);
    let abs_vec = abs(&vec);
    abs_vec.q.max(abs_vec.r.max(abs_vec.s))
}

pub fn part1(s: &str) -> String {
    let start = Cube { q: 0, r: 0, s: 0 };
    let (pos, _) = s
        .trim()
        .split(",")
        .fold((start.clone(), i32::MIN), |(curr, max_d), mov| {
            let step_dir = direction_diff(mov);
            (add(&curr, &step_dir), max_d.max(dist(&curr, &start)))
        });
    return format!("Part 1: {}", dist(&start, &pos));
}

pub fn part2(s: &str) -> String {
    let start = Cube { q: 0, r: 0, s: 0 };

    let (_, max_d) = s
        .trim()
        .split(",")
        .fold((start.clone(), i32::MIN), |(curr, max_d), mov| {
            let step_dir = direction_diff(mov);
            (add(&curr, &step_dir), max_d.max(dist(&curr, &start)))
        });

    return format!("Part 2: {}", max_d);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_ex1() {
        assert_eq!(part1("ne,ne,ne"), "Part 1: 3");
        assert_eq!(part1("ne,ne,sw,sw"), "Part 1: 0");
        assert_eq!(part1("ne,ne,s,s"), "Part 1: 2");
        assert_eq!(part1("se,sw,se,sw,sw"), "Part 1: 3");
    }
}
