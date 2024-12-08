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


let endswith a b =
  let astr = string_of_int a in
  let bstr = string_of_int b in
  let alen = String.length astr in
  let blen = String.length bstr in
  if alen <= blen then false
  else
    let rec endswith' a b alen blen =
      if blen = 0 then true
      else if astr.[alen - 1] <> bstr.[blen - 1] then false
      else endswith' a b (alen - 1) (blen - 1)
    in
    endswith' astr bstr alen blen

let unconcat a b =
  let sa = string_of_int a in
  let sb = string_of_int b in
  int_of_string (String.sub sa 0 (String.length sa - String.length sb))

let is_solveable_opt args target with_cat =
  let args_arr = Array.of_list args in
  let rec solve a target idx =
    let add = target - a.(idx) >= a.(0) in
    let mult = target mod a.(idx) = 0 in
    let contains = with_cat && endswith target a.(idx) in
    match idx with
    | 0 -> a.(0) = target
    | _ ->
      (add && solve a (target - a.(idx)) (idx - 1))
      || (mult && solve a (target / a.(idx)) (idx - 1))
      || (contains && solve a (unconcat target a.(idx))  (idx - 1))
  in 
  solve args_arr target (Array.length args_arr - 1)

let part1 filename =
  let ans = filename
  |> read_file_to_string
  |> split_on_newline
  |> List.fold_left (
    fun acc line ->
      let (target, args) = parse_line line in
      acc + (if is_solveable_opt args target false then target else 0)
  ) 0 in
  Printf.printf "Part 1: %d\n" ans


let part2 filename =
  let ans = filename
  |> read_file_to_string
  |> split_on_newline
  |> List.fold_left (
    fun acc line ->
      let (target, args) = parse_line line in
      acc + (if is_solveable_opt args target true then target else 0)
  ) 0 in
  Printf.printf "Part 2: %d\n" ans
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
