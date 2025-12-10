module Day09_impl = struct

  let tile_of_line line =
    String.split_on_char ',' line
    |> List.map (fun s -> int_of_string s)
    |> (fun x -> match x with
      | [x; y] -> (x, y)
      | _ -> failwith "Invalid input"
    )

  let pairs_of_tiles tiles = Utils.Iter.combinations tiles 2

  let area (t1, t2) =
    match t1, t2 with
    | (x1, y1), (x2, y2) -> (abs ((x2 - x1)) + 1) * (abs ((y2 - y1)) + 1)

  let print_pair (_, t1, t2) =
    Printf.printf "area: %d\n" (area (t1, t2));
    match t1, t2 with
    | (x1, y1), (x2, y2) ->
      Printf.printf "x: %d, y: %d\n" x1 y1;
      Printf.printf "x: %d, y: %d\n" x2 y2

  let sorted_rectangles_of_pairs tiles =
    tiles
    |> pairs_of_tiles
    |> List.map (fun t -> 
      match t with
      | t1 :: t2 :: _ -> (area (t1, t2), t1, t2)
      | _ -> failwith "Invalid input"
    )
    |> List.sort (fun (d, _, _) (d', _, _) -> - (compare d d'))

  let other_corners t1 t2 =
    (* quick swapski to get the other corners *)
    match t1, t2 with
    | (x1, y1), (x2, y2) ->
      (x1, y2), (x2, y1)

  let poly_edges poly =
    List.combine poly (List.tl poly @ [List.hd poly])

  let bounding_rect rect =
    (* xmin, ymin, xmax, ymax *)
    let xmin = List.fold_left (fun acc (x, _) -> min acc x) max_int rect in
    let ymin = List.fold_left (fun acc (_, y) -> min acc y) max_int rect in
    let xmax = List.fold_left (fun acc (x, _) -> max acc x) min_int rect in
    let ymax = List.fold_left (fun acc (_, y) -> max acc y) min_int rect in
    (xmin, ymin), (xmax, ymax)

  let print_grid tiles =
    let xmin = List.fold_left (fun acc (x, _) -> min acc x) max_int tiles in
    let ymin = List.fold_left (fun acc (_, y) -> min acc y) max_int tiles in
    let xmax = List.fold_left (fun acc (x, _) -> max acc x) min_int tiles in
    let ymax = List.fold_left (fun acc (_, y) -> max acc y) min_int tiles in
    let grid = Array.make_matrix (ymax - ymin + 1) (xmax - xmin + 1) '.' in
    List.iter (fun (x, y) -> grid.(y - ymin).(x - xmin) <- '#') tiles;
    Array.iter (fun row ->
      Array.iter (fun cell -> Printf.printf "%c" cell) row;
      Printf.printf "\n") grid

  let intersects bbox edges  =
  (* use aabb intersection algorithm on each edge
     - looked this up after not being able to get the 'generl' one to
       work https://kishimotostudios.com/articles/aabb_collision/
     - this only works because of how the input is set up, no 'snaking' back
       on itself or anything like that
  *)
  let (rx_min, ry_min), (rx_max, ry_max) = bbox in
  List.exists (fun edge ->
    let p1, p2 = edge in
    let min_x = min (fst p1) (fst p2) in
    let max_x = max (fst p1) (fst p2) in
    let min_y = min (snd p1) (snd p2) in
    let max_y = max (snd p1) (snd p2) in
    rx_min < max_x && rx_max > min_x && ry_min < max_y && ry_max > min_y
  ) edges


  let part1 filename =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map tile_of_line
    |> sorted_rectangles_of_pairs
    |> List.hd
    |> (fun (d, _, _) -> Printf.printf "Part 1: %d\n" d)

  let part2 filename =
    let tiles =
      filename
      |> Utils.Input.read_file_to_string
      |> Utils.Input.split_on_newline
      |> List.map tile_of_line
    in
    let rectangles =
      sorted_rectangles_of_pairs tiles
    in
    let poly_tiles = tiles @ [List.hd tiles] in
    let poly_edges = poly_edges poly_tiles in
    let rec find_best_rect candidates =
      match candidates with
      | [] -> 0
      | (d, t1, t2) :: tl ->
        let t3, t4 = other_corners t1 t2 in
        let rect = [t1; t3; t2; t4] in
        let br = bounding_rect rect in
        if intersects br poly_edges then (
          find_best_rect tl
        )
        else
          d
       in
        find_best_rect rectangles |> Printf.printf "Part 2: %d\n"

end

module Day09 : Solution.Day = Day09_impl
include Day09_impl

let () = Days.register "9" (module Day09)
