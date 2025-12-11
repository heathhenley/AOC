module Day11_impl = struct

  type node = string

  (* adjacency list - node -> list of nodes it connects to
  - example:
    aaa: you hhh
    you: bbb ccc
  -> {aaa: [you], you: [bbb, ccc]}
  will switch to ht or set if needed
  *)
  type graph = 
    (node * node list) list

  let parse_line line =
    match String.split_on_char ':' line with
    | [node; rest] ->
      let connections =
        rest
        |> String.split_on_char ' '
        |> List.filter (fun x -> x <> "")
        |> List.map (fun x -> String.trim x)
      in
      (node, connections)
    | _ -> failwith "Invalid line"

  let find_paths graph start goal =
    let rec dfs current_node visited acc =
      if current_node = goal then
        acc + 1
      else (
        if List.mem current_node visited then
          0
        else
          let neighbors = List.assoc current_node graph in
          List.fold_left (fun nacc neighbor ->
            (* recurse on the neighbors and add up *)
            nacc + dfs neighbor (current_node :: visited) acc
          ) 0 neighbors
      )
    in
    dfs start [] 0

  let part1 filename =
    let adj_list = filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map parse_line
    in
    find_paths adj_list "you" "out" |> Printf.printf "Part 1: %d\n"

  let part2 _ = print_endline"Not implemented"

end

module Day11 : Solution.Day = Day11_impl
include Day11_impl

let () = Days.register "11" (module Day11)
