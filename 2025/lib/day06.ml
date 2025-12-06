module Day06_impl = struct
  let split lines =
    match List.rev lines with
    | ops :: nums -> (ops, nums)
    | _ -> failwith "Invalid input"

  let parse_op_line line =
    String.split_on_char ' ' line
    |> List.map (fun s -> String.trim s)
    |> List.filter (fun s -> s <> "")

  let parse_num_line line =
    String.split_on_char ' ' line
    |> List.map (fun s -> String.trim s)
    |> List.filter (fun s -> s <> "")
    |> List.map int_of_string

  let to_string chars =
    List.map (fun c -> String.make 1 c) chars |> List.rev |> String.concat ""

  let rec read_single_problem col nums acc =
    if col >= String.length (List.hd nums) then (acc, col)
    else
      let chars = List.map (fun row -> String.get row col) nums in
      let num_str = to_string (List.filter (fun c -> c <> ' ') chars) in
      match num_str with
      | "" -> (acc, col)
      | _ ->
          let n = int_of_string num_str in
          read_single_problem (col + 1) nums (n :: acc)

  let part1 filename =
    let op_line, num_lines =
      Utils.Input.read_file_to_string filename
      |> Utils.Input.split_on_newline
      |> List.filter (fun line -> line <> "")
      |> split
    in
    let nums = List.map parse_num_line num_lines in
    op_line
    |> parse_op_line
    |> List.mapi (fun i op ->
        List.fold_left
          (fun acc row ->
            let f = if op = "+" then ( + ) else ( * ) in
            f acc (List.nth row i))
          (if op = "+" then 0 else 1)
          nums)
    |> List.fold_left ( + ) 0
    |> Printf.printf "Part 1: %d\n"

  let part2 filename =
    let op_line, num_lines =
      Utils.Input.read_file_to_string filename
      |> String.split_on_char '\n'
      |> split
    in
    let ops = parse_op_line (String.trim op_line) in
    let max_len = List.hd num_lines |> String.length in
    let rec read_all_problems col nums acc =
      if col >= max_len then acc
      else
        let nums, new_col = read_single_problem col nums [] in
        read_all_problems (new_col + 1) num_lines (nums :: acc)
    in
    let problems = read_all_problems 0 num_lines [] in
    ops
    |> List.rev
    |> List.mapi (fun i op ->
        let f = if op = "+" then ( + ) else ( * ) in
        List.fold_left f (if op = "+" then 0 else 1) (List.nth problems i))
    |> List.fold_left ( + ) 0
    |> Printf.printf "Part 2: %d\n"
end

module Day06 : Solution.Day = Day06_impl
include Day06_impl

let () = Days.register "6" (module Day06)
