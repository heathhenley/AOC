(*
  Generate next MD5
  - track repeat of three chars (and the index of the MD5)
  - track repeat of five chars (and the index of the MD5)

  Each time we see a five char repeat:
  - check the three char map for indices lower than ours
  - is it in there?

  - These should be hash tables on the char, with list of idx
    - eg trips [ char ] = [ i, i - 1, ... ] # hashes with trips of char
    -    quints [ char ] = [ i, i - 1, ... ] # hashes with five of char

  - each time we find one we need to increase the count as well and stop at the
    the goal
  
 --> UPDATE: That approach was a bad idea. I had trouble getting that to work
     because the important index was the index of the trip, not the quint and I
     felt like I was looking back to check. I ended up just doing it pretty
     naively, and then adding caching for the second part - only compute the
     "mega" hash for part 2 once for any index for example. Could store the
     trips and quints that we find too but I didn't bother.
*)

let match_trips str =
  let re = Str.regexp {|\([a-z0-9]\)\1\1|} in
  match Str.search_forward re str 0 with
  | _ -> Some (Str.matched_string str)
  | exception Not_found -> None


let match_quints str =
  let re = Str.regexp {|\([a-z0-9]\)\1\1\1\1|} in
  match Str.search_forward re str 0 with
  | _ -> Some (Str.matched_string str)
  | exception Not_found -> None


let set_or_update ht s idx =
  let c = String.get s 0 in
  match Hashtbl.find_opt ht c with
  | None -> Hashtbl.add ht c [idx]
  | Some x ->  Hashtbl.replace ht c (idx :: x)

let get ht s =
  let c = String.get s 0 in
  match Hashtbl.find_opt ht c with
  | None -> []
  | Some x -> x

let within_n idx idx_list n =
  List.filter (fun i -> idx > i && (idx - i) <= n) idx_list
  |> List.length > 0

let check_hashes salt goal hash_func =
  let rec aux idx acc =
    let hash = hash_func (salt ^ (string_of_int idx)) in
    if (List.length acc) >= goal then
      acc
    else
      (match match_trips hash with
      | Some t->
        let found = ref false in
        (try
          for i = idx + 1 to idx + 1000 do
            match match_quints (hash_func (salt ^ (string_of_int i))) with
            | Some q when String.get q 0 = String.get t 0 ->
                found := true; raise Exit
            | _ -> ()
          done
        with Exit -> ());
        let acc =
          if !found then idx :: acc else acc
        in
        aux (idx + 1) acc
      | None ->
        aux (idx + 1) acc)
  in aux 0 []



let part1 _ = 
  let salt, goal = "zpqevtbw", 64 in
  let key_lst = check_hashes salt goal (
    fun s -> s |> Digest.string |> Digest.to_hex
  ) in
  let srt = List.sort compare key_lst in
  let res = List.nth srt (goal - 1)
  in
  Printf.printf "Part 1: %d\n" res

let multi_hash ht n orig =
  match Hashtbl.find_opt ht orig with
  | Some x -> x
  | None ->
    let rec aux n str =
      if n = 0 then (
        Hashtbl.add ht orig str;
        str
      ) else (
        let hash = Digest.string str |> Digest.to_hex in
        aux (n - 1) hash
      )
    in aux n orig


let part2 _ =
  let ht = Hashtbl.create 1000 in
  let salt, goal = "zpqevtbw", 64 in
  let key_lst = check_hashes salt goal (multi_hash ht 2017) in
  let srt = List.sort compare key_lst in
  let res = List.nth srt (goal - 1)
  in
  Printf.printf "Part 2: %d\n" res

