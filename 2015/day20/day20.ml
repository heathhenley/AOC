(* Day 20, 2015 *)
let time_function f arg =
  let start_time = Sys.time () in
  let result = f arg in
  let end_time = Sys.time () in
  let elapsed_time = end_time -. start_time in
  Printf.printf "Elapsed time: %.6f seconds\n" elapsed_time;
  result

let puzzle_input = 34000000

let get_factors n =
  let rec get_factors' n i factors =
    match i with
    | i when i * i > n -> factors
    | i when
        (n mod i = 0)
        -> get_factors' n (i + 1) (i :: (n / i) :: factors)
    | _ -> get_factors' n (i + 1) factors
  in get_factors' n 1 []

let de_duplicate lst =
  let rec de_duplicate' list' seen =
    match list' with
    | [] -> seen
    | hd :: tl when List.mem hd seen -> de_duplicate' tl seen
    | hd :: tl -> de_duplicate' tl (hd :: seen)
  in de_duplicate' lst []

let sum_list lst =
  List.fold_left (+) 0 lst

let get_presents house multiplier limit =
  let factors = get_factors house in
  let factors = de_duplicate factors in
  let factors = List.filter (fun x -> x * limit > house) factors in 
  let presents = sum_list factors in
  presents * multiplier

let rec find_first_house target current_house multiplier limit =
  let presents = get_presents current_house multiplier limit in
  match target with
  | _ when presents >= target -> current_house
  | _ -> find_first_house target (current_house + 1) multiplier limit

let part1 _ =
  let house = find_first_house puzzle_input 1 10 1000000000 in
  Printf.printf "Part 1: %d\n" house

let part2 _ =
  let house = find_first_house puzzle_input 1 11 50 in
  Printf.printf "Part 2: %d\n" house


(* Pass the input filename in on the command line *)
let () = 
      time_function part1 "";
      time_function part2 "";
