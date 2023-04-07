from helpers import run_cmd
import os
import argparse
from util import EPS, INFINITY
from numpy import log

"""
Calculate acceptor V
Acceptor, we create an .fst weighted transducer that implements the Levenshtein distance:
Usage:
  python3 scripts/transducer_E.py -tf E.fst  -ef edits_frequency.txt -cf chars.syms 

"""

# Parse input arguments
parser = argparse.ArgumentParser(description="Transducer fst")

parser.add_argument("-tf", type=str, default="E.fst", help="Tranducer .fst filename")

parser.add_argument(
    "-ef",
    type=str,
    default="./data/edits_frequency.txt",
    help="Edit frequency .txt filename",
)
parser.add_argument(
    "-cf", type=str, default="./vocab/chars.syms", help="Characters .syms filepath"
)

args = parser.parse_args()


# Manage files and directories
fst_folder = "./fsts/"
if not os.path.exists(fst_folder):
    os.makedirs(fst_folder)

# Define input and output file paths
transducer_file = fst_folder + args.tf
chars_file = args.cf
edits_frequency_file = args.ef

# Make sure the we don't continue writing in previous output files
if os.path.exists(transducer_file):
    os.remove(transducer_file)

# Now, let's read the chars.syms file and create a symbol table.
symbol_table = {}
with open(chars_file, "r") as f:
    for line in f:
        symbol, index = line.strip().split()
        symbol_table[symbol] = int(index)

# Also, let's read the edit frequency.txt  file and create a frequency table.
edit_frequency = {}
with open(edits_frequency_file, "r") as f:
    for line in f:
        c1, c2, frequency = line.strip().split()
        edit_frequency[(c1, c2)] = float(frequency)

# Next, we'll create a string for each possible transition in the L-transducer.
# We'll represent each transition as a triple (input symbol, output symbol, weight).
# For each character c in the symbol table, we'll create three transitions:
transitions = []
for c1 in symbol_table:
    for c2 in symbol_table:
        if c1 == EPS and c2 == EPS:
            continue
        elif c1 == c2:
            transitions.append((c1, c2, 0))
        elif (c1, c2) in edit_frequency:
            transitions.append((c1, c2, -log(edit_frequency[(c1, c2)])))
        else:
            transitions.append((c1, c2, INFINITY))


# Finally, we'll write the L-transducer to the L.fst file in OpenFST text format.
# We'll use state 0 as the only state, and add transitions for each possible input symbol.
with open(transducer_file, "w") as f:
    for t in transitions:
        f.write(f"0 0 {t[0]} {t[1]} {t[2]}\n")
    f.write("0")
