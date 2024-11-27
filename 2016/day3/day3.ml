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

let side_lengths_of_line line =
  let sides = line
  |> String.trim
  |> (fun x -> Str.split (Str.regexp " +") x)
  |> List.map String.trim
  |> List.map int_of_string in
  sides

let valid_triangle sides =
  match sides with
    | [a; b; c] when
        a + b  > c
        && a + c > b
        && b + c > a
      -> 1
    | _ -> 0

let rec count_along_col sides col idx acc =
  match idx with
    | _ when idx >= List.length sides - 2 -> acc
    | _ ->
      let a = List.nth (List.nth sides idx) col in
      let b = List.nth (List.nth sides (idx + 1)) col in
      let c = List.nth (List.nth sides (idx + 2)) col in
      let count = valid_triangle [a; b; c] + acc in
      count_along_col sides col (idx + 3) count

let part1 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let sides = List.map side_lengths_of_line lines in
  let count = List.fold_left (
    fun acc item -> acc + (valid_triangle item)) 0 sides in
  Printf.printf "Part 1: %d\n" count

let part2 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let sides = List.map side_lengths_of_line lines in
  let c0 = count_along_col sides 0 0 0 in
  let c1 = count_along_col sides 1 0 0 in
  let c2 = count_along_col sides 2 0 0 in
  Printf.printf "Part 2: %d\n" (c0 + c1 + c2)
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
