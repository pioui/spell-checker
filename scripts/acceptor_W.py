import os
from numpy import log
import argparse
from util import EPS

"""
Calculate acceptor V
Acceptor, we create an .fst which corrects the word and an .fst that understands how often a word exists.
Usage:
  python3 scripts/acceptor_W.py -af W.fst -wvf words.vocab.txt -cf chars.syms -wf words.syms

"""

# Parse input arguments
parser = argparse.ArgumentParser(description="Acceptor fst")
parser.add_argument("-af", type=str, default="W.fst", help="Acceptor .fst filename")

parser.add_argument(
    "-wvf",
    type=str,
    default="./vocab/words.vocab.txt",
    help="Words vocabulary with frequencies",
)
parser.add_argument(
    "-cf", type=str, default="./vocab/chars.syms", help="Characters .syms filepath"
)
parser.add_argument(
    "-wf", type=str, default="./vocab/words.syms", help="Words .syms filepath"
)

args = parser.parse_args()

# Manage files and directories
fst_folder = "./fsts/"
if not os.path.exists(fst_folder):
    os.makedirs(fst_folder)

# Define input and output file paths
acceptor_file = fst_folder + args.af
chars_file = args.cf
words_file = args.wf
words_vocab_file = args.wvf

# Make sure the we don't continue writing in previous output files
if os.path.exists(acceptor_file):
    os.remove(acceptor_file)


# Read the words_file file and create a symbol table.
words_vocab = {}
total = 0
with open(words_vocab_file, "r") as f:
    for line in f:
        word, frequency = line.strip().split()
        words_vocab[word] = int(frequency)
        total = total + int(frequency)


# Next, we'll create a string for each possible transition in the letters of each word in the V-transducer.
# We'll represent each transition as a triple (node1, node 2, input symbol, output symbol, weight).
# For each word w in the words' table, we'll create the transision for each letter:
transitions = []
node_count = 0
first_node = 0
last_node = 92721  # TODO: calculate it more elegantly, not hard coded.

for word in words_vocab:
    if word == EPS:
        continue

    transitions.append((word, word, round(-log(words_vocab[word] / total))))

    # nodes = [*range(0,len(word),1)]
    # nodes = [node+node_count for node in nodes]
    # nodes[0]=first_node

    # word_length = len(word)
    # for i in range(word_length):

    #     if i == word_length-1:
    #         transitions.append((nodes[i], last_node, word[i], word, words_vocab[word]/total))
    #         continue

    #     # Last letter
    #     transitions.append((nodes[i], nodes[i+1], word[i], EPS, 0 ))
    #     node_count = node_count+1


# Finally, we'll write the L-transducer to the L.fst file in OpenFST text format.
# We'll use state 0 as the only state, and add transitions for each possible input symbol.
with open(acceptor_file, "w") as f:
    f.write(f"0 0 {EPS} {EPS} 0\n")
    for t in transitions:
        f.write(f"0 0 {t[0]} {t[1]} {t[2]}\n")
    f.write(f"0")
