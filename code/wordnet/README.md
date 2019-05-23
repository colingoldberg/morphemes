The code files in this folder (specifically morphemes_wn.py) have been tailored to integrate with NLTK, using this package to look up words.

Other options may be available in the future.

If you don't already have Python 3 installed, download it from https://www.python.org/downloads/

If you don't already have the NLTK package installed, you may find Anaconda a useful resource - see https://anaconda.org/anaconda/nltk

Python test script test_word.py has been provided to enable testing - one word at a time. (This script has not been written using formal unit test methodologies - please feel free to suggest same).

To test a word, run the following on the command-line:

$ python test_word.py some-word
 - where "some-word" is the word to be tested in this example
 - substitute your own choice of word to be tested

For example:
- For the word "aberrant":
- the result would be:
{'matched_char_count': 8,
 'prefix': {'form': 'ab', 'meaning': ['away from']},
 'root': {'form': 'err', 'meaning': ['stray']},
 'segments': 'ab+err+ant',
 'suffix': {'form': 'ant', 'meaning': ['inclined to', 'tending to']},
 'unmatched_char_count': 0,
 'word': 'aberrant'
}
