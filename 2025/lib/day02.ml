module Day02_impl = struct
  (*
  This updated version of the solution is heavily based on this solution
  I found on reddit: https://github.com/ranjeethmahankali/adventofcode/blob/main/2025/src/day_2.rs
  
  More info in the readme.md file and the history shows the evolution of this
  solution. I would never have figured this out on my own, especially not when
  trying to do it at open.
  *)

  let parse s = String.split_on_char '-' s |> List.map int_of_string

  let get_invalid pattern period start stop =
    (* make all the multiples of the pattern that are within the range inc.*)
    let d_start =
      if start mod pattern = 0 then start / pattern else (start / pattern) + 1
    in
    let d_min = if period = 0 then 0 else Utils.Math.pow10 (period - 1) in
    let d_min = max d_min d_start in
    let d_max = Utils.Math.pow10 period - 1 in
    let d_max = min d_max (stop / pattern) in
    if d_min > d_max then []
    else
      let rec aux acc d =
        if d > d_max then acc else aux ((d * pattern) :: acc) (d + 1)
      in
      let res = aux [] d_min in
      res

  let generate_valid_periods part stop =
    let nd = Utils.Math.digit_count stop in
    let half_nd = nd / 2 in
    match part with
    | 1 -> [ nd / 2 ]
    | 2 -> Utils.Iter.range 1 (half_nd + 1)
    | _ -> failwith "invalid part"

  let generate_patterns part stop =
    (* generate all the patterns *)
    let nd = Utils.Math.digit_count stop in
    let periods = generate_valid_periods part stop in
    let build_pattern period repeats =
      let pow = Utils.Math.pow10 period in
      let rec aux acc remaining =
        if remaining <= 1 then acc else aux ((acc * pow) + 1) (remaining - 1)
      in
      aux 1 repeats
    in
    let rec collect_repeats period repeat_max n acc =
      if n > repeat_max then acc
      else
        let pattern = build_pattern period n in
        collect_repeats period repeat_max (n + 1) ((pattern, period) :: acc)
    in
    match part with
    | 1 ->
        List.fold_left
          (fun acc period ->
            if period <= 0 then acc else (build_pattern period 2, period) :: acc)
          [] periods
    | 2 ->
        List.fold_left
          (fun acc period ->
            if period <= 0 then acc
            else
              let repeat_max = nd / period in
              if repeat_max < 2 then acc
              else collect_repeats period repeat_max 2 acc)
          [] periods
    | _ -> failwith "invalid part"

  let check_range part start stop =
    let patterns = generate_patterns part stop in
    let invalid_ids =
      List.fold_left
        (fun acc (pattern, period) ->
          get_invalid pattern period start stop @ acc)
        [] patterns
      |> List.sort_uniq compare
    in
    invalid_ids

  let solve part filename =
    filename
    |> Utils.Input.read_file_to_string
    |> String.split_on_char ','
    |> List.map parse
    |> List.fold_left
         (fun acc x -> check_range part (List.hd x) (List.nth x 1) @ acc)
         []
    |> List.sort_uniq compare
    |> List.fold_left ( + ) 0

  let part1 filename = solve 1 filename |> Printf.printf "Part 1: %d\n"
  let part2 filename = solve 2 filename |> Printf.printf "Part 2: %d\n"
end

module Day02 : Solution.Day = Day02_impl
include Day02_impl

let () = Days.register "2" (module Day02)
