let input_files_path = "/mnt/c/dev/aoc/2025/inputs"

let%expect_test "Day 1" =
  Day01.part1 (input_files_path ^ "/day1/sample.txt");
  [%expect {| Part 1: 3 |}];
  Day01.part2 (input_files_path ^ "/day1/sample.txt");
  [%expect {| Part 2: 6 |}]
