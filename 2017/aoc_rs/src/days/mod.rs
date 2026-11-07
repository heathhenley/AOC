macro_rules! days {
    ($($day:ident),* $(,)?) => {
        $(pub mod $day;)*

        pub type Part = fn(&str) -> String;

        pub const DAYS: &[(Part, Part)] = &[
            $(($day::part1, $day::part2),)*
        ];
    };
}

days!(day01, day02, day03, day04, day05, day06);
