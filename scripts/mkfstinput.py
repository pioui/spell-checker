"""
USAGE:
    python mkfstinput.py MY_WORD > my_word.fst

OR:
    python mkfstinput.py MY_WORD | fstcompile | fstcompose - MY_SPELLCHECKER.fst | ...
"""

import sys

from util import EPS, format_arc

# def write_char_symbols():
#     with open("vocab/chars.syms", "w") as f:
#         # Write the epsilon symbol
#         f.write("0\t<eps>\n")
#         # Write the lowercase letters
#         for i in range(26):
#             c = chr(ord('a') + i)
#             f.write(f"{i+1}\t{c}\n")

            
def make_input_fst(word):
    """Create an fst that accepts a word letter by letter
    This can be composed with other FSTs, e.g. the spell
    checker to provide an "input" word

    """
    s, accept_state = 0, 10000

    for i, c in enumerate(word):
        # TODO: You need to implement format_arc function in scripts/util
        print(format_arc(s, s + 1, c, c, weight=0))
        s += 1

        if i == len(word) - 1:
            print(format_arc(s, accept_state, EPS, EPS, weight=0))
    
    print(accept_state)


if __name__ == "__main__":
    word = sys.argv[1]
    make_input_fst(word)
