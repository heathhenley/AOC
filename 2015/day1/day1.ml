(* Day 1: Not Quite Lisp *)

(* read file to string - this day it's just one long single line*)
let read_file_to_string filename =
  let ic = open_in filename in
  let n = in_channel_length ic in
  let s = really_input_string ic n in
  close_in ic;
  s

(* for part 1 - go up a floor for all the ) and down a floor for all the ( *)
let traverse_floors str =
  (* easier to split list so make string a list *)
  let char_list = String.to_seq str |> List.of_seq in
  let rec traverse lst floor =
    (* match first element, increment, and recurse *)
    match lst with
    | [] -> floor
    | first :: rest ->
      if first = '(' then traverse rest (floor + 1)
      else traverse rest (floor - 1)
  in traverse char_list 0


(* for part 2 - find the first instruction that gets you to floor -1 *)
let find_basement str =
  (* easier to split list so make string a list *)
  let char_list = String.to_seq str |> List.of_seq in
  let rec traverse lst idx floor =
    (* match first element, increment, and recurse *)
    match lst with
    | [] -> idx
    | first :: rest ->
      if floor = -1 then idx
      else if first = '(' then traverse rest (idx + 1) (floor + 1)
      else traverse rest (idx + 1) (floor - 1)
  in traverse char_list 0 0


let part1 =
  let filename = "input.txt" in
  let file_contents = read_file_to_string filename in
  let floor = traverse_floors file_contents in
  Printf.printf "Part 1: %d\n" floor


let part2 = 
  let filename = "input.txt" in
  let file_contents = read_file_to_string filename in
  let instruction_index = find_basement file_contents in
  Printf.printf "Part 2: %d\n" instruction_index


let () = part1
let () = part2