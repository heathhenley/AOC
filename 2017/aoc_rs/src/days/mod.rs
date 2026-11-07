// TODO - this stuff possible with a macro? (or script it?)
pub mod day01;
pub mod day02;
pub mod day03;
pub mod day04;
pub mod day05;

pub type Part = fn(&str) -> String;

pub const DAYS: &[(Part, Part)] = &[
    (day01::part1, day01::part2),
    (day02::part1, day02::part2),
    (day03::part1, day03::part2),
    (day04::part1, day04::part2),
    (day05::part1, day05::part2),
];
