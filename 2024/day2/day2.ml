
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

let is_safe level =
  let diff_list = List.tl (List.mapi (
    fun i x -> if i = 0 then 0 else x - (List.nth level (i - 1))
  ) level) in
  let diff_list_abs = List.map (fun x -> abs x) diff_list in
  let max_diff = List.fold_left (
    fun acc x -> if x > acc then x else acc
  ) 0 diff_list_abs in
  if max_diff > 3 || max_diff < 1 then false
  else
    (* they need to all be positive or all be negative *)
    let all_positive = List.for_all (fun x -> x > 0) diff_list in
    let all_negative = List.for_all (fun x -> x < 0) diff_list in
    all_positive || all_negative

let is_safe_with_removal level =
  (* if it's not safe, we can remove one level and try again *)
  match is_safe level with
  | true -> true
  | false ->
    (* remove each level and check if it's now safe *)
    let rec remove_and_check level idx =
      match idx with
      | _ when idx = List.length level -> false
      | _ ->
        let new_level = List.filteri (fun i _ -> i <> idx) level in
        if is_safe new_level then true
        else remove_and_check level (idx + 1)
    in
    remove_and_check level 0

let part1 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let levels = List.map (fun x -> String.split_on_char ' ' x) lines in
  let safe_levels = List.fold_left (
    fun acc x -> 
      let x_int = List.map (fun x -> int_of_string x) x in
      if is_safe x_int then acc + 1
      else acc
  ) 0 levels in
  Printf.printf "Part 1: %d\n" safe_levels


let part2 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let levels = List.map (fun x -> String.split_on_char ' ' x) lines in
  let safe_levels = List.fold_left (
    fun acc x -> 
      let x_int = List.map (fun x -> int_of_string x) x in
      if is_safe_with_removal x_int then acc + 1
      else acc
  ) 0 levels in
  Printf.printf "Part 2: %d\n" safe_levels
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
