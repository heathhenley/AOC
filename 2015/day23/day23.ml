
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

type instruction =
  Hlf of char
  | Tpl of char
  | Inc of char
  | Jmp of int
  | Jie of char * int
  | Jio of char * int

let program_of_input_lines lines =
  let instruction_of_line line =
    let parts = String.split_on_char ' ' line in
    match parts with
    | ["hlf"; reg] -> Hlf (String.get reg 0)
    | ["tpl"; reg] -> Tpl (String.get reg 0)
    | ["inc"; reg] -> Inc (String.get reg 0)
    | ["jmp"; offset] -> Jmp (int_of_string offset)
    | ["jie"; reg; offset] -> Jie (String.get reg 0, int_of_string offset)
    | ["jio"; reg; offset] -> Jio (String.get reg 0, int_of_string offset)
    | _ -> failwith "Invalid instruction"
  in
  List.map instruction_of_line lines

(*let to_string instr =
  match instr with
  | Hlf reg -> Printf.sprintf "hlf %c" reg
  | Tpl reg -> Printf.sprintf "tpl %c" reg
  | Inc reg -> Printf.sprintf "inc %c" reg
  | Jmp offset -> Printf.sprintf "jmp %d" offset
  | Jie (reg, offset) -> Printf.sprintf "jie %c, %d" reg offset
  | Jio (reg, offset) -> Printf.sprintf "jio %c, %d" reg offset*)

let rec run_program instructions idx registers =
  if idx >= List.length instructions then
    registers
  else
  match List.nth instructions idx with
  | Hlf reg ->
      let v = Hashtbl.find registers reg in
      Hashtbl.replace registers reg (v / 2);
      run_program instructions (idx + 1) registers
  | Tpl reg ->
      let v = Hashtbl.find registers reg in
      Hashtbl.replace registers reg (v * 3);
      run_program instructions (idx + 1) registers
  | Inc reg ->
      let v = Hashtbl.find registers reg in
      Hashtbl.replace registers reg (v + 1);
      run_program instructions (idx + 1) registers
  | Jmp offset ->
      run_program instructions (idx + offset) registers
  | Jie (reg, offset) ->
      let v = Hashtbl.find registers reg in
      if v mod 2 = 0 then
        run_program instructions (idx + offset) registers
      else
        run_program instructions (idx + 1) registers
  | Jio (reg, offset) ->
      let v = Hashtbl.find registers reg in
      if v = 1 then
        run_program instructions (idx + offset) registers
      else
        run_program instructions (idx + 1) registers

let part1 filename =
  let registers = Hashtbl.create 2 in
  Hashtbl.add registers 'a' 0;
  Hashtbl.add registers 'b' 0;
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let program = program_of_input_lines lines in
  let registers = run_program program 0 registers in
  Printf.printf "Part 1: %d\n" (Hashtbl.find registers 'b')


let part2 filename =
  let registers = Hashtbl.create 2 in
  Hashtbl.add registers 'a' 1;
  Hashtbl.add registers 'b' 0;
  let file_contents = read_file_to_string filename in
  let lines = split_on_newline file_contents in
  let program = program_of_input_lines lines in
  let registers = run_program program 0 registers in
  Printf.printf "Part 2: %d\n" (Hashtbl.find registers 'b')
  

(* Pass the input filename in on the command line *)
let () = match Sys.argv with
  | [|_; filename|] ->
      time_function part1 filename;
      time_function part2 filename;
  | _ -> Printf.printf "Usage: %s <filename>\n" Sys.argv.(0)
