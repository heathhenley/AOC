let input_files_path = "/mnt/c/dev/aoc/2025/inputs"

let%expect_test "Day 1" =
  Printf.printf "101 wrapped: %d\n" (Day01.Day01_impl.wrap 101);
  [%expect {| 101 wrapped: 1 |}];
  Printf.printf "-1 wrapped: %d\n" (Day01.Day01_impl.wrap (-1));
  [%expect {| -1 wrapped: 99 |}];
  Printf.printf "50 wrapped: %d\n" (Day01.Day01_impl.wrap 50);
  [%expect {| 50 wrapped: 50 |}];
  Printf.printf "-50 wrapped: %d\n" (Day01.Day01_impl.wrap (-50));
  [%expect {| -50 wrapped: 50 |}];
  Printf.printf "100 wrapped: %d\n" (Day01.Day01_impl.wrap 100);
  [%expect {| 100 wrapped: 0 |}];
  Printf.printf "300 clicks left from 0: %d\n"
    (Day01.Day01_impl.count_crossings_left 0 300);
  [%expect {| 300 clicks left from 0: 3 |}];
  let new_pos, loops, zeros = Day01.Day01_impl.rotate ('R', 50) 0 in
  Printf.printf "Rotating R 50 from 0 -> new pos: %d, loops: %d, zeros: %d\n"
    new_pos loops zeros;
  [%expect {| Rotating R 50 from 0 -> new pos: 50, loops: 0, zeros: 0 |}];
  let new_pos, loops, zeros = Day01.Day01_impl.rotate ('L', 50) 0 in
  Printf.printf "Rotating L 50 from 0 -> new pos: %d, loops: %d, zeros: %d\n"
    new_pos loops zeros;
  [%expect {| Rotating L 50 from 0 -> new pos: 50, loops: 0, zeros: 0 |}];
  let new_pos, loops, zeros = Day01.Day01_impl.rotate ('L', 101) 1 in
  Printf.printf "Rotating L 101 from 1 -> new pos: %d, loops: %d, zeros: %d\n"
    new_pos loops zeros;
  [%expect {| Rotating L 101 from 1 -> new pos: 0, loops: 2, zeros: 1 |}];
  Day01.part1 (input_files_path ^ "/day1/sample.txt");
  [%expect {| Part 1: 3 |}];
  Day01.part2 (input_files_path ^ "/day1/sample.txt");
  [%expect {| Part 2: 6 |}]
