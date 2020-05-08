
import wikipedia
import re
import json
import random


def get_all_words():
    with open('all words.json', 'rt') as fin:
        data = fin.read()

    data = json.loads(data)

    all_categories = list(data.keys())
    category = random.choice(all_categories)
    word = ''

    for key, pair in data.items():
        if key == category:
            all_words = pair

    random.shuffle(all_words)

    return category, all_words

all_words, category = get_all_words()


def get_category():
    return category


def get_clue(word):
    try:
        # get the correct line on wikipedia
        main_text = wikipedia.summary(word, sentences=1)
        # remove instances of key word
        main_text = re.sub(word, '_______', main_text, flags=re.IGNORECASE)
        # if key word is "jumping" remove instances of "jump"
        if word[-3:] == 'ing':
            remove_chars = 3
            if word[-4] == word[-5]:
                remove_chars = 4
            main_text = re.sub(word[0:-remove_chars], '_______', main_text,
                               flags=re.IGNORECASE)
        # if key word is "photography" remove instances of "photograph"
        if word[-1:] == 'y':
            main_text = re.sub(word[0:-1], '_______', main_text,
                               flags=re.IGNORECASE)
        # if there are spaces, remove each word ex. Home Depot remove Home and
        # Depot
        if len(word.split(' ')) > 1:
            for part in word.split(' '):
                if part in main_text:
                    main_text = re.sub(part, '_______', main_text,
                                       flags=re.IGNORECASE)
        # remove parenthesis
        main_text = re.sub('\([^)]*\)', '', main_text,
                           flags=re.IGNORECASE)
        # (sometimes there's still some left behind)
        main_text = main_text.replace('(', '')
        main_text = main_text.replace(')', '')

        return main_text
    except:
        print('ERROR ON WORD', word)
