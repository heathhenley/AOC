(* A bool container with constant time clear *)
type t

(* create a new container with the given size - O(n) *)
val make : int -> t

(* get the value at the given index - O(1) *)
val get : t -> int -> bool

(* set the value at the given index - O(1) *)
val set : t -> int -> bool -> unit

(* clear the container - O(1) - except for overflow case *)
val clear : t -> unit
