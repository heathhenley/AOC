type disk = {
  start: int;
  disk_num: int;
  num_positions: int;
}

let int_of_disk_num s =
int_of_string @@ String.sub s 1 ((String.length s)- 1)

let disk_of_line s =
  let split = String.split_on_char ' ' s in
  {
    disk_num = int_of_disk_num @@ List.nth split 1;
    start = int_of_string @@ List.nth split 11;
    num_positions = int_of_string @@ List.nth split 3;
  }

let str_of_disk d =
  Printf.printf "Disk: %d; start: %d; num_positions: %d\n" d.disk_num d.start d.num_positions

let disk_pos_at t_start disk =
  (* where is the disk when we get there if we start at t_start? *)
  (t_start + disk.start + disk.disk_num) mod disk.num_positions


(*let solve_naive disks =
  (* naive solution - just increment by 1 and check *)
  let rec solve' t_start disks =
    if List.for_all (fun d -> disk_pos_at t_start d = 0) disks then
      t_start
    else
      solve' (t_start + 1) disks
  in
  solve' 0 disks
*)


let solve_optimized disks =
  let rec solve' t_start disks =
    if List.for_all (fun d -> disk_pos_at t_start d = 0) disks then
      t_start
    else (
      (* find the lcm of the disks that we can pass so far - once we can
         pass through a n disks, we will always be able to pass them again
         multiples of their lcm
         Eg: in the example:
         disk 1, 5 pos starts at 4 - we can pass every 5 positions
         - offsets 0, 5, 10, 15, 20, 25, ...
         disk 2 2 pos starts at 1 - we can pass every 2 positions
         - offsets 1, 3, 5, 7, 9, 11, 13, 15
         Their LCM is 10 - so we can pass them together every 10 positions...
         and so on for each added disk
      *)
      let lcm = List.fold_left (
        fun acc d ->
          let l, pass = acc in
          if pass && disk_pos_at t_start d = 0 then
            (Utils.Iter.lcm l d.num_positions, true)
          else
            (l, false)
        ) (1, true) disks in
      solve' (t_start + fst lcm) disks
    )
  in
  solve' 0 disks


let part1 filename =
  Utils.Input.read_file_to_string filename
  |> Utils.Input.split_on_newline
  |> List.map (fun x ->
    x
    |> String.split_on_char '.'
    |> (fun l -> List.nth l 0)
  )
  |> List.map disk_of_line
  |> solve_optimized
  |> Printf.printf "Part 1: %d\n"

let part2 filename =
  Utils.Input.read_file_to_string filename
  |> Utils.Input.split_on_newline
  |> List.map (fun x ->
    x
    |> String.split_on_char '.'
    |> (fun l -> List.nth l 0)
  )
  |> List.map disk_of_line
  |> ( (* add a new disk with 11 positions that starts at 0 *)
    fun ds ->
      ds @ [{disk_num = List.length ds + 1; start = 0; num_positions = 11}]
  )
  |> solve_optimized
  |> Printf.printf "Part 2: %d\n"
