let combinations lst n =
  (* combinations of n elements from lst *)
  let rec aux acc i results =
    (* we can take the current element or not *)
    if List.length acc = n then List.rev acc :: results
    else if i >= List.length lst then results
    else
      (* add i'th element to c and recurse *)
      let new_c = List.nth lst i :: acc in
      let res = aux new_c (i + 1) results in
      (* skip i'th element and recurse *)
      aux acc (i + 1) res
  in
  aux [] 0 []

let rec gcd a b =
  if b = 0 then a
  else gcd b (a mod b)

let lcm a b = (a * b) / (gcd a b)

let rec lcm_list lst =
  match lst with
  | [] -> 1
  | h :: t -> lcm h (lcm_list t)