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

let parse_line line =
  let pattern = Str.regexp {|^\([a-z\-]+\)\-\([0-9]+\)\[\(.*\)\]$|} in
  let m = Str.string_match pattern line 0 in
  match m with
  | false -> None 
  | true -> 
    let name = Str.matched_group 1 line in
    let sector_id = Str.matched_group 2 line in
    let checksum = Str.matched_group 3 line in
    Some (name, sector_id, checksum)
  
let count_chars str =
  let char_count = Hashtbl.create 26 in
  String.iter (
    fun c ->
      if c <> '-' then
        let count = 
          match Hashtbl.find_opt char_count c with
          | None -> 0
          | Some x -> x in
        Hashtbl.replace char_count c (count + 1)
  ) str;
  char_count

let build_check sorted_by_count count =
  let rec build_check' acc idx =
    if idx = count then
      acc
    else
      let (c, _) = List.nth sorted_by_count idx in
      build_check' (acc ^ (String.make 1 c)) (idx + 1) in
  build_check' "" 0

let check_valid name check =
  let char_count = count_chars name in
  let sorted_by_count =
    Hashtbl.to_seq char_count
    |> List.of_seq
    |> List.sort (
      fun (ca, a) (cb, b) ->
        if a = b then
          compare ca cb
        else
          compare b a
    ) in
  if List.length sorted_by_count < 5 then
    false
  else
    let top_5_str = build_check sorted_by_count 5 in
    top_5_str = check

let decrypt n s =
  let shift = (int_of_string s) mod 26 in
  let rec decrypt' acc idx =
    if idx = String.length n then
      acc
    else
      let c = String.get n idx in
      let new_c =
        if c = '-' then
          ' '
        else
          let base = if c >= 'a' then 'a' else 'A' in
          let new_c = Char.chr (
            ((Char.code c - (Char.code base) + shift) mod 26)
            + (Char.code base)) in
          new_c in
      decrypt' (acc ^ (String.make 1 new_c)) (idx + 1) in
  decrypt' "" 0


let part1 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let sum = List.fold_left (
    fun acc x ->
      let res = parse_line x in
      match res with
      | Some (n, s, c) ->
        let valid = check_valid n c in
        if valid then (acc + (int_of_string s)) else acc
      | None -> Printf.printf "Failed to parse line: %s\n" x; acc
  ) 0 lines in
  Printf.printf "Part 1: %d\n" sum


let part2 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let rooms = List.map (
    fun x ->
      let res = parse_line x in
      match res with
      | Some (n, s, c) ->
        let valid = check_valid n c in
        if valid then
          let decrypted = decrypt n s in
          (s, decrypted)
        else (s, "")
      | None -> Printf.printf "Failed to parse line: %s\n" x; ("", "")
  ) lines in
  let north_pole = List.find_opt(
    fun (_, name) ->
      Str.string_match (Str.regexp ".*north.*pole.*") name 0
  ) rooms in
  match north_pole with
  | None -> Printf.printf "Failed to find North Pole object storage\n"
  | Some (s, n) ->
    Printf.printf "%s - %s\n" n s;
    Printf.printf "Part 2: %s\n" s;
  ()

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
