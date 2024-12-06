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


let possible_dirs = ['^'; 'v'; '<'; '>']


let dir_to_offset = function
  | '^' -> (-1, 0)
  | 'v' -> (1, 0)
  | '<' -> (0, -1)
  | '>' -> (0, 1)
  | _ -> (0, 0)


let turn_right = function
  | '^' -> '>'
  | 'v' -> '<'
  | '<' -> '^'
  | '>' -> 'v'
  | _ -> failwith "Invalid direction"


let valid_bounds grid row col =
  row >= 0
  && row < Array.length grid
  && col >= 0
  && col < Array.length grid.(0)


let full_grid_of_input_lines lines =
  let cols = String.length (List.hd lines) in
  let rows = List.length lines in
  let grid = Array.make_matrix rows cols '.' in
  List.iteri (fun i line ->
    grid.(i) <- line |> String.to_seq |> Array.of_seq
  ) lines;
  grid


let find_start grid =
  let rows = Array.length grid in
  let cols = Array.length grid.(0) in
  let rec find_starting_point' row col =
    if not (valid_bounds grid row col) then
      None
    else
      match grid.(row).(col) with
      | x when List.mem x possible_dirs -> Some (row, col, x)
      | _ -> if row = rows - 1 && col = cols - 1 then
              None
            else if col = cols - 1 then
              find_starting_point' (row + 1) 0
            else
              find_starting_point' row (col + 1) 
  in
  find_starting_point' 0 0


let rec remove_duplicates seen = function
  | [] -> []
  | (row, col, _) :: tail ->
    if List.mem (row, col) seen then
      remove_duplicates seen tail
    else
      (row, col) :: remove_duplicates ((row, col) :: seen) tail


let rec walk grid row col dir visited =
  let (row_offset, col_offset) = dir_to_offset dir in
  let new_row = row + row_offset in
  let new_col = col + col_offset in
  if not (valid_bounds grid new_row new_col) then
    (visited, false) 
  else if List.mem (new_row, new_col, dir) visited then
    (visited, true)
  else
    match grid.(new_row).(new_col) with 
    | '#' ->
      let new_dir = turn_right dir in
      walk grid row col new_dir ((row, col, new_dir) :: visited)
    | _ ->
      walk grid new_row new_col dir ((new_row, new_col, dir) :: visited)



let part1 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let grid = full_grid_of_input_lines lines in
  let (row, col, dir) = find_start grid |> Option.get in
  let visited, _ = walk grid row col dir [(row, col, dir)] in
  let unique_visited = remove_duplicates [] visited in
  Printf.printf "Part 1: %d\n" (List.length unique_visited)


let part2 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let grid = full_grid_of_input_lines lines in
  let (srow, scol, dir) = find_start grid |> Option.get in
  let visited, is_loop = walk grid srow scol dir [(srow, scol, dir)] in
  Printf.printf "Visited: %d\n" (List.length visited);
  Printf.printf "Loop: %b\n" is_loop;
  let unique_visited = remove_duplicates [] visited in
  Printf.printf "Part 2: %d\n" (List.length unique_visited)
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
