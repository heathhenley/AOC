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


let parse_line line =
  line
  |> String.split_on_char ' '
  |> List.map int_of_string


let has_even_digits n =
  let sn = string_of_int n in
  String.length sn mod 2 = 0


let split_number n =
  let sn = string_of_int n in
  let len = String.length sn in
  let mid = len / 2 in
  let left = String.sub sn 0 mid in
  let right = String.sub sn mid (len - mid) in
  (int_of_string left, int_of_string right)


let blink stone blinks_left =
  let ht = Hashtbl.create 100 in
  let rec blink stone blinks_left =
    if blinks_left = 0 then
      1
    else
      match Hashtbl.find_opt ht (blinks_left, stone) with
      | Some x -> x
      | None when stone = 0 ->
        let result = blink 1 (blinks_left - 1) in
        Hashtbl.add ht (blinks_left, stone) result;
        result
      | None when has_even_digits stone ->
        let (left, right) = split_number stone in
        let rl = blink left (blinks_left - 1) in
        let rr = blink right (blinks_left - 1) in
        let result = rr + rl in
        Hashtbl.add ht (blinks_left, stone) result;
        result
      | _ ->
        let result = blink (stone * 2024) (blinks_left - 1) in
        Hashtbl.add ht (blinks_left, stone) result;
        result
  in blink stone blinks_left


let part1 filename =
  let final_stones = filename
  |> read_file_to_string
  |> split_on_newline
  |> List.hd
  |> parse_line
  |> List.fold_left (fun acc x -> acc + blink x 25) 0 in
  Printf.printf "Part 1: %d\n" final_stones 


let part2 filename =
  let final_stones = filename
  |> read_file_to_string
  |> split_on_newline
  |> List.hd
  |> parse_line
  |> List.fold_left (fun acc x -> acc + blink x 75) 0 in
  Printf.printf "Part 2: %d\n" final_stones
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
