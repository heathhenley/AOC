module Day02_impl : Solution.Day = struct
  let is_valid regex id = not (Str.string_match regex id 0)

  let check_range start stop f =
    let rec aux i acc =
      if i > stop then acc
      else if f (string_of_int i) then aux (i + 1) acc
      else aux (i + 1) (i :: acc)
    in
    aux start []

  let parse s = String.split_on_char '-' s |> List.map int_of_string

  let part1 filename =
    let checker = is_valid (Str.regexp {|^\(.+\)\1$|}) in
    filename
    |> Utils.Input.read_file_to_string
    |> String.split_on_char ','
    |> List.map parse
    |> List.fold_left
         (fun acc x ->
           let invalid = check_range (List.hd x) (List.nth x 1) checker in
           acc + List.fold_left (fun acc2 y -> acc2 + y) 0 invalid)
         0
    |> Printf.printf "Part 1: %d\n"

  let part2 filename =
    let checker = is_valid (Str.regexp {|^\(.+\)\1+$|}) in
    filename
    |> Utils.Input.read_file_to_string
    |> String.split_on_char ','
    |> List.map parse
    |> List.fold_left
         (fun acc x ->
           let invalid = check_range (List.hd x) (List.nth x 1) checker in
           acc + List.fold_left (fun acc2 y -> acc2 + y) 0 invalid)
         0
    |> Printf.printf "Part 2: %d\n"
end

module Day02 : Solution.Day = Day02_impl
include Day02_impl

let () = Days.register "2" (module Day02)
