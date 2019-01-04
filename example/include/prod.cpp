#pragma once

#include <functional>

#include "binop.cpp"

int prod(int a, int b) {
  return binop(std::multiplies<int>(), a, b);
}
