module Day11_impl = struct
  type node = string

  (* adjacency list - node -> list of nodes it connects to
  - example:
    aaa: you hhh
    you: bbb ccc
  -> [(aaa, [you]); (you, [bbb; ccc]);)
  *)
  type graph = (node * node list) list

  let parse_line line =
    match String.split_on_char ':' line with
    | [ node; rest ] ->
        let connections =
          rest
          |> String.split_on_char ' '
          |> List.filter (fun x -> x <> "")
          |> List.map (fun x -> String.trim x)
        in
        (node, connections)
    | _ -> failwith "Invalid line"

  let find_paths_dfs graph start goal part1 =
    (* This is the better way to do it, looked it up after the fact - if you
      want to see my kind of crazy approach with a topo sort look in the
      git history.

      Regular dfs but with memo on the state that we care about.
    *)
    let memo = Utils.Memo.memo_rec (
      fun dfs (current_node, saw_fft, saw_dac) ->
        match current_node with
        | node when node = goal && (part1 || (saw_fft && saw_dac)) -> 1
        | node when node = goal -> 0
        | node ->
            let neighbors = List.assoc_opt current_node graph in
            let fft = saw_fft || (node = "fft") in
            let dac = saw_dac || (node = "dac") in
            match neighbors with
            | Some neighbors ->
                List.fold_left (fun a n -> a + dfs (n, fft, dac)) 0 neighbors
            | None -> 0
    )
    in
    memo (start, false, false)

  let part1 filename =
    let adj_list =
      filename
      |> Utils.Input.read_file_to_string
      |> Utils.Input.split_on_newline
      |> List.map parse_line
    in
    find_paths_dfs adj_list "you" "out" true|> Printf.printf "Part 1: %d\n"

  let part2 filename =
    let adj_list =
      filename
      |> Utils.Input.read_file_to_string
      |> Utils.Input.split_on_newline
      |> List.map parse_line
    in
    let paths = find_paths_dfs adj_list "svr" "out" false in
    Printf.printf "Part 2: %d\n" paths
end

module Day11 : Solution.Day = Day11_impl
include Day11_impl

let () = Days.register "11" (module Day11)
