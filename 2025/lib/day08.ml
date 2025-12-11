module Day08_impl = struct
  type junction = {
    position : int * int * int;
    idx : int;
  }

  (* union find type - each junction will start in it's own circuit as it's own
     parent
  *)
  type circuit = {
    (* the root of the circuit for each junction *)
    junction_parents : (int, int) Hashtbl.t;
    (* the rank of the circuit for each junction *)
    junction_ranks : (int, int) Hashtbl.t;
    (* the size of the circuit for each junction *)
    junction_sizes : (int, int) Hashtbl.t;
  }

  let create_circuit junctions =
    let circuit =
      {
        junction_parents = Hashtbl.create 100;
        junction_ranks = Hashtbl.create 100;
        junction_sizes = Hashtbl.create 100;
      }
    in
    List.iter
      (fun j ->
        Hashtbl.add circuit.junction_parents j.idx j.idx;
        Hashtbl.add circuit.junction_sizes j.idx 1;
        Hashtbl.add circuit.junction_ranks j.idx 0)
      junctions;
    circuit

  let rec find_root c j_idx =
    match Hashtbl.find_opt c.junction_parents j_idx with
    | Some parent when parent = j_idx -> j_idx (* j is the root *)
    | Some parent ->
        let r = find_root c parent in
        Hashtbl.replace c.junction_parents j_idx r;
        (* path compression *)
        r
    | None -> failwith "Junction not found in circuit"

  let union c j1_idx j2_idx =
    let root1 = find_root c j1_idx in
    let root2 = find_root c j2_idx in
    if root1 = root2 then
      (* already in the same circuit *)
      ()
    else
      (* union the two circuits *)
      let rank1 = Hashtbl.find c.junction_ranks root1 in
      let rank2 = Hashtbl.find c.junction_ranks root2 in
      let size1 = Hashtbl.find c.junction_sizes root1 in
      let size2 = Hashtbl.find c.junction_sizes root2 in
      if rank1 > rank2 then (
        (* root1 is the new root - stick smaller rank under larger rank *)
        Hashtbl.replace c.junction_parents root2 root1;
        Hashtbl.replace c.junction_sizes root1 (size1 + size2);
        ())
      else if rank1 < rank2 then (
        (* root2 is the new root - stick smaller rank under larger rank *)
        Hashtbl.replace c.junction_parents root1 root2;
        Hashtbl.replace c.junction_sizes root2 (size1 + size2);
        ())
      else if rank1 = rank2 then (
        (* tie - choose root1 as the new root and increment the rank *)
        Hashtbl.replace c.junction_parents root2 root1;
        Hashtbl.replace c.junction_sizes root1 (size1 + size2);
        Hashtbl.replace c.junction_ranks root1 (rank1 + 1);
        ())

  let dist2 (x1, y1, z1) (x2, y2, z2) =
    ((x1 - x2) * (x1 - x2)) + ((y1 - y2) * (y1 - y2)) + ((z1 - z2) * (z1 - z2))

  let junction_distance j1 j2 = dist2 j1.position j2.position

  let junctions_of_lines lines =
    lines
    |> List.mapi (fun idx line ->
        line |> String.split_on_char ',' |> List.map int_of_string |> function
        | [ x; y; z ] -> { position = (x, y, z); idx }
        | _ -> failwith "Invalid point")

  let compute_pair_distances junctions =
    junctions
    |> (fun j -> Utils.Iter.combinations j 2)
    |> List.map (fun t ->
        match t with
        | j1 :: j2 :: _ -> (j1.idx, j2.idx, junction_distance j1 j2)
        | _ -> failwith "Invalid input")

  let compare_unique (r1, s1) (r2, s2) =
    if s1 > s2 then -1
    else if s1 < s2 then 1
    else if r1 < r2 then -1
    else if r1 > r2 then 1
    else 0

  let part1_impl filename n =
    let junctions =
      Utils.Input.read_file_to_string filename
      |> Utils.Input.split_on_newline
      |> junctions_of_lines
    in
    (* sort all the pairs by distance *)
    let sorted_pair_distances =
      junctions
      |> compute_pair_distances
      |> List.sort (fun (_, _, d1) (_, _, d2) -> compare d1 d2)
      |> List.take n
    in
    let circuit = create_circuit junctions in

    (* keep adding closest pair *)
    let rec add_next_closest dists =
      match dists with
      | [] -> ()
      | (j1_idx, j2_idx, _) :: tl ->
          union circuit j1_idx j2_idx;
          add_next_closest tl
    in
    add_next_closest sorted_pair_distances;

    List.map
      (fun j ->
        let root = find_root circuit j.idx in
        (root, Hashtbl.find circuit.junction_sizes root))
      junctions
    |> List.sort_uniq compare_unique
    |> List.take 3
    |> List.fold_left (fun acc (_, size) -> acc * size) 1
    |> Printf.printf "Part 1: %d\n"

  let part1 filename = part1_impl filename 1000

  let largest_circuit circuit =
    Hashtbl.fold (fun _ size acc -> max size acc) circuit.junction_sizes 0

  let fst3 (x, _, _) = x

  let part2 filename =
    let junctions =
      Utils.Input.read_file_to_string filename
      |> Utils.Input.split_on_newline
      |> junctions_of_lines
    in
    let sorted_pair_distances =
      junctions
      |> compute_pair_distances
      |> List.sort (fun (_, _, d1) (_, _, d2) -> compare d1 d2)
    in

    let circuit = create_circuit junctions in

    let num_junctions = List.length junctions in

    (* keep adding closest pair until all junctions are in the same circuit *)
    let rec add_next_closest dists =
      match dists with
      | [] -> None
      | (j1_idx, j2_idx, _) :: tl ->
          union circuit j1_idx j2_idx;
          if largest_circuit circuit < num_junctions then add_next_closest tl
          else Some (j1_idx, j2_idx)
    in
    match add_next_closest sorted_pair_distances with
    | Some (j1_idx, j2_idx) ->
        let j1 = List.find (fun j -> j.idx = j1_idx) junctions in
        let j2 = List.find (fun j -> j.idx = j2_idx) junctions in
        let x1, x2 = (fst3 j1.position, fst3 j2.position) in
        Printf.printf "Part 2: %d\n" (abs (x1 * x2))
    | None -> Printf.printf "Part 2: No solution found\n"
end

module Day08 : Solution.Day = Day08_impl
include Day08_impl

let () = Days.register "8" (module Day08)
