from helpers import run_cmd
import os
import argparse

# Parse input arguments
parser = argparse.ArgumentParser(description='Transducer fst')
parser.add_argument('-dw', type=str, default = 1, help='Deletion weight')
parser.add_argument('-iw', type=str, default = 1, help='Insertion weight')
parser.add_argument('-sw', type=str, default = 1, help='Substitution weight')

parser.add_argument('-tf', type=str, default = "L.fst", help='Tranducer .fst filename')

parser.add_argument('-cf', type=str, default = "./vocab/chars.syms", help='Characters .syms filepath')

args = parser.parse_args()


# Manage files and directories
fst_folder = './fsts/'
if not os.path.exists(fst_folder): os.makedirs(fst_folder)

# Define input and output file paths
transducer_file = fst_folder+args.tf
chars_file = args.cf

# Make sure the we don't continue writing in previous output files
if os.path.exists(transducer_file):
    os.remove(transducer_file)


# First, we need to define some constants that will be used later.
# We'll also define a weight of 1 for all non-matching character pairs.
EPS_SYMBOL = "<epsilon>"
DELETION_WEIGHT = args.dw
INSERTION_WEIGHT = args.iw
SUBSTITUTION_WEIGHT = args.sw

# Now, let's read the chars.syms file and create a symbol table.
symbol_table = {}
with open(chars_file, "r") as f:
    for line in f:
        symbol, index = line.strip().split()
        symbol_table[symbol] = int(index)

# Next, we'll create a string for each possible transition in the L-transducer.
# We'll represent each transition as a triple (input symbol, output symbol, weight).
# For each character c in the symbol table, we'll create three transitions:
transitions = []
for c1 in symbol_table:
    for c2 in symbol_table:
        # No edit
        if c1 == EPS_SYMBOL and c2 == EPS_SYMBOL:
            continue
        elif c1 == c2:
            transitions.append((c1, c2, 0))
        # Insertion
        elif c1 == EPS_SYMBOL:
            transitions.append((EPS_SYMBOL, c2, INSERTION_WEIGHT))
        # Deletion
        elif c2 == EPS_SYMBOL:
            transitions.append((c1, EPS_SYMBOL, DELETION_WEIGHT))
        # Subsitution
        else:
            transitions.append((c1, c2, SUBSTITUTION_WEIGHT))

# Finally, we'll write the L-transducer to the L.fst file in OpenFST text format.
# We'll use state 0 as the only state, and add transitions for each possible input symbol.
with open(transducer_file, "w") as f:
    for t in transitions:
        f.write(f"0\t0\t{t[0]}\t{t[1]}\t{t[2]}\n")

# TODO: make a seperate bash file
## Fstcompile –help | prep “isymbols”
# run_cmd(f"fstcompile --isymbols={chars_file} --osymbols={chars_file} {transducer_file} >  {transducer_binfile}")
# print(f"fstcompile --isymbols={chars_file} --osymbols={chars_file} {transducer_file} >  ./fsts/L.binfst")