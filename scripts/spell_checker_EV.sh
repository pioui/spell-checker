#!/usr/bin/env bash

# Run pipeline for weigted edit distance spell checker EV

# Usage:
# bash scripts/spell_checker_EV.py 

# Make and compile tranducer
python3 scripts/transducer_E.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/chars.syms ./fsts/E.fst ./fsts/E.binfst

# Sort output of transducer and input of acceptor to match
fstarcsort --sort_type="olabel" ./fsts/E.binfst ./fsts/E_sorted.fst

# Compose to create the spellcheckers
fstcompose ./fsts/E_sorted.fst ./fsts/V_sorted.fst ./fsts/EV.fst


# Test it
echo 'Correction of word cit'
bash scripts/predict.sh ./fsts/EV.fst cit
echo
echo 'Correction of word cwt'
bash scripts/predict.sh ./fsts/EV.fst cwt
echo
