import os


cc_base_flag = '-O2 -Werror -Wextra -Wshadow -Wno-unused-result'
ml_base_flag = '-linkpkg -thread -package str,num,threads,batteries'

# C++
cc = os.getenv('CXX', 'gcc')
ccflags = os.getenv('CCFLAGS', cc_base_flag)

# C++
cxx = os.getenv('CXX', 'g++')
cxxflags = os.getenv('CXXFLAGS', '--std=c++17 ' + cc_base_flag)

# Haskell
ghc = os.getenv('GHC', 'ghc')
ghcflags = os.getenv('GHCFLAGS', '-O2')

# OCaml
ocamlopt = os.getenv('OCAMLOPT', 'ocamlfind ocamlopt')
ocamloptflags = os.getenv('OCAMLOPTFLAGS', ml_base_flag)
