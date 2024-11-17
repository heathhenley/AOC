(* Day 21 - 2015 *)
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

type gearState = {
  weapon: int;
  armor: int;
  ring1: int;
  ring2: int;
}

let initialGearState = {weapon = 0; armor = -1; ring1 = -1; ring2 = -1}

let time_function f arg =
  let start_time = Sys.time () in
  let result = f arg in
  let end_time = Sys.time () in
  let elapsed_time = end_time -. start_time in
  Printf.printf "Elapsed time: %.6f seconds\n" elapsed_time;
  result

let get_damage s =
  (* if -1, 0 for that category - else get the appropriate thing *)
  let w_damage = if s.weapon = -1 then 0 else weapons.(s.weapon).damage in
  let r1_damage = if s.ring1 = -1 then 0 else rings.(s.ring1).damage in
  let r2_damage = if s.ring2 = -1 then 0 else rings.(s.ring2).damage in
  w_damage + r1_damage + r2_damage

let get_defense s =
  let a_armor = if s.armor = -1 then 0 else armor.(s.armor).armor in
  let r1_armor = if s.ring1 = -1 then 0 else rings.(s.ring1).armor in
  let r2_armor = if s.ring2 = -1 then 0 else rings.(s.ring2).armor in
  a_armor + r1_armor + r2_armor

let get_cost_of_gear (s: gearState) =
  (if s.weapon = -1 then 0 else weapons.(s.weapon).cost) +
  (if s.armor = -1 then 0 else armor.(s.armor).cost) +
  (if s.ring1 = -1 then 0 else rings.(s.ring1).cost) +
  (if s.ring2 = -1 then 0 else rings.(s.ring2).cost)

let player_will_win (boss: character) (player: character) (s: gearState) =
  let player_damage = get_damage s in
  let player_defense = get_defense s in
  let player_damage_per_turn = max 1 (player_damage - boss.armor) in
  let boss_damage_per_turn = max 1 (boss.damage - player_defense) in
  let player_turns_to_win = boss.hp / player_damage_per_turn in
  let boss_turns_to_win = player.hp / boss_damage_per_turn in
  let player_hp_left = player.hp - boss_turns_to_win * boss_damage_per_turn in
    (player_turns_to_win < boss_turns_to_win)
    || (player_turns_to_win = boss_turns_to_win && player_hp_left > 0)

let valid_gear_state s =
  let r1 = s.ring1 in
  let r2 = s.ring2 in
  (r1 = -1 || r2 = -1 || r1 <> r2) && (
    s.weapon < Array.length weapons
    && s.armor < Array.length armor
    && s.ring1 < Array.length rings
    && s.ring2 < Array.length rings
  )

let neighbors s =
  let n = 
  [{s with weapon = s.weapon + 1};
   {s with armor = s.armor + 1};
   {s with ring1 = s.ring1 + 1};
   {s with ring2 = s.ring2 + 1};]
  in List.filter valid_gear_state n


(* Get the min cost of items you need to buy in the shop to be able
to beat the boss*)
let min_cost_to_win boss player =
  let memo = Hashtbl.create 10000 in
  let rec min_cost current s =
    match Hashtbl.find_opt memo s with
    | Some v ->  v
    | None ->
      let current_cost = 
        if player_will_win boss player s
        then get_cost_of_gear s
        else current
      in
      let neighbor_costs = List.map (min_cost current_cost) (neighbors s) in
      let best_cost =
        List.fold_left min current_cost neighbor_costs
      in Hashtbl.add memo s best_cost;
  best_cost in 
  min_cost max_int initialGearState

(* Get the max cost of items you need to buy in the shop but still lose *)
let max_cost_to_lose boss player =
  let memo = Hashtbl.create 10000 in
  let rec max_cost current s =
    match Hashtbl.find_opt memo s with
    | Some v ->  v
    | None ->
      let current_cost = 
        if player_will_win boss player s
        then current
        else get_cost_of_gear s
      in
      let neighbor_costs = List.map (max_cost current_cost) (neighbors s) in
      let best_cost =
        List.fold_left (fun acc x -> max acc x) current_cost neighbor_costs
      in Hashtbl.add memo s best_cost;
  best_cost in 
  max_cost 0 initialGearState

let part1 _ =
  let boss = {hp = 103; damage = 9; armor = 2} in 
  let player = {hp = 100; damage = 0; armor = 0} in
  let min_cost = min_cost_to_win boss player in 
  Printf.printf "Part 1: %d\n" (min_cost)

let part2 _ =
  let boss = {hp = 103; damage = 9; armor = 2} in 
  let player = {hp = 100; damage = 0; armor = 0} in
  let max_cost = max_cost_to_lose boss player in 
  Printf.printf "Part 2: %d\n" (max_cost)
  
(* Pass the input filename in on the command line *)
let () = time_function part1 "";
         time_function part2 "";
