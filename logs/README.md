Log Files:

To back up the 88% result referred to in the code README, the following file shows the results of an iterative process on Wordnet adjectives.

- wordnet_adjectives_05232019.log

The summary in this file (at the end) shows:
- zero_unmatched_count:  16172 = 88%
- nonzero_unmatched_count:  2108
- total_count:  18280

where "zero_unmatched_count" is the total of lines ending with 0

eg. as per snippet below:
```
...
abbreviated ab+brev+iated 0
abdicable ab+dic+able 0
abdominal ab+domin+al 0
abdominous ab+domin+ous 0
abdominovesical ab+domin+ical 4
abducent ab+du+cent 0
abducting ab+duct+ing 0
…
```
The script used to produce this output has not been uploaded to Github - but it essentially iterates through the input file (in this case Wordnet adjectives) using the same algorithm.
