module Day07_impl = struct
  let grid_of_input lines =
    let rows = List.length lines in
    let cols = String.length (List.hd lines) in
    let grid = Array.make_matrix rows cols '.' in
    List.iteri
      (fun i line -> String.iteri (fun j c -> grid.(i).(j) <- c) line)
      lines;
    grid

  let valid_bounds grid row col =
    row >= 0
    && row < Array.length grid
    && col >= 0
    && col < Array.length grid.(0)

  let neighbors grid row col =
    match grid.(row).(col) with
    | '.' | 'S' ->
        let new_row = row + 1 in
        if valid_bounds grid new_row col then [ (new_row, col) ] else []
    | '^' ->
        List.filter_map
          (fun (dr, dc) ->
            let new_row = row + dr in
            let new_col = col + dc in
            if valid_bounds grid new_row new_col then Some (new_row, new_col)
            else None)
          [ (1, 1); (1, -1) ]
    | _ -> failwith "Invalid grid cell"

  let print_grid grid =
    Array.iter
      (fun row ->
        Array.iter (fun cell -> Printf.printf "%c" cell) row;
        Printf.printf "\n")
      grid

  let find_start grid =
    Utils.Search.bfs (0, 0) ~size:100
      ~neighbors:(fun (row, col) ->
        List.filter_map
          (fun (dr, dc) ->
            let new_row = row + dr in
            let new_col = col + dc in
            if valid_bounds grid new_row new_col then Some (new_row, new_col)
            else None)
          [ (1, 0); (0, 1); (-1, 0); (0, -1) ])
      ~on_visit:(fun node _ ->
        match node with
        | row, col when grid.(row).(col) = 'S' -> `Stop (row, col)
        | _ -> `Continue)

  let count_paths grid start =
    let q = Queue.create () in
    let paths_to_node = Hashtbl.create 100 in
    Queue.add start q;
    Hashtbl.add paths_to_node start 1;
    while not (Queue.is_empty q) do
      let r, c = Queue.pop q in
      let current_paths = Hashtbl.find paths_to_node (r, c) in
      List.iter
        (fun (new_r, new_c) ->
          if not (Hashtbl.mem paths_to_node (new_r, new_c)) then (
            Queue.add (new_r, new_c) q;
            Hashtbl.add paths_to_node (new_r, new_c) current_paths)
          else
            let prev_paths = Hashtbl.find paths_to_node (new_r, new_c) in
            Hashtbl.replace paths_to_node (new_r, new_c)
              (prev_paths + current_paths))
        (neighbors grid r c)
    done;
    let num_rows = Array.length grid in
    Hashtbl.fold
      (fun (r, _) paths acc -> if r = num_rows - 1 then acc + paths else acc)
      paths_to_node 0

  let count_paths_dfs grid start =
    (*
       Saw this after the fact in reviewing solutions. Much simpler than what
       I originally did, that version is count_paths above.
    *)
    let dfs =
      Utils.Memo.memo_rec (fun self (row, col) ->
          if not (valid_bounds grid row col) then 0
          else if row = Array.length grid - 1 then 1
          else
            match grid.(row).(col) with
            | '.' | 'S' -> self (row + 1, col)
            | '^' -> self (row + 1, col + 1) + self (row + 1, col - 1)
            | _ -> failwith "Invalid grid cell")
    in
    dfs start

  let part1 filename =
    let grid =
      Utils.Input.read_file_to_string filename
      |> Utils.Input.split_on_newline
      |> grid_of_input
    in
    let start = find_start grid |> Option.get in
    let splits = ref 0 in
    let _ =
      Utils.Search.bfs start ~size:100
        ~neighbors:(fun (row, col) -> neighbors grid row col)
        ~on_visit:(fun (row, col) _ ->
          match grid.(row).(col) with
          | '^' ->
              splits := !splits + 1;
              `Continue
          | _ -> `Continue)
    in
    Printf.printf "Part 1: %d\n" !splits

  let part2 filename =
    let grid =
      Utils.Input.read_file_to_string filename
      |> Utils.Input.split_on_newline
      |> grid_of_input
    in
    let start = find_start grid |> Option.get in
    let paths = count_paths_dfs grid start in
    Printf.printf "Part 2: %d\n" paths
end

module Day07 : Solution.Day = Day07_impl
include Day07_impl

let () = Days.register "7" (module Day07)
