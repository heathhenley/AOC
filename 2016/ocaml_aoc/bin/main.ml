let days : (string * (module Solution.Day)) list =
  [ ("1", (module Day01))
  ; ("6", (module Day06))
  ; ("7", (module Day07))
  ]

let run_day day_module filename =
  let module D = (val day_module : Solution.Day) in
  Utils.Timing.time_function D.part1 filename;
  Utils.Timing.time_function D.part2 filename

let () =
  match Sys.argv with
  | [| _; day_str; filename |] -> (
      Printf.printf "\nDay %s\n" day_str;
      match List.assoc_opt day_str days with
      | Some day_module -> run_day day_module filename
      | None -> Printf.printf "Day %s not implemented yet\n" day_str)
  | _ -> Printf.printf "Usage: %s <day> <filename>\n" Sys.argv.(0)
