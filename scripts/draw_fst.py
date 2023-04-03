from graphviz import Source
from helpers import run_cmd

run_cmd('fstdraw --isymbols=./vocab/chars.syms --osymbols=./vocab/chars.syms ./fsts/L.binfst binary.dot')

path = '/home/pigi/repos/spell-checker/binary.dot'
s = Source.from_file(path)
s.view()
