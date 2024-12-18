let read_file_to_string filename =
  let ic = open_in filename in
  let n = in_channel_length ic in
  let s = really_input_string ic n in
  close_in ic;
  s

let split_on_newline str =
  let split = str
  |> String.split_on_char '\n'
  |> List.map String.trim
  |> List.filter (fun x -> String.length x > 0) in
  split

let time_function f arg =
  let start_time = Sys.time () in
  let result = f arg in
  let end_time = Sys.time () in
  let elapsed_time = end_time -. start_time in
  Printf.printf "Elapsed time: %.6f seconds\n" elapsed_time;
  result

let valid_dirs =[
  (0, 1);
  (0, -1);
  (1, 0);
  (-1, 0);
]

let valid r c rmax cmax =
  r >= 0 && r <= rmax && c >= 0 && c <= cmax

let get_neighbors r c rmax cmax =
  let neighbors  = valid_dirs 
    |> List.map (fun (dr, dc) -> (r + dr, c + dc))
    |> List.filter (fun (r, c) -> valid r c rmax cmax)
  in
  neighbors

let first_n lst n =
  List.filteri (fun i _ -> i < n) lst


let dijkstra start goal bad_locs rmax cmax =
  (* using a hashtbl instead of heap *)
  let visited = Hashtbl.create 100 in
  let q = Hashtbl.create 100 in
  Hashtbl.add q start 0;

  (* this is because we're using a hashtbl instead of heap *)
  let find_smallest tbl =
    Hashtbl.fold
      (fun k v acc ->
        match acc with
        | None -> Some (k, v)
        | Some (_, min_v) -> if v < min_v then Some (k, v) else acc)
      tbl None
  in

  let rec dijkstra' () =
    match find_smallest q with
    | None -> None
    | Some ((r, c), cost) ->
      Hashtbl.remove q (r, c);
      if Hashtbl.mem visited (r, c) then
        dijkstra' ()
      else begin
        Hashtbl.add visited (r, c) true;
        if (r, c) = goal then
          Some cost
        else
          let neighbors =
            get_neighbors r c rmax cmax
            |> List.filter (fun (nr, nc) -> not (List.mem (nr, nc) bad_locs))
            |> List.filter (fun (nr, nc) -> not (Hashtbl.mem visited (nr, nc)))
          in
          List.iter
            (fun (nr, nc) ->
              let new_cost = cost + 1 in
              match Hashtbl.find_opt q (nr, nc) with
              | None -> Hashtbl.add q (nr, nc) new_cost
              | Some old_cost ->
                if new_cost < old_cost then
                  Hashtbl.replace q (nr, nc) new_cost)
            neighbors;
          dijkstra' ()
      end
  in
  dijkstra' ()

let slice lst start stop =
  let rec slice' lst acc idx =
    match lst with
    | [] -> acc
    | x::xs -> 
      if idx >= start && idx < stop then
        slice' xs (x::acc) (idx + 1)
      else if idx >= stop then
        acc
      else
        slice' xs acc (idx + 1)
  in
  List.rev (slice' lst [] 0)

let rec binary_search left right f bad_lst =
  if left >= right then
    List.nth bad_lst left
  else
    let mid = (left + right) / 2 in
    let cost = f (slice bad_lst 0 (mid + 1)) in
    match cost with
    | None ->
      binary_search left mid f bad_lst
    | Some _ ->
      binary_search (mid + 1) right f bad_lst
  


let part1 filename =
  let cost = filename
    |> read_file_to_string
    |> split_on_newline
    |> List.map (
        fun x ->
          x |> String.split_on_char ',' |> List.map int_of_string
      )
    |> (fun x -> first_n x 1024)
    |> List.map (fun x -> (List.nth x 1, List.nth x 0))
    |> (fun x -> dijkstra (0, 0) (70, 70) x 70 70) in
  match cost with
  | None -> Printf.printf "No path found\n"
  | Some cost ->
    Printf.printf "Part 1: %d\n" cost


let part2 filename =
  let (rbad, cbad) = filename
    |> read_file_to_string
    |> split_on_newline
    |> List.map (
        fun x ->
          x |> String.split_on_char ',' |> List.map int_of_string
      )
    |> List.map (fun x -> (List.nth x 1, List.nth x 0))
    |> (fun x -> 
         binary_search 0 ((List.length x) - 1) (
            fun bad_lst -> dijkstra (0, 0) (70, 70) bad_lst 70 70
          ) x ) in
  Printf.printf "Part 2: (%d, %d)\n" cbad rbad
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
