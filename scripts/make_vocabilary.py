from collections import defaultdict

# Open the corpus file and read its contents
with open('./data/gutenberg.txt', 'r') as corpus_file:
    corpus = corpus_file.read()

# Create a defaultdict to store the token frequencies
freq_dict = defaultdict(int)

# Split the corpus into tokens 
# TODO: use nltk tokenizer
tokens = corpus.split()

# Count the frequency of each token
for token in tokens:
    freq_dict[token] += 1

# Create a list of tokens to exclude
exclude_list = [token for token in freq_dict.keys() if freq_dict[token] < 5]

# Remove the excluded tokens from the frequency dictionary
for token in exclude_list:
    del freq_dict[token]

# Open the output file and write the frequency dictionary to it
with open('vocab/words.vocab.txt', 'w') as output_file:
    for token, freq in freq_dict.items():
        output_file.write(f'{token}\t\t{freq}\n')