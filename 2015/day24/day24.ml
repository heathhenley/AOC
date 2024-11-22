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

let rec combinations lst total target =
  match lst with
  | [] -> if total = target then [[]] else []
  | head :: tail ->
      if total > target then []
      else
        let without_head = combinations tail total target in
        let with_head = combinations tail (total + head) target in
        (List.map (fun x -> head :: x) with_head) @ without_head

let rec get_qe group acc =
  match group with
  | [] -> 1
  | h :: t -> get_qe t acc * h

let part1 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let packages = List.map int_of_string lines in
  let tw = List.fold_left (+) 0 packages in
  let gw = tw / 3 in
  let groups = combinations packages 0 gw in
  let min_len = List.fold_left (fun acc x -> min acc (List.length x)) max_int groups in
  let good_groups = List.filter (fun x -> List.length x = min_len) groups in
  let min_qe = List.fold_left (
    fun acc x ->
       min acc (get_qe x 1)) max_int good_groups
  in
  Printf.printf "Part 1: %d\n" min_qe


let part2 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let packages = List.map int_of_string lines in
  let tw = List.fold_left (+) 0 packages in
  let gw = tw / 4 in
  let groups = combinations packages 0 gw in
  let min_len = List.fold_left (fun acc x -> min acc (List.length x)) max_int groups in
  let good_groups = List.filter (fun x -> List.length x = min_len) groups in
  let min_qe = List.fold_left (
    fun acc x ->
       min acc (get_qe x 1)) max_int good_groups
  in
  Printf.printf "Part 2: %d\n" min_qe
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
