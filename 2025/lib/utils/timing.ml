let pretty_print_time elapsed_time =
  if elapsed_time < 0.001 then
    Printf.printf "Elapsed time: %.2f us\n" (elapsed_time *. 1_000_000.0)
  else if elapsed_time < 0.01 then
    Printf.printf "Elapsed time: %.2f ms\n" (elapsed_time *. 1000.0)
  else if elapsed_time < 60.0 then
    Printf.printf "Elapsed time: %.2f secs\n" elapsed_time
  else if elapsed_time < 3600.0 then
    Printf.printf "Elapsed time: %.2f mins\n" (elapsed_time /. 60.0)
  else Printf.printf "Elapsed time: %.2f hrs\n" (elapsed_time /. 3600.0)

let time_function f arg =
  let start_time = Sys.time () in
  let result = f arg in
  let end_time = Sys.time () in
  let elapsed_time = end_time -. start_time in
  pretty_print_time elapsed_time;
  result
