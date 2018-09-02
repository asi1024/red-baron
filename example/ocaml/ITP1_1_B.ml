let () =
  let x = Scanf.scanf "%d" (fun x -> x) in
  Printf.printf "%d\n" (x * x * x)
;;
