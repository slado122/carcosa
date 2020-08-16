import os
import sys
import datetime
import time
import itertools
import argparse
from random import randint, choice
import concurrent.futures

global name, __author__,  __version__
name = 'carcosa.py'
__author__ = 'slado122'
__version__ = '0.1'
__status__ = 'Development'

# Constants
separators = ('.', '_', '-', '123', '$', '%', '&', '#', '@')
leet_alphabet = {'a': '4', 'i': '1', 'e': '3', 's': '5', 'b': '8', 'o': '0'}
THREADS_NUM = 4


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


# ---- Args definition ----

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


parser.add_argument('-o', '--output', action="store", metavar='', type=str,
                    dest='outfile', default='tmp.txt',
                    help='output file to save the wordlist (default: tmp.txt)')

parser.add_argument('--prefix', action="store", metavar='', type=str,
                    dest='prefix', default='', help='add prefix')

parser.add_argument('--postfix', action="store", metavar='', type=str,
                    dest='postfix', default='', help='add postfix')

parser.add_argument('--title', action="store_true", help='add title version of each word')
parser.add_argument('--upper', action="store_true", help='add upper-case version of each word')

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


def chunk(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def run_in_multiprocessing(func, wordlist, *args):
    results = list()
    with concurrent.futures.ProcessPoolExecutor(max_workers=THREADS_NUM) as executor:
        futures = list()
        for c in chunk(wordlist, THREADS_NUM):
            futures.append(
                executor.submit(func, c, *args)
            )

        for f in futures:
            results.extend(f.result())

    return results


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
    new_wordlist = []
    combinations = itertools.permutations(wordlist, 2)

    for c in combinations:
        for s in separators:
            new_wordlist.append(s.join(c))
            new_wordlist.append(s + ''.join(c))
            new_wordlist.append(''.join(c) + s)

            # print(len(new_wordlist))

    for s in separators:
        for w in wordlist:
            new_wordlist.append(w + s)
            new_wordlist.append(s + w)

    return new_wordlist


#** Combinator **#
def combinator(wordlist, nWords):
    combinations = list()

    for n in range(2, nWords+1):
        combinations.extend(
            list(map(
                lambda combination: ''.join(combination),
                itertools.permutations(wordlist, n)
            ))
        )

    return list(set(combinations))


# ** Remove word if its length is out of range **#
def remove_by_lengths(wordlist, minLength, maxLength):
    return list(filter(
        lambda word: len(word) in range(minLength, maxLength+1),
        wordlist
    ))


#** Transfroming spaces inside the word and returning all the variations **#
def space_transforms(word):
    word_variations = []
    word_variations.append(word.replace(' ', ''))
    word_variations.append(word.replace(' ', '.'))
    word_variations.append(word.replace(' ', '_'))
    word_variations.append(word.replace(' ', '-'))
    return list(set(word_variations))


#** Case transformation **#
def case_transforms(wordlist):
    case_transformed = list()
    for word in wordlist:
        # Make each one upper (hello => Hello, hEllo, heLlo, helLo, hellO)
        i = 0
        for char in word:
            new_word = word[:i] + char.upper() + word[i+1:]
            i += 1
            case_transformed.append(new_word)

        # Make pairs and odds upper (hello => HeLlO)
        i = 0
        pairs_upper = ''
        for char in word:
            if i % 2 == 0:
                pairs_upper += char.upper()
            else:
                pairs_upper += char
            i += 1
        odds_upper = pairs_upper.swapcase()
        case_transformed.append(pairs_upper)
        case_transformed.append(odds_upper)

        # Make consonants and vowels upper (hello => HeLLo)
        vowels = 'aeiou'
        consonants_upper = ''
        for char in word:
            if char not in vowels:
                consonants_upper += char.upper()
            else:
                consonants_upper += char

        vowels_upper = consonants_upper.swapcase()

        case_transformed.append(vowels_upper)
        case_transformed.append(consonants_upper)

    return list(set(case_transformed))


#** Leet transformation **#
def leet_transforms(wordlist):
    leet_transformed = list()

    for word in wordlist:
        i = 0
        for char in word:
            if char.lower() in leet_alphabet.keys():
                word = word[:i] + leet_alphabet[char.lower()] + word[i + 1:]
                leet_transformed.append(word)
            i += 1

    return leet_transformed


#** Title transformation **#
def title_transform(wordlist):
    return list(map(
        lambda word: word.title,
        wordlist,
    ))


#** Upper transformation **#
def upper_transform(wordlist):
    return list(map(
        lambda word: word.title,
        wordlist,
    ))


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
    title = input(u'  {}[?]{} Do you want to make title transform? [y/n] >>> '.format(color.BLUE, color.END))
    upper = input(u'  {}[?]{} Do you want to make upper transform? [y/n] >>> '.format(color.BLUE, color.END))
    prefix = input(u'  {}[?]{} Enter a prefix if you want to >>> '.format(color.BLUE, color.END))
    postfix = input(u'  {}[?]{} Enter a postfix if you want to >>> '.format(color.BLUE, color.END))

    if leet.lower() == 'y': leet = True
    else: leet = False

    if case.lower() == 'y': case = True
    else: case = False

    if title.lower() == 'y': title = True
    else: title = False

    if upper.lower() == 'y': upper = True
    else: upper = False

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
            wordlist.append(i)

    return wordlist, minLength, maxLength, leet, case, title, upper, prefix, postfix, nWords, outfile


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
        base_wordlist, minLength, maxLength, leet, case, title, upper, prefix, postfix, nWords, outfile = asks()

    else:
        base_wordlist = []
        if args.words:
            raw_wordlist = args.words.split(',')
            for word in raw_wordlist:
                base_wordlist.append(word)
        minLength = args.min
        maxLength = args.max
        case = args.case
        leet = args.leet
        title = args.title
        upper = args.upper
        nWords = args.nWords
        outfile = args.outfile
        prefix = args.prefix
        postfix = args.postfix


    # Initial timestamp
    start_time = time.time()

    wordlist = base_wordlist[:]  # copying

    # Title transform
    startT = time.time()
    if title:
        wordlist += title_transform(wordlist)
    totalT = round(time.time() - startT, 2)
    print(f'\n{totalT}s for title transform')

    startT = time.time()
    wordlist = list(set(wordlist))
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for checking for duplicates')

    # Upper transform
    startT = time.time()
    if upper:
        wordlist += upper_transform(wordlist)
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for upper transform')

    startT = time.time()
    wordlist = list(set(wordlist))
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for checking for duplicates')

    # Case transforms
    startT = time.time()
    if case:
        wordlist += case_transforms(wordlist)
    totalT = round(time.time() - startT, 2)
    print(f'\n{totalT}s for case transforms')

    startT = time.time()
    wordlist = list(set(wordlist))
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for checking for duplicates')

    # Leet transforms
    startT = time.time()
    if leet:
        wordlist += leet_transforms(wordlist)
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for leet transforms')

    startT = time.time()
    wordlist = list(set(wordlist))
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for checking for duplicates')

    startT = time.time()
    # Word combinations
    wordlist = combinator(wordlist, nWords)
    # wordlist = run_in_multiprocessing(
    #     combinator,
    #     wordlist, nWords
    # )
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for combinator')

    # Word combinations with common separators
    startT = time.time()
    wordlist += add_common_separators(base_wordlist)
    # Check for duplicates
    wordlist = list(set(wordlist))
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for adding separators')

    # Remove words which doesn't match the min-max range established
    startT = time.time()
    wordlist = remove_by_lengths(wordlist, minLength, maxLength)
    # wordlist = run_in_multiprocessing(
    #     remove_by_lengths,
    #     wordlist, minLength, maxLength
    # )
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for remove_by_lengths')

    # Case transforms
    startT = time.time()
    if case:
        wordlist += case_transforms(wordlist)
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for case transforms')

    startT = time.time()
    wordlist = list(set(wordlist))
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for checking for duplicates')

    # Leet transforms
    startT = time.time()
    if leet:
        wordlist += leet_transforms(wordlist)
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for leet transforms')

    startT = time.time()
    wordlist = list(set(wordlist))
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for checking for duplicates')

    # Adding prefix and postfix
    startT = time.time()
    if prefix or postfix:
        wordlist = list(map(
            lambda word: prefix + word + postfix,
            wordlist
        ))
    totalT = round(time.time() - startT, 2)
    print(f'{totalT}s for adding prefix and postfix')

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

