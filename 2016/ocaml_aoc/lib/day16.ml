(* I knew I would regret doing this the most straight forward way for part 1...
  - actually make the string according to the rules
  - compress it "checksum"ing according to the rules
  - repeat until odd --> works fine for part 1

  Part 2 - doing way too much string creating etc, and there's going to be a
  way to optimize because of the pattern...
  I'm sure ther's a way to do this using all binary operations too but I haven't
  though much about it. I think the naive-ish approach will still work if it's
  a little more optimized (maybe it will run in secs/minutes though), tbd
*)
let rev s =
  let n = String.length s in
   let rec aux acc i =
    match i with
    | x when x >= n -> acc
    | _ -> aux ((String.sub s i 1) ^ acc) (i + 1)
  in
  aux "" 0

let flip s =
  let n = String.length s in
   let rec aux acc i =
    if i >= n then
      acc
    else (
      match String.get s i with
      | '0' -> aux (acc ^ "1") (i + 1)
      | '1' -> aux (acc ^ "0") (i + 1)
      | _ -> failwith "None 0, 1 char not allowed"
    )
  in
  aux "" 0

let explode seed goal =
  let rec aux acc =
    if String.length acc >= goal then (
      String.sub acc 0 goal (* return the first goal chars *)
    ) else (
      aux (acc ^ "0" ^ (acc |> rev |> flip))
    ) in
  aux seed

let checksum s =
  let rec aux acc idx =
    (* check the first two chars and build checksum *)
    if idx >= String.length s - 1 then
      acc
    else
      match String.get s idx, String.get s (idx + 1) with
      | '0', '0' -> aux (acc ^ "1") (idx + 2)
      | '1', '1' -> aux (acc ^ "1") (idx + 2)
      | '0', '1' -> aux (acc ^ "0") (idx + 2)
      | '1', '0' -> aux (acc ^ "0") (idx + 2)
      | _ -> failwith "Invalid characters"
    in
    aux "" 0


let rec compress s =
  if String.length s mod 2 = 1 then
    s
  else
    compress (checksum s)

(*let rec char_at i seed current_len =
  Printf.printf "char_at %d %s %d\n" i seed current_len;
  if String.length seed = current_len then
    String.get seed i
  else (
    let prev = (current_len - 1) / 2 in
    if i < prev then (* in the first half *)
      char_at i seed prev
    else if i = prev then (* the middle char *)
      '0'
    else  (* in the flipped part *)
      let flip_i = current_len - i - 1 in
      let c = char_at flip_i seed prev in
      if c = '0' then '1' else '0'
  )

let rec checksum_len n =
  if n mod 2 = 1 then
    n
  else
    checksum_len (n / 2)
*)

let part1_impl goal seed = 
  explode seed goal |> compress |> Printf.printf "Part 1: %s\n"

let part1 _ =
  part1_impl 272 "00111101111101000"

let part2 _ = (* we're gonna need a bigger boat *) ()

