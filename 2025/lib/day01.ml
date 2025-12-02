module Day01_impl = struct
  let dial_size = 100

  let instruction_of_line line =
    ( String.get line 0,
      int_of_string (String.sub line 1 (String.length line - 1)) )

  let wrap n =
    let result = n mod dial_size in
    if result < 0 then dial_size + result else result

  let count_crossings_left position step =
    if position = 0 then step / dial_size
    else if step < position then 0
    else ((step - position) / dial_size) + 1

  let rotate instr current =
    match instr with
    | 'R', x ->
        let new_pos = wrap (current + x) in
        let loops = (current + x) / dial_size in
        let zeros = if new_pos = 0 && current <> 0 then 1 else 0 in
        (new_pos, loops, zeros)
    | 'L', x ->
        let new_pos = wrap (current - x) in
        let loops = count_crossings_left current x in
        let zeros = if new_pos = 0 && current <> 0 then 1 else 0 in
        (new_pos, loops, zeros)
    | _ -> failwith "unexpected char"

  let unlock_safe start f instructions =
    let rec aux acc position inst =
      match inst with
      | [] -> acc (* nothing left *)
      | i :: rest ->
          let new_pos, loops, zeros = rotate i position in
          aux (f acc zeros loops) new_pos rest
    in
    aux 0 start instructions

  let part1 filename =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map instruction_of_line
    |> unlock_safe 50 (fun acc zeros _ -> acc + zeros)
    |> Printf.printf "Part 1: %d\n"

  let part2 filename =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map instruction_of_line
    |> unlock_safe 50 (fun acc _ loops -> acc + loops)
    |> Printf.printf "Part 2: %d\n"
end

module Day01 : Solution.Day = Day01_impl

include Day01_impl

let () = Days.register "1" (module Day01)
