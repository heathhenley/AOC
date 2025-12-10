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

  let point_on_edge (a, b) (c, d) (x, y) =
    if a = c && x = a then (* vertical edge *)
      min b d <= y && y <= max b d
    else if b = d && y = b then (* horizontal edge *)
      min a c <= x && x <= max a c
    else false

  let point_in_poly poly (x, y) =
    (* Ray casting copy/pasta from python impl online*)
    let len = List.length poly in
    let check_point inside j i =
      let xi, yi = List.nth poly i in
      let xj, yj = List.nth poly j in
      let yi, yj = float_of_int yi, float_of_int yj in
      let xi, xj = float_of_int xi, float_of_int xj in
      let x, y = float_of_int x, float_of_int y in
      if point_on_edge (xi, yi) (xj, yj) (x, y) then true else
      if (yi > y) <> (yj > y) then
        let x_intersection = (xj -. xi) *. (y -. yi) /. (yj -. yi) +. xi in
        if x < x_intersection then not inside else inside
      else
        inside
    in
    let rec aux i j inside =
      if i >= len then inside
      else aux (i + 1) i (check_point inside j i)
    in
    aux 0 (len - 1) false

  let poly_edges poly =
    List.combine poly (List.tl poly @ [List.hd poly])

  let rect_edges rect =
    List.combine rect (List.tl rect @ [List.hd rect])

  let bounding_rect rect =
    (* xmin, ymin, xmax, ymax *)
    let xmin = List.fold_left (fun acc (x, _) -> min acc x) max_int rect in
    let ymin = List.fold_left (fun acc (_, y) -> min acc y) max_int rect in
    let xmax = List.fold_left (fun acc (x, _) -> max acc x) min_int rect in
    let ymax = List.fold_left (fun acc (_, y) -> max acc y) min_int rect in
    (xmin, ymin), (xmax, ymax)

  let edge_intersects_rect (ex1, ey1) (ex2, ey2) br =
    let rx1, ry1 = fst br in
    let rx2, ry2 = snd br in
    if ey1 = ey2 then (* horizontal edge *)
      ry1 < ey1 && ey1 < ry2 && max ex1 ex2 > rx1 && min ex1 ex2 < rx2
    else if ex1 = ex2 then (* vertical edge *)
      rx1 < ex1 && ex1 < rx2 && max ey1 ey2 > ry1 && min ey1 ey2 < ry2
    else
      false

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
    print_grid tiles;
    let rectangles =
      sorted_rectangles_of_pairs tiles
    in
    (* just going to go though them starting with the biggest possible rectangle
       - need to make the other corners
       - they need to be within the bounds of the polygon defined by the
         original tiles
       - and finally now edges of the rectange can intersect with the polygon
    *)
    let poly_tiles = tiles @ [List.hd tiles] in
    let rec find_best_rect candidates =
      (* they are sorted by area so as soon as we find one we're done *)
      match candidates with
      | [] -> 0
      | (d, t1, t2) :: tl ->
        (* get the other corners - these can be any two corners of the rect?*)
        let t3, t4 = other_corners t1 t2 in
        let rect = [t1; t3; t2; t4] in
        Printf.printf "Checking - area: %d\n" d;
        List.iter (fun (x, y) -> Printf.printf "(%d, %d)\n" x y) rect;
        Printf.printf "\n";
        
        (* now we need to check if all corners are with in the poly *)
        if not (List.for_all (point_in_poly poly_tiles) rect) then (
          Printf.printf "Not in poly\n";
          find_best_rect tl
        )
        else
          (*
          maybe we found it - check the edges now
          - WIP almost working but answer too low so we're filtering out some valid ones, I think it's the right idea and it's actually completing
          so that's a start
          *)
          let br = bounding_rect rect in
          let poly_edges = poly_edges tiles in
          Printf.printf "In poly\n";
          (* do any of the edges of poly intersect with the rect? *)
          if List.exists (fun edge ->
            let p1, p2 = edge in
            Printf.printf "bbox: (%d, %d) - (%d, %d)\n" (fst (fst br)) (snd (fst br)) (fst (snd br)) (snd (snd br));
            let res = edge_intersects_rect p1 p2 br in 
            Printf.printf "edge (%d, %d) - (%d, %d) intersects: %b\n" (fst p1) (snd p1) (fst p2) (snd p2) res;
            res
          ) poly_edges then (
            Printf.printf "Edges intersect\n";
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
