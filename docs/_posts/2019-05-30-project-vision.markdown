---
layout: post
title:  "Project Vision"
date:   2019-05-30 16:40:56
categories: morpheme update
---

Wikipedia, et al, define a morpheme as the smallest meaningful unit in a language. The vision of this project is the creation of a resource that not only segments words into morphemes (prefixes, roots/stems, and suffixes), but also associates meanings with them. This is in contrast to the many resources out there that focus only on segmentation.

The objective is that this store of meaning-based morphemes will provide a resource to assist in determining the meanings of words.

Entries, grouped by "meaning", are contained in the dataset morphemes.json (in the repo data folder).

An initial test successfully segmented 88% of Wordnet adjectives. Of course the real test - yet to be determined, is: how many of the results yielded appropriate meanings - the objective of this repository in the first place.

Try it out! Use the form on the right to retrieve results online. Please help improve the dataset by indicating whether the results you get make sense or not.

You also have the option of downloading the repo. Currently, the Python scripts provided in the Github repo operate on one word at a time, and integrate with the NLTK Wordnet package.

Any comments and suggestions are appreciated - please use the Issues tab at https://github.com/colingoldberg/morphemes.

See the next posts for more details.
