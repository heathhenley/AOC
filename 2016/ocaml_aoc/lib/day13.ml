(*
  We can go up, down, left right
  - from start, do a bfs
  - need to be able to determine if the potential
    step is a wall or not  
*)

let rec num_set_bits acc num =
  (* add 1 if lsb is set - then trim it and try again *)
  if num <= 0 then acc else num_set_bits (acc + (num land 1)) (num asr 1)

let is_odd x = x mod 2 = 1

let f x y c = (x * x) + (3 * x) + (2 * x * y) + y + (y * y) + c

let is_wall x y c = f x y c |> num_set_bits 0 |> is_odd

let is_valid x y c = x >= 0 && y >= 0 && not (is_wall x y c)

let get_neighbors c (x, y) =
  [ (0, 1); (0, -1); (1, 0); (-1, 0) ]
  |> List.filter_map (fun (dx, dy) ->
         let nx, ny = (x + dx, y + dy) in
         if is_valid nx ny c then Some (nx, ny) else None)

let bfs start ~get_neighbors ~stop_condition ~init_result ~result_maker =
  let q = Queue.create () in
  let v = Hashtbl.create 100 in
  let res = init_result () in
  Queue.add (start, 0) q;
  Hashtbl.add v start ();

  while not (Queue.is_empty q) do
    let node, dist = Queue.pop q in
    (* get all neighbors
       filter invalid
       enque
    *)
    if stop_condition dist node v then res := result_maker node dist v
    else
      get_neighbors node
      |> List.iter (fun (nx, ny) ->
             if not (Hashtbl.mem v (nx, ny)) then (
               Queue.add ((nx, ny), dist + 1) q;
               Hashtbl.add v (nx, ny) ()))
  done;
  !res

let part1_impl number start goal =
  Printf.printf "Start: (%d, %d)\n" (fst start) (snd start);
  Printf.printf "Goal: (%d, %d)\n" (fst goal) (snd goal);
  Printf.printf "Secrete number: %d\n" number;
  let res =
    bfs start
      ~get_neighbors:(get_neighbors number)
      ~stop_condition:(fun _ node _ -> node = goal) 
      ~init_result:(fun () -> ref 0)
      ~result_maker:(fun _ dist _ -> dist)
  in
  Printf.printf "Part 1: %d\n" res

let part2_impl number start steps =
  let res =
    bfs start
      ~get_neighbors:(get_neighbors number)
      ~stop_condition:(fun dist _ _ -> dist = steps)
      ~init_result:(fun () -> ref 0)
      ~result_maker:(fun _ _ v -> Hashtbl.length v)
  in
  Printf.printf "Part 2: %d\n" res

let part1 _ = part1_impl 1362 (1, 1) (31, 39)
let part2 _ = part2_impl 1362 (1, 1) 50
