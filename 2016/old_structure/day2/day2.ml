
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


let direction_to_vector dir =
  match dir with
  | 'U' -> (0, -1)
  | 'D' -> (0, 1)
  | 'L' -> (-1, 0)
  | 'R' -> (1, 0)
  | _ -> (0, 0)


let valid_position (x, y) keypad =
  let max = Array.length keypad in (* assume it's square *)
  x >= 0 && x < max && y >= 0 && y < max && keypad.(y).(x) <> ' '


let rec move (x, y) dlist keypad =
  match dlist with
  | [] -> (x, y)
  | hd :: tl ->
      let (dx, dy) = direction_to_vector hd in
      let new_x = x + dx in
      let new_y = y + dy in
      if valid_position (new_x, new_y) keypad then
        move (new_x, new_y) tl keypad
      else
        move (x, y) tl keypad


let get_code keypad lines start =
  let rec get_code' lines position code =
    match lines with
    | [] -> code
    | line :: rest ->
        let dlist = String.to_seq line |> List.of_seq in
        let (new_x, new_y) = move position dlist keypad in
        let new_code = code ^ (String.make 1 keypad.(new_y).(new_x)) in
        get_code' rest (new_x, new_y) new_code
  in
  get_code' lines start ""
    

let part1 filename =
  let keypad = [|
    [|'1'; '2'; '3'|];
    [|'4'; '5'; '6'|];
    [|'7'; '8'; '9'|]
  |] in
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let code = get_code keypad lines (1, 1) in
  Printf.printf "Part 1: %s\n" code


let part2 filename =
  let keypad = [|
    [|' '; ' '; '1'; ' '; ' '|];
    [|' '; '2'; '3'; '4'; ' '|];
    [|'5'; '6'; '7'; '8'; '9'|];
    [|' '; 'A'; 'B'; 'C'; ' '|];
    [|' '; ' '; 'D'; ' '; ' '|];
  |] in
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let code = get_code keypad lines (0, 2) in
  Printf.printf "Part 2: %s\n" code
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
