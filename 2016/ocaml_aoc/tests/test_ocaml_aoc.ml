let input_files_path = "/mnt/c/dev/aoc/2016/ocaml_aoc/inputs"

let%expect_test "Day 1" =
  Day01.part1 (input_files_path ^ "/day01/sample_input.txt");
  [%expect {|
    Part 1: 8
    |}];
  Day01.part2 (input_files_path ^ "/day01/sample_input.txt");
  [%expect {| Part 2: 4 |}]


let%expect_test "Day 6" =
  Day06.part1 (input_files_path ^ "/day06/sample_input.txt");
  [%expect {|
    Part 1: easter
    |}];
  Day06.part2 (input_files_path ^ "/day06/sample_input.txt");
  [%expect {|
    Part 2: advent
    |}]
  
