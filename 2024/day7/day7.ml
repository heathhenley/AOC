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

let parse_line line =
  let c_idx = String.index line ':' in
  let left = int_of_string (String.sub line 0 c_idx) in
  let right = String.sub line (c_idx + 2) (String.length line - c_idx - 2) in
  let args = right
  |> String.split_on_char ' '
  |> List.map String.trim
  |> List.filter (fun x -> String.length x > 0)
  |> List.map int_of_string in
  (left, args)


let cat a b =
  let sa = string_of_int a in
  let sb = string_of_int b in
  int_of_string (sa ^ sb)


let is_solvable args target with_cat =
  let rec solve args target curr =
    match args with
    | [] -> curr = target
    | hd :: tl ->
        solve tl target (curr + hd)
        || solve tl target (curr * hd)
        || (with_cat && solve tl target (cat curr hd))
  in
  solve args target 0


let part1 filename =
  let ans = filename
  |> read_file_to_string
  |> split_on_newline
  |> List.fold_left (
    fun acc line ->
      let (target, args) = parse_line line in
      acc + (if is_solvable args target false then target else 0)
  ) 0 in
  Printf.printf "Part 1: %d\n" ans


let part2 filename =
  let ans = filename
  |> read_file_to_string
  |> split_on_newline
  |> List.fold_left (
    fun acc line ->
      let (target, args) = parse_line line in
      acc + (if is_solvable args target true then target else 0)
  ) 0 in
  Printf.printf "Part 2: %d\n" ans
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
