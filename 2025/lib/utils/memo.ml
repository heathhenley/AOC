(* Memoization for recursive functions  - kind of weird we need the sig
to change from (f: a -> b) to (f : a -> b) -> a -> b

like: 
let rec fib n =
  if n <= 1 then n
  else fib (n-1) + fib (n-2)

to:
let fib = memo_rec (fun f n ->
  if n <= 1 then n
  else f (n-1) + f (n-2)

So inside the recursive calls will actuall use the memo'd version instead of
of the real function
)

*)
let memo_rec ?(init_size = 1000) ?(key = fun x -> x) f =
  let ht = Hashtbl.create init_size in
  let rec memo_rec' x =
    let k = key x in
    match Hashtbl.find_opt ht (key x) with
    | Some v -> v
    | None ->
        let v = f memo_rec' x in
        Hashtbl.add ht k v;
        v
  in
  memo_rec'

let memo ?(init_size = 1000) ?(key = fun x -> x) f =
  memo_rec ~init_size ~key (fun _ -> f)
