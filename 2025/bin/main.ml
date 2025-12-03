let run_day day_module filename =
  let module D = (val day_module : Solution.Day) in
  Utils.Timing.time_function D.part1 filename;
  Utils.Timing.time_function D.part2 filename

let run day_str filename =
  Printf.printf
  "**************************************\n******** 2025 - Day %s ****************\n**************************************\n" day_str;
  match Days.find day_str with
  | Some day_module -> run_day day_module filename
  | None -> Printf.printf "Day %s not implemented yet\n" day_str

let () =
  match Sys.argv with
  | [| _; day_str; filename |] -> run day_str filename
  | [| _; day_str |] -> run day_str "-"
  | _ -> Printf.printf "Usage: %s <day> [<filename>]\n" Sys.argv.(0)
