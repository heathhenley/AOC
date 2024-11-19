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

let valid_neighbors grid row col =
  let neighbors = 
    [(row-1, col-1); (row-1, col); (row-1, col+1);
     (row, col-1);                 (row, col+1);
     (row+1, col-1); (row+1, col); (row+1, col+1)] in
  List.filter (fun (r, c) -> valid_bounds grid r c) neighbors

let light_array_of_line line =
  let lights = Array.make (String.length line) false in
  String.iteri (fun i c ->
    lights.(i) <- c = '#'
  ) line;
  lights

(* A list of lines into 2d grid of bools*)
let full_grid_of_input_lines lines =
  let cols = String.length (List.hd lines) in
  let rows = List.length lines in
  let lights = Array.make_matrix rows cols false in
  List.iteri (fun i line ->
    lights.(i) <- light_array_of_line line
  ) lines;
  lights

let sum_up_neighbors grid row col =
  let neighbors = valid_neighbors grid row col in
  List.fold_left (fun acc (r, c) ->
    acc + if grid.(r).(c) then 1 else 0
  ) 0 neighbors

let print_grid grid =
  Array.iter (fun row ->
    Array.iter (fun light ->
      Printf.printf "%c" (if light then '#' else '.')
    ) row;
    Printf.printf "\n"
  ) grid

let rec run_simulation grid n special_rules =
  match n with
  | 0 -> grid
  | _ -> 
    let rows = Array.length grid in
    let cols = Array.length grid.(0) in
    let new_grid = Array.make_matrix rows cols false in
    Array.iteri (fun row _ ->
      Array.iteri (fun col _  ->
        let neighbor_sum = sum_up_neighbors grid row col in
        match neighbor_sum with
        | 3 -> new_grid.(row).(col) <- true
        | 2 -> new_grid.(row).(col) <- grid.(row).(col)
        | _ -> new_grid.(row).(col) <- false
      ) grid.(row);
    ) grid;
    let new_grid = special_rules new_grid in
  run_simulation new_grid (n-1) special_rules

let count_lights grid =
  Array.fold_left (fun acc row ->
    acc + Array.fold_left (fun acc light ->
      acc + if light then 1 else 0
    ) 0 row
  ) 0 grid

let part1 filename =
  let file_contents = read_file_to_string filename in
  let n = 100 in
  let lines = split_on_newline file_contents in
  let grid = full_grid_of_input_lines lines in
  let grid = run_simulation grid n (fun x -> x) in
  let count = count_lights grid in
  Printf.printf "After n=%d steps:\n" n;
  print_grid grid;
  Printf.printf "Part 1: %d\n" count

let set_corners_on grid =
  let rows = Array.length grid in
  let cols = Array.length grid.(0) in
  grid.(0).(0) <- true;
  grid.(0).(cols-1) <- true;
  grid.(rows-1).(0) <- true;
  grid.(rows-1).(cols-1) <- true;
  grid


let part2 filename =
  (* This is the same as part 1, but with the four corners always on *)
  let file_contents = read_file_to_string filename in
  let n = 100 in
  let lines = split_on_newline file_contents in
  let grid = full_grid_of_input_lines lines in
  let grid = set_corners_on grid in
  let grid = run_simulation grid n set_corners_on in
  let count = count_lights grid in
  Printf.printf "After n=%d steps:\n" n;
  print_grid grid;
  Printf.printf "Part 2: %d\n" count
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
