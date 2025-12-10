module Day10_impl = struct

  let part1 _ =
    Printf.printf "Part 1: %d\n" 0

  let part2 _=
    Printf.printf "Part 2: %d\n" 0

end

module Day10 : Solution.Day = Day10_impl
include Day10_impl

let () = Days.register "10" (module Day10)
