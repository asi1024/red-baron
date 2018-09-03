#include <iostream>

int a[8];

int main() {
  for (int i = 0;; ++i) {
    a[i] = 100;
    std::cout << a[i] << std::endl;
  }
  return 0;
}
