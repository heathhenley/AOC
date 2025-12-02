module Day01 : Solution.Day = struct
  let instruction_of_line line =
    ( String.get line 0,
      int_of_string (String.sub line 1 (String.length line - 1)) )

  let wrap n =
    let result = n mod 100 in
    if result < 0 then 100 + result else result

  let count_crossings_left position step =
    (* count how many times we cross 0 - this includes landing on 0*)
    if position = 0 then step / 100
    else if step < position then (* didn't make it there, no crossings *)
      0
    (* count loops and we cross the first time, and then again for how
       ever many times 100 fits *)
      else ((step - position) / 100) + 1

  let to_position instr current =
    match instr with
    | 'R', x ->
        let new_pos = wrap (current + x) in
        let loops = (current + x) / 100 in
        let zeros = if new_pos = 0 && current <> 0 then 1 else 0 in
        (new_pos, loops, zeros)
    | 'L', x ->
        let new_pos = wrap (current - x) in
        let loops = count_crossings_left current x in
        let zeros = if new_pos = 0 && current <> 0 then 1 else 0 in
        (new_pos, loops, zeros)
    | _ -> failwith "unexpected char"

  let rot start f instructions =
    let rec aux acc position inst =
      match inst with
      | [] -> acc (* nothing left *)
      | i :: rest ->
          let new_pos, loops, zeros = to_position i position in
          aux (f acc zeros loops) new_pos rest
    in
    aux 0 start instructions

  let part1 filename =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map instruction_of_line
    |> rot 50 (fun acc zeros _ -> acc + zeros)
    |> Printf.printf "Part 1: %d\n"

  let part2 filename =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map instruction_of_line
    |> rot 50 (fun acc _ loops -> acc + loops)
    |> Printf.printf "Part 2: %d\n"
end

include Day01

let () = Days.register "1" (module Day01)
