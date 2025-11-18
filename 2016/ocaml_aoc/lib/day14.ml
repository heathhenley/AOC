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
  | None -> Hashtbl.add ht c [ idx ]
  | Some x -> Hashtbl.replace ht c (idx :: x)

let get ht s =
  let c = String.get s 0 in
  match Hashtbl.find_opt ht c with
  | None -> []
  | Some x -> x

let within_n idx idx_list n =
  List.filter (fun i -> idx > i && idx - i <= n) idx_list |> List.length > 0

let check_hashes salt goal hash_func =
  let match_t_mem = Utils.Memo.memo ~key:(fun s -> s) match_trips in
  let match_q_mem = Utils.Memo.memo ~key:(fun s -> s) match_quints in
  let rec aux idx acc =
    let hash = hash_func (salt ^ string_of_int idx) in
    if List.length acc >= goal then acc
    else
      match match_t_mem hash with
      | Some t ->
          let found = ref false in
          (try
             for i = idx + 1 to idx + 1000 do
               match match_q_mem (hash_func (salt ^ string_of_int i)) with
               | Some q when String.get q 0 = String.get t 0 ->
                   found := true;
                   raise Exit
               | _ -> ()
             done
           with Exit -> ());
          let acc = if !found then idx :: acc else acc in
          aux (idx + 1) acc
      | None -> aux (idx + 1) acc
  in
  aux 0 []

let md5 s = s |> Digest.string |> Digest.to_hex

let md5_stretched n s =
  let rec aux n s = if n = 0 then s else aux (n - 1) (md5 s) in
  aux n s

let part1 _ =
  let salt, goal = ("zpqevtbw", 64) in
  let memod = Utils.Memo.memo ~key:(fun s -> s) md5 in
  let key_lst = check_hashes salt goal memod in
  let srt = List.sort compare key_lst in
  let res = List.nth srt (goal - 1) in
  Printf.printf "Part 1: %d\n" res

let part2 _ =
  let salt, goal = ("zpqevtbw", 64) in
  let memod = Utils.Memo.memo ~key:(fun s -> s) (md5_stretched 2017) in
  let key_lst = check_hashes salt goal memod in
  let srt = List.sort compare key_lst in
  let res = List.nth srt (goal - 1) in
  Printf.printf "Part 2: %d\n" res
