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

# Calculate the frequency of each word edit 
python3 edit_frequency.py
