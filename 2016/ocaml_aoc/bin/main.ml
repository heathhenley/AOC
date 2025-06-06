let () =
  match Sys.argv with
  | [|_; day; filename|] -> (
      match day with
      | "1" ->
          Printf.printf "\nDay 1\n";
          Utils.Timing.time_function Day01.part1 filename;
          Utils.Timing.time_function Day01.part2 filename
      | "6" ->
          Printf.printf "\nDay 6\n";
          Utils.Timing.time_function Day06.part1 filename;
          Utils.Timing.time_function Day06.part2 filename
      | _ -> Printf.printf "Day %s not implemented\n" day
    )
  | _ -> Printf.printf "Usage: %s <day> <filename>\n" Sys.argv.(0)
