
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


let split_to_ints line =
  let _ = Str.string_match (Str.regexp {|^\([0-9]+\) +\([0-9]+\)$|}) line 0 in
  let a = int_of_string (Str.matched_group 1 line) in
  let b = int_of_string (Str.matched_group 2 line) in
  [a; b]


let part1 filename =
  let file_contents = read_file_to_string filename in
  let left = file_contents
  |> split_on_newline
  |> List.map split_to_ints
  |> List.map (fun x -> List.hd x) in
  let right = file_contents
  |> split_on_newline
  |> List.map split_to_ints
  |> List.map (fun x -> List.hd (List.tl x)) in

  let sorted_left = List.sort compare left in
  let sorted_right = List.sort compare right in
  let score = List.fold_left2 (
    fun acc l r -> acc + abs (l - r)
  ) 0 sorted_left sorted_right in
  Printf.printf "Part 1: %d\n" score


let part2 filename =
  let file_contents = read_file_to_string filename in
  let left = file_contents
  |> split_on_newline
  |> List.map split_to_ints
  |> List.map (fun x -> List.hd x) in
  let right = file_contents
  |> split_on_newline
  |> List.map split_to_ints
  |> List.map (fun x -> List.hd (List.tl x)) in

  let sorted_left = List.sort compare left in
  let right_freq = Hashtbl.create 1000 in
  List.iter (
    fun x ->
    let freq = Hashtbl.find_opt right_freq x in
    match freq with
    | Some f -> Hashtbl.replace right_freq x (f + 1)
    | None -> Hashtbl.add right_freq x 1
  ) right;
  let score = List.fold_left (
    fun acc x ->
      let freq = Hashtbl.find_opt right_freq x in
      match freq with
      | Some f -> acc + x * f
      | None -> acc
  ) 0 sorted_left in
  Printf.printf "Part 2: %d\n" score
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
