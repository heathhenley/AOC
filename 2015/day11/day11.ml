open Str

let time_function f arg =
  let start_time = Sys.time () in
  let result = f arg in
  let end_time = Sys.time () in
  let elapsed_time = end_time -. start_time in
  Printf.printf "Elapsed time: %.6f seconds\n" elapsed_time;
  result

(* This is the starting password *)
let puzzle_input = "hepxcrrq"


(* go from base 26 string to base 10 number *)
let base26_to_base10 str =
  let chars = "abcdefghijklmnopqrstuvwxyz" in
  let max_base = String.length str - 1 in
  let rec base26_to_base10' str idx total =
    (* idx is the location in the string, total is sum of bits up to idx *)
    match str with
    | _ when idx > max_base -> total (* we're done *)
    | first :: rest ->
      (* get the index of the character - this is the digit *)
      let char_idx = String.index chars first in
      (* add the digit to the total *)
      let exponent = int_of_float (
        (float_of_int 26) ** (float_of_int (max_base - idx))) in
      let new_total = total + (char_idx * exponent) in
      base26_to_base10' rest (idx + 1) new_total
    | _ -> total
  in base26_to_base10' (List.of_seq (String.to_seq str)) 0 0


(* go from base 10 number to base 26 string *)
let base10_to_base26 num =
  let chars = "abcdefghijklmnopqrstuvwxyz" in
  let rec base10_to_base26' num b26_str =
    match num with
    | 0 -> b26_str
    | _ ->
      (* get the digit for this place *)
      let digit = num mod 26 in 
      (* add the digit to the string and recurse *)
      let new_b26_str = (String.make 1 (String.get chars digit)) ^ b26_str in
      base10_to_base26' (num / 26) new_b26_str
  in base10_to_base26' (int_of_string num) ""

(* helper to increment base 26 *)
let incr_b26 str =
  let num = base26_to_base10 str in
  let new_num = num + 1 in
  base10_to_base26 (string_of_int new_num)


let str_match str pattern idx = Str.string_match (regexp pattern) str idx

(* helper to check for two distinct pairs *)
let has_two_distinct_pairs str =
  let pattern = "\\(\\([a-z]\\)\\)\\1" in
  let rec find_pairs idx pairs =
    match idx with
    | _ when idx >= String.length str -> pairs (* we're done *)
    | _ when str_match str pattern idx ->
      let new_pairs = Str.matched_string str in
      let matched_pos = Str.match_beginning () in
      (* if it's a new match, skip otherwise add it to the list *)
      if (List.mem new_pairs pairs) then find_pairs (matched_pos + 1) pairs
      else find_pairs (matched_pos + 2) (new_pairs :: pairs)
    | _ -> find_pairs (idx + 1) pairs
  in let pairs = find_pairs 0 [] in
  List.length pairs >= 2


(* helper to check for 3 character run *)
let has_3_char_run str =
  let rec find_run lst =
    match lst with
    | a :: b :: c :: rest ->
      if (Char.code a + 1 = Char.code b) && (Char.code b + 1 = Char.code c) then true
      else find_run (b :: c :: rest)
    | _ -> false
  in find_run (List.of_seq (String.to_seq str))



(* find the password - keep recursing until one matches the constraints *)
let next_password current_b26 =
  let rec next current_b26 =
    (* check the current one for stopping constraint *)
    match current_b26 with
    | _ when str_match ".*[iol].*" current_b26 0 ->
      next (incr_b26 current_b26)
    | _ when not (has_two_distinct_pairs current_b26) ->
      next (incr_b26 current_b26)
    | _ when not (has_3_char_run current_b26) ->
      next (incr_b26 current_b26)
    | _ -> current_b26
  in next (incr_b26 current_b26)



let part1 () =
  Printf.printf "Part 1: %s, next: %s\n"
    puzzle_input (next_password puzzle_input)


let part2 () =
  let part1_result = next_password puzzle_input in
  Printf.printf "Part 2: %s\n" (next_password part1_result)
  
let () = time_function part1 (); time_function part2 ();
