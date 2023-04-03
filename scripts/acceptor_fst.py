from helpers import run_cmd
import os

# Manage files and directories
if not os.path.exists('fsts'): os.makedirs('fsts')

# Define input and output file paths
acceptor_file = "./fsts/V.fst"
optacceptor_file = "./fsts/V_opt.fst"
acceptor_binfile = "./fsts/V.binfst"
optacceptor_binfile = "./fsts/V_opt.binfst"

chars_file = "./vocab/chars.syms"
words_file = "./vocab/words.syms"

# Make sure the we don't continue writing in previous output files
if os.path.exists(acceptor_file):
    os.remove(acceptor_file)

if os.path.exists(optacceptor_file):
    os.remove(optacceptor_file)

if os.path.exists(acceptor_binfile):
    os.remove(acceptor_binfile)

if os.path.exists(optacceptor_binfile):
    os.remove(optacceptor_binfile)

# First, we need to define some constants that will be used later.
# We'll also define a weight of 1 for all non-matching character pairs.

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

run_cmd(f"fstcompile --isymbols={chars_file} --osymbols={words_file} {acceptor_file} >  {acceptor_binfile}")

run_cmd(f"fstrmepsilon {acceptor_binfile} | fstdeterminize | fstminimize > {optacceptor_binfile}")

# run_cmd(f"fstcompile --isymbols={chars_file} --osymbols={words_file} {optacceptor_file} >  {optacceptor_binfile}")

