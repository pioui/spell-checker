#!/usr/bin/env bash

# Run pipeline for vanilla edit distance spell checker

# Usage:
# bash scripts/spell_checkers_pipeline.py 

# Make, compile and sort character's tranducer L
python3 scripts/transducer_L.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/chars.syms ./fsts/L.fst ./fsts/L.binfst
fstarcsort --sort_type="olabel" ./fsts/L.binfst ./fsts/L_sorted.fst

# Make, compile and sort character's tranducer L
python3 scripts/transducer_L.py -dw 5 -iw 2 -sw 2 -tf Lu.fst
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/chars.syms ./fsts/Lu.fst ./fsts/Lu.binfst
fstarcsort --sort_type="olabel" ./fsts/Lu.binfst ./fsts/Lu_sorted.fst

# Make optimize, compile and sort vocabulary acceptor V
python3 scripts/acceptor_V.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/words.syms ./fsts/V.txt ./fsts/V.fst
fstrmepsilon ./fsts/V.fst | fstdeterminize | fstminimize > ./fsts/V_opt.fst
fstarcsort ./fsts/V_opt.fst ./fsts/V_sorted.fst

# Make, compile and sort tranducer E
python3 scripts/transducer_E.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/chars.syms ./fsts/E.fst ./fsts/E.binfst
fstarcsort --sort_type="olabel" ./fsts/E.binfst ./fsts/E_sorted.fst

# Make optimize and compile vocabulary acceptor W
python3 scripts/acceptor_W.py
fstcompile --isymbols=./vocab/words.syms --osymbols=./vocab/words.syms ./fsts/W.fst ./fsts/W.binfst
fstarcsort ./fsts/W.binfst ./fsts/W_sorted.fst

# Compose to create the spellcheckers
fstcompose ./fsts/E_sorted.fst ./fsts/V_sorted.fst ./fsts/EV.fst

fstcompose ./fsts/L.binfst ./fsts/V_sorted.fst ./fsts/LV.fst
fstcompose ./fsts/Lu.binfst ./fsts/V_sorted.fst ./fsts/LuV.fst

fstcompose ./fsts/LV.fst ./fsts/W_sorted.fst ./fsts/LVW.fst
fstcompose ./fsts/LuV.fst ./fsts/W_sorted.fst ./fsts/LuVW.fst

fstcompose ./fsts/EV.fst ./fsts/W_sorted.fst ./fsts/EVW.fst

# Remove files that are no longer usefull
rm ./fsts/L.binfst
rm ./fsts/L_sorted.fst
rm ./fsts/L.fst
rm ./fsts/Lu.fst
rm ./fsts/Lu.binfst
rm ./fsts/Lu_sorted.fst
rm ./fsts/V.fst
rm ./fsts/V.txt
rm ./fsts/V_opt.fst
rm ./fsts/V_sorted.fst
rm ./fsts/E.fst
rm ./fsts/E.binfst
rm ./fsts/E_sorted.fst
rm ./fsts/W.fst
rm ./fsts/W.binfst
rm ./fsts/W_sorted.fst

