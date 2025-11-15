type 'r visit_result = [`Stop of 'r | `Continue ]

let bfs ?(size=10) start ~neighbors ~on_visit =
  let q = Queue.create () in
  let v = Hashtbl.create size in
  Queue.add (start, 0) q;
  Hashtbl.add v start ();
  let rec bfs' () =
    if Queue.is_empty q then None
    else 
      let node, dist = Queue.pop q in
      match on_visit node dist with
      | `Stop r -> Some r
      | `Continue ->
        neighbors node
        |> List.iter (fun n ->
              if not (Hashtbl.mem v n) then (
                Queue.add (n, dist + 1) q;
                Hashtbl.add v n ()));
        bfs' ()
  in
  bfs' ()

