let test_const_clear () =
  let cont = Container.Const_clear.make 10 in
  assert (Container.Const_clear.get cont 0 = false);
  assert (Container.Const_clear.get cont 1 = false);
  assert (Container.Const_clear.get cont 2 = false);

  Container.Const_clear.set cont 0 true;
  assert (Container.Const_clear.get cont 0 = true);
  assert (Container.Const_clear.get cont 1 = false);
  assert (Container.Const_clear.get cont 2 = false);

  Container.Const_clear.set cont 1 true;
  assert (Container.Const_clear.get cont 0 = true);
  assert (Container.Const_clear.get cont 1 = true);
  assert (Container.Const_clear.get cont 2 = false);

  Container.Const_clear.set cont 2 true;
  assert (Container.Const_clear.get cont 0 = true);
  assert (Container.Const_clear.get cont 1 = true);
  assert (Container.Const_clear.get cont 2 = true);
  assert (Container.Const_clear.get cont 3 = false);

  Container.Const_clear.clear cont;
  assert (Container.Const_clear.get cont 0 = false);
  assert (Container.Const_clear.get cont 1 = false);
  assert (Container.Const_clear.get cont 2 = false);

  match Container.Const_clear.get cont 10 with
  | _ -> assert false
  | exception Invalid_argument _ -> ();

  match Container.Const_clear.set cont 10 true with
  | _ -> assert false
  | exception Invalid_argument _ -> ()

let () = test_const_clear ()
