let read_file_to_string filename =
  let ic = open_in filename in
  let n = in_channel_length ic in
  let s = really_input_string ic n in
  close_in ic;
  s

let split_on_newline str =
  let split =
    str |> String.split_on_char '\n' |> List.map String.trim
    |> List.filter (fun x -> String.length x > 0)
  in
  split
