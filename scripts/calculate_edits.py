from helpers import run_cmd
import os

import argparse
from util import EPS

# Script to make edits file from a given txt and calculate also the frequence of each

# Parse input arguments
parser = argparse.ArgumentParser(description='Word edits calculation')
parser.add_argument('-df', type=str, default = "./data/wiki.txt", help='common mistakes data .txt filename')
parser.add_argument('-ef', type=str, default = "./data/edits.txt", help='.txt filename to save all word edits ')
parser.add_argument('-ff', type=str, default = "./data/edits_frequency.txt", help='.txt filename to save all word edits and their frequency')

args = parser.parse_args()

# Define input and output file paths
data_file = args.df
edits_file = args.ef
edits_frequency_file = args.ff

# Make sure the we don't continue writing in previous output files
if os.path.exists(edits_file):
    os.remove(edits_file)
if os.path.exists(edits_frequency_file):
    os.remove(edits_frequency_file)

# Read the data_file file and create a symbol table.
edits = []
with open(data_file, "r") as f:
    for line in f:
        wrong, correct = line.strip().split()
        try:
            word_edits = str(run_cmd(f'bash ./scripts/word_edits.sh {wrong} {correct}')).strip().split()
        except :
            # Raise exception in case the word has characters other than lowercase letters
            word_edits = ''
            continue

        for i in range(0,len(word_edits),2):
            source = word_edits[i]
            target = word_edits[i+1]
            edits.append((source, target))


# Write all edits in save_file
with open(edits_file, "w") as f:
    for e in edits:
        f.write(f"{e[0]} {e[1]}\n")

# For each edit calculate it's frequency and save it on the dictionary
edit_frequency = {}
for e in edits:
    if e not in edit_frequency:
        edit_frequency[e]=1
    else:
        edit_frequency[e] += 1

# Write all edits' frequency in save_file
with open(edits_frequency_file, "w") as f:
    for e in edit_frequency.keys():
        f.write(f"{e[0]} {e[1]} {edit_frequency[e]}\n")