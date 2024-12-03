
let read_file_to_string filename =
  let ic = open_in filename in
  let n = in_channel_length ic in
  let s = really_input_string ic n in
  close_in ic;
  s

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
      let m = Str.matched_group 0 str in
      get_all_matches' ptn str (Str.match_end ()) (m::acc)
    with Not_found -> acc
  in
  get_all_matches' ptn str 0 []


let part1 filename =
  let mult_ptn = Str.regexp {|mul(\([0-9]+\),\([0-9]+\))|} in
  let file_contents = read_file_to_string filename in
  let matches = get_all_matches mult_ptn file_contents in
  let res = List.fold_left (
    fun acc m ->
      match m with
      | s ->
        let _ = Str.string_match mult_ptn s 0 in
        let x = int_of_string @@ Str.matched_group 1 s in
        let y = int_of_string @@ Str.matched_group 2 s in
        acc + x * y
  ) 0 matches in
  Printf.printf "Part 1: %d\n" res


let part2 filename =
  let mult_ptn = Str.regexp {|mul(\([0-9]+\),\([0-9]+\))\|do()\|don't()|} in
  let file_contents = read_file_to_string filename in
  let matches = List.rev (get_all_matches mult_ptn file_contents) in
  let rec get_result enabled acc matches =
    match matches with
    | [] -> acc
    | hd::tl when hd = "do()" -> get_result true acc tl
    | hd::tl when hd = "don't()" -> get_result false acc tl
    | hd::tl when enabled ->
      let _ = Str.string_match mult_ptn hd 0 in
      let x = int_of_string @@ Str.matched_group 1 hd in
      let y = int_of_string @@ Str.matched_group 2 hd in
      get_result enabled (acc + x * y) tl
    | _::tl -> get_result enabled acc tl
    in 
  Printf.printf "Part 2: %d\n" (get_result true 0 matches)
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
