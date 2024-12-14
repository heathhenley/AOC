(* Learning how to use scanf for parsing fancier inputs - based on
  https://gist.github.com/p1xelHer0/98633ed78e74485c6827d08493884a8d

*)
let parse fmt map line = try Some (Scanf.sscanf line fmt map) with _ -> None


let rec try_parse parsers line =
  match parsers with
  | [] ->
    failwith (Printf.sprintf "could not parse line: %s" line)
  | parser:: parsers ->
    match parser line with
    | Some x -> x
    | None -> try_parse parsers line

type button = {
  dx: float;
  dy: float;
}

type prize = {
  x: float;
  y: float;
}

type input_line =
  | Button of button
  | Prize of prize

type game = {
  button_a: button;
  button_b: button;
  prize: prize;
}

(*
Input looks like:
Button A: X+94, Y+34             
Button B: X+22, Y+67
Prize: X=8400, Y=5400
...
...
*)

let parsers = [
  parse "Button %c: X+%d, Y+%d" (
    fun _ dx dy ->
      let dx = float_of_int dx in
      let dy = float_of_int dy in
      Button {dx; dy});
  parse "Prize: X=%d, Y=%d" (fun x y ->
    let x = float_of_int x in
    let y = float_of_int y in
    Prize {x; y})
]

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

let games_of_lines lines =
  (* each game is two rows of buttons and then a prize location *)
  let rec loop lines acc =
    match lines with
    | Button button_a :: Button button_b :: Prize prize :: tail ->
      let game = { button_a; button_b; prize } in
      loop tail (game :: acc)
    | [] -> List.rev acc
    | _ -> failwith "Invalid input"
  in
  loop lines []

let round x = int_of_float (x +. 0.5)

let is_integer x = abs_float (x -. float_of_int (round x)) < 0.001

let cost a b = 3 * a + b

let solve game offset =
  (* this only works because of special input, yada yada, I'm so smart, matrix
  rank, yada, determinant, blah *)
  let tx, ty = game.prize.x +. offset, game.prize.y +. offset in
  let bady = game.button_a.dy in
  let badx = game.button_a.dx in
  let bbdy = game.button_b.dy in
  let bbdx = game.button_b.dx in
  let nb = ((tx /. badx) -. (ty /. bady)) /. ((bbdx /. badx) -. (bbdy /. bady)) in
  let na = (ty -. nb *. bbdy) /. bady in
  if na < 0.0 || nb < 0.0 then
    0
  else if is_integer na && is_integer nb then
    cost (round na)  (round nb)
  else
    0

let part1 filename =
  let cost = filename
    |> read_file_to_string
    |> split_on_newline
    |> List.map (fun line -> try_parse parsers line)
    |> games_of_lines
    |> List.fold_left (fun acc game ->
      let game_cost = solve game 0.0 in
      acc + game_cost
    ) 0 in
  Printf.printf "Part 1: %d\n" cost


let part2 filename =
  let cost = filename
    |> read_file_to_string
    |> split_on_newline
    |> List.map (fun line -> try_parse parsers line)
    |> games_of_lines
    |> List.fold_left (fun acc game ->
      let game_cost = solve game 10000000000000.0 in
      acc + game_cost
    ) 0 in
  Printf.printf "Part 2: %d\n" cost
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
