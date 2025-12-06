module Day06_impl = struct
  let split lines =
    match List.rev lines with
    | ops :: nums -> ops, nums
    | _ -> failwith "Invalid input"
  
  let parse_op_line line =
    String.split_on_char ' ' line
    |> List.map (fun s -> String.trim s)
    |> List.filter (fun s -> s <> "")

  let parse_num_line line =
    String.split_on_char ' ' line
    |> List.map (fun s -> String.trim s)
    |> List.filter (fun s -> s <> "")
    |> List.map (fun x -> Printf.printf "x: %s\n" x; x)
    |> List.map int_of_string

  let to_string chars =
    List.map (fun c -> String.make 1 c) chars
    |> List.rev
    |> String.concat ""
  
  let rec read_single_problem col nums acc =
    (* read all the chars at position col from all rows and concat them *)
    let chars = List.map (fun row -> String.get row col) nums in
    (* filter out the ' ' chars *)
    let num_str = to_string (List.filter (fun c -> c <> ' ') chars) in
    match num_str with
    | "" -> (acc, col) (* we got all spaces we this is the full problem *)
    | _  -> let n = int_of_string num_str in
            read_single_problem (col + 1) nums (n :: acc)

  let part1 filename =
    let op_line, num_lines = Utils.Input.read_file_to_string filename
      |> Utils.Input.split_on_newline
      |> List.filter (fun line -> line <> "")
      |> split
    in
    let ops = parse_op_line op_line in
    let nums = List.map parse_num_line num_lines in
    Printf.printf "rows: %d\n" (List.length nums);
    List.iteri (fun i row -> Printf.printf "row %d has %d columns\n" i (List.length row)) nums;
    List.iteri (
      fun i op -> Printf.printf "op %d: %s\n" i op
    ) ops;
    List.iteri (
      fun i row -> 
        List.iteri (
          fun j num -> Printf.printf "i: %d, j: %d, num %d:\n" i j num
        ) row
      ) nums;
    let col_results = List.mapi (fun i op ->
      (* fold over col i nums using op on all rows *)
      List.fold_left (
        fun acc row ->
          let f = if op = "+" then (+) else ( * ) in
          f acc (List.nth row i)
        ) (if op = "+" then 0 else 1) nums
    ) ops
    in
    let result = List.fold_left (+) 0 col_results in
    Printf.printf "Part 1: %d\n" result

  let part2 filename =
    let op_line, num_lines = Utils.Input.read_file_to_string filename
      |> String.split_on_char '\n'
      |> split
    in
    List.iteri (
      fun i line -> Printf.printf "line %d: %s\n" i line
    ) num_lines;
    let ops = parse_op_line (String.trim op_line) in
    (* attempt at a soln
      - read down each colmn of chars, push the non ' ' characters to string, 
       these are the numbers for that col - whenever we have a full column of
       empty ' ' chars, that means we have completed the "problem"
       eg:
       123
       1
        7
      will give, reading down the first column 1 1 ' ', so we push 11 to the 
      list, then 2 ' ' 7, so we push 27, 3 ' ' ' ', so we push 3. When we see
      " " in all rows, we now we have completed the col and start again
    *)

    let rec read_single_problem col nums acc =
      (* read all the chars at position col from all rows and concat them *)
      Printf.printf "reading problem at col %d\n" col;
      if col >= String.length (List.hd nums) then (acc, col) else
      let chars = List.map (
        fun row -> Printf.printf "row: %s len: %d\n" row (String.length row); String.get row col) nums in
      (* filter out the ' ' chars *)
      let num_str = to_string (List.filter (fun c -> c <> ' ') chars) in
      match num_str with
      | "" -> (acc, col) (* we got all spaces we this is the full problem *)
      | _  -> let n = int_of_string num_str in
              read_single_problem (col + 1) nums (n :: acc)
    in
    (*let nums, _ = read_single_problem 0 num_lines [] in
    List.iteri (
      fun i num -> Printf.printf "num %d: %d\n" i num
    ) nums;*)
    (* if we do this for each "problem" then we have part 1 back, we just have
      put it in the right format *)
    let max_len = List.hd num_lines |> String.length in
    Printf.printf "max_len: %d\n" max_len;
    let rec read_all_problems col nums acc =
      (* read each problem and add to a list *)
      (* do we need ot make sure they're the same length? *)
      Printf.printf "reading all problems at col %d\n" col;
      if col >= max_len then acc
      else
        let nums, new_col = read_single_problem col nums [] in
        Printf.printf "read problem at col %d, new_col: %d\n" col new_col;
        read_all_problems (new_col + 1) num_lines (nums :: acc)
    in
    let problems = read_all_problems 0 num_lines [] in
    List.iteri (
      fun i nums -> Printf.printf "problem %d: %s\n" i (String.concat " " (List.map string_of_int nums))
    ) problems;
    let prob_results = List.mapi (fun i op ->
      let f = if op = "+" then (+) else ( * ) in
      List.fold_left f (if op = "+" then 0 else 1) (List.nth problems i)
    ) (List.rev ops) in
    let result = List.fold_left (+) 0 prob_results in
    Printf.printf "Part 2: %d\n" result
end

module Day06 : Solution.Day = Day06_impl
include Day06_impl

let () = Days.register "6" (module Day06)
