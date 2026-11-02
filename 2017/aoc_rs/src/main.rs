use std::time::{Duration, Instant};

use aoc_rs::days::DAYS;

fn timeit<T>(f: impl FnOnce() -> T) -> (T, Duration) {
    let start = Instant::now();
    let res = f();
    (res, start.elapsed())
}

fn main() {
    let day: usize = std::env::args()
        .nth(1)
        .expect("usage: aoc_rs <day>")
        .parse()
        .expect("day must be a number");

    let &(p1, p2) = day
        .checked_sub(1)
        .and_then(|i| DAYS.get(i))
        .unwrap_or_else(|| panic!("day not impl'd"));

    let path = format!("inputs/{day:02}.txt");
    let input =
        std::fs::read_to_string(&path).unwrap_or_else(|e| panic!("couldn't read file {path}: {e}"));

    for part in [p1, p2] {
        let (res, time) = timeit(|| part(&input));
        println!("{res} ({time:.2?})");
    }
}
