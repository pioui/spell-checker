#!/usr/bin/env bash

# Run pipeline for edit distance spell checker

# Usage:
# bash scripts/spell_checker_S.py 

# Fetch data
python3 scripts/fetch_gutenberg.py > data/gutenberg.txt

# Create vocabulary and symbolic files
python3 scripts/make_vocabulary.py
python3 scripts/words_chars_syms.py

# Make and compile tranducer
python3 scripts/transducer_L.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/chars.syms ./fsts/L.fst ./fsts/L.binfst

# Make and compile transducer with un-balanced weights
python3 scripts/transducer_L.py -iw 1 -dw 2 -sw 3 -tf L_unbalanced.fst
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/chars.syms ./fsts/L_unbalanced.fst ./fsts/L_unbalanced.binfst

# Make optimize and compile acceptor
python3 scripts/acceptor_V.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/words.syms ./fsts/V.txt ./fsts/V.fst
fstrmepsilon ./fsts/V.fst | fstdeterminize | fstminimize > ./fsts/V_opt.fst


# Sort output of transducer and input of acceptor to match
fstarcsort --sort_type="olabel" ./fsts/L.binfst ./fsts/L_sorted.fst
fstarcsort --sort_type="olabel" ./fsts/L_unbalanced.binfst ./fsts/L_unbalanced_sorted.fst

fstarcsort ./fsts/V_opt.fst ./fsts/V_sorted.fst

# Compose to create the spellcheckers
fstcompose ./fsts/L_sorted.fst ./fsts/V_sorted.fst ./fsts/S.fst
fstcompose ./fsts/L_unbalanced_sorted.fst ./fsts/V_sorted.fst ./fsts/S_unbalanced.fst


# Test it
echo 'Correction of word cit'
echo Balanced: 
bash scripts/predict.sh ./fsts/S.fst cit
echo
echo Unbalanced: 
bash scripts/predict.sh ./fsts/S_unbalanced.fst cit
echo
echo 'Correction of word cwt'
echo Balanced: 
bash scripts/predict.sh ./fsts/S.fst cwt
echo
echo Unbalanced: 
bash scripts/predict.sh ./fsts/S_unbalanced.fst cwt
echo