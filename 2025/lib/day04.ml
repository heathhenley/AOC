module Day04_impl = struct
  let grid_of_input lines =
    let rows = List.length lines in
    let cols = String.length (List.hd lines) in
    let grid = Array.make_matrix rows cols '.' in
    List.iteri
      (fun i line -> String.iteri (fun j c -> grid.(i).(j) <- c) line)
      lines;
    grid

  let directions =
    [ (0, 1); (1, 0); (0, -1); (-1, 0); (1, 1); (1, -1); (-1, 1); (-1, -1) ]

  let valid_bounds grid row col =
    row >= 0
    && row < Array.length grid
    && col >= 0
    && col < Array.length grid.(0)

  let neighbors grid row col =
    List.filter_map
      (fun (dr, dc) ->
        let new_row = row + dr in
        let new_col = col + dc in
        if valid_bounds grid new_row new_col then Some (new_row, new_col)
        else None)
      directions

  let print_grid grid =
    Array.iter
      (fun row ->
        Array.iter (fun cell -> Printf.printf "%c" cell) row;
        Printf.printf "\n")
      grid

  let is_accessible grid row col =
    List.fold_left
      (fun acc (r, c) -> acc + if grid.(r).(c) = '.' then 0 else 1)
      0 (neighbors grid row col)
    < 4

  let accessible_indices grid =
    let indices = ref [] in
    Array.iteri
      (fun i row ->
        Array.iteri
          (fun j cell ->
            if cell = '@' && is_accessible grid i j then
              indices := (i, j) :: !indices)
          row)
      grid;
    !indices

  let count_rolls grid =
    Array.fold_left
      (fun total_acc row ->
        Array.fold_left
          (fun row_acc cell -> if cell = '@' then row_acc + 1 else row_acc)
          0 row
        + total_acc)
      0 grid

  let solve grid =
    let initial_rolls = count_rolls grid in
    let indices = accessible_indices grid in
    let rec solve' idx =
      match idx with
      | [] -> initial_rolls - count_rolls grid
      | idx_list ->
          (* set all i, j in idx to '.' and recompute the accessible indices*)
          List.iter (fun (i, j) -> grid.(i).(j) <- '.') idx_list;
          solve' (accessible_indices grid)
    in
    solve' indices

  let part1 filename =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> grid_of_input
    |> accessible_indices
    |> List.length
    |> Printf.printf "Part 1: %d\n"

  let part2 filename =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> grid_of_input
    |> solve
    |> Printf.printf "Part 2: %d\n"
end

module Day04 : Solution.Day = Day04_impl
include Day04_impl

let () = Days.register "4" (module Day04)
