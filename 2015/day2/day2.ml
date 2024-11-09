(* Day 2 I was told there would be no math *)


let read_file_to_string filename =
  let ic = open_in filename in
  let n = in_channel_length ic in
  let s = really_input_string ic n in
  close_in ic;
  s


let split_on_newline str =
  let split = String.split_on_char '\n' str in
  split


let box_dims_to_ints dims =
  let dims = String.split_on_char 'x' dims in
  match dims with
  | [l; w; h] -> (int_of_string (String.trim l),
                  int_of_string (String.trim w),
                  int_of_string (String.trim h))
  | _ -> failwith "Invalid line"


let get_box_area l w h =
  (* A special surface area to account for waste *)
  let lw = l * w in
  let wh = w * h in
  let hl = h * l in
  2 * (lw + wh + hl) + min (min lw wh) hl


let rec get_total_area lines total_area =
  match lines with
  | [] -> total_area
  | line :: rest ->
    let (l, w, h) = box_dims_to_ints line in
    let area = get_box_area l w h in
    get_total_area rest (total_area + area)


let get_box_ribbon l w h =
  (* the amount of ribbon they need to wrap the present *)
  2 * (min (l + w) (min (w + h) (h + l))) + l * w * h


let rec get_total_ribbon lines total =
  match lines with
  | [] -> total
  | line :: rest ->
    let (l, w, h) = box_dims_to_ints line in
    let ribbon = get_box_ribbon l w h in
    get_total_ribbon rest (total + ribbon)


let time_function f arg =
  let start_time = Sys.time () in
  let result = f arg in
  let end_time = Sys.time () in
  let elapsed_time = end_time -. start_time in
  Printf.printf "Elapsed time: %.6f seconds\n" elapsed_time;
  result


let part1 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let total_area = get_total_area lines 0 in
  Printf.printf "Part 1: %d\n" total_area


let part2 filename =
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let total_ribbon = get_total_ribbon lines 0 in
  Printf.printf "Part 2: %d\n" total_ribbon
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)