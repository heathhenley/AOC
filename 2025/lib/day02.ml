module Day02_impl : Solution.Day = struct

  let is_valid id =
    let n = String.length id in
    if n mod 2 = 1 then
      true
    else
      let s1 = String.sub id 0 (n/2) in
      let s2 = String.sub id (n/2) (n/2) in
      if s1 = s2 then false else true
  
  let is_valid2 id =
    let regex = Str.regexp {|^\(.+\)\1+$|} in
    not (Str.string_match regex id 0)

  
  let check_range start stop =
    let rec aux i acc =
      if i > stop then
        acc
      else if is_valid (string_of_int i) then
        aux (i + 1) acc
      else
        aux (i + 1) (i :: acc)
    in aux start []
  
  let check_range2 start stop =
    let rec aux i acc =
      if i > stop then
        acc
      else if is_valid2 (string_of_int i) then
        aux (i + 1) acc
      else
        aux (i + 1) (i :: acc)
    in aux start []

  let parse s =
    String.split_on_char '-' s
    |> List.map int_of_string

  let part1 filename =
  filename
  |> Utils.Input.read_file_to_string
  |> String.split_on_char ','
  |> List.map parse
  |> List.fold_left (fun acc x ->
     (*Printf.printf "start: %d, stop: %d\n" (List.hd x) (List.nth x 1);*)
     let invalid = check_range (List.hd x) (List.nth x 1) in
     (*List.iter (Printf.printf "  invalid: %d\n") invalid;*)
     acc + List.fold_left (fun acc2 y -> acc2 + y ) 0 invalid
  ) 0
  |> Printf.printf "Part 1: %d\n"

  let part2 filename =
  filename
  |> Utils.Input.read_file_to_string
  |> String.split_on_char ','
  |> List.map parse
  |> List.fold_left (fun acc x ->
     (*Printf.printf "start: %d, stop: %d\n" (List.hd x) (List.nth x 1);*)
     let invalid = check_range2 (List.hd x) (List.nth x 1) in
     (*List.iter (Printf.printf "  invalid: %d\n") invalid;*)
     acc + List.fold_left (fun acc2 y -> acc2 + y ) 0 invalid
  ) 0
  |> Printf.printf "Part 2: %d\n"


end


module Day02 : Solution.Day = Day02_impl

include Day02_impl

let () = Days.register "2" (module Day02)