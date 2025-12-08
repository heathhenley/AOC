module Day08_impl = struct

  type junction = {
    position: int * int * int;
    idx: int;
  }

  type circuit = {
    junctions: junction list;
    edges: (int * int) list; (* junction.idx * junction.idx *)
  }

  let add_node circuit node =
    { circuit with junctions = node :: circuit.junctions }

  let add_edge circuit node1 node2 =
    { circuit with edges = (node1, node2) :: circuit.edges }

  let get_neighbors circuit node =
    let node_idx = node.idx in
    List.filter_map (
      fun (n1, n2) -> if n1 = node_idx then Some n2 else if n2 = node_idx then Some n1 else None) circuit.edges
    |> List.map (fun idx -> List.find (fun j -> j.idx = idx) circuit.junctions)
  
  let search circuit start goal =
    Utils.Search.bfs start
    ~neighbors:(get_neighbors circuit)
    ~on_visit:(
      fun node _ ->
        if node.idx = goal.idx then
          `Stop (Some node)
        else
          `Continue)
  
  let get_connected_components circuit =
    (* use a dfs to find the connected components *)
    let rec dfs acc cur visited =
      if List.mem cur visited then
        acc
      else
        (* add the neighbors to the accumulator *)
        let neighbors = get_neighbors circuit cur in
        let acc = List.fold_left (fun acc n -> n :: acc) acc neighbors in
        (* recurse on the neighbors *)
        List.fold_left (fun acc n -> dfs acc n (n :: visited)) acc neighbors
      in List.map (fun j -> dfs [] j []) circuit.junctions

  let print_points points =
    List.iter (fun (x, y, z) ->
      Printf.printf "%d %d %d\n" x y z
    ) points

  let dist2 (x1, y1, z1) (x2, y2, z2) =
    (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) + (z1 - z2) * (z1 - z2)

  let junction_distance j1 j2 =
    dist2 j1.position j2.position

  let junctions_of_lines lines =
    lines
    |> List.mapi (fun idx line ->
      line
      |> String.split_on_char ','
      |> List.map int_of_string
      |> (function [x; y; z] -> { position = (x, y, z); idx = idx } | _ -> failwith "Invalid point")
    )

  let closest_junction juction junctions =
    junctions
    |> List.map (fun j -> (j,  junction_distance juction j))
    |> List.sort (fun (_, d1) (_, d2) -> compare d1 d2)
    |> List.take 2
    |> (fun x -> List.nth x 1)

  let dedup_compare j1 j2 k1 k2 d1 d2 =
    (* make ij and ji compare equal so sort_uniq works *)
    if d1 < d2 then -1 else if d1 > d2 then 1
    else if j1.position < k2.position then -1
    else if j2.position > k1.position then 1 else 0

  let fst3 (x, _, _) = x
  let snd3 (_, y, _) = y
  let trd3 (_, _, z) = z
  
  let part1 filename = 
    let junctions =
      Utils.Input.read_file_to_string filename
      |> Utils.Input.split_on_newline
      |> junctions_of_lines
    in
    (* for each point junction, find the point closest to it, and the distance 
       between, them and sort by that, this is the order to process them in,
       but we need to depulicate
    *)
    let ordered =
    junctions
    |> List.map (
      fun j -> let (j2, dist) = closest_junction j junctions in (j, j2, dist))
    |> List.sort_uniq (fun (j1, j2, d1) (k1, k2, d2) -> dedup_compare j1 j2 k1 k2 d1 d2)
    |> List.map (
      fun (j1, j2, dist) ->
        Printf.printf "%d: (%d, %d, %d) -> (%d, %d, %d) = %d\n" j1.idx (fst3 j1.position) (snd3 j1.position) (trd3 j1.position) (fst3 j2.position) (snd3 j2.position) (trd3 j2.position) dist; (j1, j2, dist))
    in
    (* for each of the top ordered pairs, make new circuit connection between
       them unless they are already connected
    *)
    (* add all the edges to the circuit *)
    let circuit = List.fold_left (
      fun circuit (j1, j2, _) ->
        match search circuit j1 j2 with
        | Some _ -> circuit (* already connected *)
        | None -> add_edge circuit j1.idx j2.idx
    ) { junctions = junctions; edges = [] } ordered in
    let connected_components = get_connected_components circuit in
    List.iter (fun c -> Printf.printf "Connected component: %d\n" (List.length c)) connected_components;
    Printf.printf "Part 1: %d\n" 0

  let part2 _ = Printf.printf "Part 2: %d\n" 0
end

module Day08 : Solution.Day = Day08_impl
include Day08_impl

let () = Days.register "8" (module Day08)
