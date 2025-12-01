module Day01 : Solution.Day = struct
  let instruction_of_line line =
    ( String.get line 0,
      int_of_string (String.sub line 1 (String.length line - 1)) )

  let wrap n =
    let result = n mod 100 in
    if result < 0 then 100 + result else result

  let to_position instr current =
    match instr with
    | 'R', x -> wrap (current + x)
    | 'L', x -> wrap (current - x)
    | _ -> failwith "unexpected char"

  let count_hits position n =
    if position = 0 then (* already there, only count loops *)
      n / 100
    else if n < position then (* didn't make it there, no hits *)
      0
    else ((n - position) / 100) + 1 (* count loops and we cross *)

  let to_position2 instr current =
    (* same as above but we need to return how many times we
    would go by 0 *)
    match instr with
    | 'R', x -> (wrap (current + x), (current + x) / 100)
    | 'L', x -> (wrap (current - x), count_hits current x)
    | _ -> failwith "unexpected char"

  let rot start instructions =
    let rec aux acc position inst =
      match inst with
      | [] -> acc (* nothing left *)
      | i :: rest ->
          (* rotate, increment if at zero, recurse *)
          let new_pos = to_position i position in
          if new_pos = 0 then aux (acc + 1) new_pos rest
          else aux acc new_pos rest
    in
    aux 0 start instructions

  let rot2 start instructions =
    let rec aux acc position inst =
      match inst with
      | [] -> acc (* nothing left *)
      | i :: rest ->
          (* rotate, increment if at zero, recurse *)
          let new_pos, flips = to_position2 i position in
          aux (acc + flips) new_pos rest
    in
    aux 0 start instructions

  let part1 filename =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map instruction_of_line
    |> rot 50
    |> Printf.printf "Part 1: %d\n"

  let part2 filename =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map instruction_of_line
    |> rot2 50
    |> Printf.printf "Part 2: %d\n"
end

include Day01

let () = Days.register "1" (module Day01)
