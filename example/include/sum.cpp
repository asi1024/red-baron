#pragma once

#include <functional>

#include "binop.cpp"

int sum(int a, int b) {
  return binop(std::plus<int>(), a, b);
}
