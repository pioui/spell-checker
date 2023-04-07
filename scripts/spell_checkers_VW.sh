#!/usr/bin/env bash

# Run pipeline for edit distance spell checker

# Usage:
# bash scripts/spell_checker_EV.py 

# Make and compile tranducer L
python3 scripts/transducer_L.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/chars.syms ./fsts/L.fst ./fsts/L.binfst

# Make and compile tranducer E
python3 scripts/transducer_E.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/chars.syms ./fsts/E.fst ./fsts/E.binfst


# Make optimize and compile acceptor V
python3 scripts/acceptor_V.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/words.syms ./fsts/V.txt ./fsts/V.fst
fstrmepsilon ./fsts/V.fst | fstdeterminize | fstminimize > ./fsts/V_opt.fst

# Make optimize and compile acceptor W
python3 scripts/acceptor_W.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/words.syms ./fsts/W.txt ./fsts/W.fst
fstrmepsilon ./fsts/W.fst | fstdeterminize | fstminimize > ./fsts/W_opt.fst


# Sort output of transducer and input of acceptor to match
fstarcsort --sort_type="olabel" ./fsts/E.binfst ./fsts/E_sorted.fst

fstarcsort ./fsts/V_opt.fst ./fsts/V_sorted.fst
fstarcsort ./fsts/W_opt.fst ./fsts/W_sorted.fst

# Compose to create the spellcheckers
fstcompose ./fsts/L.fst ./fsts/V_sorted.fst ./fsts/LV.fst

fstrmepsilon ./fsts/LV.fst | fstdeterminize | fstminimize > ./fsts/LV_opt.fst
fstarcsort ./fsts/LV_opt.fst ./fsts/LV_sorted.fst

fstcompose ./fsts/LV_sorted.fst ./fsts/W.fst ./fsts/LVW.fst


# Test it
echo 'Correction of word cit'
bash scripts/predict.sh ./fsts/LVW.fst cit
echo
echo 'Correction of word cwt'
bash scripts/predict.sh ./fsts/LVW.fst cwt
echo
