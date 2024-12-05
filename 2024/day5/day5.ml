
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

let parse_input lines =
  let orders =  lines
    |> List.filter (fun x -> String.contains x '|')
    |> List.map (fun x -> String.split_on_char '|' x)
    |> List.map (fun x -> List.map int_of_string x)
  in
  let updates = lines
    |> List.filter (fun x -> String.contains x ',')
    |> List.map (fun x -> String.split_on_char ',' x)
    |> List.map (fun x -> List.map String.trim x)
    |> List.map (fun x -> List.map int_of_string x)
  in
  (orders, updates)

let is_good update orders =
  List.for_all (
    fun order ->
      (* if order(1) and order(2) are in update, make sure 1 is before 2 *)
      if List.mem (List.hd order) update && List.mem (List.nth order 1) update then
        let index1 = List.find_index (fun x -> x = List.hd order) update in
        let index2 = List.find_index (fun x -> x = List.nth order 1) update in
        index1 < index2
      else
        true
  ) orders


let part1 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let orders, updates = parse_input lines in
  let good_updates = List.filter (fun x -> is_good x orders) updates in
  let sum_middle = List.fold_left (
    fun acc x ->
      acc + List.nth x (List.length x / 2)
  ) 0 good_updates in
  Printf.printf "Part 1: %d\n" sum_middle

let orders_to_map orders =
  let ht = Hashtbl.create (List.length orders) in
  List.iter (
    fun order ->
      match Hashtbl.find_opt ht (List.hd order) with
      | None -> Hashtbl.add ht (List.hd order) [(List.nth order 1)]
      | Some x -> Hashtbl.replace ht (List.hd order) ((List.nth order 1)::x)
  ) orders;
  ht

let part2 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let orders, updates = parse_input lines in
  let bad_updates = List.filter (fun x -> not (is_good x orders)) updates in
  let orders_map = orders_to_map orders in
  let fixed_bad_updates = List.map (
    fun x ->
      List.sort (fun a b ->
        match Hashtbl.find_opt orders_map a with
        | None -> 0
        | Some lst ->
          if List.exists (fun y -> y = b) lst then 1
          else if
            List.exists (fun y -> y = a) lst then -1
          else 0
      ) x
  ) bad_updates in
  let sum_middle = List.fold_left (
    fun acc x ->
      acc + List.nth x (List.length x / 2)
  ) 0 fixed_bad_updates in
  Printf.printf "Part 2: %d\n" sum_middle
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
