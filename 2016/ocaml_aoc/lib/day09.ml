type group = {
  len : int;
  n : int;
  m : int;
  group_start : int;
}

let group_len g1 g2 =
  (* the '()'s and the 'x' plus the digits *)
  3 + String.length g1 + String.length g2

let check_for_group str start =
  let ptn = Str.regexp {|(\([0-9]+\)x\([0-9]+\))|} in
  if Str.string_match ptn str start then
    let g1, g2 = (Str.matched_group 1 str, Str.matched_group 2 str) in
    let n, m = (int_of_string g1, int_of_string g2) in
    Ok { len = group_len g1 g2; n; m; group_start = start }
  else Error "No group found"

let expanded_size str =
  let n = String.length str in
  (* this helper is basically to loop *)
  let rec aux idx acc =
    if idx >= n then acc
    else
      match check_for_group str idx with
      | Ok { len; n; m; _ } -> aux (idx + len + n) (acc + (n * m))
      | Error _ -> aux (idx + 1) (acc + 1)
  in
  aux 0 0

let rec expanded_size_rec str =
  (*
    for part 2, we need to recurse and expand the chars inside any groups to
    get the total length of the string.
  *)
  let n = String.length str in
  (* this helper is basically to loop *)
  let rec aux idx acc =
    if idx >= n then acc
    else
      match check_for_group str idx with
      | Ok { len; n; m; group_start } ->
          (* we have a group to expand - recursively *)
          let start_exp = group_start + len in
          let group_str = String.sub str start_exp n in
          let count = expanded_size_rec group_str in
          aux (idx + len + n) (acc + (count * m))
      | Error _ -> aux (idx + 1) (acc + 1)
  in
  aux 0 0

let part1 filename =
  let total =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.fold_left (fun acc s -> acc + expanded_size s) 0
  in
  Printf.printf "Part 1: %d\n" total

let part2 filename =
  let total =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.fold_left (fun acc s -> acc + expanded_size_rec s) 0
  in
  Printf.printf "Part 2: %d\n" total
