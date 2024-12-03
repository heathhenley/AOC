
let read_file_to_string filename =
  let ic = open_in filename in
  let n = in_channel_length ic in
  let s = really_input_string ic n in
  close_in ic;
  s

  let split_on_newline str =
    let split = str
    |> String.split_on_char '\n'
    |> List.map String.trim
    |> List.filter (fun x -> String.length x > 0) in
    split

let time_function f arg =
  let start_time = Sys.time () in
  let result = f arg in
  let end_time = Sys.time () in
  let elapsed_time = end_time -. start_time in
  Printf.printf "Elapsed time: %.6f seconds\n" elapsed_time;
  result

let get_all_matches ptn str =
  let rec get_all_matches' ptn str start acc =
    try
      let _ = Str.search_forward ptn str start in
      let x = int_of_string @@ Str.matched_group 1 str in
      let y = int_of_string @@ Str.matched_group 2 str in
      get_all_matches' ptn str (Str.match_end ()) ((x, y)::acc)
    with Not_found -> acc
  in
  get_all_matches' ptn str 0 []


let part1 filename =
  let mult_ptn = Str.regexp {|mul(\([0-9]+\),\([0-9]+\))|} in
  let file_contents = read_file_to_string filename in
  let matches = get_all_matches mult_ptn file_contents in
  let res = List.fold_left (fun acc (x, y) -> acc + x * y) 0 matches in
  Printf.printf "Part 1: %d\n" res


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
