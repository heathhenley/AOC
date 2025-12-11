module Day10_impl = struct

  type button = int array

  type machine = {
    (* list of desired state for each indicator - 0 = off, 1 = on

    eg. [| 1; 0; 1; 0; 1 |]
    means the machine wants indicator 0 to be on, indicator 1 to be off,
    indicator 2 to be on etc
    *)
    indicator_goal : int array;
    (* buttons available to press - each button describes which indicators it
       affects by idx
       eg. [| [| 3 |]; [| 1; 2 |]; [| 0 |] |]
       means there are three buttons, the first button toggles indicator 3, the
       second button toggles indicators 1 and 2, and the third button toggles
       indicator 0.
    *)
    buttons : button array;

    (* list of joltage desired state - the goal is to have the joltage array 
       incremented by button presses to the desired state
       eg. [| 3; 5; 4; 7|]
       means it shoudl have 3 at idx 0, 5 at idx 1, etc
    *)
    joltage_goal : int array;
  }

  let joltage_goal_of_string str =
    str
    |> (fun s -> String.sub s 1 (String.length s - 2)) (* remove the {} *)
    |> String.split_on_char ','
    |> List.map int_of_string
    |> Array.of_list

  let indicator_goal_of_string str =
    str
    |> (fun s -> String.sub s 1 (String.length s - 2)) (* remove the [] *)
    |> String.to_seq
    |> Seq.map (fun c -> if c = '.' then 0 else 1)
    |> Array.of_seq

  let buttons_of_string strs =
    strs
    |> List.take_while (fun s -> String.contains s '(')
    |> List.map (fun s -> String.sub s 1 (String.length s - 2))
    |> List.map (fun s -> String.split_on_char ',' s)
    |> List.map (fun lst -> List.map int_of_string lst)
    |> Array.of_list
    |> Array.map (fun lst -> Array.of_list lst)


  let print_machine machine =
    Printf.printf "Machine:\n";
    machine.indicator_goal
    |> Array.to_seq
    |> Seq.map string_of_int
    |> Seq.iter (
      fun s -> Printf.printf "%s " s
    );
    Printf.printf "\n";
    machine.buttons
    |> Array.to_seq
    |> Seq.iter (fun btn ->
      Printf.printf "Button: ";
      Array.to_seq btn
      |> Seq.iter (
        fun i -> Printf.printf "%d " i
      );
      Printf.printf "\n"
    );
    Printf.printf "Joltage goal: ";
    machine.joltage_goal
    |> Array.to_seq
    |> Seq.map string_of_int
    |> Seq.iter (
      fun s -> Printf.printf "%s " s
    );
    Printf.printf "\n"


  let machine_of_line line =
    (* parse the line into a machine record
      eg. [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    *)
    let parts = String.split_on_char ' ' line in
    let indc = List.hd parts in
    let indicator_goal = indicator_goal_of_string indc in
    let joltage_goal = joltage_goal_of_string (List.rev parts |> List.hd) in
    let buttons = buttons_of_string (List.tl parts) in
    { indicator_goal; buttons; joltage_goal }

  let solve_machine machine =
    (* use a vanilla bfs to find the shortest path to the goal state *)
    let neighbors machine current_state =
      (* use the buttons to map the current state to the possible next states *)
      let buttons = machine.buttons in
      Array.map (
        fun btn -> (* apply the button the current state *)
            let new_state = Array.copy current_state in
            (* todo- use map*)
            Array.iter (
              fun idx -> 
                (* toggle the indicator *)
                new_state.(idx) <- if new_state.(idx) = 0 then 1 else 0
            ) btn;
            new_state
      ) buttons
      |> Array.to_list
    
    in

    (* start with all indicators off *)
    let start_state = Array.make (Array.length machine.indicator_goal) 0 in
    (* use the bfs to find the shortest path to the goal state *)
    Utils.Search.bfs
     ~neighbors:(neighbors machine)
     ~on_visit:(fun state dist ->
      if state = machine.indicator_goal then `Stop dist
      else `Continue
     )
    start_state ~size:100
    |> Option.get

  let solve_machine_part2 machine =
    (* of course it's not going to work but let's set it up anyway and see if
      if can solve the sample input *)
    let neighbors machine current_state =
      (* use the buttons to map the current state to the possible next states *)
      let buttons = machine.buttons in
      Array.map (
        fun btn -> (* apply the button the current state *)
            let new_state = Array.copy current_state in
            Array.iter (
              fun idx -> 
                (* UP THE JOLTAGE! *)
                new_state.(idx) <- new_state.(idx) + 1
            ) btn;
            new_state
      ) buttons
      |> Array.to_list
      |> List.filter (fun state ->
        Array.for_all2 (fun x y -> x <= y) state machine.joltage_goal
      )
    
    in

    (* start with all indicators off *)
    let start_state = Array.make (Array.length machine.joltage_goal) 0 in
    (* use the bfs to find the shortest path to the goal state *)
    Utils.Search.bfs
     ~neighbors:(neighbors machine)
     ~on_visit:(fun state dist ->
      if state = machine.joltage_goal then `Stop dist
      else `Continue
     )
    start_state ~size:100
    |> Option.get


  let part1 filename =
    (* for any given state - the buttons describe the possible neighbors that
       we can reach - once we've been to a given state - we don't need to go
       back to it...
    - we want to find the shortest path to the goal state
    - we can probably use a normal bfs? maybe need some sort of culling or something
      smart?
    *)
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map machine_of_line
    (*|> List.map (fun machine ->
      print_machine machine; machine
    )*)
    |> List.map solve_machine
    (*|> List.iteri (fun i ans ->
      Printf.printf "Machine %d: %d\n" i ans
    )*)
    |> List.fold_left ( + ) 0
    |> Printf.printf "Part 1: %d\n"

  let part2 filename =
    (* part 2 - similar to part 1 but now uses the joltage part of the input
      - each time the button is pressed the relevant joltage idx's are incremented
      - need to hit the goal indicated by the state in the line in the minimum
        number of button presses

      - assuming that bfs will blow up this time...
      the state would need to be the current state of the joltage array - some
      of these are probably redundant, like with day 11 2016 elevator (many
      headaches were had) - it's a little tricker with the buttons corresponding
      to differenct sets of indicies I think..
      - would djikstra make sense? the edges don't have weights so it wouldn't
        help would it? 
      
      - normal bfs solves the sample input... so maybe we need to make the
        neighbors smarter - eg stop exploring any states that bump the
        joltage beyond the goal?
      - super slow as expected...
      - maybe go backwards from the goal state and try the ones that get us
        closer to the start state first
    *)
    filename
    |> Utils.Input.read_file_to_string
    |> Utils.Input.split_on_newline
    |> List.map machine_of_line
    |> List.map solve_machine_part2
    |> List.map (fun ans ->
      Printf.printf "Answer: %d\n" ans; flush stdout; ans
    )
    |> List.fold_left ( + ) 0
    |> Printf.printf "Part 2: %d\n"


end

module Day10 : Solution.Day = Day10_impl
include Day10_impl

let () = Days.register "10" (module Day10)
