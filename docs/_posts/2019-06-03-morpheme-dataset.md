---
layout: post
title:  "Morpheme Dataset"
date:   2019-06-03 11:36:00
categories: morpheme dataset
---

This dataset (in morphemes.json) has been curated with the objective of enabling automated access. 

It houses morphemes(prefixes, roots/stems, and suffixes), along with meanings and other associated characteristics.

An initial count shows 2400+ groupings, containing 3000+ prefixes, 1000+ roots/stems, and 800+ suffixes.


**Prefixes:**

Fields associated with prefixes are as follows:
* form: the prefix characters as they would exist in a word (eg. "ab")
* root: reference to the form,with "-" appended (eg. "ab-")
* loc: the fixed value "prefix"
* attach_to: a list of parts of speech that this prefix would attach to (eg. ["noun"])
* category: one of the following values (this list is extensible):
  * preposition-like
  * relating to
  * negation
  * ...


**Suffixes:**

Fields associated with suffixes are as follows:
* form: the suffix characters as they would exist in a word (eg. "able")
* root: reference to the form,with "-" prepended (eg. "-able")
* loc: the fixed value "suffix"
* pos: part of speech (allows for multiples)
* type:
  * derivational
  * inflectional


**Roots/Stems:**

Fields associated with roots/stems are as follows:
* form: the root/stem characters as they would exist in a word (eg. "fess")
* root: reference to the form,with "-" prepended and appended (eg. "-fess-")
* loc: the fixed value "embedded"


Entries are grouped according to meaning. Fields in a grouping are:
* meaning: a list of words or phrases that apply to all the prefixes, suffixes, and roots/stems in the grouping
* theme: a categorization of the grouping (eg. "society"). Some values of theme are:
  * color
  * society
  * diminutive
  * human_body
  * gender
  * movement
  * negation
  * proportion
  * ...
* origin: language of origin (eg. "Latin")
* etymology: details where available
* examples: a list of words that contain one or more affixes in the grouping

Note 1: Some of the fields above do not have values. This is particularly true of prefix fields "attach_to", "category",  suffix fields "pos", "type", and grouping fields "origin", "etymology". Completion of these field values is an ongoing project. Please contribute if you can.

Note 2: Ordering of some entries, particularly prefixes, is important to facilitate search.


To illustrate the contents of this dataset, here are some typical entries:

- prefix only
```
"be-": {
  "forms": [{
    "root": "be-",
    "form": "be",
    "loc": "prefix",
    "attach_to": ["verb"],
    "category": "preposition-like"
  }],
  "meaning": ["equipped with", "covered with", "beset with"],
  "origin": "",
  "etymology": "",
  "examples": ["bedeviled", "becalm", "bedazzle", "bewitch"]
},
```

- suffix only:
```
"-acy": {
  "forms": [{
    "root": "-acy",
    "form": "acy",
    "pos": "noun",
    "type": "derivational",
    "loc": "suffix"
  }],
  "meaning": ["state", "quality", "resemblance"],
  "origin": "",
  "etymology": "",
  "examples": ["democracy", "accuracy", "lunacy"]
},
```

See the README file under code/wordnet in the repo for details on Python scripts that can be used in conjunction with this dataset.

