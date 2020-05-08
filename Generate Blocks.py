
import random
import Crossword

"""
with open('all words.json', 'rt') as fin:
    data = fin.read()

import json
data = json.loads(data)

max_len = 0
for key, pair in data.items():
    for element in pair:
        if len(element) > max_len:
            max_len = len(element)
"""


rows, cols = (20, 20)
area = [[' ' for i in range(cols)] for j in range(rows)]
"""
def draw_across_word(down_word, across_word, down_x, down_y):
    down_offset = 0
    for down_char in down_word:
        down_offset = down_offset + 1
        for across_char in across_word:
            if across_char == down_char:

                increasing_counter = 0
                for counter in range(across_word.index(across_char),
                                     across_word.index(across_char) - len(across_word),
                                     -1):
                    if area[down_y + down_offset - 1][down_x - counter] != ' ' and \
                       area[down_y + down_offset - 1][down_x - counter] != down_char:
                        return False
                    increasing_counter = increasing_counter + 1
                    for row in area:
                        print(row)
                    print('')

                increasing_counter = 0
                for counter in range(across_word.index(across_char),
                                     across_word.index(across_char) - len(across_word),
                                     -1):
                    area[down_y + down_offset - 1][down_x - counter] = \
                        across_word[increasing_counter]
                    increasing_counter = increasing_counter + 1
                    for row in area:
                        print(row)
                    print('')
                return True
"""

def try_across_placement(x, y, word):
    """Tests placing a word horizontally and assigns it a score
    depending on how many vertical words it overlaps

    a score of -1 signifies its not a suitable location, and will never be
    the max score"""
    test_x = x
    test_y = y
    score = 0
    try:
        for iteration in range(len(word)):
            # make sure each character is placable there
            if area[test_y][test_x] != ' ' and area[test_y][test_x] != word[iteration]:
                return {-1: [x, y]}
            # make sure the character before and after the word are blank
            if area[y][x - 1] != ' ' or area[y][x + len(word)] != ' ':
                return {-1: [x, y]}
            # this location gets +1 score for every word it overlaps
            if area[test_y][test_x] == word[iteration]:
                score = score + 1
            test_x = test_x + 1
        return {score: [x, y]}
    except IndexError:
        return {-1: [x, y]}


category, all_words = '', []
down = ['temp']
down_saved = ['temp']
across = []
across_saved = []

# convert to uppercase
down = [down_upper.upper() for down_upper in down]
across = [across_upper.upper() for across_upper in across]

while len(across_saved) < len(down_saved):
    category, all_words = Crossword.get_all_words()
    down = all_words[0:5]
    down_saved = down.copy()  # TEMPORARY
    across = all_words[5:]
    across_saved = []  # TEMPORARY

    # convert to uppercase
    down = [down_upper.upper() for down_upper in down]
    across = [across_upper.upper() for across_upper in across]


    # draw horizontal words
    while len(down) > 0:
        word = down.pop(0)

        try_again = True
        while try_again:
            try:
                rand_x = random.randint(0, cols)
                rand_y = random.randint(0, rows)

                for counter in range(len(word)):
                    # make sure the entire line where you're going to place
                    # the word is empty
                    if area[rand_y + counter][rand_x] != ' ':
                        raise IndexError
                    # make sure the left and right spaces are empty
                    if area[rand_y + counter][rand_x - 1] != ' ' or\
                       area[rand_y + counter][rand_x + 1] != ' ':
                        raise IndexError
                # make sure the above and below spaces are empty
                if area[rand_y - 1][rand_x] != ' ' or \
                   area[rand_y + len(word)][rand_x] != ' ':
                    raise IndexError
                for counter in range(len(word)):
                    area[rand_y + counter][rand_x] = word[counter]
                # word successfully created vertically
                try_again = False

            except IndexError:
                try_again = True


    for across_word in across:
        x = 0
        y = 0
        max_score = {-1: [0, 0]}
        for row in area:
            for placed_char in row:
                if placed_char != ' ':
                    for word_char in across_word:
                        new_score = {-1: [0, 0]}
                        if placed_char == word_char:
                            new_score = try_across_placement(
                                        x - across_word.index(word_char),
                                        y,
                                        across_word
                                        )
                        if list(max_score.keys())[0] < list(new_score.keys())[0]:
                            # make sure the X and Y values are positive
                            # (sometimes the computer will want to
                            # put a word outside of the borders)
                            if list(new_score.values())[0][0] >= 0 and \
                               list(new_score.values())[0][1] >= 0:
                                max_score = new_score
                x = x + 1
            y = y + 1
            x = 0

        # make sure there IS a place for the word
        # only use words that are above a 1 score (temporary)
        if list(max_score.keys())[0] > 1:
            # get the x and y starting pos of the word
            start_x = list(max_score.values())[0][0]
            start_y = list(max_score.values())[0][1]
            # put the word down character by character
            for char in across_word:
                area[start_y][start_x] = char
                start_x = start_x + 1

            across_saved.append(across_word)                        # TEMPORARY ?


for row in area:
    for col in row:
        print(' {0:<1s} '.format(col), end='')
    print(' ')
print(' ')

# TEMPORARY
print('Category:', category)
print('\n\tDown:', end='\n\n')
for counter in range(0, 5):
    word = down_saved[counter]
    clue = Crossword.get_clue(word)
    print('\t\t{0:<2}. {1}'.format(counter+1, clue), end='\n')

print('\n\tAcross:', end='\n\n')
for counter in range(0, len(across_saved)):
    word = across_saved[counter]
    clue = Crossword.get_clue(word)
    print('\t\t{0:<2}. {1}'.format(counter+1, clue), end='\n')

input('')

