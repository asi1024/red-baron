#pragma once

#include <iostream>

#include "prod.cpp"
#include "sum.cpp"

void solve(int a, int b) {
  std::cout << prod(a, b) << " " << sum(a, b) * 2 << std::endl;
}
