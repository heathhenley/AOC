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

let starts_with str substr =
  (* true if the str starts with substr *)
  let len = String.length substr in
  if String.length str < len then
    false
  else
    String.sub str 0 len = substr

let count_makable strings patterns =
  let ht = Hashtbl.create 100 in
  let rec count_makable' string patterns =
    if String.length string = 0 then
      1
    else
      match Hashtbl.find_opt ht string with
      | Some count -> count
      | None ->
        (* try each patten that matched the beginning of the string *)
        let count = List.fold_left (
          fun acc ptn ->
            if starts_with string ptn then
              let len = String.length ptn in
              let new_str = String.sub string len (String.length string - len) in
              acc + count_makable' new_str patterns
            else
              acc
        ) 0 patterns in
        Hashtbl.add ht string count;
        count
  in
  List.fold_left (
    fun acc string ->
      acc + count_makable' string patterns
  ) 0 strings


let part1 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let patterns = lines
    |> List.hd
    |> String.split_on_char ','
    |> List.map String.trim
  in
  let strings = List.tl lines
    |> List.map String.trim
  in
  let count = List.fold_left (
    fun acc s ->
      if count_makable [s] patterns > 0 then
        acc + 1
      else
        acc
    ) 0 strings in
  Printf.printf "Part 1: %d\n" count


let part2 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let patterns = lines
    |> List.hd
    |> String.split_on_char ','
    |> List.map String.trim
  in
  let strings = List.tl lines
    |> List.map String.trim
  in
  let count = count_makable strings patterns in
  Printf.printf "Part 2: %d\n" count
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
