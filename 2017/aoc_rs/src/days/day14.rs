use crate::days::day10::knot_hash;
use hex;

pub fn part1(s: &str) -> String {
    let res = (0..128).fold(0, |ones, i| {
        let hash = knot_hash(format!("{}-{}", s.trim(), i).as_str());
        // don't remember hamming weight and don't fell like looking it up
        // literally make the binary string and count ones
        hex::decode(hash)
            .expect("failed to decode, input probably wrong")
            .into_iter()
            .fold(String::new(), |bin_str, d| format!("{}{:08b}", bin_str, d))
            .chars()
            .fold(0, |acc, c| {
                if c == '1' {
                    return acc + 1;
                }
                acc
            })
            + ones
    });
    return format!("Part 1: {}", res);
}

pub fn part2(_: &str) -> String {
    return format!("Part 2: {}", 0);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_ex1() {
        assert_eq!(part1("flqrgnkx"), "Part 1: 8108");
    }
}
