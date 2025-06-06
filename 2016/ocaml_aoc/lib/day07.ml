let part1 filename =
  let file_contents = Utils.Input.read_file_to_string filename in
  let lines = Utils.Input.split_on_newline file_contents in
  List.iter (fun l ->
    Printf.printf "Line: %s\n" l
  ) lines

let part2 filename =
  let file_contents = Utils.Input.read_file_to_string filename in
  let lines = Utils.Input.split_on_newline file_contents in
  List.iter (fun l ->
    Printf.printf "Line: %s\n" l
  ) lines
