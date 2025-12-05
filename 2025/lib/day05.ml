module Day05_impl = struct
  type range = {
    start : int;
    stop : int;
  }

  type ingredient = int

  type lines =
    | Range of range
    | Ingredient of ingredient
    | Empty of unit

  let parsers =
    [
      Utils.Input.parse "%d-%d" (fun start stop -> Range { start; stop });
      Utils.Input.parse "%d" (fun ingredient -> Ingredient ingredient);
    ]

  let is_fresh ingredient ranges =
    List.exists
      (fun range -> ingredient >= range.start && ingredient <= range.stop)
      ranges

  let merge_ranges ranges =
    (* we need to merge overlapping ranges int minimal set of ranges so we
     figure out how many ingredients they all cover
     - sort ranges by start
     - if end of current is greater than end of next, merge (start_current, end_next) --> (this is actually covered the max below)
     - if end of current is greater than start of next, merge them with
      (start_current, max(end_current, end_next))
    - if end of current is less than start of next, add current to result - they cannot be merged
     *)
    let sorted = List.sort (fun a b -> compare a.start b.start) ranges in

    let rec aux acc remaining =
      match remaining with
      | [] -> List.rev acc
      | curr :: next :: rest ->
          if curr.stop >= next.start then
            let merged =
              { start = curr.start; stop = max curr.stop next.stop }
            in
            aux acc (merged :: rest)
          else aux (curr :: acc) (next :: rest)
      | [ curr ] -> curr :: acc
    in
    aux [] sorted

  let part1 filename =
    let parsed =
      filename
      |> Utils.Input.read_file_to_string
      |> Utils.Input.split_on_newline
      |> List.map (Utils.Input.try_parse parsers)
    in
    let ranges =
      parsed
      |> List.filter (function
        | Range _ -> true
        | _ -> false)
      |> List.map (function
        | Range x -> x
        | _ -> failwith "Expected range")
    in
    let available =
      parsed
      |> List.filter (function
        | Ingredient _ -> true
        | _ -> false)
      |> List.map (function
        | Ingredient x -> x
        | _ -> failwith "Expected ingredient")
    in
    let fresh_ingredients =
      available |> List.filter (fun ingredient -> is_fresh ingredient ranges)
    in
    Printf.printf "Part 1: %d\n" (List.length fresh_ingredients)

  let part2 filename =
    let parsed =
      filename
      |> Utils.Input.read_file_to_string
      |> Utils.Input.split_on_newline
      |> List.map (Utils.Input.try_parse parsers)
    in
    let res =
      parsed
      |> List.filter (function
        | Range _ -> true
        | _ -> false)
      |> List.map (function
        | Range x -> x
        | _ -> failwith "Expected range")
      |> merge_ranges
      (*|> List.iter (
      fun range -> Printf.printf "Range: %d-%d\n" range.start range.stop
    )*)
      |> List.fold_left
           (fun acc range -> acc + (range.stop - range.start + 1))
           0
    in
    Printf.printf "Part 2: %d\n" res
end

module Day05 : Solution.Day = Day05_impl
include Day05_impl

let () = Days.register "5" (module Day05)
