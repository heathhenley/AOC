use aoc_rs::days::DAYS;

fn main() {
    let day: usize = std::env::args().nth(1).unwrap().parse().unwrap();
    let input = std::fs::read_to_string(format!("inputs/{day:02}.txt")).unwrap();
    let (p1, p2) = DAYS[day - 1];
    println!("{}\n{}", p1(&input), p2(&input));
}
