type 'r visit_result =
  [ `Stop of 'r
  | `Continue
  ]

let bfs ?(size = 10) ?(key = fun x -> x) start ~neighbors ~on_visit =
  let queue = Queue.create () in
  let visited = Hashtbl.create size in
  Queue.add (start, 0) queue;
  Hashtbl.add visited (key start) ();
  let rec bfs' () =
    if Queue.is_empty queue then None
    else
      let node, dist = Queue.pop queue in
      match on_visit node dist with
      | `Stop r -> Some r
      | `Continue ->
          neighbors node
          |> List.iter (fun neighbor ->
                 if not (Hashtbl.mem visited (key neighbor)) then (
                   Queue.add (neighbor, dist + 1) queue;
                   Hashtbl.add visited (key neighbor) ()));
          bfs' ()
  in
  bfs' ()
