module Day03_impl = struct

  let part1 filename =
    let file_contents = Utils.Input.read_file_to_string filename in
    let lines = Utils.Input.split_on_newline file_contents in
    Printf.printf "Part 1: %d\n" (List.length lines)

  let part2 filename =
    let file_contents = Utils.Input.read_file_to_string filename in
    let lines = Utils.Input.split_on_newline file_contents in
    Printf.printf "Part 2: %d\n" (List.length lines)

end

module Day03 : Solution.Day = Day03_impl
include Day03_impl

let () = Days.register "3" (module Day03)
