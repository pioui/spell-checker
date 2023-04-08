# OpenFST Spell checker 

## Setup

Clone repository

```bash
git clone git@github.com:pioui/spell-checker.git
cd spell-checker
```

Create conda envirioment

```bash
conda create --name spell-checker python=3.6
conda activate spell-checker
```

To setup openfst in your machine run.

```bash
bash install_openfst.sh
```

Leave the `OPENFST_VERSION=1.6.1`, since next versions are not supported for this lab / contain breaking changes.

Install python dependencies with:

```bash
pip install -r requirements.txt
```

## If the setup is already done

```bash
cd repos/spell-checker
conda activate spell-checker
```

## Data 
Fetch the NLTK Gutenberg corpus and do the neccesery preproccessing in the data using the following script.

```bash
bash scripts/data_pipeline.sh
```
This script downloads and preprocesses the corpus, creates the vocabulary, the .syms files for the words and the characters and calculates the frequency of the word edits.

##

## Create Spell Checkers

```bash
bash scripts/spell_ckeckers_pipeline.sh
```
This scrips creates 4 spell-checkers: LV, EV, LVW, EVW. Which are different combinations of .fst automata L, E, V, E. Each of the automatum has a different functionality:

- L: it is an edit distance Lavenstein transducer.
- E: it is an weighted edit distance Lavenstein transducer. The weight of each edit is calculated by it's frequency.
- V: it is an simple vocabulary word acceptor.
- W: it is a more sophisticated vocabulary word acceptor which takes into considaration the frequency of each word in the corpus.

## Spell checker evaluation

Once we have implemented a spell checker, e.g. `fsts/MY_SPELL_CHECKER.binfst` you can use the
following script for evaluation on the provided test set.

Run:

```bash
python scripts/run_evaluation.py fsts/MY_SPELL_CHECKER.binfst
```

The script will run the spell checker on the test set and print the model accuracy (percentage
of misspelled words that are corrected appropriately).

### Results

| Spell-checker  | Accuracy  |
|--------------- |-----------|
|LV  |0.5962962962962963     | 
|EV  |0.6925925925925925     |
|LVW |0.02962962962962963    |
|EVW |0.6370370370370371     |

