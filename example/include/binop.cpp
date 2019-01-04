#pragma once

template<class BinOp>
int binop(BinOp op, int a, int b) {
  return op(a, b);
}
