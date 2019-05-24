The Python scripts in this folder are intended for single word segmentation of words in Wordnet.

Some points to note:
- they have been tailored to integrate with NLTK, using this package to look up words
- as an initial goal, they assume that words have one each of prefix, root/stem, suffix

Other options may be available in the future.

If you don't already have Python 3 installed, download it from https://www.python.org/downloads/

If you don't already have the NLTK package installed, you may find Anaconda a useful resource - see https://anaconda.org/anaconda/nltk

Python test script test_word.py has been provided to enable testing - one word at a time. (This script has not been written using formal unit test methodologies - please feel free to suggest same).

Generally, the script performs the following:
* try up to 4 strategies for search only in the dataset (morphemes.json)
  * "suffix", "root", "prefix"
  * "suffix", "prefix", "root"
  * "prefix", "root", "suffix"
  * "prefix", "suffix", "root"
* if there is one unmatched character remaining, try consonant doubling where it applies
  * first combining root/stem with suffix (if both exist)
  * then prefix with suffix (assumes no root/stem)
* if any unmatched characters remaining, try:
  * search Wordnet, using characters remaining after removing the suffix
  * search Wordnet, using characters remaining after removing the suffix and prefix
  * search Wordnet, using characters remaining after removing the prefix
* success is assumed if there are no unmatched characters remaining

To test a word, run the following on the command-line:

$ python test_word.py some-word
 - where "some-word" is the word to be tested in this example
 - substitute your own choice of word to be tested

For example:
- For the word "aberrant":
 - $ python test_word.py aberrant
- the result would be:
```
{
  'matched_char_count': 8,
  'prefix': {'form': 'ab', 'meaning': ['away from']},
  'root': {'form': 'err', 'meaning': ['stray']},
  'segments': 'ab+err+ant',
  'suffix': {'form': 'ant', 'meaning': ['inclined to', 'tending to']},
  'unmatched_char_count': 0,
  'word': 'aberrant'
}
```

Note: An initial test successfully segmented 88% of Wordnet adjectives. The real test is: how many of the results yielded appropriate meanings - the objective of this repository in the first place. Any comments on the validity or otherwise of any results you may get will be appreciated.
