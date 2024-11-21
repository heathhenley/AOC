open Minttea

type model = {
  rows: int;
  cols: int;
  grid: bool array array;
  steps: int;
}

let grid_to_string m =
  let grid = m.grid in
  let buf = Buffer.create (m.rows * m.cols) in
  Array.iter (fun row ->
    Array.iter (fun light ->
      Buffer.add_char buf (if light then '#' else '.')
    ) row;
    Buffer.add_char buf '\n'
  ) grid;
  Buffer.contents buf

let valid_bounds grid row col =
  row >= 0
  && row < Array.length grid
  && col >= 0
  && col < Array.length grid.(0)

let valid_neighbors grid row col =
  let neighbors = 
    [(row-1, col-1); (row-1, col); (row-1, col+1);
     (row, col-1);                 (row, col+1);
     (row+1, col-1); (row+1, col); (row+1, col+1)] in
  List.filter (fun (r, c) -> valid_bounds grid r c) neighbors

let sum_up_neighbors grid row col =
  let neighbors = valid_neighbors grid row col in
  List.fold_left (fun acc (r, c) ->
    acc + if grid.(r).(c) then 1 else 0
  ) 0 neighbors

let rec run_simulation grid n special_rules =
  match n with
  | 0 -> grid
  | _ -> 
    let rows = Array.length grid in
    let cols = Array.length grid.(0) in
    let new_grid = Array.make_matrix rows cols false in
    Array.iteri (fun row _ ->
      Array.iteri (fun col _  ->
        let neighbor_sum = sum_up_neighbors grid row col in
        match neighbor_sum with
        | 3 -> new_grid.(row).(col) <- true
        | 2 -> new_grid.(row).(col) <- grid.(row).(col)
        | _ -> new_grid.(row).(col) <- false
      ) grid.(row);
    ) grid;
    let new_grid = special_rules new_grid in
  run_simulation new_grid (n-1) special_rules

let count_lights grid =
  Array.fold_left (fun acc row ->
    acc + Array.fold_left (fun acc light ->
      acc + if light then 1 else 0
    ) 0 row
  ) 0 grid

let info_to_string m =
  Format.sprintf
    "After n=%d steps, lights lit: %d" m.steps (count_lights m.grid)

let init _model = Command.Noop

(* get a random grid *)
let initial_model =
  let model = { rows = 20; cols = 60; grid = [||]; steps = 0 } in
  let grid = Array.make_matrix model.rows model.cols false in
  Array.iteri (fun row _ ->
    Array.iteri (fun col _ ->
      grid.(row).(col) <- Random.bool ()
    ) grid.(row)
  ) grid;
  { model with grid }

let reset_grid model =
  let grid = Array.make_matrix model.rows model.cols false in
  Array.iteri (fun row _ ->
    Array.iteri (fun col _ ->
      grid.(row).(col) <- Random.bool ()
    ) grid.(row)
  ) grid;
  { model with grid; steps = 0 }

let update event model =
  match event with
  | Event.KeyDown (Key "q" | Escape) -> (model, Command.Quit)
  | Event.KeyDown (Key "r") -> (reset_grid model, Command.Noop)
  | Event.KeyDown (Key "n") ->
    let grid = run_simulation model.grid 1 (fun x -> x) in
    let steps = model.steps + 1 in
    ({ model with grid; steps }, Command.Noop)
  | _ -> (model, Command.Noop)

let view model =
  let grid = grid_to_string model in
  let info = info_to_string model in
  let intructions = "Press 'n' to advance one step, 'r' to reset, 'q' to quit" in
  Format.sprintf
  {|
%s

%s

%s
  |} info grid intructions

let app = Minttea.app ~init ~update ~view ()
let () = Minttea.start app ~initial_model