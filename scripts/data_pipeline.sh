#!/usr/bin/env bash

# Run pipeline for data mining and preproceccing in order to use it in the spell checker

# Usage:
# bash scripts/data_pipeline.py 


# Fetch data
python3 scripts/fetch_gutenberg.py > data/gutenberg.txt

# Create vocabulary 
python3 scripts/make_vocabulary.py

# and symbolic files
python3 scripts/words_chars_syms.py

# Make, compile and sort character's tranducer L
python3 scripts/transducer_L.py
fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/chars.syms ./fsts/L.fst ./fsts/L.binfst
fstarcsort --sort_type="olabel" ./fsts/L.binfst ./fsts/L_sorted.fst

# Calculate the frequency of each word edit 
python3 scripts/edit_frequency.py
