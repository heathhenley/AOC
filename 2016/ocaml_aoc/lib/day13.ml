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

let part1_impl number start goal =
  Printf.printf "Start: (%d, %d)\n" (fst start) (snd start);
  Printf.printf "Goal: (%d, %d)\n" (fst goal) (snd goal);
  Printf.printf "Secret number: %d\n" number;
  let res =
    Utils.Search.bfs start
      ~neighbors:(get_neighbors number)
      ~on_visit:(fun node dist -> if node = goal then `Stop dist else `Continue)
  in
  Printf.printf "Part 1: %d\n" (Option.get res)

let part2_impl number start steps =
  let visited = ref 0 in 
  let res =
    Utils.Search.bfs start
      ~neighbors:(get_neighbors number)
      ~on_visit:(
        fun _ dist ->
          if dist > steps then `Stop (!visited)
          else (
            visited := !visited + 1;
            `Continue
          )
      )
  in
  Printf.printf "Part 2: %d\n" (Option.get res)

let part1 _ = part1_impl 1362 (1, 1) (31, 39)
let part2 _ = part2_impl 1362 (1, 1) 50
