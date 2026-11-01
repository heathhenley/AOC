pub mod day01;

pub type Part = fn(&str) -> String;

pub const DAYS: &[(Part, Part)] = &[(day01::part1, day01::part2)];
