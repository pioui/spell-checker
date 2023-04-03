from graphviz import Source
from helpers import run_cmd

# TODO: make a seperate bash file
run_cmd('fstdraw --isymbols=./vocab/chars.syms --osymbols=./vocab/chars.syms ./fsts/L.binfst L.dot')
run_cmd('fstdraw --isymbols=./vocab/chars.syms --osymbols=./vocab/words.syms ./fsts/V_opt.binfst V.dot')

Lpath = '/home/pigi/repos/spell-checker/L.dot'
Vpath = '/home/pigi/repos/spell-checker/V.dot'

s = Source.from_file(Lpath)
s.view()

# TODO: do it in a subset, takes ages like that
s = Source.from_file(Vpath)
s.view()