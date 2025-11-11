type t = {
  data : int array;
  size : int;
  mutable generation : int;
}

let make size = { data = Array.make size (-1); size; generation = 0 }

let get cont idx =
  cont.data.(idx) = cont.generation

let set cont idx v =
  if v then cont.data.(idx) <- cont.generation else cont.data.(idx) <- -1

let clear cont =
  if cont.generation = max_int then (
    (* this is not O(1) but doesn't happen often *)
    cont.generation <- 0;
    Array.fill cont.data 0 cont.size (-1))
  else
    (* increment the generation  - this is O(1) - normal case *)
    cont.generation <- cont.generation + 1
