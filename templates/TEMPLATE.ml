
let read_file_to_string filename =
  let ic = open_in filename in
  let n = in_channel_length ic in
  let s = really_input_string ic n in
  close_in ic;
  s

let split_on_newline str =
  let split = String.split_on_char '\n' str in
  split


let time_function f arg =
  let start_time = Sys.time () in
  let result = f arg in
  let end_time = Sys.time () in
  let elapsed_time = end_time -. start_time in
  Printf.printf "Elapsed time: %.6f seconds\n" elapsed_time;
  result


let part1 filename =
  let file_contents = read_file_to_string filename in
  let _ = split_on_newline file_contents in
  Printf.printf "Part 1: %d\n" 0


let part2 filename =
  let file_contents = read_file_to_string filename in
  let _ = split_on_newline file_contents in
  Printf.printf "Part 2: %d\n" 0
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
