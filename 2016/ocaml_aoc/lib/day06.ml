let most_common_char_in_list list =
  let hash_table = Hashtbl.create 26 in
  List.iter (fun char -> 
    if Hashtbl.mem hash_table char then
      Hashtbl.replace hash_table char (Hashtbl.find hash_table char + 1)
    else
      Hashtbl.add hash_table char 1
  ) list;
  Hashtbl.fold (fun char count acc ->
    if count > (snd acc) then
      (char, count)
    else
      acc 
  ) hash_table (' ', 0)
  |> fst

let least_common_char_in_list list =
  let hash_table = Hashtbl.create 26 in
  List.iter (fun char -> 
    if Hashtbl.mem hash_table char then
      Hashtbl.replace hash_table char (Hashtbl.find hash_table char + 1)
    else
      Hashtbl.add hash_table char 1
  ) list;
  Hashtbl.fold (fun char count acc ->
    if count < (snd acc) then
      (char, count)
    else
      acc
  ) hash_table (' ', 10000)
  |> fst

let most_common_chars lines num_chars =
  let rec find_most_common_char col result =
    if col >= num_chars then
      (* done - return the result *)
      result
    else
      (* for each line, get the char at the current column *)
      let chars = List.map (fun line -> String.get line col) lines in
      (* find the most common char *)
      let most_common_char = most_common_char_in_list chars in
      (* Printf.printf "Most common char: %c\n" most_common_char; *)
      find_most_common_char (col + 1) (most_common_char :: result)
  in
  find_most_common_char 0 []
  |> List.rev


let least_common_chars lines num_chars =
  let rec find_least_common_char col result =
    if col >= num_chars then
      result
    else
      let chars = List.map (fun line -> String.get line col) lines in
      let least_common_char = least_common_char_in_list chars in
      find_least_common_char (col + 1) (least_common_char :: result)
  in
  find_least_common_char 0 []
  |> List.rev




let part1 filename =
  let file_contents = Utils.Input.read_file_to_string filename in
  let lines = Utils.Input.split_on_newline file_contents in
  let num_chars = String.length (List.hd lines) in
  let most_common_chars = most_common_chars lines num_chars in
  Printf.printf "Part 1: %s\n" (String.of_seq (List.to_seq most_common_chars))

let part2 filename =
  let file_contents = Utils.Input.read_file_to_string filename in
  let lines = Utils.Input.split_on_newline file_contents in
  let num_chars = String.length (List.hd lines) in
  let least_common_chars = least_common_chars lines num_chars in
  Printf.printf "Part 2: %s\n" (String.of_seq (List.to_seq least_common_chars))
