struct Layer {
    pos: u32,
    depth: u32,
}

fn caught(pos: u32, depth: u32) -> bool {
    pos % ((depth - 1) * 2) == 0
}

fn input_to_layers(s: &str) -> Vec<Layer> {
    s.trim()
        .lines()
        .map(|line| {
            let idx = line.find(":").expect("invalid input");
            Layer {
                pos: line[0..idx].trim().parse().expect("failed to parse layer"),
                depth: line[idx + 1..]
                    .trim()
                    .parse()
                    .expect("failed to parse depth"),
            }
        })
        .collect()
}

pub fn part1(s: &str) -> String {
    let layers: Vec<Layer> = input_to_layers(s);
    // might have to deal with the start/end thing? but I think
    // we're "caught" at any layers where the pos % (depth - 1) * 2 == 0
    // 3 --> 4 [0, 4, 8, ...]
    // 2 --> 2 [0, 2, 4, 6, 8, ...]
    // 4 --> 6 [0, 6, 12, 18, ...]
    let severity = layers.into_iter().fold(0, |sev, layer| {
        if caught(layer.pos, layer.depth) {
            return layer.pos * layer.depth + sev;
        }
        sev
    });
    return format!("Part 1: {}", severity);
}

pub fn part2(s: &str) -> String {
    let layers: Vec<Layer> = input_to_layers(s);
    // find the smallest number we can add to each pos so that they are all not 0...
    // todo: is there some math way to figure it out?
    let mut off = 0;
    while layers.iter().any(|l| caught(l.pos + off, l.depth)) {
        off += 1
    }
    return format!("Part 2: {}", off);
}

#[cfg(test)]
mod tests {
    use super::*;

    const EX: &str = "
    0: 3
    1: 2
    4: 4
    6: 4
    ";

    #[test]
    fn p1_ex1() {
        assert_eq!(part1(EX), "Part 1: 24");
    }

    #[test]
    fn p2_ex1() {
        assert_eq!(part2(EX), "Part 2: 10");
    }
}
