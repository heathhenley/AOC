module Day02_impl = struct
  let is_valid_re regex id = not (Str.string_match regex (string_of_int id) 0)

  let check_range start stop valid =
    let rec aux i acc =
      if i > stop then acc
      else if valid i then aux (i + 1) acc
      else aux (i + 1) (i :: acc)
    in
    aux start []

  let parse s = String.split_on_char '-' s |> List.map int_of_string

  let solve filename valid =
    filename
    |> Utils.Input.read_file_to_string
    |> String.split_on_char ','
    |> List.map parse
    |> List.fold_left
         (fun acc x ->
           let invalid = check_range (List.hd x) (List.nth x 1) valid in
           acc + List.fold_left (+) 0 invalid)
         0

  let part1 filename =
    let valid n =
      let nd = Utils.Math.digit_count n in
      if nd mod 2 <> 0 then true
      else
        let period = nd / 2 in
        let pattern = int_of_float (1. +. 10. ** (float_of_int period)) in
        n mod pattern <> 0
    in
    solve filename valid |> Printf.printf "Part 1: %d\n"

  let part2 filename =
    let valid n =
      let nd = Utils.Math.digit_count n in
      let half = nd / 2 in
      (* now we need to try more periods / repeats - test numbers up to half *)
      let rec aux period =
        if period > half then true
        else if nd mod period <> 0 then aux (period + 1)
        else (* found a valid period *)
          let repeats = nd / period in
          (* need to make the pattern like
          p = 10^(0*period) + 10^(1*period) + 10^(2*period) + ... + 10^((repeats-1)*period) *)
          let pattern = List.fold_left (
            fun acc k -> 
              int_of_float (10. ** (float_of_int (k * period))) + acc
            ) 0 (Utils.Iter.range 0 repeats)
            in
          (* check if any patterns divide n evenly *)
          if n mod pattern <> 0 then aux (period + 1) else false
        in
        aux 1
    in
    solve filename valid |> Printf.printf "Part 2: %d\n"
end

module Day02 : Solution.Day = Day02_impl
include Day02_impl

let () = Days.register "2" (module Day02)
