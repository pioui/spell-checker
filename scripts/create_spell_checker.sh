#!/usr/bin/env bash

# Run pipeline for edit distance spell checker

# Usage:
# bash scripts/create_spell_checker.py 



python3 scripts/transducer_fst.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/chars.syms ./fsts/L.fst >  ./fsts/L.binfst
fstarcsort ./fsts/L.binfst ./fsts/L_sorted.binfst



python3 scripts/acceptor_fst.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/words.syms ./fsts/V.fst >  ./fsts/V.binfst
fstrmepsilon ./fsts/V.binfst | fstdeterminize | fstminimize > ./fsts/V_opt.binfst
fstarcsort ./fsts/V_opt.binfst ./fsts/V_opt_sorted.binfst


fstcompose ./fsts/L_sorted.binfst ./fsts/V_opt_sorted.binfst ./fsts/S.binfst 

