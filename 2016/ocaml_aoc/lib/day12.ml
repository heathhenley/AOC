type register =
  | A
  | B
  | C
  | D

type operand =
  | Register of register
  | Int of int

type instruction =
  | Cpy of operand * register
  | Inc of register
  | Dec of register
  | Jnz of operand * int

type program_state = {
  registers : int array;
  pointer : int;
  program : instruction array;
}

let make program num_reg =
  { pointer = 0; program; registers = Array.make num_reg 0 }

let parse_reg reg =
  match reg with
  | "a" -> A
  | "b" -> B
  | "c" -> C
  | "d" -> D
  | x -> failwith ("unexpected register [" ^ x ^ "]")

let parse_operand op =
  try Int (int_of_string op) with _ -> Register (parse_reg op)

let parse_instruction instruction =
  match String.split_on_char ' ' (String.trim instruction) with
  | [ "cpy"; r; op ] -> Cpy (parse_operand r, parse_reg op)
  | [ "inc"; r ] -> Inc (parse_reg r)
  | [ "dec"; r ] -> Dec (parse_reg r)
  | [ "jnz"; r; op ] -> Jnz (parse_operand r, int_of_string op)
  | _ -> failwith "unexpected instruction"

let print = function
  | Cpy (_, _) -> Printf.printf "CPY\n"
  | Inc _ -> Printf.printf "INC\n"
  | Dec _ -> Printf.printf "DEC\n"
  | Jnz _ -> Printf.printf "JNZ\n"

let get state reg =
  match reg with
  | A -> state.registers.(0)
  | B -> state.registers.(1)
  | C -> state.registers.(2)
  | D -> state.registers.(3)

let set state reg value =
  let registers = Array.copy state.registers in
  (match reg with
  | A -> registers.(0) <- value
  | B -> registers.(1) <- value
  | C -> registers.(2) <- value
  | D -> registers.(3) <- value);
  { state with registers }

let cpy state x y =
  match x with
  | Int x ->
      let new_state = set state y x in
      { new_state with pointer = new_state.pointer + 1 }
  | Register x ->
      let v = get state x in
      let new_state = set state y v in
      { new_state with pointer = new_state.pointer + 1 }

let inc state x =
  let v = get state x in
  let new_state = set state x (v + 1) in
  { new_state with pointer = state.pointer + 1 }

let dec state x =
  let v = get state x in
  let new_state = set state x (v - 1) in
  { new_state with pointer = state.pointer + 1 }

let jnz state r x =
  let v =
    match r with
    | Register r -> get state r
    | Int i -> i
  in
  if v <> 0 then { state with pointer = state.pointer + x }
  else { state with pointer = state.pointer + 1 }

let rec run_program state =
  if state.pointer >= Array.length state.program then state
  else
    let ins = state.program.(state.pointer) in
    match ins with
    | Cpy (x, y) -> run_program (cpy state x y)
    | Inc x -> run_program (inc state x)
    | Dec x -> run_program (dec state x)
    | Jnz (r, x) -> run_program (jnz state r x)

let part1 filename =
  let program =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map parse_instruction
    |> Array.of_list
  in
  let state = make program 4 in
  let res = run_program state in
  Printf.printf "Part 1: %d\n" res.registers.(0)

let part2 filename =
  let program =
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map parse_instruction
    |> Array.of_list
  in
  let state = make program 4 in
  let res = run_program (set state C 1) in
  Printf.printf "Part 2: %d\n" res.registers.(0)
