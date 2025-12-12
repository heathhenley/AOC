module Day12_impl = struct

  let areas = [7; 6; 7; 7; 7; 5]

  let part1 filename =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.filter (fun line -> line <> "")
    |> List.map (fun line -> String.trim line)
    |> List.filter_map (
      fun line ->
        if String.contains line 'x' then
          match String.split_on_char ':' line with
          | [ base_s; rest ] ->
            let base =
              base_s
              |> String.split_on_char 'x'
              |> List.filter (
                fun s -> s <> "")
              |> List.map int_of_string in
            let counts = rest
            |> String.split_on_char ' '
            |> List.filter (fun s -> s <> "")
            |> List.map int_of_string
            in Some (base, counts)
          | _ -> None
        else
          None
    )
    |> List.fold_left (fun acc (base, counts) ->
      let area = List.hd base * List.hd (List.tl base) in
      let min_needed = List.fold_left2 (
        fun acc2 count area -> acc2 + count * area
      ) 0 counts areas in
      let max_needed = (List.fold_left (+) 0 counts) * 9 in
      (* not even enough area in the grid *)
      if area < min_needed then
        acc
      else if area >= max_needed then (* plenty of area in the grid *)
        acc + 1
      else (* might fit, but would need manipulate *)
        failwith "You're gonna have to actually solve this one"
      ) 0
    |> Printf.printf "Part 1: %d\n"
  let part2 _ = ()
end

module Day12 : Solution.Day = Day12_impl
include Day12_impl

let () = Days.register "12" (module Day12)
