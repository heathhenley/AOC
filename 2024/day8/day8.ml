(*
Day 8 ported to ocaml - borrowing a lot from the implementation by
https://github.com/veeenu/adventofcode2024/blob/main/day08.ml
*)
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

let valid grid row col =
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

let get_antenna_positions grid =
  let antenna_map = Hashtbl.create 1000 in
  Array.iteri (fun i row ->
    Array.iteri (fun j cell ->
      match cell with
      | '.' -> ()
      | x ->
        match Hashtbl.find_opt antenna_map x with
        | None -> Hashtbl.add antenna_map x [(i, j)]
        | Some lst -> Hashtbl.replace antenna_map x ((i, j)::lst)
    ) row
  ) grid;
  antenna_map

let rec get_pairs lst =
  match lst with
  | [] -> []
  | _ :: [] -> []
  | hd :: tl -> List.map (fun x -> (hd, x)) tl @ get_pairs tl

let get_antinodes pair =
  let (x1, y1), (x2, y2) = pair in
  [ ( 2 * x2 - x1, 2 * y2 - y1); (2 * x1 - x2, 2 * y1 - y2) ]

let get_harmonic_antinodes pair grid =
  let (x1, y1), (x2, y2) = pair in
  let (dx, dy) = (x2 - x1, y2 - y1) in
  let rec harmonic_antinodes (x, y) (dx, dy) =
    let cx, cy = (x + dx, y + dy) in
    if valid grid cx cy then
      (cx, cy) :: harmonic_antinodes (cx, cy) (dx, dy)
    else
      []
    in harmonic_antinodes (x1, y1) (dx, dy)
    @ harmonic_antinodes (x2, y2) (-dx, -dy)

let part1 filename =
  let grid = filename
  |> read_file_to_string
  |> split_on_newline
  |> full_grid_of_input_lines in
  let unique = grid
  |> get_antenna_positions
  |> (fun x -> Hashtbl.fold (fun _ v acc ->
      let an = v
      |> get_pairs
      |> List.map get_antinodes
      |> List.flatten
      |> List.filter (fun (x, y) -> valid grid x y)
      in
      an @ acc
    ) x [] ) 
  |> (fun x -> List.sort_uniq compare x) in
  Printf.printf "Part 1: %d\n" (List.length unique)

let part2 filename =
  let grid = filename
  |> read_file_to_string
  |> split_on_newline
  |> full_grid_of_input_lines in
  let unique = grid
  |> get_antenna_positions
  |> (fun x -> Hashtbl.fold (fun _ v acc ->
      let an = v
        |> get_pairs
        |> List.map (fun x -> get_harmonic_antinodes x grid)
        |> List.flatten
        |> List.filter (fun (x, y) -> valid grid x y)
      in
      an @ acc
    ) x [] ) 
  |> (fun x -> List.sort_uniq compare x) in
  Printf.printf "Part 2: %d\n" (List.length unique)
  
(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
