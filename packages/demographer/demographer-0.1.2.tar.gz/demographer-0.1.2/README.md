# Demographer
### Extremely simple demographics from Twitter names
### Authors: Josh Carroll <carroll.joshk@gmail.com>, Mark Dredze <mdredze@cs.jhu.edu>, Rebecca Knowles <rknowle2@jhu.edu>
##### Supports: Python 2.7+

> **Demographer**: one who studies subjects including the geographical distribution of people, birth and death rates, socioeconomic status, and age and sex distributions in order to identify the influences on population growth, structure, and development. (Dictionary.com)

Demographer is a Python package that identifies demographic characteristics based on a name. It's designed for Twitter, where it takes the name of the user and returns information about his or her likely demographics.

###Why demographics?
Many downstream applications that consume Twitter data benefit from knowing information about a user. Analyzing opinions and trends based on demographics is a cornerstone analysis common in many areas of social science. While some social media platforms provide demographics for users, Twitter does not.

### Why only look at the name?
There are *many* papers that have proposed methods for demographic identification using what a user's posts or who they follow. These methods can be quite good, and likely do better than only looking at the name for many tasks. Why only look at the name? Often times you only have a single tweet for a user, and it's not feasible to get more data. In these settings, content analysis isn't feasible; one tweet isn't enough. Demographer is designed for these settings. We can produce a reasonable guess even if we only have a single tweet.

### Name or Username?
We use the "name" field within the "user" field, rather than the "username" field. This is because even twitter users who have usernames wholly unrelated to their own names sometimes use their real names (or some part of their name, or something name-like) in the "name" field.

### How good is it?
Overall, the tool is quite good, possibly the best tool available for this task (see our paper cited below.) for specific names, it depends. Some names make it easy to identify some demographic characteristics, and some make it impossible. The distribution over these names changes by task, so its hard to give accuracy guarantees across datasets. The tool is focused on western names, so it may do poorly on Chinese or Arabic names. 

### Can I extend demographer?
Yes! We designed the package to be highly extensible. If you have new types of training data, or a different approach entirely, you should be able to add it to the package. You need to subclass `Demographer`.

### What demographics does it include?
The current release includes gender based on US census data. You can often guess gender accurately as many names are almost exclusively used with one gender.

### I want to learn more!
To find out more, check out our paper:

 Rebecca Knowles, Josh Carroll, Mark Dredze. Demographer: Extremely Simple Name Demographics. EMNLP Workshop on Natural Language Processing and Computational Social Science, 2016. [[PDF](http://aclweb.org/anthology/W16-5614)]


### Gender.c
We also include code that (roughly) implements `gender.c`, which is described here: 
[http://www.heise.de/ct/ftp/07/17/182/](http://www.heise.de/ct/ftp/07/17/182/)

The code is available in `demographer/gender_c.py`. The data for `gender.c` is here:
```
demographer/data/nam_dict.txt.gz
```
and is redistributed under a GNU Free Documentation License, Version 1.2.

### Please cite our work
If you use demographer in a paper, you should cite it as follows:

```
@inproceedings{W16-5614,
  author = 	"Knowles, Rebecca and Carroll, Josh and Dredze, Mark",
  title = 	"Demographer: Extremely Simple Name Demographics",
  booktitle = 	"EMNLP Workshop on NLP and Computational Social Science",
  year = 	"2016",
  publisher = 	"Association for Computational Linguistics",
  pages = 	"108--113",
  location = 	"Austin, Texas",
  url = 	"http://aclweb.org/anthology/W16-5614"
}
```


## Installation
With pip:

```
pip install demographer
```
From source, you can use `setuptools`

```
python setup.py install
```

This uses pre-built data files and classifiers. If you want to build your own data files and classifiers from scratch, run the script `get_data.sh`


## Examples

### API Access

We provide a simple API to demographer. Here is an example of how you annotate a single tweet. Note that this examples uses a sample tweet file distributed with the library (users installing via pip can download `faketweets.txt` from the `data` directory at the root of this repository).
  
> from demographer import process_tweet
> 
> import json
> 
> tweet = json.loads(open('data/faketweets.txt').readline())
> 
> result = process_tweet(tweet)

The first time you call `process_tweet` expect to wait a bit. This command loads the data to initialize the underlying demographers.

`result` stores a list of dictionary objects, each corresponding to the output from one demographer. Here is an example of `result`:

> [{u'gender': [{u'count': 1099936, u'prob': 0.9977160044772844, u'value': u'F'}, {u'count': 2518, u'prob': 0.002283995522715687, u'value': u'M'}]}]

In this example, the first dictionary in the list is the output for gender. It contains probability estimates (M)ale and (F)emale.

### Command Line Access
We also provide a script that processes a file containing tweets and adds demographic information to each one. The input file contains tweets, each encoded in json, one object per line. The output file contains the same tweets with a new field `demographics` which contains the list from above.

> python -m demographer.cli.process\_tweets --input INPUT_FILE --output OUTPUT_FILE
> 