let parse fmt map line = try Some (Scanf.sscanf line fmt map) with _ -> None

let rec try_parse parsers line =
  match parsers with
  | [] ->
    failwith (Printf.sprintf "could not parse line: %s" line)
  | parser:: parsers ->
    match parser line with
    | Some x -> x
    | None -> try_parse parsers line

type register = {
  label: string;
  value: int;
}

type instruction = {
  op: int;
  arg: int;
}

(* each line of input can be register or list of instructions *)
type input_line =
  | Register of register
  | Instruction of instruction list

type program = {
  registers: register list;
  instructions: instruction list;
}
let str_of_char c = String.make 1 c

let inst_str_to_int_list str =
  let int_lst = str
  |> String.split_on_char ','
  |> List.map int_of_string in
  int_lst

let ints_to_instruction_list lst =
  (* each pair of ints defines a unique instruction and arg *)
  let rec loop list acc =
    match list with
    | [] -> acc
    | x::y::xs -> loop xs ({op = x; arg = y}::acc)
    | _ -> failwith "Invalid instruction list" in
  let res = loop lst [] in
  List.rev res

let parsers = [
  parse "Register %c: %d" (
    fun label value ->
      let label = str_of_char label in
      Register {label; value}
  );
  parse "Program: %s" (fun str_program ->
    let instructions = str_program
    |> inst_str_to_int_list
    |> ints_to_instruction_list in
    Instruction instructions
  )
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

let parsed_to_program parsed =
  let rec loop parsed acc_registers acc_instructions =
    match parsed with
    | [] -> {registers = acc_registers; instructions = acc_instructions}
    | Register {label; value}::xs -> loop xs ({label; value}::acc_registers) acc_instructions
    | Instruction instructions::xs -> loop xs acc_registers (acc_instructions @ instructions) in
  loop parsed [] []

let combo_op registers arg =
  match arg with
  | _ when arg < 4 -> arg
  | 4 ->
    let register = List.find (fun r -> r.label = "A") registers in
    register.value
  | 5 ->
    let register = List.find (fun r -> r.label = "B") registers in
    register.value
  | 6 ->
    let register = List.find (fun r -> r.label = "C") registers in
    register.value
  | _ -> failwith "Invalid arg"

let pow a b =
  let rec loop a b acc =
    match a, b with
    | 0, 0 -> acc
    | 0, _ -> 0
    | _, 0 -> acc
    | _ -> loop a (b - 1) (acc * a) in
  loop a b 1

let run program =
  let rec run' registers ptr out =
    if ptr >= List.length program.instructions then
      out
    else
      let instruction = List.nth program.instructions ptr in
      match instruction.op with
      | 0 -> (* adv *)
        let operand = combo_op registers instruction.arg in
        let new_registers = List.map (
          fun r ->
            match r.label with
            | "A" -> {r with value = r.value / (pow 2 operand)}
            | _ -> r
        ) registers in
        run' new_registers (ptr + 1) out
      | 1 -> (* bxl - xor *)
        let new_registers = List.map (
          fun r ->
            match r.label with
            | "B" -> {r with value = r.value lxor instruction.arg}
            | _ -> r
        ) registers in
        run' new_registers (ptr + 1) out
      | 2 -> (* bst *)
        let operand = combo_op registers instruction.arg in
        let new_registers = List.map (
          fun r ->
            match r.label with
            | "B" -> {r with value = operand mod 8}
            | _ -> r
        ) registers in
        run' new_registers (ptr + 1) out
      | 3 -> (* jnz *)
        let rega = List.find (fun r -> r.label = "A") registers in
        if rega.value <> 0 then
          run' registers (instruction.arg / 2) out
        else
          run' registers (ptr + 1) out
      | 4 -> (* bxc *)
        let regc = List.find (fun r -> r.label = "C") registers in
        let new_registers = List.map (
          fun r ->
            match r.label with
            | "B" -> {r with value = r.value lxor regc.value}
            | _ -> r
        ) registers in
        run' new_registers (ptr + 1) out
      | 5 -> (* out *)
        let operand = combo_op registers instruction.arg in
        run' registers (ptr + 1) (out @ [operand mod 8])
      | 6 -> (* bdv *)
        let rega = List.find (fun r -> r.label = "A") registers in
        let operand = combo_op registers instruction.arg in
        let new_registers = List.map (
          fun r ->
            match r.label with
            | "B" -> {r with value = rega.value / (pow 2 operand)}
            | _ -> r
        ) registers in
        run' new_registers (ptr + 1) out
      | 7 -> (* cdv *)
        let rega = List.find (fun r -> r.label = "A") registers in
        let operand = combo_op registers instruction.arg in
        let new_registers = List.map (
          fun r ->
            match r.label with
            | "C" -> {r with value = rega.value / (pow 2 operand)}
            | _ -> r
        ) registers in
        run' new_registers (ptr + 1) out
      | _ -> (* invalid instruction *)
        failwith "Invalid instruction" in
  run' program.registers 0 []

let octal_to_decimal digits =
  let rec loop digits acc =
    match digits with
    | [] -> acc
    | x::xs -> loop xs (acc * 8 + x)  in
  loop digits 0

let solve program =

  let int_program = program.instructions
    |> List.map (fun i -> [i.op; i.arg] ) 
    |> List.flatten
  in

  let rec solve' idx digits =
    let n = List.length digits in
    if idx >= List.length int_program then
      Some digits
    else
      let try_digit digit =
        let new_digits = 
          List.mapi (fun i x -> if i = idx then digit else x) digits 
        in
        let decimal = octal_to_decimal new_digits in

        let new_registers = 
          List.map (fun r -> 
            match r.label with
            | "A" -> { r with value = decimal }
            | _ -> { r with value = 0 }
          ) program.registers 
        in
        let new_program = { program with registers = new_registers } in
        let out = run new_program in
        if List.length out <> n then
          None
        else 
          let out_val = List.nth out (n - idx - 1) in
          let program_val = List.nth int_program (n - idx - 1) in
          if out_val = program_val then
            solve' (idx + 1) new_digits
        else
          None
      in
      let rec try_all_digits digits =
        match digits with
        | [] -> None
        | d :: ds -> (
            match try_digit d with
            | Some solution -> Some solution
            | None -> try_all_digits ds
          )
      in
      try_all_digits [0; 1; 2; 3; 4; 5; 6; 7]
  in
  solve' 0 (List.init (List.length int_program) (
    fun _ -> 0
  ))



let part1 filename =
  let out = filename
  |> read_file_to_string
  |> split_on_newline
  |> List.map (fun x -> try_parse parsers x)
  |> parsed_to_program
  |> run
  |> List.fold_left (fun acc x -> acc ^ (string_of_int x) ^ ",") "" in
  Printf.printf "Part 1: %s\n" out


let part2 filename =
  let digits = filename
  |> read_file_to_string
  |> split_on_newline
  |> List.map (fun x -> try_parse parsers x)
  |> parsed_to_program
  |> solve in
  match digits with
  | Some digits ->
    octal_to_decimal digits
    |> Printf.printf "Part 2: %d\n"
  | None ->
    Printf.printf "Part 2: No solution found\n"
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
