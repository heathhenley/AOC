module Day03_impl = struct

  let split_to_ints s =
    String.to_seq s |> List.of_seq |> List.map ( fun c -> int_of_char c - int_of_char '0')

  let print_numbers numbers =
    Array.iteri (
      fun i n -> Printf.printf "%d: %s\n" i (String.concat " " (List.map string_of_int n))
    ) numbers

  let find_best_combo row n =
    (* need to take n numbers from the row, in order, and concat them
      to form the largest number possible - too big to brute force, so we need to pick smarter
    *)
    let rec aux acc i =
      let nd = String.length acc in
      if nd = n then
        int_of_string acc
      else if i >= List.length row then
        0
      else
        (* how many digits are left to take? *)
        let digits_left = n - nd in
        (* take the largest digit [i, length - digits_left] *)
        let start_idx = i in
        let end_idx = List.length row - digits_left in
        let max_idx, max_digit =
          row
          |> List.mapi (fun idx digit -> (idx, digit))
          |> List.fold_left
            (fun best (idx, digit) ->
              match best with
              | None ->
                  if idx >= start_idx && idx <= end_idx then
                    Some (idx, digit)
                  else
                    None
              | Some (best_idx, best_digit) ->
                  if idx >= start_idx && idx <= end_idx && digit > best_digit then
                    Some (idx, digit)
                  else
                    Some (best_idx, best_digit)
            )
            None
          |> Option.get
        in
        (* it's backwards so switch *)
        let new_acc = acc ^ (string_of_int max_digit) in
        aux new_acc (max_idx + 1)
    in
    aux "" 0

  let part1 filename =
    let file_contents = Utils.Input.read_file_to_string filename in
    let lines = Utils.Input.split_on_newline file_contents in
    let numbers = List.map split_to_ints lines in
    let res = List.fold_left (
      fun acc row ->
        let combos = Utils.Iter.combinations row 2 in
        let max_combo = List.fold_left (
          fun acc combo ->
            let x = List.nth combo 0 in
            let y = List.nth combo 1 in
            max acc (int_of_string (string_of_int x ^ string_of_int y))
        ) 0 combos in
        acc + max_combo
      ) 0 numbers in
    Printf.printf "Part 1: %d\n" res

  let part2 filename =
    let file_contents = Utils.Input.read_file_to_string filename in
    let lines = Utils.Input.split_on_newline file_contents in
    let numbers = List.map split_to_ints lines in
    let res = List.fold_left (
      fun acc row -> (acc + find_best_combo row 12)
    ) 0 numbers in
    Printf.printf "Part 2: %d\n" res

end

module Day03 : Solution.Day = Day03_impl
include Day03_impl

let () = Days.register "3" (module Day03)
