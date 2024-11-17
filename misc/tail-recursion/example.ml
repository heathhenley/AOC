(* Non tail-recursive list len function *)
let rec len lst =
  match lst with
  | [] -> 0
  | _::t -> 1 + len t

(* Tail-recursive list len function *)
let len_tr lst =
  let rec len_tr' lst current_len =
    match lst with
    | [] -> current_len
    | _::t -> len_tr' t (current_len + 1)
  in
  len_tr' lst 0

  (* Non tail-recursive sum function*)
let rec sum lst =
  match lst with
  | [] -> 0
  | h::t -> h + sum t
  
  (* Tail-recursive sum function *)
let sum_tr lst =
  let rec sum_tr' lst current_sum =
    match lst with
    | [] -> current_sum
    | h::t -> sum_tr' t (current_sum + h)
  in
  sum_tr' lst 0

(* Non tail-recursive factorial function *)
let rec factorial n =
  match n with
  | 0 -> 1
  | _ -> n * factorial (n - 1)

(* Tail-recursive factorial function *)
let factorial_tr n =
  let rec factorial_tr' n current_factorial =
    match n with
    | 0 -> current_factorial
    | _ -> factorial_tr' (n - 1) (n * current_factorial)
  in
  factorial_tr' n 1

(* Non tail-recursive fibonacci function *)
let rec fibonacci n =
  match n with
  | 0 -> 0
  | 1 -> 1
  | _ -> fibonacci (n - 1) + fibonacci (n - 2)

(* Tail-recursive fibonacci function *)
let fibonacci_tr n =
  let rec fibonacci_tr' n a b =
    match n with
    | 0 -> a
    | _ -> fibonacci_tr' (n-1) b (a+b)
  in
  fibonacci_tr' n 0 1

let () =
  Printf.printf "Running the examples (small cases):\n";
  Printf.printf "len [1;2;3;4;5] = %d\n" (len [1;2;3;4;5]);
  Printf.printf "len_tr [1;2;3;4;5] = %d\n" (len_tr [1;2;3;4;5]);
  Printf.printf "sum [1;2;3;4;5] = %d\n" (sum [1;2;3;4;5]);
  Printf.printf "sum_tr [1;2;3;4;5] = %d\n" (sum_tr [1;2;3;4;5]);
  Printf.printf "factorial 5 = %d\n" (factorial 5);
  Printf.printf "factorial_tr 5 = %d\n" (factorial_tr 5);
  Printf.printf "fibonacci 10 = %d\n" (fibonacci 10);
  Printf.printf "fibonacci_tr 10 = %d\n" (fibonacci_tr 10);