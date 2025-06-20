(*
# Example input
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2

# First things first - parse
- value setting
- bot rules

Parse the input into a list of bot rules and value settings.

Then make a map of bot_id: bot

Process the rules and settings recursively
*)

type bot_or_output = Bot of int | Output of int

type bot_rule = {
  low_to: bot_or_output;
  high_to: bot_or_output;
}

type instruction =
  | ValueSetting of {value: int; bot_id: int}
  | BotRule of {bot_id: int; rule: bot_rule option}

let bot_or_output_of_string str id =
  match str with
  | "bot" -> Bot id
  | "output" -> Output id
  | _ -> failwith "Invalid bot or output type"

type state = {
  bots: (int, int list) Hashtbl.t;
  outputs: (int, int list) Hashtbl.t;
}

let bot_rule_of_string low_to high_to =
  Some { low_to; high_to }

let parsers = [
  Utils.Input.parse "value %d goes to bot %d" (fun value bot_id -> ValueSetting { value; bot_id });
  Utils.Input.parse "bot %d gives low to %s %d and high to %s %d" (
    fun bot_id low_to_type low_to_id high_to_type high_to_id ->
      let low_to = bot_or_output_of_string low_to_type low_to_id in
      let high_to = bot_or_output_of_string high_to_type high_to_id in
      let rule = bot_rule_of_string low_to high_to in
      BotRule { bot_id; rule }
  );
]

let string_of_bot_or_output bot_or_output =
  match bot_or_output with
  | Bot id -> Printf.sprintf "bot %d" id
  | Output id -> Printf.sprintf "output %d" id

let string_of_rule rule =
  match rule with
  | Some { low_to; high_to } ->
    Printf.sprintf "low to %s, high to %s" (string_of_bot_or_output low_to) (string_of_bot_or_output high_to)
  | None -> "no rule"

 
(* initialize a list with bots the we know will exist, there will be more that
   we don't know about yet - they get values - we'll add them as they come up *)
let init_bots instructions =
  let bot_ids = List.map (
    fun inst ->
      match inst with
      | BotRule { bot_id; _ } -> bot_id
      | ValueSetting { bot_id; _ } -> bot_id
  ) instructions in
  List.map (fun bot_id -> (bot_id, [])) bot_ids

let find_rule find_id rules =
  List.find_map (
    fun rule ->
      match rule with
      | BotRule { bot_id; rule } when bot_id = find_id -> rule
      | _ -> None
  ) rules

let string_of_instruction inst =
  match inst with
  | ValueSetting {value; bot_id} -> Printf.sprintf "Value %d goes to bot %d" value bot_id
  | BotRule {bot_id; rule} ->
    match rule with
    | Some { low_to; high_to } ->
      Printf.sprintf "Bot %d gives low to %s and high to %s" bot_id (string_of_bot_or_output low_to) (string_of_bot_or_output high_to)
    | None -> Printf.sprintf "Bot %d has no rule" bot_id

let rec process_bots bots rules values target_low target_high =
  match values with
  | [] -> None
  | v::rest ->
    (*Printf.printf "Processing value %s\n" (string_of_instruction v);*)
    match v with
    | ValueSetting {bot_id; value} ->
      if List.mem_assoc bot_id bots then
        let current_values = List.assoc bot_id bots in
        (*Printf.printf "Bot %d already exists with values %s\n" bot_id (String.concat ", " (List.map string_of_int current_values));*)
        let new_values = List.sort compare (value :: current_values) in
        if List.length new_values = 2 then
          if List.mem target_low new_values && List.mem target_high new_values then
            Some bot_id
          else
            (* apply rule and continue *)
            let rule = find_rule bot_id rules in
            let low = List.nth new_values 0 in
            let high = List.nth new_values 1 in
            match rule with
            | Some { low_to; high_to } ->
              let new_instructions = 
                List.filter_map (fun (v, dst) ->
                  match dst with
                  | Bot id -> Some (ValueSetting { value = v; bot_id = id })
                  | Output _ -> None
                ) [low, low_to; high, high_to] in
              (* take this bot out of the list *)
              let new_bots = List.remove_assoc bot_id bots in
              process_bots new_bots rules (new_instructions @ rest) target_low target_high
            | _ -> process_bots bots rules rest target_low target_high
        else
          let new_bots = List.remove_assoc bot_id bots in
          let new_bot = (bot_id, new_values) in
          process_bots (new_bot :: new_bots) rules rest target_low target_high
      else
        let new_bot = (bot_id, [value]) in
        process_bots (new_bot :: bots) rules rest target_low target_high
    | _ -> process_bots bots rules rest target_low target_high


let part1_impl filename low high =
    let instructions =
      filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map (Utils.Input.try_parse parsers)
  in
  let rules = List.filter (
    fun inst ->
      match inst with
      | BotRule _ -> true
      | _ -> false
    ) instructions in
  let values = List.filter (
    fun inst ->
      match inst with
      | ValueSetting _ -> true
      | _ -> false
  ) instructions in
  let initial_bots = init_bots instructions in
  (* Process bots recursively
    - assign each value
    - if we have two make new bots list with right values 
    - add ValueSetting instructions and recurse
    *)
  let bot_id  = process_bots initial_bots rules values low high in
  match bot_id with
  | Some bot_id -> Printf.printf "Part 1: Bot %d is the one we're looking for\n" bot_id
  | None -> Printf.printf "No bot found\n"

 let part1 filename =
  part1_impl filename 17 61     

let part2 _ = print_endline "Not implemented"