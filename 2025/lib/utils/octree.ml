type point = int * int * int

type cube = {
  xmin: int;
  xmax: int;
  ymin: int;
  ymax: int;
  zmin: int;
  zmax: int;
}

type t = {
  max_points: int;
  boundary_cube: cube;
  node: node;
} and
node =
| Leaf of point list
| Branch of branch
and branch = {
  top_ne: t;
  top_se: t;
  top_sw: t;
  top_nw: t;
  bottom_ne: t;
  bottom_se: t;
  bottom_sw: t;
  bottom_nw: t;
}

let branch_children branch = [
  branch.top_ne;
  branch.top_se;
  branch.top_sw;
  branch.top_nw;
  branch.bottom_ne;
  branch.bottom_se;
  branch.bottom_sw;
  branch.bottom_nw;
]

let cube_distance_sq (px, py, pz) cube =
  let dx =
    if px < cube.xmin then cube.xmin - px
    else if px > cube.xmax then px - cube.xmax
    else 0
  in
  let dy =
    if py < cube.ymin then cube.ymin - py
    else if py > cube.ymax then py - cube.ymax
    else 0
  in
  let dz =
    if pz < cube.zmin then cube.zmin - pz
    else if pz > cube.zmax then pz - cube.zmax
    else 0
  in
  dx * dx + dy * dy + dz * dz


let boundary_cube_of_points points =
  let xmin = List.fold_left (fun acc (x, _, _) -> min x acc) max_int points in
  let xmax = List.fold_left (fun acc (x, _, _) -> max x acc) min_int points in
  let ymin = List.fold_left (fun acc (_, y, _) -> min y acc) max_int points in
  let ymax = List.fold_left (fun acc (_, y, _) -> max y acc) min_int points in
  let zmin = List.fold_left (fun acc (_, _ ,z)  -> min z acc) max_int points in
  let zmax = List.fold_left (fun acc (_, _ ,z) -> max z acc) min_int points in
  { xmin; xmax; ymin; ymax; zmin; zmax }

let is_in_cube cube point =
  let x, y, z = point in
  x >= cube.xmin && x <= cube.xmax &&
  y >= cube.ymin && y <= cube.ymax &&
  z >= cube.zmin && z <= cube.zmax

(* Create a new empty octree *)
let create max_points boundary_cube = {
  max_points = max_points;
  boundary_cube = boundary_cube;
  node = Leaf [];
}

let dist2 (x1, y1, z1) (x2, y2, z2) =
  (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) + (z1 - z2) * (z1 - z2)


let rec total_points t =
  match t.node with
  | Leaf points -> List.length points
  | Branch branch ->
    List.fold_left (fun acc child -> acc + total_points child) 0 (branch_children branch)

(* Find the nearest point to a given point in the octree *)
let find_nearest point k t =
  let rec find_nearest_helper point t acc =
    if List.length acc >= k then
      acc
    else if List.length acc > total_points t then
      acc
    else (
      match t.node with
      | Leaf points ->
        let merged = points @ acc in
        let sorted_points = List.sort (fun p1 p2 ->
          compare (dist2 point p1) (dist2 point p2)
        ) merged in
        if List.length sorted_points <= k then
          sorted_points
        else
          List.take k sorted_points
      | Branch branch ->
        let children = branch_children branch in
        let inside, outside =
          List.partition (fun child -> is_in_cube child.boundary_cube point) children
        in
        let acc =
          List.fold_left (fun acc child ->
            if List.length acc >= k then acc
            else find_nearest_helper point child acc
          ) acc inside
        in
        if List.length acc >= k then
          acc
        else
          let ordered_outside =
            List.sort (fun c1 c2 ->
              compare
                (cube_distance_sq point c1.boundary_cube)
                (cube_distance_sq point c2.boundary_cube)
            ) outside
          in
          List.fold_left (fun acc child ->
            if List.length acc >= k then acc
            else find_nearest_helper point child acc
          ) acc ordered_outside
    )

  in
  find_nearest_helper point t []

let rec insert point t =
  if not (is_in_cube t.boundary_cube point) then
    invalid_arg "QuadTree.insert: point outside boundary"
  else
    match t.node with
    | Leaf points when List.length points < t.max_points ->
      { t with node = Leaf (point :: points) }
    | Leaf points ->
      let branch = split_leaf t (point :: points) in
      { t with node = branch }
    | Branch branch ->
      let updated_branch = insert_into_branch point branch in
      { t with node = Branch updated_branch }

and insert_into_branch point branch =
  if is_in_cube branch.top_ne.boundary_cube point then
    { branch with top_ne = insert point branch.top_ne }
  else if is_in_cube branch.top_se.boundary_cube point then
    { branch with top_se = insert point branch.top_se }
  else if is_in_cube branch.top_sw.boundary_cube point then
    { branch with top_sw = insert point branch.top_sw }
  else if is_in_cube branch.top_nw.boundary_cube point then
    { branch with top_nw = insert point branch.top_nw }
  else if is_in_cube branch.bottom_ne.boundary_cube point then
    { branch with bottom_ne = insert point branch.bottom_ne }
  else if is_in_cube branch.bottom_se.boundary_cube point then
    { branch with bottom_se = insert point branch.bottom_se }
  else if is_in_cube branch.bottom_sw.boundary_cube point then
    { branch with bottom_sw = insert point branch.bottom_sw }
  else if is_in_cube branch.bottom_nw.boundary_cube point then
    { branch with bottom_nw = insert point branch.bottom_nw }
  else
    invalid_arg "it doesn't fit anywhere ?!"

and split_leaf t points =
  (* split the boundary cube into 8 smaller cubes *)
  (* must be a better way to do this?*)
  let xmin = t.boundary_cube.xmin in
  let xmax = t.boundary_cube.xmax in
  let ymin = t.boundary_cube.ymin in
  let ymax = t.boundary_cube.ymax in
  let zmin = t.boundary_cube.zmin in
  let zmax = t.boundary_cube.zmax in
  let xmid = (xmin + xmax) / 2 in
  let ymid = (ymin + ymax) / 2 in
  let zmid = (zmin + zmax) / 2 in
  let top_ne = { xmin = xmid; xmax = xmax; ymin = ymid; ymax = ymax; zmin = zmin; zmax = zmid } in
  let top_se = { xmin = xmid; xmax = xmax; ymin = ymin; ymax = ymid; zmin = zmin; zmax = zmid } in
  let top_sw = { xmin = xmin; xmax = xmid; ymin = ymid; ymax = ymax; zmin = zmin; zmax = zmid } in
  let top_nw = { xmin = xmin; xmax = xmid; ymin = ymin; ymax = ymid; zmin = zmin; zmax = zmid } in
  let bottom_ne = { xmin = xmid; xmax = xmax; ymin = ymid; ymax = ymax; zmin = zmid; zmax = zmax } in
  let bottom_se = { xmin = xmid; xmax = xmax; ymin = ymin; ymax = ymid; zmin = zmid; zmax = zmax } in
  let bottom_sw = { xmin = xmin; xmax = xmid; ymin = ymid; ymax = ymax; zmin = zmid; zmax = zmax } in
  let bottom_nw = { xmin = xmin; xmax = xmid; ymin = ymin; ymax = ymid; zmin = zmid; zmax = zmax } in
  let make_child boundary_cube =
    { max_points = t.max_points; boundary_cube; node = Leaf [] }
  in
  let initial_branch = {
    top_ne = make_child top_ne;
    top_se = make_child top_se;
    top_sw = make_child top_sw;
    top_nw = make_child top_nw;
    bottom_ne = make_child bottom_ne;
    bottom_se = make_child bottom_se;
    bottom_sw = make_child bottom_sw;
    bottom_nw = make_child bottom_nw;
  } in
  let populated_branch =
    List.fold_left (fun branch point -> insert_into_branch point branch) initial_branch points
  in
  Branch populated_branch