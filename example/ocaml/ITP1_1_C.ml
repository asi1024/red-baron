(*+ import ../include/ITP_1_C.1.ml +*)

let () =
  let a, b = Scanf.scanf "%d %d" (fun x y -> x, y) in
  solve a b
;;
