# First, we need to define some constants that will be used later.
# We'll represent the characters 'e' and '<eps>' with the same symbol.
# We'll also define a weight of 1 for all non-matching character pairs.
from helpers import run_cmd

EPS_SYMBOL = "<eps>"
DELETION_WEIGHT = "1"
INSERTION_WEIGHT = "1"
SUBSTITUTION_WEIGHT = "1"

# Now, let's read the chars.syms file and create a symbol table.
symbol_table = {EPS_SYMBOL: 0}
with open("./vocab/chars.syms", "r") as f:
    for line in f:
        symbol, index = line.strip().split()
        symbol_table[symbol] = int(index)

# Next, we'll create a string for each possible transition in the L-converter.
# We'll represent each transition as a triple (input symbol, output symbol, weight).
# For each character c in the symbol table, we'll create three transitions:
# 1. (c, c, 0) - no edit
# 2. (c, EPS_SYMBOL, DELETION_WEIGHT) - deletion
# 3. (EPS_SYMBOL, c, INSERTION_WEIGHT) - insertion
# We'll also create transitions between each pair of characters with weight SUBSTITUTION_WEIGHT.

transitions = []
for c1 in symbol_table:
    for c2 in symbol_table:
        if c1 == EPS_SYMBOL and c2 == EPS_SYMBOL:
            continue
        if c1 == EPS_SYMBOL:
            transitions.append((EPS_SYMBOL, c2, INSERTION_WEIGHT))
        elif c2 == EPS_SYMBOL:
            transitions.append((c1, EPS_SYMBOL, DELETION_WEIGHT))
        elif c1 == c2:
            transitions.append((c1, c2, 0))
        else:
            transitions.append((c1, c2, SUBSTITUTION_WEIGHT))

# Finally, we'll write the L-converter to the L.fst file in OpenFST text format.
# We'll use state 0 as the only state, and add transitions for each possible input symbol.

with open("./fsts/L.fst", "w") as f:
    f.write("0\n")
    for s in symbol_table:
        for t in transitions:
            f.write(f"0\t0\t{s}\t{t[1]}\t{t[2]}\n")
    f.write("0\n")

run_cmd("fstcompile --isymbols=./vocab/chars.syms --osymbols=./vocab/chars.syms ./fsts/L.fst >  ./fsts/L.binfst")
