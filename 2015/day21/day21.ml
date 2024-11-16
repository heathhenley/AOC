(* the items that are available in the shop *)
[@@@ocaml.warning "-69"] (* disable warning for unused field name (name) *)
type shopItem = {
  name: string;
  cost: int;
  damage: int;
  armor: int;
}

type character = {
  hp: int;
  damage: int;
  armor: int;
}
(*
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
*)


(* tell ocaml these are items *)
let weapons = [|
  {name = "Dagger"; cost = 8; damage = 4; armor = 0};
  {name = "Shortsword"; cost = 10; damage = 5; armor = 0};
  {name = "Warhammer"; cost = 25; damage = 6; armor = 0};
  {name = "Longsword"; cost = 40; damage = 7; armor = 0};
  {name = "Greataxe"; cost = 74; damage = 8; armor = 0};
|]
let armor = [|
  {name = "Leather"; cost = 13; damage = 0; armor = 1};
  {name = "Chainmail"; cost = 31; damage = 0; armor = 2};
  {name = "Splintmail"; cost = 53; damage = 0; armor = 3};
  {name = "Bandedmail"; cost = 75; damage = 0; armor = 4};
  {name = "Platemail"; cost = 102; damage = 0; armor = 5};
|]
let rings = [|
  {name = "Damage +1"; cost = 25; damage = 1; armor = 0};
  {name = "Damage +2"; cost = 50; damage = 2; armor = 0};
  {name = "Damage +3"; cost = 100; damage = 3; armor = 0};
  {name = "Defense +1"; cost = 20; damage = 0; armor = 1};
  {name = "Defense +2"; cost = 40; damage = 0; armor = 2};
  {name = "Defense +3"; cost = 80; damage = 0; armor = 3};
|]

let time_function f arg =
  let start_time = Sys.time () in
  let result = f arg in
  let end_time = Sys.time () in
  let elapsed_time = end_time -. start_time in
  Printf.printf "Elapsed time: %.6f seconds\n" elapsed_time;
  result

let get_damage w r1 r2 =
  (* if -1, 0 for that category - else get the appropriate thing *)
  let w_damage = if w = -1 then 0 else weapons.(w).damage in
  let r1_damage = if r1 = -1 then 0 else rings.(r1).damage in
  let r2_damage = if r2 = -1 then 0 else rings.(r2).damage in
  w_damage + r1_damage + r2_damage

let get_defense a r1 r2 =
  let a_armor = if a = -1 then 0 else armor.(a).armor in
  let r1_armor = if r1 = -1 then 0 else rings.(r1).armor in
  let r2_armor = if r2 = -1 then 0 else rings.(r2).armor in
  a_armor + r1_armor + r2_armor

let player_will_win boss player_hp player_dmg player_armor =
  let player_damage_per_turn = max 1 (player_dmg - boss.armor) in
  let boss_damage_per_turn = max 1 (boss.damage - player_armor) in
  let player_turns_to_win = boss.hp / player_damage_per_turn in
  let boss_turns_to_win = player_hp / boss_damage_per_turn in
  let player_hp_left = player_hp - boss_turns_to_win * boss_damage_per_turn in
    (player_turns_to_win < boss_turns_to_win)
    || (player_turns_to_win = boss_turns_to_win && player_hp_left > 0)

let cost_of_gear w a r1 r2 =
  (if w = -1 then 0 else weapons.(w).cost) +
  (if a = -1 then 0 else armor.(a).cost) +
  (if r1 = -1 then 0 else rings.(r1).cost) +
  (if r2 = -1 then 0 else rings.(r2).cost)

(* Get the min cost of items you need to buy in the shop to be able
to beat the boss*)
let min_cost_to_win boss player =
  let memo = Hashtbl.create 10000 in
  let rec min_cost w a r1 r2 current_min =
    if Hashtbl.mem memo (w, a, r1, r2) then
      Hashtbl.find memo (w, a, r1, r2)
    else
      let player_damage = get_damage w r1 r2 in
      let player_defense = get_defense a r1 r2 in
      let cost = cost_of_gear w a r1 r2 in
      let wins = player_will_win boss player.hp player_damage player_defense in
      let two_diff_rings = r1 = -1 || r2 = -1 || r1 <> r2 in
      let current_min  =
        if (wins && two_diff_rings) then (min cost current_min)
        else current_min
      in
      (* if any out of bounds, skip *)
      if w = (Array.length weapons) - 1
        || a = (Array.length armor) - 1
        || r1 = (Array.length rings) - 1
        || r2 = (Array.length rings) - 1 then
        let result = current_min in
        Hashtbl.add memo (w, a, r1, r2) result;
        result
      else
        (* try all combinations *)
        let w_iter = min_cost (w + 1) a r1 r2 current_min in
        let a_iter = min_cost w (a + 1) r1 r2 current_min in
        let r1_iter = min_cost w a (r1 + 1) r2 current_min in
        let r2_iter = min_cost w a r1 (r2 + 1) current_min in
        let result = min (
          min (min a_iter w_iter) (min r1_iter r2_iter)) current_min in
        Hashtbl.add memo (w, a, r1, r2) result;
        result
  in 
  (* start with -1 for all items, except weapon (we must have a weapon) *)
  min_cost (0) (-1) (-1) (-1) max_int


let max_cost_to_lose boss player =
  let memo = Hashtbl.create 10000 in
  let rec max_cost w a r1 r2 current_max =
    if Hashtbl.mem memo (w, a, r1, r2) then
      Hashtbl.find memo (w, a, r1, r2)
    else
      let player_damage = get_damage w r1 r2 in
      let player_defense = get_defense a r1 r2 in
      let cost = cost_of_gear w a r1 r2 in
      let wins = player_will_win boss player.hp player_damage player_defense in
      let two_diff_rings = r1 = -1 || r2 = -1 || r1 <> r2 in
      let current_max  =
        if ((not wins) && two_diff_rings) then (max cost current_max)
        else current_max;
      in
      (* if any out of bounds, skip *)
      if w = (Array.length weapons) - 1
        || a = (Array.length armor) - 1
        || r1 = (Array.length rings) - 1
        || r2 = (Array.length rings) - 1 then
        let result = current_max in
        Hashtbl.add memo (w, a, r1, r2) result;
        result
      else
        (* try all combinations *)
        let w_iter = max_cost (w + 1) a r1 r2 current_max in
        let a_iter = max_cost w (a + 1) r1 r2 current_max in
        let r1_iter = max_cost w a (r1 + 1) r2 current_max in
        let r2_iter = max_cost w a r1 (r2 + 1) current_max in
        let result = max (
          max (max a_iter w_iter) (max r1_iter r2_iter)) current_max in
        Hashtbl.add memo (w, a, r1, r2) result;
        result
  in 
  (* start with -1 for all items, except weapon (we must have a weapon) *)
  max_cost (0) (-1) (-1) (-1) 0


let part1 _ =
  let boss = {hp = 103; damage = 9; armor = 2} in 
  let player = {hp = 100; damage = 0; armor = 0} in
  let min_costf = min_cost_to_win boss player in 
  Printf.printf "Part 1: %d\n" (min_costf)

let part2 _ =
  let boss = {hp = 103; damage = 9; armor = 2} in 
  let player = {hp = 100; damage = 0; armor = 0} in
  let max_costf = max_cost_to_lose boss player in
  Printf.printf "Part 2: %d\n" (max_costf)
  
(* Pass the input filename in on the command line *)
let () = time_function part1 "";
         time_function part2 "";
