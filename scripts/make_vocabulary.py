from collections import defaultdict
import matplotlib.pyplot as plt
import os


"""
Script to create and save the vocabulary
Usage:
  python3 scripts/make_vocabulary.py 

"""

# Manage files and directories
vocab_folder = "./vocab/"
if not os.path.exists(vocab_folder):
    os.makedirs(vocab_folder)

# Define input and output file paths
words_vocab_file = "vocab/words.vocab.txt"

# Make sure the we don't continue writing in previous output files
if os.path.exists(words_vocab_file):
    os.remove(words_vocab_file)

# Open the corpus file and read its contents
with open("./data/gutenberg.txt", "r") as corpus_file:
    corpus = corpus_file.read()

# Create a defaultdict to store the token frequencies
words_vocab = defaultdict(int)

# Split the corpus into tokens
# TODO: use nltk tokenizer
tokens = corpus.split()

# Count the frequency of each token
for token in tokens:
    words_vocab[token] += 1

# Create a list of tokens to exclude
exclude_list = [token for token in words_vocab.keys() if words_vocab[token] < 5]

# Remove the excluded tokens from the frequency dictionary
for token in exclude_list:
    del words_vocab[token]

# Open the output file and write the frequency dictionary to it
with open(words_vocab_file, "w") as output_file:
    for token, freq in words_vocab.items():
        output_file.write(f"{token}\t{freq}\n")


sorted_freq = sorted(words_vocab.items(), key=lambda x: x[1], reverse=True)

# create a list of word frequencies and labels for plotting
labels = [pair[0] for pair in sorted_freq]
freqs = [pair[1] for pair in sorted_freq]

# plot the histogram
plt.bar(labels[:100], freqs[:100])
plt.xticks(rotation=90)
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.show()
