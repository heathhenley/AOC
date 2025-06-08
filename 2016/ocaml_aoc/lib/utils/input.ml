let read_file_to_string filename =
  let ic = open_in filename in
  let n = in_channel_length ic in
  let s = really_input_string ic n in
  close_in ic;
  s

let split_on_newline str =
  let split =
    str
    |> String.split_on_char '\n'
    |> List.map String.trim
    |> List.filter (fun x -> String.length x > 0)
  in
  split

(* Scanf try parse pattern stolen from: https://gist.github.com/p1xelHer0/98633ed78e74485c6827d08493884a8d *)
let parse fmt map line = try Some (Scanf.sscanf line fmt map) with _ -> None

let rec try_parse parsers line =
  match parsers with
  | [] -> failwith ("could not parse: " ^ line)
  | parse :: parsers -> (
      match parse line with
      | None -> try_parse parsers line
      | Some result -> result)
