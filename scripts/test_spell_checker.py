from helpers import run_cmd
# Define input file path
test_file = './data/spell_test.txt'

# Limit tests to the first 20 words
count = 0

# Create a dictionary of correct words and the wrong spelled words
word_table = {}
with open(test_file, "r") as f:
    for line in f:
        split_line = line.split()
        # First word is the corrrect one, the rest are the mispelled.
        word_table[split_line[0][:-1]] = split_line[1:]

        count = count +1
        if count == 20: break

# For every mispelled word run the spellchecker S.fst and print the prediction
for word in word_table.keys():
    print('-----------------------------------')
    print('{:20s} {:20s}'.format('Correct word:', word))
    print('{:20s} {:20s}'.format('Input word ', 'Prediction'))
    print('-----------------------------------')
    for wrong_word in word_table[word]:
        prediction = run_cmd(f'bash scripts/predict.sh ./fsts/S.fst {wrong_word}')
        # print(f' {wrong_word} --> {prediction}')
        print('{:20s} {:20s}'.format(wrong_word, prediction))
    print('-----------------------------------')
