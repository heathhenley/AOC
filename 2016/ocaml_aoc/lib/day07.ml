let is_abba str =
  (* some checks *)
  if String.length str < 4 then false
  else str.[0] = str.[3] && str.[1] = str.[2] && str.[0] <> str.[1]

let is_line_abba line =
  (* start at zero index, increment and check chunks of 4*)
  let rec window start_idx inside_bracket has_abba_out =
    if start_idx + 3 >= String.length line then has_abba_out
    else
      match line.[start_idx] with
      (* we're starting a bracket section *)
      | '[' -> window (start_idx + 1) true has_abba_out
      (* we're closing a bracket section *)
      | ']' -> window (start_idx + 1) false has_abba_out
      (* any other char *)
      | _ ->
          let is_abba_str = is_abba (String.sub line start_idx 4) in
          if is_abba_str && inside_bracket then
            (* we can't support TLS if we have an abba in brackets *)
            false
          else
            (* need to keep going *)
            window (start_idx + 1) inside_bracket (has_abba_out || is_abba_str)
  in
  window 0 false false

let is_aba str =
  if String.length str < 3 then false
  else if str.[0] = str.[1] then false
  else str.[0] = str.[2] && str.[0] <> str.[1]

let bab_of_aba str =
  [ str.[1]; str.[0]; str.[1] ] |> List.to_seq |> String.of_seq

type substr_state =
  | In
  | Out
  | Both

let new_state state inside_bracket =
  match state with
  | Some In -> if not inside_bracket then Both else In
  | Some Out -> if inside_bracket then Both else Out
  | Some Both -> Both
  | None -> if inside_bracket then In else Out

let put_state hash_tbl aba state inside_bracket =
  let new_state = new_state state inside_bracket in
  Hashtbl.add hash_tbl aba new_state

let is_line_ssl line =
  let hash_tbl = Hashtbl.create 100 in
  let rec window start_idx inside_bracket =
    if start_idx + 2 >= String.length line then false
    else
      match line.[start_idx] with
      | '[' -> window (start_idx + 1) true
      | ']' -> window (start_idx + 1) false
      | _ ->
          let aba = String.sub line start_idx 3 in
          if is_aba aba then (
            (* add the aba to the hash table - update to be In, Out, or Both *)
            let aba_state = Hashtbl.find_opt hash_tbl aba in
            put_state hash_tbl aba aba_state inside_bracket;
            (* see if we have bab already and if it's in the right place *)
            let bab = bab_of_aba aba in
            let bab_state = Hashtbl.find_opt hash_tbl bab in
            match bab_state with
            | Some Both -> true
            | Some Out ->
                if inside_bracket then true
                else window (start_idx + 1) inside_bracket
            | Some In ->
                if not inside_bracket then true
                else window (start_idx + 1) inside_bracket
            | None -> window (start_idx + 1) inside_bracket)
          else window (start_idx + 1) inside_bracket
  in
  window 0 false

let part1 filename =
  (*
  We need to process each line and check if it supports 'TLS'
    - check if the line contains an abba sequence (outside of brackets)
    - check if the line contains an abba sequence (inside of brackets)
    - if it has an abba sequence in brackets, it does not support TLS
    - if it has an abba sequence outside of brackets, and not in brackets, it supports TLS
    - abba sequence is a pair of character followed by the reverse of that pair
      and they need to be two different characters (so aaaa is not valid)

  Thinking:
  - process chunks of four chars at a time in a string
  - check if a given sequence is abba
  - track if we are in a bracket or not
  - early return if we have an abba in bracket
  *)
  let count_tls =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.fold_left (fun acc l -> if is_line_abba l then acc + 1 else acc) 0
  in
  Printf.printf "Part 1: %d\n" count_tls

let part2 filename =
  (*
  We need to process each line and check if it supports 'SSL'
    - to support 'SSL' it needs an 'aba' sequence outside of brackets and
      a 'bab' sequence inside of brackets
  
  Thinking:
  - this time, instead of deciding on the fly - and to avoid a double loop
  - use one pass to find all the aba/bab sequences and save if they are in or
    out of brackets
  - track it in a hash table, we can still do it in one pass - just need to
    track if we've seen the substring in brackets, out of brackets, or both
  *)
  let count_ssl =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.fold_left (fun acc l -> if is_line_ssl l then acc + 1 else acc) 0
  in
  Printf.printf "Part 2: %d\n" count_ssl
