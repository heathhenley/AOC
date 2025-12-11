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

  let find_paths graph start goal skip =
    let rec dfs current_node visited acc =
      if current_node = goal then (
        Printf.printf "Found a path: %s -> %s\n" start goal; flush stdout;
        acc + 1
      )
      else if List.mem current_node skip then
        0
      else (
        if List.mem current_node visited then
          0
        else if current_node = "out" then
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


  (* of course this doesn't work but had to try
  let find_paths_2 graph start goal =
    let rec dfs current_node visited acc =
      if current_node = goal then
        if List.mem "dac" visited && List.mem "fft" visited then (
          Printf.printf "Found a path: %d\n" (acc + 1); flush stdout;
          acc + 1
        )
        else
          0
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
    *)

  let part1 _ = ()
  (*
  let part1 filename = ()
    let adj_list = filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map parse_line
    in
    find_paths adj_list "you" "out" |> Printf.printf "Part 1: %d\n"
    *)

  let part2 filename =
    let adj_list = filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map parse_line
    in
    let svr_to_dac = find_paths adj_list "svr" "dac" ["fft"] in
    let svr_to_fft = find_paths adj_list "svr" "fft" ["dac"] in
    let dac_to_fft = find_paths adj_list "dac" "fft" ["out"] in
    let fft_to_dac = find_paths adj_list "fft" "dac" ["out"] in
    let fft_to_out = find_paths adj_list "fft" "out" ["dac"] in
    let dac_to_out = find_paths adj_list "dac" "out" ["fft"] in
    Printf.printf "svr to dac: %d\n" svr_to_dac; flush stdout;
    Printf.printf "svr to fft: %d\n" svr_to_fft; flush stdout;
    Printf.printf "dac to fft: %d\n" dac_to_fft; flush stdout;
    Printf.printf "fft to dac: %d\n" fft_to_dac; flush stdout;
    Printf.printf "fft to out: %d\n" fft_to_out; flush stdout;
    Printf.printf "dac to out: %d\n" dac_to_out; flush stdout;
    let n1 = svr_to_dac * dac_to_fft * fft_to_out in
    let n2 = svr_to_fft * fft_to_dac * dac_to_out in
    Printf.printf "Part 2: %d\n" (n1 + n2)




end

module Day11 : Solution.Day = Day11_impl
include Day11_impl

let () = Days.register "11" (module Day11)
