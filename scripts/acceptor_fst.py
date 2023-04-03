from helpers import run_cmd
import os

import argparse

# Parse input arguments
parser = argparse.ArgumentParser(description='Acceptor fst')
parser.add_argument('-af', type=str, default = "V.fst", help='Acceptor .fst filename')

parser.add_argument('-cf', type=str, default = "./vocab/chars.syms", help='Characters .syms filepath')
parser.add_argument('-wf', type=str, default = "./vocab/words.syms", help='Words .syms filepath')

args = parser.parse_args()

# Manage files and directories
fst_folder = './fsts/'
if not os.path.exists(fst_folder): os.makedirs(fst_folder)

# Define input and output file paths
acceptor_file = fst_folder+args.af
chars_file = args.cf
words_file = args.wf

# Make sure the we don't continue writing in previous output files
if os.path.exists(acceptor_file):
    os.remove(acceptor_file)


# First, we need to define some constants that will be used later.
# We'll also define a weight of 0 for all word pairs.
EPS_SYMBOL = "<epsilon>"
EDGE_WEIGHT = "0"

# Read the words_file file and create a symbol table.
words_table = {}
with open(words_file, "r") as f:
    for line in f:
        word, index = line.strip().split()
        words_table[word] = int(index)


# Next, we'll create a string for each possible transition in the letters of each word in the V-transducer.
# We'll represent each transition as a triple (node1, node 2, input symbol, output symbol, weight).
# For each word w in the words' table, we'll create the transision for each letter:
transitions = []
node_count = 1
for word in words_table:
    if word == EPS_SYMBOL: continue
    transitions.append((0, node_count, word[0], word, EDGE_WEIGHT))

    for i in range(len(word)-1):
        transitions.append((node_count, node_count+1, word[i+1], EPS_SYMBOL, EDGE_WEIGHT))
        node_count = node_count+1
    node_count = node_count+1


# Finally, we'll write the L-transducer to the L.fst file in OpenFST text format.
# We'll use state 0 as the only state, and add transitions for each possible input symbol.
with open(acceptor_file, "w") as f:
    for t in transitions:
        f.write(f"{t[0]}\t{t[1]}\t{t[2]}\t{t[3]}\t{t[4]}\n")

## Fstcompile –help | prep “isymbols”

# TODO: make a seperate bash file
# Optimize lexicon

# print(f"fstcompile --isymbols={chars_file} --osymbols={words_file} {acceptor_file} >  {acceptor_binfile}")

# print(f"fstrmepsilon {acceptor_binfile} | fstdeterminize | fstminimize > {optacceptor_binfile}")

# print(f"fstcompile --isymbols={chars_file} --osymbols={words_file} {optacceptor_file} >  {optacceptor_binfile}")
