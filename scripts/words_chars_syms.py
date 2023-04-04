from util import EPS
import os


# Define input and output file paths
vocab_file = "./vocab/words.vocab.txt"
words_file = "./vocab/words.syms"
chars_file = "./vocab/chars.syms"

# Make sure the we don't continue writing in previous output files
if os.path.exists(words_file):
    os.remove(words_file)
if os.path.exists(chars_file):
    os.remove(chars_file)


def create_char_map():
    char_map = {EPS: 0}
    for i in range(97, 123):
        char_map[chr(i)] = i - 96
    return char_map

char_map = create_char_map()
with open(chars_file, "w") as f:
    for char, index in char_map.items():
        f.write(f"{char}\t{index}\n")


# Create dictionary of word indices
word_indices = {}
with open(vocab_file, "r") as f:
    for line in f:
        word = line.strip().split()[0]
        word_indices[word] = len(word_indices) + 1  # start index from 1

# Write word indices to output file
with open(words_file, "w") as f:
    # Write epsilon symbol
    f.write(f"{EPS}\t0\n")
    # Write word indices
    for word, index in word_indices.items():
        f.write(f"{word}\t{index}\n")