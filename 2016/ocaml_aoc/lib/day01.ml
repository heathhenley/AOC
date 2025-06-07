let parse_instruction instruction =
  let stripped = String.trim instruction in
  let direction = stripped.[0] in
  let distance =
    stripped
    |> (fun s -> String.sub s 1 (String.length stripped - 1))
    |> int_of_string
  in
  (direction, distance)

(* had to rethink things to get part 2 to work *)
let apply_turn current_dir turn_dir =
  match (current_dir, turn_dir) with
  | 'N', 'R' -> 'E'
  | 'N', 'L' -> 'W'
  | 'S', 'R' -> 'W'
  | 'S', 'L' -> 'E'
  | 'E', 'R' -> 'S'
  | 'E', 'L' -> 'N'
  | 'W', 'R' -> 'N'
  | 'W', 'L' -> 'S'
  | _ -> failwith "Invalid direction"

let direction_to_vector dir =
  match dir with
  | 'N' -> (0, 1)
  | 'S' -> (0, -1)
  | 'E' -> (1, 0)
  | 'W' -> (-1, 0)
  | _ -> failwith "Invalid direction"

let apply_instruction (x, y, direction) (new_direction, distance) =
  let new_direction = apply_turn direction new_direction in
  let dx, dy = direction_to_vector new_direction in
  (x + (dx * distance), y + (dy * distance), new_direction)

let part1 filename =
  let file_contents = Utils.Input.read_file_to_string filename in
  let lines = Utils.Input.split_on_newline file_contents in
  let x, y, _ =
    List.hd lines
    |> String.split_on_char ','
    |> List.map String.trim
    |> List.map parse_instruction
    |> List.fold_left apply_instruction (0, 0, 'N')
  in
  Printf.printf "Part 1: %d\n" (abs x + abs y)

module PointSet = Set.Make (struct
  type t = int * int

  let compare = compare
end)

let rec find_repeat x y d visited inst =
  match inst with
  | [] -> None (* No repeat found *)
  | (turn, move) :: rest ->
      let new_dir = apply_turn d turn in
      let dx, dy = direction_to_vector new_dir in
      let rec move_and_check x y visited move =
        if move = 0 then find_repeat x y new_dir visited rest
        else
          let new_x = x + dx in
          let new_y = y + dy in
          if PointSet.mem (new_x, new_y) visited then
            Some (abs new_x + abs new_y)
          else
            move_and_check new_x new_y
              (PointSet.add (new_x, new_y) visited)
              (move - 1)
      in
      move_and_check x y visited move

let part2 filename =
  let file_contents = Utils.Input.read_file_to_string filename in
  let lines = Utils.Input.split_on_newline file_contents in
  let inst =
    List.hd lines
    |> String.split_on_char ','
    |> List.map String.trim
    |> List.map parse_instruction
  in
  let x, y, d = (0, 0, 'N') in
  let visited = PointSet.empty in
  match find_repeat x y d visited inst with
  | Some x -> Printf.printf "Part 2: %d\n" x
  | None ->
      Printf.printf "No repeat found\n";
      Printf.printf "Part 2: %d\n" x
