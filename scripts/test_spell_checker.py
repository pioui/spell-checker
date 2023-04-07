from helpers import run_cmd
import argparse

# Parse input arguments
parser = argparse.ArgumentParser(description="Transducer fst")
parser.add_argument(
    "-tf", type=str, default="./data/spell_test.txt", help="Test file .txt"
)
parser.add_argument(
    "-scf",
    type=str,
    default="./fsts/S.fst",
    help="Spell checker .fst file to be tested",
)


args = parser.parse_args()

# Define input file path
test_file = args.tf
spell_checker_fst = args.scf

# Limit tests to the first 20 words
count = 0

# Create a dictionary of correct words and the wrong spelled words
word_table = {}
with open(test_file, "r") as f:
    for line in f:
        split_line = line.split()
        # First word is the corrrect one, the rest are the mispelled.
        word_table[split_line[0][:-1]] = split_line[1:]

        count = count + 1
        if count == 20:
            break

# For every mispelled word run the spellchecker S.fst and print the prediction
for word in word_table.keys():
    print("{:20s} {:20s}".format("Correct word:", word))
    for wrong_word in word_table[word]:
        prediction = run_cmd(
            f"bash scripts/predict.sh {spell_checker_fst} {wrong_word}"
        )
        print("{:20s} --> {:20s}".format(wrong_word, prediction))
    print("-----------------------------------")
