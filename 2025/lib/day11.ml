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

  let find_paths graph start goal =
    let rec dfs current_node visited acc =
      if current_node = goal then (
        acc + 1)
      else if List.mem current_node visited then 0
      else if current_node = "out" then 0
      else
        let neighbors = List.assoc current_node graph in
        List.fold_left
          (fun nacc neighbor ->
            (* recurse on the neighbors and add up *)
            nacc + dfs neighbor (current_node :: visited) acc)
          0 neighbors
    in
    dfs start [] 0

  let build_indegree_graph graph =
    (* loop over the graph and build a ht with node -> indegree
       where indegree is the number of nodes that point to this node 
       https://www.geeksforgeeks.org/dsa/topological-sorting-indegree-based-solution/
      - anything with 0 has nothing pointing to it
    *)
    let indegree = Hashtbl.create 100 in
    List.iter (fun (node, _) -> Hashtbl.add indegree node 0) graph;
    List.iter
      (fun (_, neighbors) ->
        List.iter
          (fun neighbor ->
            if not (Hashtbl.mem indegree neighbor) then
              Hashtbl.add indegree neighbor 1
            else
              let current = Hashtbl.find indegree neighbor in
              Hashtbl.replace indegree neighbor (current + 1))
          neighbors)
      graph;
    indegree

  let build_topological_sort graph =
    (* return the nodes in topo order
     used: https://www.geeksforgeeks.org/dsa/topological-sorting-indegree-based-solution/
    *)
    let indegree = build_indegree_graph graph in
    let indegree_list = Hashtbl.to_seq indegree |> List.of_seq in
    let sorted_nodes =
      List.sort
        (fun (_, indegree1) (_, indegree2) -> compare indegree1 indegree2)
        indegree_list
    in
    let q = Queue.create () in
    List.iter
      (fun (node, indegree) -> if indegree = 0 then Queue.add node q else ())
      sorted_nodes;
    let rec aux acc =
      if Queue.is_empty q then List.rev acc
      else
        let node = Queue.pop q in
        let res = node :: acc in
        match List.assoc_opt node graph with
        | Some neighbors ->
            List.iter
              (fun neighbor ->
                let current = Hashtbl.find indegree neighbor in
                Hashtbl.replace indegree neighbor (current - 1);
                if current - 1 = 0 then Queue.add neighbor q else ())
              neighbors;
            aux res
        | None -> aux res
    in
    aux []

  let build_memo graph =
    (* build memo table in topo order
    memo(node, saw_fft, saw_dac) = number of paths to this node from the start
    *)
    let memo = Hashtbl.create 100 in
    Hashtbl.add memo ("svr", false, false) 1;
    let sorted_nodes = build_topological_sort graph in
    let rec aux nodes =
      match nodes with
      | [] -> ()
      | node :: rest -> (
          let children = List.assoc_opt node graph in
          match children with
          | Some children ->
              (* update this node's memo entry*)
              List.iter
                (fun child ->
                  let fft = if child = "fft" then true else false in
                  let dac = if child = "dac" then true else false in
                  (* update each state (whether found fft or dac) *)
                  List.iter
                    (fun (saw_fft, saw_dac) ->
                      let pnum =
                        match
                          Hashtbl.find_opt memo (node, saw_fft, saw_dac)
                        with
                        | Some num -> num
                        | None -> 0
                      in
                      let new_state = (child, saw_fft || fft, saw_dac || dac) in
                      let cnum =
                        match Hashtbl.find_opt memo new_state with
                        | Some num -> num
                        | None -> 0
                      in
                      Hashtbl.replace memo new_state (cnum + pnum))
                    [
                      (false, false); (true, false); (false, true); (true, true);
                    ])
                children;
              aux rest
          | None -> aux rest)
    in
    aux sorted_nodes;
    memo

  let part1 filename =
    let adj_list =
      filename
      |> Utils.Input.read_file_to_string
      |> Utils.Input.split_on_newline
      |> List.map parse_line
    in
    find_paths adj_list "you" "out" |> Printf.printf "Part 1: %d\n"

  let part2 filename =
    let adj_list =
      filename
      |> Utils.Input.read_file_to_string
      |> Utils.Input.split_on_newline
      |> List.map parse_line
    in
    let memo = build_memo adj_list in
    Printf.printf "Part 2: %d\n" (Hashtbl.find memo ("out", true, true))
end

module Day11 : Solution.Day = Day11_impl
include Day11_impl

let () = Days.register "11" (module Day11)
