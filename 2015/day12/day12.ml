
let read_file_to_string filename =
  let ic = open_in filename in
  let n = in_channel_length ic in
  let s = really_input_string ic n in
  close_in ic;
  s

(*let split_on_newline str =
let split_on_newline str =
  let split = String.split_on_char '\n' str in
  split
  *)


let time_function f arg =
  let start_time = Sys.time () in
  let result = f arg in
  let end_time = Sys.time () in
  let elapsed_time = end_time -. start_time in
  Printf.printf "Elapsed time: %.6f seconds\n" elapsed_time;
  result


(* Part 1 -  Walk the json recursively - add any numbers up *)
let walk_json json =
  let rec walk_json' json =
    (* These are polymorphic variant tags - so not actual types, the are
       defined in json to represent the json elements so that they can be
       matched against at run time *)
    match json with
    (* fold left is just reduce *)
    | `Assoc lst -> List.fold_left (fun acc (_,v) -> acc + walk_json' v) 0 lst
    | `List lst -> List.fold_left (fun acc v -> acc + walk_json' v) 0 lst
    | `Int i -> i
    | `String _ -> 0
    | `Bool _ -> 0
    | `Null -> 0
    | `Float _ -> 0
  in
  walk_json' json


(* Part 2 -  Walk the json recursively - add any numbers up - but skip any
    object that has a value of "red" *)
let walk_json_skip_red json =
  let rec walk_json' json =
    match json with
    | `Assoc lst when List.exists (fun (_,v) -> v = `String "red") lst -> 0
    | `Assoc lst -> List.fold_left (fun acc (_,v) -> acc + walk_json' v) 0 lst
    | `List lst -> List.fold_left (fun acc v -> acc + walk_json' v) 0 lst
    | `Int i -> i
    | `String _ -> 0
    | `Bool _ -> 0
    | `Null -> 0
    | `Float _ -> 0
  in
  walk_json' json

let part1 filename =
  let file_contents = read_file_to_string filename in
  let json = Yojson.Basic.from_string file_contents in
  let sum = walk_json json in
  Printf.printf "Part 1: %d\n" sum


let part2 filename =
  let file_contents = read_file_to_string filename in
  let json = Yojson.Basic.from_string file_contents in
  let sum = walk_json_skip_red json in
  Printf.printf "Part 2: %d\n" sum
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
