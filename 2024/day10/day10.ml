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

let valid_bounds grid row col =
  row >= 0
  && row < Array.length grid
  && col >= 0
  && col < Array.length grid.(0)

let int_of_char_digit c =
  Char.code c - Char.code '0'

let full_grid_of_input_lines lines =
  let cols = String.length (List.hd lines) in
  let rows = List.length lines in
  let grid = Array.make_matrix rows cols 0 in
  List.iteri (fun i line ->
    grid.(i) <-
      line
      |> String.to_seq |> Array.of_seq |> Array.map int_of_char_digit
  ) lines;
  grid

let directions = [
  (* no diagonal steps *)
  (0, 1); (1, 0); (0, -1); (-1, 0)
]

let walk grid start target_val =
  (* find the distinct paths to get to a node with target_val from start *)
  let rec dfs' row col path all_paths =
    match grid.(row).(col) with
    | x when x = target_val -> path :: all_paths
    | _ ->
      List.fold_left (
        fun acc (row_offset, col_offset) ->
          let new_row = row + row_offset in
          let new_col = col + col_offset in
          let vb = valid_bounds grid new_row new_col in
          if vb && grid.(new_row).(new_col) - grid.(row).(col) == 1 then
              dfs' new_row new_col (path @ [(new_row, new_col)]) acc
          else
            acc
      ) all_paths directions
  in
  dfs' (fst start) (snd start) [start] []
        

let find_starts grid start_val =
  let rows = Array.length grid in
  let cols = Array.length grid.(0) in
  let rec find_start' row col acc =
    if row = rows then
      acc
    else if col = cols then
      find_start' (row + 1) 0 acc
    else if grid.(row).(col) = start_val then
      find_start' row (col + 1) ((row, col) :: acc)
    else
      find_start' row (col + 1) acc
  in
  find_start' 0 0 []

let count_nines paths =
  paths
  |> List.map (fun path -> List.hd (List.rev path))
  |> List.sort_uniq compare
  |> List.length


let part1 filename =
  let grid = filename
    |> read_file_to_string
    |> split_on_newline
    |> full_grid_of_input_lines in
  let nine_count = find_starts grid 0
    |> List.fold_left (fun acc start ->
      acc + (walk grid start 9 |> count_nines)
    ) 0 in
  Printf.printf "Part 1: %d\n" nine_count


let part2 filename =
  let grid = filename
    |> read_file_to_string
    |> split_on_newline
    |> full_grid_of_input_lines in
  let trail_count = find_starts grid 0
    |> List.fold_left (fun acc start ->
      acc + (walk grid start 9 |> List.length)
    ) 0 in
  Printf.printf "Part 2: %d\n" trail_count
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
