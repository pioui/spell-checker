#!/usr/bin/env bash

# Run pipeline for edit distance spell checker

# Usage:
# bash scripts/spell_checkers_EV.py 

# # Make optimize and compile acceptor W
python3 scripts/acceptor_W.py
fstcompile --isymbols=./vocab/words.syms --osymbols=./vocab/words.syms ./fsts/W.fst ./fsts/W.binfst
fstarcsort ./fsts/W.binfst ./fsts/W_sorted.fst

# Compose to create the spellcheckers
fstcompose ./fsts/L.binfst ./fsts/V_sorted.fst ./fsts/LV.fst
fstcompose ./fsts/LV.fst ./fsts/W_sorted.fst ./fsts/LVW.fst

fstcompose ./fsts/E_sorted.fst ./fsts/V_sorted.fst ./fsts/EV.fst
fstcompose ./fsts/EV.fst ./fsts/W_sorted.fst ./fsts/EVW.fst

