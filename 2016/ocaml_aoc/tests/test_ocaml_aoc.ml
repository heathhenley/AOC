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

let%expect_test "Day 7" =
  Day07.part1 (input_files_path ^ "/day07/sample_input.txt");
  [%expect {| Part 1: 2 |}];
  Day07.part2 (input_files_path ^ "/day07/sample_input_2.txt");
  [%expect {| Part 2: 3 |}]

let%expect_test "Day 8" =
  Day08.part1_internal
    (input_files_path ^ "/day08/sample_input.txt")
    ~rows:3 ~cols:7;
  [%expect
    {|
    Part 1
    Rows: 3, Cols: 7
    Part 1: 6
    Part 2 (read final grid):
    ###....
    ###....
    .......
    |}];

  Day08.part1_internal
    (input_files_path ^ "/day08/sample_input_2.txt")
    ~rows:3 ~cols:7;
  [%expect
    {|
    Part 1
    Rows: 3, Cols: 7
    Part 1: 6
    Part 2 (read final grid):
    .#..#.#
    #.#....
    .#.....
    |}];

  Day08.part2_internal
    (input_files_path ^ "/day08/sample_input.txt")
    ~rows:3 ~cols:7;
  [%expect
    {|
    Part 1
    Rows: 3, Cols: 7
    Part 1: 6
    Part 2 (read final grid):
    ###....
    ###....
    .......
    |}]

let%expect_test "Day 8 - rotate_vector" =
  let v = [| false; false; false; false; true |] in
  print_endline "Before";
  Array.iter (fun b -> print_string (if b then "#" else ".")) v;
  print_endline "";
  let v' = Day08.rotate_vector v 2 in
  print_endline "After";
  Array.iter (fun b -> print_string (if b then "#" else ".")) v';
  print_endline "";
  [%expect {|
    Before
    ....#
    After
    .#...
    |}]

let%expect_test "Day 8 - rotate_vector" =
  let v = [| true; false; false; false; true |] in
  print_endline "Before";
  Array.iter (fun b -> print_string (if b then "#" else ".")) v;
  print_endline "";
  let v' = Day08.rotate_vector v 2 in
  print_endline "After";
  Array.iter (fun b -> print_string (if b then "#" else ".")) v';
  print_endline "";
  [%expect {|
    Before
    #...#
    After
    .##..
    |}]

let%expect_test "Day 8 - count_pixels" =
  let grid =
    [|
      [| true; false; true; false; true |];
      [| false; true; false; true; false |];
      [| true; false; true; false; true |];
    |]
  in
  let count = Day08.count_pixels grid in
  print_endline (string_of_int count);
  [%expect {| 8 |}]

let%expect_test "Day 9 - part 1 - expanded_size" =
  let strs =
    [
      "ADVENT";
      "(1x10)A(1x10)A";
      "(3x3)XYZ";
      "A(1x5)BC";
      "X(8x2)(3x3)ABCY";
      "AAAA(1x20)B";
    ]
  in
  List.iter
    (fun str -> Printf.printf "%s: %d\n" str (Day09.expanded_size str))
    strs;
  [%expect
    {|
    ADVENT: 6
    (1x10)A(1x10)A: 20
    (3x3)XYZ: 9
    A(1x5)BC: 7
    X(8x2)(3x3)ABCY: 18
    AAAA(1x20)B: 24
    |}]

let%expect_test "Day 9 - part 2 - expanded_size_rec" =
  let strs =
    [
      "ADVENT";
      "(1x10)A(1x10)A";
      "X(8x2)(3x3)ABCY";
      "AAAA(1x20)B";
      "(27x12)(20x12)(13x14)(7x10)(1x12)A";
      "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN";
    ]
  in
  List.iter
    (fun str -> Printf.printf "%s: %d\n" str (Day09.expanded_size_rec str))
    strs;
  [%expect
    {|
    ADVENT: 6
    (1x10)A(1x10)A: 20
    X(8x2)(3x3)ABCY: 20
    AAAA(1x20)B: 24
    (27x12)(20x12)(13x14)(7x10)(1x12)A: 241920
    (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN: 445
    |}]

let%expect_test "Day 10 - part 1" =
  Day10.part1_impl (input_files_path ^ "/day10/sample_input.txt") 2 5;
  [%expect {| Part 1: Bot 2 is the one we're looking for |}];
  Day10.part2 (input_files_path ^ "/day10/sample_input.txt");
  [%expect {| Part 2: 30 |}]

let%expect_test "Day 11 - part 1" =
  let state = [| [ "HM"; "LM" ]; [ "HG" ]; [ "LG" ]; [] |] in
  Day11.partn_impl 1 state;
  [%expect {| Part 1: 11 |}]

let%expect_test "Day 12 - part 1" =
  Day12.part1 (input_files_path ^ "/day12/sample_input.txt");
  [%expect {| Part 1: 42 |}]

let%expect_test "Day 12 - part 2" =
  Day12.part2 (input_files_path ^ "/day12/sample_input.txt");
  [%expect {| Part 2: 42 |}]

let%expect_test "Day 13 - shift" =
  Printf.printf "1 has %d set bits" (Day13.num_set_bits 0 1);
  [%expect {| 1 has 1 set bits |}];
  Printf.printf "2 has %d set bits" (Day13.num_set_bits 0 2);
  [%expect {| 2 has 1 set bits |}];
  Printf.printf "3 has %d set bits" (Day13.num_set_bits 0 3);
  [%expect {| 3 has 2 set bits |}];
  Printf.printf "5 has %d set bits" (Day13.num_set_bits 0 5);
  [%expect {| 5 has 2 set bits |}];
  Printf.printf "413 has %d set bits" (Day13.num_set_bits 0 413);
  [%expect {| 413 has 6 set bits |}];
  Printf.printf "2^63 - 1 has %d set bits" (Day13.num_set_bits 0 max_int);
  [%expect {| 2^63 - 1 has 62 set bits |}];
  Day13.part1_impl 10 (1, 1) (7, 4);
  [%expect
    {|
    Start: (1, 1)
    Goal: (7, 4)
    Secrete number: 10
    Part 1: 11
    |}]

let%expect_test "Day 13 - part 2" =
  Day13.part2_impl 10 (1, 1) 50;
  [%expect {| Part 2: 151 |}]
