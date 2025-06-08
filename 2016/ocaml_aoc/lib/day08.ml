(*
- Parse input - probably scanf parse technique?
- Make a grid of 'pixels' - they are all off
- Perform rotates on rows and cols
*)

type instruction =
  | Rect of {
      rows : int;
      cols : int;
    }
  | RotateCol of {
      col : int;
      by : int;
    }
  | RotateRow of {
      row : int;
      by : int;
    }

let parsers =
  [
    Utils.Input.parse "%s %dx%d" (fun _ cols rows -> Rect { rows; cols });
    Utils.Input.parse "rotate row y=%d by %d" (fun n by ->
        RotateRow { row = n; by });
    Utils.Input.parse "rotate column x=%d by %d" (fun n by ->
        RotateCol { col = n; by });
  ]

let make_grid rows cols = Array.make_matrix rows cols false

let print_grid grid =
  Array.iter
    (fun row ->
      Array.iter (fun pixel -> print_string (if pixel then "#" else ".")) row;
      print_endline "")
    grid

let apply_rect grid rows cols =
  for r = 0 to rows - 1 do
    for c = 0 to cols - 1 do
      grid.(r).(c) <- true
    done
  done

(* this could be in place...*)
let rotate_vector v n =
  let len = Array.length v in
  let res = Array.make len false in
  for i = 0 to len - 1 do
    res.((i + n) mod len) <- v.(i)
  done;
  res

let get_column_vector grid col =
  let rows = Array.length grid in
  Array.init rows (fun row -> grid.(row).(col))

let put_column_vector grid col vec =
  let rows = Array.length grid in
  for row = 0 to rows - 1 do
    grid.(row).(col) <- vec.(row)
  done

let apply_rotate_col grid col by =
  let col_vec = get_column_vector grid col in
  let rot_col = rotate_vector col_vec by in
  put_column_vector grid col rot_col

let apply_rotate_row grid row by = grid.(row) <- rotate_vector grid.(row) by

let string_of_instruction instruction =
  match instruction with
  | Rect { rows; cols } -> Printf.sprintf "Rect %d %d" rows cols
  | RotateCol { col; by } -> Printf.sprintf "RotateCol %d %d" col by
  | RotateRow { row; by } -> Printf.sprintf "RotateRow %d %d" row by

let count_pixels grid =
  Array.fold_left
    (fun acc row ->
      acc + Array.fold_left (fun a v -> if v then a + 1 else a) 0 row)
    0 grid

(* using partn_internal to keep rows and cols configurable - easier to test *)
let part1_internal filename ~rows ~cols =
  print_endline "Part 1";
  Printf.printf "Rows: %d, Cols: %d\n" rows cols;
  let grid = make_grid rows cols in

  let _ =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map (Utils.Input.try_parse parsers)
    |> List.iteri
         (fun
           (* Maps over the instructions and applies them to the grid*)
             _
           instr
         ->
           (*Printf.printf "Instruction %d, %s\n" i (string_of_instruction instr); *)
           match instr with
           | Rect { rows; cols } -> apply_rect grid rows cols
           | RotateCol { col; by } -> apply_rotate_col grid col by
           | RotateRow { row; by } -> apply_rotate_row grid row by)
  in
  Printf.printf "Part 1: %d\n" (count_pixels grid);
  Printf.printf "Part 2 (read final grid):\n";
  print_grid grid;
  ()

let part2_internal filename ~rows ~cols = part1_internal filename ~rows ~cols

(* to match the interface of a Day module *)
let part1 filename = part1_internal filename ~rows:6 ~cols:50
let part2 filename = part2_internal filename ~rows:6 ~cols:50
