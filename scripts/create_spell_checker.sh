#!/usr/bin/env bash

# Run pipeline for edit distance spell checker

# Usage:
# bash scripts/create_spell_checker.py 


# python3 scripts/fetch_gutenberg.py > data/gutenberg.txt

# python3 scripts/make_vocabulary.py
# python3 scripts/words_chars_syms.py





# python3 scripts/transducer_fst.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/chars.syms ./fsts/L.fst ./fsts/L.binfst


# python3 scripts/acceptor_fst.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/words.syms ./fsts/V.txt ./fsts/V.fst




fstarcsort --sort_type="olabel" ./fsts/L.binfst ./fsts/Lsorted.fst
fstarcsort ./fsts/V.fst ./fsts/Vsorted.fst
fstcompose ./fsts/Lsorted.fst ./fsts/Vsorted.fst ./fsts/S.fst


# bash scripts/predict.sh ./fsts/S.fst cit