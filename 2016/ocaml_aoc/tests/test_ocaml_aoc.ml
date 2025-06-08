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
