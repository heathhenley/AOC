let pow10 n =
  let rec aux acc i = if i = 0 then acc else aux (acc * 10) (i - 1) in
  aux 1 n

(* How many base 10 digits are in n? *)
let digit_count n = log10 (float_of_int n) +. 1.0 |> int_of_float

(* Return a number of len digits from n start at start - eg
  get_subnumber 1234 0 2 = 12
  get_subnumber 1234 2 2 = 34
*)
let get_subnumber n start len =
  let num_digits = digit_count n in
  if start + len > num_digits then
    failwith "start + len is greater than the number of digits"
  else
    (* remove digits on the right by dividing by 10**(?) *)
    (* we end at start + len, there are num_digits - (start + len) digits to remove - need to divide by 10**(num_digits - (start + len)) *)
    let right_mask =
      int_of_float @@ (10. ** float_of_int (num_digits - (start + len)))
    in
    (* note: can avoid the divide if we compute the mask accounting for it, need
      tto think about the right offset - I think we substract however many we
      trimmed on the right
    *)
    let left_mask =
      int_of_float @@ (10. ** float_of_int (num_digits - start))
    in
    n / right_mask mod (left_mask / right_mask)
