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

  let handle_input filename =
    let parsed =
      filename
      |> Utils.Input.read_file_to_string
      |> Utils.Input.split_on_newline
      |> List.filter (fun line -> line <> "")
      |> List.map (Utils.Input.try_parse parsers)
    in
    ( parsed
      |> List.filter_map (function
        | Range x -> Some x
        | _ -> None),
      parsed
      |> List.filter_map (function
        | Ingredient x -> Some x
        | _ -> None) )

  let part1 filename =
    let ranges, available = handle_input filename in
    available
    |> List.filter (fun ingredient -> is_fresh ingredient ranges)
    |> List.length
    |> Printf.printf "Part 1: %d\n"

  let part2 filename =
    handle_input filename
    |> fst
    |> merge_ranges
    |> List.fold_left (fun acc range -> acc + (range.stop - range.start + 1)) 0
    |> Printf.printf "Part 2: %d\n"
end

module Day05 : Solution.Day = Day05_impl
include Day05_impl

let () = Days.register "5" (module Day05)
