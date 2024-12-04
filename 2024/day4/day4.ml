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


let get_wordsearch lines =
  let rows = List.length lines in
  let cols = String.length (List.hd lines) in
  let ws = Array.make_matrix rows cols ' ' in
  List.iteri (fun i line ->
    String.iteri (fun j c ->
      ws.(i).(j) <- c
    ) line
  ) lines;
  ws

(* a list of the (dr, dc) to get words in all directions *)
let dirs = [
  [(0, 0); (0, 1); (0, 2); (0, 3)]; (*right*)
  [(0, 0); (1, 0); (2, 0); (3, 0)]; (*down*)
  [(0, 0); (1, 1); (2, 2); (3, 3)]; (*down-right*)
  [(0, 0); (1, -1); (2, -2); (3, -3)]; (*down-left*)
  [(0, 0); (-1, 0); (-2, 0); (-3, 0)]; (*up*)
  [(0, 0); (-1, 1); (-2, 2); (-3, 3)]; (*up-right*)
  [(0, 0); (-1, -1); (-2, -2); (-3, -3)]; (*up-left*)
  [(0, 0); (0, -1); (0, -2); (0, -3)]; (*left*)
]

let dirs_cross = [
      [(-1, -1); (0, 0); (1, 1)]; (*up-left, down-right*)
      [(1, -1); (0, 0); (-1, 1)]; (*down-left, up-right*)
]

(* extract word from grid with the given list of (dr, dc) values and starting
postion *)
let get_word_from ws i j dir =
  let rows = Array.length ws in
  let cols = Array.length ws.(0) in
  let get_word acc (dr, dc) =
    let i' = i + dr in
    let j' = j + dc in
    if i' < 0 || i' >= rows || j' < 0 || j' >= cols then
      None
    else
      Some (acc ^ (String.make 1 ws.(i').(j')))
  in
  List.fold_left (fun acc' d -> match acc' with
    | None -> None
    | Some acc' -> let w = get_word acc' d in
      match w with
      | None -> None
      | Some w -> 
      Some w
  ) (Some "") dir 

let rec matches_at_this_spot ws i j target_word dirs =
  match dirs with
  | [] -> 0
  | dir :: rest ->
    let word = get_word_from ws i j dir in
    match word with
    | None -> matches_at_this_spot ws i j target_word rest
    | Some word when word = target_word ->
      1 + matches_at_this_spot ws i j target_word rest
    | _ -> matches_at_this_spot ws i j target_word rest

let rec solve_wordsearch ws target_word i j count =
  let rows = Array.length ws in
  let cols = Array.length ws.(0) in
  match (i, j) with
  | (i, _) when i >= rows -> count
  | (i, j) when j >= cols -> solve_wordsearch ws target_word (i + 1) 0 count
  | _ ->
    let new_count = count + (matches_at_this_spot ws i j target_word dirs) in
    solve_wordsearch ws target_word i (j + 1) new_count

let rec reverse str acc =
  match str with
  | "" -> acc
  | _ -> reverse (String.sub str 1 ((String.length str) - 1)) ((String.make 1 str.[0]) ^ acc)

let rec solve_wordsearch_cross ws target_word i j count =
  let rows = Array.length ws in
  let cols = Array.length ws.(0) in
  match (i, j) with
  | (i, _) when i >= rows -> count
  | (i, j) when j >= cols ->
    solve_wordsearch_cross ws target_word (i + 1) 0 count
  | _ ->
    let new_count =
      matches_at_this_spot ws i j target_word dirs_cross +
      matches_at_this_spot ws i j (reverse target_word "") dirs_cross
    in
      if new_count = 2 then (* we find a MAS in both dirs *)
        solve_wordsearch_cross ws target_word i (j + 1) (count + 1)
      else
        solve_wordsearch_cross ws target_word i (j + 1) count

let part1 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let ws = get_wordsearch lines in
  let target_word = "XMAS" in
  let res = solve_wordsearch ws target_word 0 0 0 in
  Printf.printf "Part 1: %d\n" res

let part2 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let ws = get_wordsearch lines in
  let target_word = "MAS" in
  let res = solve_wordsearch_cross ws target_word 0 0 0 in
  Printf.printf "Part 2: %d\n" res


(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
