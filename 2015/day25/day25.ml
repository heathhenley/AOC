let time_function f arg =
  let start_time = Sys.time () in
  let result = f arg in
  let end_time = Sys.time () in
  let elapsed_time = end_time -. start_time in
  Printf.printf "Elapsed time: %.6f seconds\n" elapsed_time;
  result

let get_code start target_row target_col =
  let rec get_code' row col code =
    if row = target_row && col = target_col then code
    else
      let code' = (code * 252533) mod 33554393 in
      (* just need to calculate what the x, y of the next code is *)
      let row' = if row - 1 < 0 then col + 1 else row - 1 in
      let col' = if row - 1 < 0 then 0 else col + 1 in
      get_code' row' col' code'
  in
  get_code' 0 0 start

let part1 _ =
  let start = 20151125 in
  let res = get_code start 2980 3074 in
  Printf.printf "Part 1: %d\n" res


let part2 _ =
  Printf.printf "Part 2: %d\n" 0
  

let () =
      time_function part1 ();
      time_function part2 ();
