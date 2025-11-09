(* state looks like:
   item: floor

   - parse input into state - I'm an idiot - input is only 4 floors and
     it's text, not a grid - so just going to input it
   - try all available moves (need an "is valid state" check)
   - stop when we find one with all on the last floor
*)

type t = {
  items : string list array; (* a list of the items on each floor *)
  elevator : int; (* the floor the elevator is on *)
}

let is_blank str =
  (* todo: maybe useful for input module *)
  let n = String.length str in
  let rec aux i =
    if i >= n then true
    else
      match str.[i] with
      | ' ' | '\t' | '\r' | '\012' -> aux (i + 1)
      | _ -> false
  in
  aux 0

let stop state =
  (* all things on the top floor ? *)
  let num_floors = Array.length state.items in
  let num_items =
    Array.fold_left (fun acc items -> acc + List.length items) 0 state.items
  in
  List.length state.items.(num_floors - 1) = num_items

let can_match item idx floor =
  (* check if any item can be matched with the item at idx *)
  let item_type = String.get item 0 in
  floor
  |> List.mapi (fun i it -> (i, it))
  |> List.exists (fun (item_idx, item) ->
         item_type = String.get item 0 && idx <> item_idx)

(*let check_valid_floor floor  =
  (* check if the floor is valid ...
    - floor is in bounds
    - two "generators" can't be on the same floor without a matching a microchip
    - at least one item must be with the elevator at 'floor'
    *)
    (* for each item on the floor - if we can match it, remove it from the
      list - it's matched so it's basically inert now *)
    let unmatched_items = List.filteri (fun idx item ->
      not (can_match item idx floor)
    ) floor in
    if List.length unmatched_items = 0 then
      true
    else
      (* might still be ok ...*)
      (* if there's an unmatched 'G' and unmatched 'M' that's not ok *)
      (* otherwise, there can be multiple G's together or multiple M's together *)
      let has_g = List.exists (fun str -> String.get str 1 = 'G') unmatched_items in
      let has_m = List.exists (fun str -> String.get str 1 = 'M') unmatched_items in
      not (has_g && has_m)
*)

let check_valid_floor2 fl =
  (* the labels for the Gens on this floor *)
  let gens =
    fl |> List.filter (fun s -> s.[1] = 'G') |> List.map (fun s -> s.[0])
  in
  match gens with
  | [] -> true (* no gens on this floor, so it's valid *)
  | gens ->
      fl
      |> List.for_all (fun s ->
             s.[1] <> 'M' (* not a micro chip*)
             || List.mem s.[0] gens (* or it's a chip but the gen is here too *))

let is_valid_state { items; elevator } =
  (* check if the state is valid
    - floor is in bounds
    - two "generators" can't be on the same floor without a matching a microchip
    - at least one item must be with the elevator at 'elevator'
  *)
  if elevator < 0 || elevator >= Array.length items then false
  else
    (* check if the floor has any items  - eg where the elevator is *)
    let items_on_floor = items.(elevator) in
    List.length items_on_floor > 0 && Array.for_all check_valid_floor2 items

let is_empty_below_elevator { items; elevator } =
  (* if there are no items on any floor below the elevator, then
    we won't need to check states that go down
  *)
  let rec aux i =
    if i = elevator then (* base case - we're at the elevator *)
      true
    else
      (* floor is empty - go up one *)
      List.length items.(i) = 0 && aux (i + 1)
  in
  aux 0

let generate_possible_moves { items; elevator } =
  (* We can go up or down from where the elevator is, with 1 or 2
   of the items on the current floor *)
  let items_on_floor = items.(elevator) in
  let item_1comb = Utils.Iter.combinations items_on_floor 1 in
  let item_2comb = Utils.Iter.combinations items_on_floor 2 in
  (* trimming a bit
     - no need to go down if there are no
     items down there
     - try up2 first, then up1, then down1
     - TBD: do we ever need to go down2?
       --> Apparently not for part1, but seems needed for part2, without it
           is was never finding a solution [ possible I didn't wait long enough though ]
     should have probably used BFS instead of DFS with all this trimming...
  *)
  let make_states combos dir =
    let target_floor = elevator + dir in
    if target_floor < 0 || target_floor >= Array.length items then []
    else
      List.filter_map
        (fun bring ->
          let new_items = Array.copy items in
          (* remove these items from the current floor *)
          new_items.(elevator) <-
            List.filter
              (fun item -> not (List.mem item bring))
              new_items.(elevator);
          (* add these items to the target floor *)
          new_items.(target_floor) <- bring @ new_items.(target_floor);
          if check_valid_floor2 new_items.(target_floor) then
            Some { items = new_items; elevator = target_floor }
          else None)
        combos
  in
  let up2 = make_states item_2comb 1 in
  let up1 = make_states item_1comb 1 in
  let down1 = make_states item_1comb (-1) in
  let down2 = make_states item_2comb (-2) in
  if up2 <> [] then up2 @ down2 @ down1 else up2 @ up1 @ down2 @ down1

let key_of_state state =
  let floor_key fl = fl |> List.sort String.compare |> String.concat "," in
  let floors = state.items |> Array.map floor_key |> Array.to_list in
  String.concat "|" floors ^ "|E:" ^ string_of_int state.elevator

let key_of_state_ignore_names { items; elevator } =
  let tbl = Hashtbl.create 16 in
  Array.iteri
    (fun f lst ->
      List.iter
        (fun s ->
          let el = s.[0] in
          (* label*)
          let kind = s.[1] in
          let chip_floor, gen_floor =
            match Hashtbl.find_opt tbl el with
            | Some (chip_floor, gen_floor) -> (chip_floor, gen_floor)
            | None -> (-1, -1)
          in
          (* update the right part of th tuple*)
          let chip_floor, gen_floor =
            if kind = 'M' then (f, gen_floor) else (chip_floor, f)
          in
          Hashtbl.replace tbl el (chip_floor, gen_floor))
        lst)
    items;
  (* dump so that states with labels swapped look the same to trim the states

  eg for example:
    0:1|0:2|E:0 for example can be both:

    F1: HM, LM
    F2: HG
    F3: LG

    and also:
    F1: HM, LM
    F2: LG
    F3: HG
  *)
  let pairs =
    Hashtbl.fold (fun _ (mf, gf) acc -> (mf, gf) :: acc) tbl []
    |> List.sort compare
    |> List.map (fun (m, g) -> string_of_int m ^ ":" ^ string_of_int g)
    |> String.concat "|"
  in
  pairs ^ "|E:" ^ string_of_int elevator

let rec walk state moves_so_far current_best visited =
  (* let key = key_of_state state in *)
  let key = key_of_state_ignore_names state in
  (* much faster for part2 *)
  match Hashtbl.find_opt visited key with
  | Some x when x <= moves_so_far -> current_best
  | _ ->
      Hashtbl.add visited key moves_so_far;
      (* check if we're out of bounds *)
      if moves_so_far >= current_best then current_best
      else if stop state then min current_best moves_so_far
      else
        (* get all possible moves from the current state  - it's a list of
         * new states *)
        let possible_moves =
          List.filter is_valid_state (generate_possible_moves state)
        in
        List.fold_left
          (fun (* recurse on the new state, add 1 to the moves, and take the min *)
                 acc new_state ->
            let new_best = walk new_state (moves_so_far + 1) acc visited in
            min acc new_best)
          current_best possible_moves

let partn_impl n state =
  (*
  start with state and elev at 1st floor
  - we always need at least one item (does it need to be M / G?)
  - we can move up or down one floor at a time
  - we can bring 1 or 2 items at a time
  - M / G can only be together on the same if they're matching (LM + LG)
  - So they either always need to be alone, or if they're together they need to
    be matched
  - Min moves to get to the top floor with all items?

To solve:
  - need to generate a possible moves from current state
  - recurse on them
  - early stop if the move isn't valid
  - early stop if the number of moves is greater than the current best soln
  *)
  let visited = Hashtbl.create 10000 in
  let result = walk { items = state; elevator = 0 } 0 max_int visited in
  Printf.printf "Part %d: %d\n" n result;
  flush stdout

let part1 _ =
  let state =
    [|
      [ "TG"; "TM"; "PG"; "SG" ];
      (* 1st floor *)
      [ "PM"; "SM" ];
      (* 2nd floor *)
      [ "MG"; "MM"; "RG"; "RM" ];
      (* 3rd floor *)
      [];
      (* 4th floor *)
    |]
  in
  partn_impl 1 state

let part2 _ =
  let state =
    [|
      [ "TG"; "TM"; "PG"; "SG"; "EG"; "EM"; "DG"; "DM" ];
      (* 1st floor *)
      [ "PM"; "SM" ];
      (* 2nd floor *)
      [ "MG"; "MM"; "RG"; "RM" ];
      (* 3rd floor *)
      [];
      (* 4th floor *)
    |]
  in
  partn_impl 2 state
