import os
import sys
import datetime
import time
import itertools
import argparse
from random import randint, choice
from collections import OrderedDict
from multiprocessing.dummy import Pool as ThreadPool

global name, __author__,  __version__
name = 'carcosa.py'
__author__ = 'slado122'
__version__ = '0.1'
__status__ = 'Development'

# Constants
separators = ('.', '_', '-', )#'123', '$', '%', '&', '#', '@')
leet_alphabet = {'a': '4', 'i': '1', 'e': '3', 's': '5', 'b': '8', 'o': '0'}

#** Class Color **#
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\033[33m'
    END = '\033[0m'

    RAND_KEY_COLOR = [PURPLE, CYAN, DARKCYAN, YELLOW, ORANGE]
    KEY_HIGHL = choice(RAND_KEY_COLOR)


#** Args definition **#

parser = argparse.ArgumentParser(description='Generates smart and powerful wordlists.')

parser.add_argument('-i', '--interactive', action="store_true",
                    help='interactive mode, the script will ask you about target')

parser.add_argument('-w', action="store", metavar='', type=str, dest='words',
                    help='words to combine comma-separated (non-interactive mode)')

parser.add_argument('--min', action="store", metavar='', type=int, dest='min',
                    default=4, help='min length for the words to generate '
                                    '(default: 4)')
parser.add_argument('--max', action="store", metavar='', type=int, dest='max',
                    default=32, help='max length for the words to generate '
                                     '(default: 32)')

parser.add_argument('-c', '--case', action="store_true", help='enable case transformations')
parser.add_argument('-l', '--leet', action="store_true", help='enable leet transformations')

parser.add_argument('-n', action="store", metavar='', type=int, dest='nWords',
                    default=2, help='max amount of words to combine each time '
                                    '(default: 2)')

parser.add_argument('-x', '--exclude', action="store", metavar='', type=str,
                    dest='exclude', default=False,
                    help='exclude all the words included in other wordlists '
                         '(several wordlists should be comma-separated)')

parser.add_argument('-o', '--output', action="store", metavar='', type=str,
                    dest='outfile', default='tmp.txt',
                    help='output file to save the wordlist (default: tmp.txt)')


#** Banner function **#
def banner():
    name_rand_leet = leet_transforms(name)
    name_rand_leet = name_rand_leet[randint(0, (len(name_rand_leet) - 1))]
    name_rand_case = case_transforms(name)
    name_rand_case = name_rand_case[randint((len(name_rand_case) - 3), (len(name_rand_case) - 1))]

    print(u'\n  ,----------------------------------------------------,  ,------------,')
    print(u'  | [][][][][]  [][][][][]  [][][][]  [][__]  [][][][] |  |    v{}{}{}    |'.format(color.BLUE, __version__, color.END))
    print(u'  |                                                    |  |------------|')
    print(u'  |  [][][][][][][][][][][][][][_]    [][][]  [][][][] |  | {}{}{} |'.format(color.RED, name_rand_leet, color.END))
    print(u'  |  [_][][][]{}[]{}[][][][]{}[][]{}[][][ |   [][][]  [][][][] |  | {}{}{}{} |'.format(color.KEY_HIGHL, color.END, color.KEY_HIGHL, color.END, color.BOLD, color.RED, name, color.END))
    print(u'  | [][_][]{}[]{}[][][][][]{}[]{}[][][][]||     []    [][][][] |  | {}{}{} |'.format(color.KEY_HIGHL, color.END, color.KEY_HIGHL, color.END, color.RED, name_rand_case, color.END))
    print(u'  | [__][][][]{}[]{}[]{}[]{}[][][][][][__]    [][][]  [][][]|| |  |------------|'.format(color.KEY_HIGHL, color.END, color.KEY_HIGHL, color.END))
    print(u'  |   [__][________________][__]              [__][]|| |  |{}  {}  {}|'.format(color.GREEN, __author__, color.END))
    print(u'  `----------------------------------------------------´  `------------´\n')


#** Clear function for terminal/cmd **#
def clear():
    """Clear the screen. Works on Windows and Linux."""
    os.system(['clear', 'cls'][os.name == 'nt'])


#** Check if the variable is empty **#
def is_empty(variable):
    """
    Check if a variable is empty.
    :param date_str: var to check
    :return: True or False
    """
    return not variable


#** Check if the date is valid **#
def is_valid_date(date_str):
    """
    Check if a string corresponds to a valid date.
    :param date_str: date to check
    :return: True or False
    """
    try:
        datetime.datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False


#** Add all the common separators to a wordlist **#
def add_common_separators(wordlist):
    """
    Take a wordlist and generate all possible combinations between the words
    contained and another wordlist which contains common separator (e.g. _ ).

    :param wordlist: the base wordlist to combine
    :return: a new wordlist with all the combinations
    """
    words = wordlist[:]
    new_wordlist = []
    combinations = itertools.permutations(words, 2)

    for c in combinations:
        for s in separators:
            new_wordlist.append(f'{s}'.join(c))
            new_wordlist.append(s + ''.join(c))
            new_wordlist.append(''.join(c) + s)

    for s in separators:
        for w in words:
            new_wordlist.append(w + s)
            new_wordlist.append(s + w)

    return new_wordlist



#** Combinator **#
def combinator(wordlist, nWords):
    new_wordlist = wordlist[:]  # I need copy to use itertools properly
    wlist_combined = itertools.permutations(new_wordlist, nWords)
    for combination in wlist_combined:
        new_wordlist.append(''.join(combination))

    return list(set(new_wordlist))


#** Remove word if its length is out of range **#
def remove_by_lengths(wordlist, minLength, maxLength):
    for word in wordlist:
        if (len(word) < minLength) or (len(word) > maxLength): wordlist.remove(word)
    return wordlist


#** Work with threads **#
def thread_transforms(transform_type, wordlist):
    pool = ThreadPool(16)
    # process each word in their own thread and return the results
    new_wordlist = pool.map(transform_type, wordlist)
    pool.close()
    pool.join()
    for lists in new_wordlist:
        wordlist += lists
    #return new_wordlist


#** Transfroming spaces inside the word and returning all the variations **#
def space_transforms(word):
    new_wordlist = []
    new_wordlist.append(word.replace(' ', ''))
    new_wordlist.append(word.replace(' ', '.'))
    new_wordlist.append(word.replace(' ', '_'))
    new_wordlist.append(word.replace(' ', '-'))
    return new_wordlist


#** Needed for map **#
def exclude(word):
    if word not in words_to_exclude:
        #return word
        yield word


#** Case transformation **#
def case_transforms(word):
    new_wordlist = []

    # Make each one upper (hello => Hello, hEllo, heLlo, helLo, hellO)
    i = 0
    for char in word:
        new_word = word[:i] + char.upper() + word[i+1:]
        i += 1
        new_wordlist.append(new_word)

    # Make pairs and odds upper (hello => HeLlO)
    i = 0
    pairs_upper = ''
    for char in word:
        if i % 2 == 0: pairs_upper += char.upper()
        else: pairs_upper += char
        i += 1
    odds_upper = pairs_upper.swapcase()
    new_wordlist.append(pairs_upper)
    new_wordlist.append(odds_upper)

    # Make consonants and vowels upper (hello => HeLLo)
    vowels = 'aeiou'
    consonants_upper = ''
    for char in word:
        if char not in vowels: consonants_upper += char.upper()
        else: consonants_upper += char
    vowels_upper = consonants_upper.swapcase()
    if consonants_upper not in new_wordlist: new_wordlist.append(consonants_upper)
    if vowels_upper not in new_wordlist: new_wordlist.append(vowels_upper)

    return list(set(new_wordlist))


#** Leet transformation **#
def leet_transforms(word):
    new_wordlist = []

    i = 0
    for char in word:
        if char.lower() in leet_alphabet.keys():
            word = word[:i] + leet_alphabet[char.lower()] + word[i + 1:]
            new_wordlist.append(word)
        i += 1

    return new_wordlist


#** Asking the config (only in interactive mode) **#
def asks():
    while True:
        minLength = input(u'  {}[?]{} Password\'s min length [1] >>> '.format(color.BLUE, color.END))
        if is_empty(minLength):
            minLength = 1
            break
        else:
            try:
                minLength = int(minLength)
                break
            except ValueError:
                print(u'  {}[!]{} Min length should be an integer'.format(color.RED, color.END))
    while True:
        maxLength = input(u'  {}[?]{} Password\'s max length [99] >>> '.format(color.BLUE, color.END))
        if is_empty(maxLength):
            maxLength = 99
            break
        else:
            try:
                maxLength = int(maxLength)
                if maxLength < minLength: print(u'  {}[!]{} Max should be greater or equal than min'.format(color.RED, color.END))
                else: break
            except ValueError:
                print(u'  {}[!]{} Max length should be an integer'.format(color.RED, color.END))

    firstname = input(u'  {}[?]{} First name >>> '.format(color.BLUE, color.END))
    surname = input(u'  {}[?]{} Surname >>> '.format(color.BLUE, color.END))
    lastname = input(u'  {}[?]{} Last name >>> '.format(color.BLUE, color.END))

    while True:
        birth = input(u'  {}[?]{} Birth date (DD/MM/YYYY) >>> '.format(color.BLUE, color.END))
        if not is_empty(birth) and not is_valid_date(birth):
            print(u'  {}[!]{} Birthdate wrong format'.format(color.RED, color.END))
        else:
            break

    others = input(u'  {}[?]{} Some other relevant words (comma-separated) >>> '.format(color.BLUE, color.END))

    leet = input(u'  {}[?]{} Do you want to make leet transforms? [y/n] >>> '.format(color.BLUE, color.END))
    case = input(u'  {}[?]{} Do you want to make case transforms? [y/n] >>> '.format(color.BLUE, color.END))

    if leet.lower() == 'y': leet = True
    else: leet = False

    if case.lower() == 'y': case = True
    else: case = False

    while True:
        nWords = input(u'  {}[?]{} How much words do you want to combine at most [2] >>> '.format(color.BLUE, color.END))
        if is_empty(nWords):
            nWords = 2
            break
        else:
            try:
                nWords = int(nWords)
                if nWords < 1:
                    print(u'  {}[!]{} Should be greater or equal than 1'.format(color.RED, color.END))
                else:
                    break
            except ValueError:
                print(u'  {}[!]{} Should be an integer'.format(color.RED, color.END))

    while True:
        exclude = input(u'  {}[?]{} Exclude words from other wordlists? >>> '.format(color.BLUE, color.END))
        if is_empty(exclude):
            exclude = False
            break
        else:
            exclude = exclude.split(',')
            valid_paths = True
            for wl_path in exclude:
                if not os.path.isfile(wl_path):
                    valid_paths = False
                    print(u'  {}[!]{} {} not found'.format(color.RED, color.END, wl_path))

            if valid_paths:
                break

    outfile = input(u'  {}[?]{} Output file [tmp.txt] >>> '.format(color.BLUE, color.END))
    if is_empty(outfile): outfile = u'tmp.txt'

    wordlist = []

    if not is_empty(firstname):
        firstname = firstname.lower()
        wordlist.append(firstname)
    if not is_empty(surname):
        surname = surname.lower()
        wordlist.append(surname)
    if not is_empty(lastname):
        lastname = lastname.lower()
        wordlist.append(lastname)
    if not is_empty(birth):
        birth = birth.split('/')
        for i in birth:
            wordlist.append(i)
        wordlist.append((birth[2])[-2:])  # Also add two last digits of the year
    if not is_empty(others):
        others = others.split(',')
        for i in others:
            wordlist.append(i.lower())

    return wordlist, minLength, maxLength, leet, case, nWords, exclude, outfile


#** Main **#
def main():
    args = parser.parse_args()
    interactive = args.interactive
    if len(sys.argv) == 1: # Print help and exit when runs without args
        parser.print_help(sys.stdout)
        sys.exit(2)  


    # Settings
    if interactive:
        clear()
        banner()
        base_wordlist, minLength, maxLength, leet, case, nWords, exclude_wordlists, outfile = asks()

    else:
        base_wordlist = []
        if args.words:
            raw_wordlist = (args.words).split(',')
            for word in raw_wordlist:
                base_wordlist.append(word.lower())
        minLength = args.min
        maxLength = args.max
        case = args.case
        leet = args.leet
        nWords = args.nWords
        outfile = args.outfile

        exclude_wordlists = args.exclude
        if exclude_wordlists:
            exclude_wordlists = exclude_wordlists.split(',')
            for wl_path in exclude_wordlists:
                if not os.path.isfile(wl_path):
                    print(u'  {}[!]{} {} not found'.format(color.RED, color.END, wl_path))
                    sys.exit(4)


    # Initial timestamp
    start_time = time.time()

    wordlist = base_wordlist[:] # Copy to preserve the original

    # Word combinations
    if nWords > 1:
        wordlist = combinator(base_wordlist, 2)
        i = 2
        while i < nWords:
            i += 1
            wordlist += combinator(base_wordlist, i)

    # Word combinations with common separators
    wordlist += add_common_separators(base_wordlist)
    # Check for duplicates
    wordlist = list(OrderedDict.fromkeys(wordlist))
    # Remove words which doesn't match the min-max range established
    wordlist = remove_by_lengths(wordlist, minLength, maxLength)

    # Case transforms
    startT = time.time()
    if case:
        thread_transforms(case_transforms, wordlist)
    totalT = round(time.time() - startT, 2)
    print(f'\n{totalT}s for case transforms')

    startT = time.time()
    wordlist = list(set(wordlist))
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for checking for duplicates')

    # Leet transforms
    startT = time.time()
    if leet:
        thread_transforms(leet_transforms, wordlist)
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for leet transforms')

    startT = time.time()
    wordlist = list(set(wordlist))
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for checking for duplicates')


    # Exclude from other wordlists
    startT = time.time()
    if exclude_wordlists:
        global words_to_exclude
        words_to_exclude = []

        for wl_path in exclude_wordlists:
            with open(wl_path, 'r') as wlist_file:
                wl = wlist_file.read()
            wl = wl.split('\n')
            words_to_exclude += wl

        pool = ThreadPool(16)
        final_wordlist = pool.map(exclude, wordlist)
        pool.close()
        pool.join()

        wordlist = [word for word in final_wordlist if word is not None]
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for excluding from other wordlists')

    # Check for duplicates
    if exclude_wordlists:
        startT = time.time()
        wordlist = list(set(wordlist))
        totalT = round(time.time() - startT, 2)
        print(f'{totalT}s for checking for duplicates')

    startT = time.time()
    # Saving data to a file
    with open(outfile, 'w') as f:
        for word in wordlist:
            f.write(word + '\n')
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for saving data to a file')

    # Final timestamp
    end_time = time.time()
    total_time = round(end_time - start_time, 2)

    # Printing the results
    print(u'\n  {}[+]{} Time elapsed:\t{}s'.format(color.GREEN, color.END, total_time))
    print(u'  {}[+]{} Output file:\t{}{}{}{}'.format(color.GREEN, color.END, color.BOLD, color.BLUE, outfile, color.END))
    print(u'  {}[+]{} Words generated:\t{}{}{}\n'.format(color.GREEN, color.END, color.RED, len(wordlist), color.END))
    sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(u'\n\n  {}[!]{} Exiting...\n'.format(color.RED, color.END))
        sys.exit(3)

