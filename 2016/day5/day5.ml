open Digestif


let time_function f arg =
  let start_time = Sys.time () in
  let result = f arg in
  let end_time = Sys.time () in
  let elapsed_time = end_time -. start_time in
  Printf.printf "Elapsed time: %.6f seconds\n" elapsed_time;
  result


let generate_password start length difficulty =
  let check_str = String.make difficulty '0' in
  let rec generate_password' password idx =
    if String.length password = length then
      password
    else
      let idx_str = string_of_int idx in
      let hash = MD5.digest_string (start ^ idx_str) |> MD5.to_hex in
      if String.sub hash 0 difficulty = check_str then
        generate_password' (password ^ String.sub hash difficulty 1) (idx + 1)
      else
        generate_password' password (idx + 1)
  in
  generate_password' "" 0


let generate_password_2 start length difficulty =
  let check_str = String.make difficulty '0' in
  let rec generate_password' password idx =
    let count_set = Array.fold_left (
      fun acc x -> if x = ' ' then acc else acc + 1
    ) 0 password in
    if count_set = length then
      password
    else
      let idx_str = string_of_int idx in
      let hash = MD5.digest_string (start ^ idx_str) |> MD5.to_hex in
      if String.sub hash 0 difficulty = check_str then
        if hash.[difficulty] >= '0' && hash.[difficulty] <= '7' then
          let char_idx = int_of_string (String.sub hash difficulty 1) in
          let next_char = String.sub hash (difficulty + 1) 1 in
          if char_idx < length && password.(char_idx) = ' ' then
            Array.set password char_idx next_char.[0];
            generate_password' password (idx + 1)
          else
            generate_password' password (idx + 1)
        else
          generate_password' password (idx + 1)
  in
  let password = Array.make length ' ' in
  generate_password' password 0 |> Array.to_seq |> String.of_seq


let part1 _ =
  let puzzle_input = "uqwqemis" in
  let password = generate_password puzzle_input 8 5 in
  Printf.printf "Part 1: %s\n" password 


let part2 _ =
  let puzzle_input = "uqwqemis" in
  let password = generate_password_2 puzzle_input 8 5 in
  Printf.printf "Part 2: %s\n" password
  

(* Pass the input filename in on the command line *)
let () =
      time_function part1 ();
      time_function part2 ();
